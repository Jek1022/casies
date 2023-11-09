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
from datetime import datetime
from decouple import config
from jose import jws
from datatransmission.models import TokenModel, InquiryResult
from eiscredential.models import EisCredential, Setting

APPLICATION_ID = "YOUR_APPLICATION_ID" # Set Application ID
ACCREDITATION_ID = "YOUR_EIS_CERT_NUMBER" # Set Test EIS Cert Number
AUTH_TOKEN = "AUTH_TOKEN" # Set auth token key
SESSION_KEY = "SESSION_KEY" # Set session key

HMAC_SHA_256 = "HmacSHA256"
URL = "https://eis-cert.bir.gov.ph/api/invoice_result"


class ResultInquiry():
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
        self.resultinquiry_url = credential.inquiry_result_url
        
    def get_status(self, request, submit_id, data_id, invoice_no): 
        # create HMAC
        method = "GET"
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        value = date_time + method + "/api/invoice_result/" + str(submit_id)
        mac = base64.b64encode(hmac.new(self.session_key.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).digest())
        signature = "Bearer " + mac.decode('utf-8')

        #header    
        headers = {
            'AuthToken': self.auth_token,
            'Authorization': signature, 
            'ApplicationId': self.application_id, 
            'AccreditationId': self.application_id,
            'Datetime': date_time, 
            'Content-Type': 'application/json; charset=utf-8'
        }

        # GET
        # res = requests.get(URL+"/"+submit_id, data="", headers=headers)
        res = requests.get("https://run.mocky.io/v3/1560094f-82b2-4f4f-b903-16f547ea6bb4")

        # response result
        response_json = json.loads(res.text)

        #case Error
        if (res.status_code != 200):
            print("status_code : " + str(res.status_code))
            print("errorCode : " + response_json["errorDetails"]["errorCode"])
            print("errorMessage : " + response_json["errorDetails"]["errorMessage"])
            
        print('status_code : ' + str(res.status_code))
        # print(response_json)
        proc_status_code = response_json['data']['processStatusCode']

        if proc_status_code == '01':
            status_definition = 'Processing completed'
            result = {
                    'status': 'success',
                    'message': f"<span class='text-success'>{status_definition}: {invoice_no}</span>"
                }
        elif proc_status_code == '02':
            status_definition = 'In processing'
            result = {
                    'status': 'success',
                    'message': f"<span class='text-primary'>{status_definition}: {invoice_no}</span>"
                }
        elif proc_status_code == '03':
            status_definition = 'Unable to process'

            fail_status_code = response_json['data']['failReasonStatusCode']

            if fail_status_code == 'FRS001':
                fail_reason = 'Not exists Submit Id'
            elif fail_status_code == 'FRS002':
                fail_reason = 'Decryption failure'
            result = {
                    'status': 'success',
                    'message': f"<span class='text-danger'>{status_definition}: {invoice_no}. Failure reason: {fail_reason}</span>"
                }
            
        InquiryResult.objects.create(
            datatransmission_id = data_id,
            transfer_status = response_json['status'],
            acknowledgement_id=response_json['data']['ackId'],
            response_datetime=response_json['data']['responseDtm'],
            process_status_code=response_json['data']['processStatusCode'],
            result_status_code=response_json['data']['processedDocuments'][0]['resultStatusCode'],
            inquired_by=request.user
            
        )
        
        return result