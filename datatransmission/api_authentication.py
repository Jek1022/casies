import sys
import hmac
import hashlib
import requests
import json
import hmac
import base64
import random
from django.http import JsonResponse
from django.views import View
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from datetime import datetime, timedelta
from requests.exceptions import ConnectionError, ConnectTimeout
from eiscredential.models import EisCredential, Setting
from .models import TokenModel


def unpad(s):
    ''' Unpad for AES decryption '''
    return s[:-ord(s[len(s)-1:])]


def generate_key(length=32):
    ''' Generate a 32-character auth key '''
    base71chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#$%^&*()"
    return ''.join(random.choice(base71chars) for _ in range(length))


class Authentication(View):
    def __init__(self):
        super().__init__()
        system_mode = Setting.objects.get(pk=1).config_eis_system_mode
        credential = EisCredential.objects.get(access_level=system_mode)

        self.public_key = credential.public_key
        self.user_id = credential.user_id
        self.user_password = credential.user_password
        self.auth_key = generate_key()
        self.authentication_url = credential.authentication_url
        self.accreditation_id = credential.accreditation_id
        self.application_id = credential.application_id
        self.application_secret_key = credential.application_secret_key
        self.force_refresh_token = credential.force_refresh_token

    def get(self, request):
        response = self.send(request)
        return JsonResponse(response)

    def send(self, request):
        response = ''
        try:
            # Set Request URL
            url = self.authentication_url

            data_map = {"userId": self.user_id, "password": self.user_password, "authKey": self.auth_key}
            data = json.dumps(data_map)

            # User information encrypted
            pub_key = base64.b64decode(self.public_key)
            key = RSA.importKey(pub_key)
            cipher = PKCS1_v1_5.new(key)
            ciphertext = base64.b64encode(cipher.encrypt(bytes(data, "utf-8")))

            # Set body data
            body_json = {"data": ciphertext.decode("utf-8"), "forceRefreshToken": self.force_refresh_token} 
            body = json.dumps(body_json)

            # Create HMAC signature
            method = "POST"
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            message = current_datetime + method + "/api/authentication"
            mac = base64.b64encode(hmac.new(self.application_secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest())
            signature = "Bearer " + mac.decode('utf-8')
            
            # Set Request Header
            headers = {
                'datetime': current_datetime,
                'authorization': signature,
                'accreditationId': self.accreditation_id,
                'applicationId': self.application_id,
                'Content-Type': 'application/json; charset=utf-8'
            }

            # res = requests.post(url, data=body, headers=headers)
            res = requests.post('https://run.mocky.io/v3/4ddbd46d-baa6-46f0-8fc6-2e4d3dd2615d', data='', headers='')

            response_json = json.loads(res.text)
            
            if (res.status_code != 200):
                print("errorCode : " + response_json["errorDetails"]["errorCode"])
                print("errorMessage : " + response_json["errorDetails"]["errorMessage"])
            else:
                # response data decrypted
                res_data = base64.b64decode(response_json["data"])
                iv = self.auth_key[:AES.block_size]
                cipher_aes = AES.new(self.auth_key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
                response_result = unpad(cipher_aes.decrypt(res_data))
                
                # response data to JSON
                # response_result_json = json.loads(response_result.decode('utf-8'))

                # hardcoded response
                current_time = datetime.now()
                new_time = current_time + timedelta(hours=6)
                formatted_time = new_time.strftime("%Y-%m-%dT%H:%M:%S")
                response_result_json = {
                    "accreditationId": "test accreditation id (test EIS Cert Number)",
                    "userId": "testuser",
                    "authToken": "53A8CJFLEK3CE9MQ7L2X9V76TUIPZ4YU",
                    "sessionKey": "WmZq4t7w!z$C&F)J@NcRfUjXn2r5u8x/",
                    "tokenExpiry": formatted_time
                }
                # End hardcoded response

                auth_token = response_result_json["authToken"]
                session_key = response_result_json["sessionKey"]
                token_expiry = response_result_json["tokenExpiry"]

                token_instance = TokenModel.load()
                token_instance.auth_token = auth_token
                token_instance.session_key = session_key
                token_instance.token_expiry = token_expiry
                token_instance.entered_by = request.user
                token_instance.save()

                # print("AUTHTOKEN : " + auth_token)
                # print("SESSION KEY : " + session_key)
                # print("TOKEN EXPIRY : " + token_expiry)

                date_time_obj = datetime.fromisoformat(token_expiry)
                readable_date_time = date_time_obj.strftime("%B %d, %Y, %I:%M:%S %p")
                response = {
                    "status": "success",
                    "message": f"Authentication token acquired. Valid until {readable_date_time}."
                }
                
                return response
        except json.JSONDecodeError as e:
            response = {
                "status": "failed",
                "message": f"JSON decoding error: {str(e)}"
            }
        except ConnectTimeout as e:
            response = {
                "status": "failed",
                "message": f"Connection timed out: {e}"
            }
        except ConnectionError as e:
            response = {
                "status": "failed",
                "message": f"Connection error: {e}"
            }
        except Exception as e:
            response = {
                "status": "failed",
                "message": f"An error occured: {e}"
            }

        return response
