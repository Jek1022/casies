import hmac
import hashlib
import requests
import json
import base64
import random
import os
import time
from threading import Thread
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto import Random
from cryptography.hazmat.primitives import serialization
from datetime import datetime
from jose import jws
from decouple import config
from eiscredential.models import EisCredential, Setting
from cas.models import Cas
from .helpers import DecimalEncoder
from .models import TokenModel, DataTransmission

# r_pad function for AES encrypt
def r_pad(payload, block_size=16):
    length = block_size - (len(payload) % block_size)
    return payload + chr(length) * length

# unpad function for AES decrypt
def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def to_public_pem(public_key):
    pem = ['-----BEGIN PUBLIC KEY-----']
    key_str = str(public_key)
    
    # Split the key string into lines of 64 characters each
    for i in range(0, len(key_str), 64):
        pem.append(key_str[i:i+64])
    
    pem.append('-----END PUBLIC KEY-----')
    return '\n'.join(pem)

def to_private_pem(private_key):
    pem = ['-----BEGIN RSA PRIVATE KEY-----']
    key_str = private_key
    for i in range(0, len(key_str), 64):
        pem.append(key_str[i:i+64])
    pem.append('-----END RSA PRIVATE KEY-----')
    return '\n'.join(pem)

class Transmit():
    def __init__(self):
        super().__init__()
        self.system_mode = Setting.load().config_eis_system_mode
        credential = EisCredential.load(self.system_mode)
        token_instance = TokenModel.load()

        self.application_id = credential.application_id
        self.accreditation_id = credential.accreditation_id
        self.jws_key_id = credential.jws_key_id
        self.jws_private_key = config(credential.jws_private_key)
        self.auth_token = token_instance.auth_token
        self.session_key = token_instance.session_key
        self.invoices_url = credential.invoices_url

    def jws_token(self, json_format):
        
        # create invoice JWS
        json_data = json.dumps(json_format, cls=DecimalEncoder)
        private_key = to_private_pem(self.jws_private_key)
        
        token = jws.sign(json_data.encode('utf-8'), private_key, headers={"kid": self.jws_key_id}, algorithm="RS256")
        return token
    
    def get_submit_id(self):
        rand_result = ""
        for i in range(12):
            rand_result += random.choice('0123456789abcdef')
            
        submit_id = self.accreditation_id+"-"+datetime.now().strftime("%Y%m%d")+"-"+rand_result
        print("SUBMIT ID : " + submit_id)
        return submit_id
    
    def execute(self, request, invoice_no, invoice_id, json_format):
        token = self.jws_token(json_format)
        submit_id = self.get_submit_id()

        # JWS encrypted
        iv = self.session_key[:AES.block_size]
        cipherAES = AES.new(self.session_key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        encrypted = cipherAES.encrypt(r_pad(token, AES.block_size).encode("utf-8"))
        encrypted_data = base64.b64encode(encrypted)
        
        # body
        bodyJson = {
            "submitId": submit_id, 
            "data": encrypted_data.decode("utf-8")
        }
        body = json.dumps(bodyJson)

        # create HMAC
        method = "POST"
        date_time_now = datetime.now().strftime("%Y%m%d%H%M%S")
        value = date_time_now + method + "/api/invoices"
        mac = base64.b64encode(hmac.new(self.session_key.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).digest())
        signature = "Bearer " + mac.decode('utf-8')

        #header
        headers = {
            'AuthToken': self.auth_token,
            'Authorization': signature, 
            'ApplicationId': self.application_id, 
            'AccreditationId': self.accreditation_id,
            'Datetime': date_time_now, 
            'Content-Type': 'application/json; charset=utf-8`'
        }

        for id in invoice_id:
            Cas.objects.filter(pk=id).update(
                submit_id=submit_id
            )

        # POST (JSON)
        # res = requests.post(self.invoices_url, data=body, headers=headers)
        # res = requests.post("https://run.mocky.io/v3/43d32ea2-c8b4-49a6-a924-5544e297b0f4", data=None, headers={'Content-Type': 'application/json; charset=utf-8'})
        res = requests.post("https://run.mocky.io/v3/d0301583-aeee-444b-b7f3-8de7dd2ce670", data=None, headers={'Content-Type': 'application/json; charset=utf-8'})

        # response result logic
        response_json = json.loads(res.text)
        
        #case Error
        if (res.status_code != 200):
            print("errorCode : " + response_json["errorDetails"]["errorCode"])
            print("errorMessage : " + response_json["errorDetails"]["errorMessage"])

        # response data decrypted
        raw_data = base64.b64decode(response_json["data"])
        iv = self.session_key[:AES.block_size]
        cipher = AES.new(self.session_key.encode("utf-8"),
                            AES.MODE_CBC, iv.encode("utf-8"))
        result = unpad(cipher.decrypt(raw_data))
        # print(result)
        # response data to JSON
        # result_json = json.loads(result.decode('utf-8'))
        result_json = {
            "accreditationId": self.accreditation_id,
            "userId": "testuser",
            "refSubmitId": submit_id,
            "ackId": "BIR-20210325154527-E8QN3",
            "responseDtm": "2021-03-25T15:45:28",
            "description": "Transmission has been successfully processed. EIS will process the final registration within the next business day."
        }

        transfer_status = '1' if response_json["status"] == "1" else '0'
        
        for id in invoice_id:
            
            DataTransmission.objects.create(
                cas_id = id,
                transfer_status = transfer_status,
                ref_submit_id = result_json['refSubmitId'],
                acknowledgement_id = result_json['ackId'],
                response_datetime = result_json['responseDtm'],
                description = result_json['description'],
                system_configuration_mode = self.system_mode,
                transmitted_by = request.user,
            )
            
        result = {
                    'status': 'success',
                    'message': f"<span class='text-primary'>Done invoice no. {invoice_no}</span>"
                }
        return result
    