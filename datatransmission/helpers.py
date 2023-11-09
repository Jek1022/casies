# Author: Jek
# put here data validation, converter, calculation etc.
import re
import json
import decimal
from datetime import datetime

class DataValidator:
    ''' Program driven revalidation '''
    validation_rules = {
            "company_invoice_number": {
                "required": True,
                "format": "^[A-Za-z0-9_]+$",
                "max_length": 50
            },
            "issue_date": {
                "required": True,
                "format": "^\d{8}$",
            },
            "document_type": {
                "required": True,
                "format": "^[0-9]+$",
                "length": 2
            },
            "transaction_classification": {
                "required": True,
                "format": "^[0-9]+$",
                "length": 2
            },
            "is_correction": {
                "required": True,
                "format": "^[YN]$",
                "length": 1
            },
            "correction_code": {
                "required": False,
                "format": "^\d{2}$"
            },
            "previous_unique_id": {
                "required": False,
                "format": "^[A-Za-z0-9]+$",
                "length": 24
            },
            "remarks_1": {
                "required": False,
                "format": "[\s\S]*",
                "max_length": 500
            },
            "seller_info_tin": {
                "required": True,
                "format": "^\d{9}$",
                "max_length": 9
            },
            "seller_info_branch_code": {
                "required": True,
                "format": "^\d{5}$",
                "length": 5
            },
            "seller_info_type": {
                "required": True,
                "format": "^\d{1}$",
            },
            "seller_info_registered_name": {
                "required": True,
                "format": "^[A-Za-z0-9ñÑ\s\.,'#&():;\/\\-]+$",
                "max_length": 200
            },
            "seller_info_business_name": {
                "required": True,
                "format": "^[A-Za-z0-9ñÑ\s\.,'#&():;\/\\-]+$",
                "max_length": 200
            },
            "seller_info_email": {
                "required": False,
                "format": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "max_length": 100
            },
            "seller_info_registered_address": {
                "required": True,
                "format": "^[A-Za-z0-9ñÑ\s\.,'#&():;\/\\-]+$",
                "max_length": 300
            },
            "buyer_info_tin": {
                "required": True,
                "format": "^\d{9}$",
                "max_length": 9
            },
            "buyer_info_branch_code": {
                "required": True,
                "format": "^\d{5}$",
                "length": 5
            },
            "buyer_info_registered_name": {
                "required": True,
                "format": "^[A-Za-z0-9ñÑ\s\.,'#&():;\/\\-]+$",
                "max_length": 200
            },
            "buyer_info_business_name": {
                "required": True,
                "format": "^[A-Za-z0-9ñÑ\s\.,'#&():;\/\\-]+$",
                "max_length": 200
            },
            "buyer_info_email": {
                "required": False,
                "format": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "max_length": 100
            },
            "buyer_info_registered_address": {
                "required": False,
                "format": "^[A-Za-z0-9ñÑ\s\.,'#&():;\/\\-]+$",
                "max_length": 300
            },
            "buyer_info_delivery_address": {
                "required": False,
                "format": "^[A-Za-z0-9ñÑ\s\.,'#&():;\/\\-]+$",
                "max_length": 300
            },
            "buyer_info_airway_bill_number": {
                "required": False,
                "format": "^[A-Za-z0-9]$",
                "max_length": 50
            },
            "buyer_info_airway_bill_number_date": {
                "required": False,
                "format": "^\d{8}$",
            },
            "buyer_info_bill_of_lading_number": {
                "required": False,
                "format": "^[A-Za-z0-9]$",
                "max_length": 50
            },
            "buyer_info_bill_of_lading_number_date": {
                "required": False,
                "format": "^\d{8}$",
            },
            "item_list_name": {
                "required": True,
                "format": "^[\s\S]*",
                "max_length": 100
            },
            "item_list_description": {
                "required": False,
                "format": "^[\s\S]*",
                "max_length": 100
            },
            "item_list_quantity": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 10
            },
            "item_list_unit_of_measure": {
                "required": False,
                "format": "^[A-Za-z0-9.]+$",
                "max_length": 50
            },
            "item_list_unit_cost": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "item_list_sales_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "item_list_regular_discount_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "item_list_special_discount_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "item_list_net_of_sales": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "item_list_total_net_sales": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "senior_citizen_discount_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "pwd_discount_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "regular_discount_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "special_discount_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "remarks_2": {
                "required": False,
                "format": "[\s\S]*",
                "max_length": 500
            },
            "other_tax_revenue": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "total_net_sales_after_discounts": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "vat_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "withholding_tax_income_tax": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "withholding_tax_business_vat": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "withholding_tax_business_percentage": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "other_non_taxable_charges": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "net_amount_payable": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "currency": {
                "required": True,
                "format": "^[A-Za-z]+$",
                "length": 3
            },
            "conversion_rate": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "forex_amount": {
                "required": True,
                "format": "^\d+(\.\d{1,2})?$",
                "max_length": 28
            },
            "ptu_number": {
                "required": True,
                "format": "^[A-Za-z0-9\s-]+$",
                "max_length": 50
            }
        }
            
    def __init__(self):
        self.validated_data = []

    def validate(self, data):
        has_error = False
        errors = []
         
        for field_name, field_rules in self.validation_rules.items():
            field_value = getattr(data, field_name)

            if isinstance(field_value, decimal.Decimal):
                field_value = str(field_value)

            verbose_name = data._meta.get_field(field_name).verbose_name

            # check if the field is required
            if field_rules.get("required") and not field_value:
                has_error = True
                errors.append({
                    "error_message": f"{verbose_name} is required",
                    "field_value": field_value
                })
     
            if field_value:
                # check field format if specified
                format_pattern = field_rules.get("format")
                if format_pattern and not re.match(format_pattern, field_value):
                    has_error = True
                    errors.append({
                        "error_message": f"Invalid format for {verbose_name}",
                        "field_value": field_value
                    })

                # check field length if specified
                expected_length = field_rules.get("length")
                if expected_length is not None and len(field_value) != expected_length:
                    has_error = True
                    errors.append({
                        "error_message": f"{verbose_name} must be {expected_length} characters long",
                        "field_value": field_value})

                # check max length if specified
                max_length = field_rules.get("max_length")
                if max_length is not None and len(field_value) > max_length:
                    has_error = True
                    errors.append({
                        "error_message": f"{verbose_name} exceeded {max_length} characters long",
                        "field_value": field_value
                    })

        if has_error:
            return errors
        
        return None
    

class DecimalEncoder(json.JSONEncoder):
    ''' Convert Decimal to float and round to 2 decimal places '''
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return round(float(obj), 2)
        return super(DecimalEncoder, self).default(obj)
    

class Credential():
    def __init__(self):
        # Set EIS Public key : Fixed value - EIS Public key published on the download page of the EIS Certification portal.
        self.PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgMbSxoPRLi4P98qbfdFvwYCEf6l2QcKHhyE+m7Fh8OSqKqQFWud0+SSqydzYZzQYZIQ0hwZ/Vvd6StsEY80O7XC6ELVZ052s91PjAlh38TSzmJGy8ZZUYLsg8S2DzKaCpQ0ZmvphYf0ZB8ZoOXBTVPpg4cGBVbMZLdTtnXYxSegXhog6XBsIkAXmAWHwzJ0t6x0NbMnsfbHvFlqtUrsbwBc4BD+0rO3lJHPbDO4HEiMmrlM/bD/hL4uKzXv3jeXCkDbQdYsZZgI7tglu2Al/jB8VdMDJRJjsQf0Z5Ye3FdOsqp1v3SF3ENns8F/0A8xrrB/SuKcwO7Rvm2fjogoqqwIDAQAB"
    
        # Set User ID, Password
        self.USER_ID = "YOUR_USER_ID"
        self.USER_PASSWORD = "YOUR_PASSWORD"

        # Set Application ID
        self.APPLICATION_ID = "YOUR_APPLICATION_ID" 
        # Set Applicat Key - You can see or regenerate it on the setting page of your application in the EIS Certification portal.
        self.APPLICATION_SECRET_KEY = "YOUR_APPLICATION_KEY"
        self.ACCREDITATION_ID = "YOUR_EIS_CERT_NUMBER" # Set Test EIS Cert Number
        self.FORCE_REFRESH_TOKEN = "false" # Set Force refresh token

        self.HMAC_SHA_256 = "HmacSHA256"
        self.AUTHORIZATION_URL = "https://eis-cert.bir.gov.ph/api/authentication"
        
        
def readable_datetime(token_expiry):
    date_time_obj = datetime.fromisoformat(token_expiry)
    return date_time_obj.strftime("%B %d, %Y, %I:%M:%S %p")
    
    