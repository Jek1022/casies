from django.db import models
from django.urls import reverse

# Create your models here.
class Cas(models.Model):
    company_invoice_number = models.CharField(max_length=50, verbose_name='Company SI/OR/SB/DM/CM No.')
    issue_date = models.CharField(max_length=8, verbose_name='SI/OR/SB/DM/CM Issuance Date - YYYYMMDD')
    eis_unique_id = models.CharField(max_length=24, verbose_name='BIR e-invoice Unique ID')
    DOCUMENT_TYPE_CHOICES = (
        ('01', 'Sales Invoice (SI)'),
        ('02', 'Debit Memo (DM)'),
        ('03', 'Credit Memo (CM)'),
        ('04', 'Service Billing (SB / Billing Statement)'),
        ('05', 'Official Reciept (OR)'),
    )
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPE_CHOICES, verbose_name='Document Type')
    TRANSACTION_CLASSIFICATION_CHOICES = (
        ('01', 'VATable'),
        ('02', 'Zero-Rated'),
        ('03', 'VAT Exempt'),
    )
    transaction_classification = models.CharField(max_length=2, choices=TRANSACTION_CLASSIFICATION_CHOICES, verbose_name='Transaction Classification')
    IS_CORRECTION_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'Not'),
    )
    is_correction = models.CharField(max_length=1, choices=IS_CORRECTION_CHOICES, verbose_name='Correction Yes or Not')
    CORRECTION_CODE_CHOICES = (
        ('01', 'Error'),
        ('02', 'Duplication'),
        ('03', 'Addition/reduction'),
        ('04', 'Cancellation'),
        ('05', 'Return'),
        ('09', 'Others'),
    )
    correction_code = models.CharField(max_length=2, choices=CORRECTION_CODE_CHOICES, null=True, blank=True, verbose_name='e-Invoice Correction Code')
    previous_unique_id = models.CharField(max_length=24, null=True, blank=True, verbose_name='E-Invoice Unique ID of the document to be corrected')
    remarks_1 = models.CharField(max_length=500, null=True, blank=True, verbose_name='Remarks1')

    seller_info_tin = models.CharField(max_length=9, default='000000000', verbose_name='Seller TIN')
    seller_info_branch_code = models.CharField(max_length=5, default='00000', verbose_name='Seller Branch Code')
    SELLER_INFO_TYPE_CHOICES = (
        ('0', 'VAT registered'),
        ('1', 'Non-VAT registered'),
    )
    seller_info_type = models.CharField(max_length=1, choices=SELLER_INFO_TYPE_CHOICES, verbose_name='Seller Type')
    seller_info_registered_name = models.CharField(max_length=200, verbose_name='Seller Registered Name')
    seller_info_business_name = models.CharField(max_length=200, verbose_name='Seller Business Name/Trade Name')
    seller_info_email = models.CharField(max_length=100, default='null', null=True, blank=True, verbose_name='Seller Email address')
    seller_info_registered_address = models.CharField(max_length=300, verbose_name='Seller Registered Address')
    buyer_info_tin = models.CharField(max_length=9, default='000000000', verbose_name='Buyer TIN')
    buyer_info_branch_code = models.CharField(max_length=5, default='00000', verbose_name='Buyer Branch Code')
    buyer_info_registered_name = models.CharField(max_length=200, verbose_name='Buyer Registered Name')
    buyer_info_business_name = models.CharField(max_length=200, verbose_name='Buyer Business Name/Trade Name')
    buyer_info_email = models.CharField(max_length=100, default='null', null=True, blank=True, verbose_name='Buyer Email address')
    buyer_info_registered_address = models.CharField(max_length=300, default='null', null=True, blank=True, verbose_name='Buyer Registered Address')
    buyer_info_delivery_address = models.CharField(max_length=300, default='null', null=True, blank=True, verbose_name='Buyer Delivery Address')
    buyer_info_airway_bill_number = models.CharField(max_length=50, default='null', null=True, blank=True, verbose_name='Airway Bill Number')
    buyer_info_airway_bill_number_date = models.CharField(max_length=8, default='null', null=True, blank=True, verbose_name='Airway Bill Number Date')
    buyer_info_bill_of_lading_number = models.CharField(max_length=50, default='null', null=True, blank=True, verbose_name='Bill of Lading Number')
    buyer_info_bill_of_lading_number_date = models.CharField(max_length=8, default='null', null=True, blank=True, verbose_name='Bill of Lading Number Date')
    item_list_name = models.CharField(max_length=100, verbose_name='Item Name')
    item_list_description = models.CharField(max_length=100, default='null', verbose_name='Item Description/Service')
    item_list_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Item Quantity')
    item_list_unit_of_measure = models.CharField(max_length=50, default='null', null=True, blank=True, verbose_name='Item Unit of measure')
    item_list_unit_cost = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Unit Cost')
    item_list_sales_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Item Sales Amount')
    item_list_regular_discount_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Regular Discount Amount')
    item_list_special_discount_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Special Discount Amount')
    item_list_net_of_sales = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Net of Item Sales')
    item_list_total_net_sales = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Total of Net of Item Sales')
    senior_citizen_discount_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Senior Citizen Discount Amount')
    pwd_discount_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='PWD Discount Amount')
    regular_discount_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Regular Discount Amount')
    special_discount_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Special Discount Amount')
    remarks_2 = models.CharField(max_length=500, default='null', null=True, blank=True, verbose_name='Remarks2 - Brief explanation of discount if needed')
    other_tax_revenue = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Other Taxable Revenue')
    total_net_sales_after_discounts = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Total Net Sales After Discounts')
    vat_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='VAT Amount')
    withholding_tax_income_tax = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Withholding Tax-Income Tax')
    withholding_tax_business_vat = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Withholding Tax-Business VAT')
    withholding_tax_business_percentage = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Withholding Tax-Business Percentage')
    other_non_taxable_charges = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Other Non-Taxable Charges')
    net_amount_payable = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, verbose_name='Net Amount Payable')
    currency = models.CharField(max_length=3, null=True, blank=True, verbose_name='Currency')
    conversion_rate = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Conversion Rate')
    forex_amount = models.DecimalField(max_digits=28, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Currency Amount')
    ptu_number = models.CharField(max_length=50, verbose_name='PTU Number/Acknowledgment Certificate Control Number')
    ptu_expiry_date = models.CharField(max_length=8, verbose_name='Expiry Date of PTU')
    CAS_TYPE_CHOICES = (
        ('01', 'iES Advertising'),
        ('02', 'Circulation'),
    )
    cas_type = models.CharField(max_length=2, choices=CAS_TYPE_CHOICES, verbose_name='CAS Type - Advertising/Circulation')
    item_id = models.IntegerField(verbose_name='Transaction item ID no.')
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('C', 'Cancelled'),
        ('O', 'Posted'),
        ('P', 'Printed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    submit_id = models.CharField(max_length=255, null=True, blank=True, default='')
    entered_by = models.IntegerField(default=1)
    entered_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(default=1)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk)
    
    def get_absolute_url(self):
        return reverse('cas:detail', kwargs={'pk': self.pk})
    
    class Meta:
        db_table = 'cas'
        ordering = ['-pk']
        
    def document_type_verbose(self):
        return dict(self.DOCUMENT_TYPE_CHOICES).get(self.document_type)

    def transaction_classification_verbose(self):
        return dict(self.TRANSACTION_CLASSIFICATION_CHOICES).get(self.transaction_classification)
    
    def is_correction_verbose(self):
        return dict(self.IS_CORRECTION_CHOICES).get(self.is_correction)
    
    def correction_code_verbose(self):
        return dict(self.CORRECTION_CODE_CHOICES).get(self.correction_code)
    
    def seller_info_type_verbose(self):
        return dict(self.SELLER_INFO_TYPE_CHOICES).get(self.seller_info_type)
    
    def cas_type_verbose(self):
        return dict(self.CAS_TYPE_CHOICES).get(self.cas_type)

    def status_verbose(self):
        return dict(self.STATUS_CHOICES).get(self.status)
    
    def to_json_format(self, pks):
        item_list = []
        for pk in pks:
            item = Cas.objects.filter(pk=pk).values(
                'item_list_name', 
                'item_list_description', 
                'item_list_quantity', 
                'item_list_unit_of_measure', 
                'item_list_unit_cost', 
                'item_list_sales_amount', 
                'item_list_regular_discount_amount', 
                'item_list_special_discount_amount',
                'item_list_net_of_sales'
            )
            
            item_list.append({
                "Nm":           item[0]['item_list_name'],
                "Desc":         item[0]['item_list_description'],
                "Qty":          item[0]['item_list_quantity'],
                "Unit":         item[0]['item_list_unit_cost'],
                "UnitCost":     item[0]['item_list_unit_cost'],
                "SalesAmt":     item[0]['item_list_sales_amount'],
                "RegDscntAmt":  item[0]['item_list_regular_discount_amount'],
                "SpeDscntAmt":  item[0]['item_list_special_discount_amount'],
                "NetSales":     item[0]['item_list_net_of_sales']
            })
            
        json_data = {
            "CompInvoiceId":    self.company_invoice_number,
            "IssueDtm":         self.issue_date,
            "EisUniqueId":      self.eis_unique_id,
            "DocType":          self.document_type,
            "TransClass":       self.transaction_classification,
            "CorrYN":           self.is_correction,
            "CorrectionCd":     self.correction_code,
            "PrevUniqueId":     self.previous_unique_id,
            "Rmk1":             self.remarks_1,
            "SellerInfo": {
                "Tin":          self.seller_info_tin,
                "BranchCd":     self.seller_info_branch_code,
                "Type":         self.seller_info_type,
                "RegNm":        self.seller_info_registered_name,
                "BusinessNm":   self.seller_info_registered_name,
                "Email":        self.seller_info_email,
                "RegAddr":      self.seller_info_registered_address
            },
            "BuyerInfo": {
                "Tin":          self.buyer_info_tin,
                "BranchCd":     self.buyer_info_branch_code,
                "RegNm":        self.buyer_info_registered_name,
                "BusinessNm":   self.buyer_info_business_name,
                "Email":        self.buyer_info_email,
                "RegAddr":      self.buyer_info_registered_address,
                "DevAddr":      self.buyer_info_delivery_address,
                "AirNum":       self.buyer_info_airway_bill_number,
                "AirNumDt":     self.buyer_info_airway_bill_number_date,
                "LadNum":       self.buyer_info_bill_of_lading_number,
                "LadNumDt":     self.buyer_info_bill_of_lading_number_date
            },
            "ItemList": item_list,
            "TotNetItemSales": self.item_list_total_net_sales,
            "Discount": {
                "ScAmt":    self.senior_citizen_discount_amount,
                "PwdAmt":   self.pwd_discount_amount,
                "RegAmt":   self.regular_discount_amount,
                "SpeAmt":   self.special_discount_amount,
                "Rmk2":     self.remarks_2
            },
            "OtherTaxRev":          self.other_tax_revenue,
            "TotNetSalesAftDisct":  self.total_net_sales_after_discounts,
            "VATAmt":               self.vat_amount,
            "WithholdIncome":       self.withholding_tax_income_tax,
            "WithholdBusVAT":       self.withholding_tax_business_vat,
            "WithholdBusPT":        self.withholding_tax_business_percentage,
            "OtherNonTaxCharge":    self.other_non_taxable_charges,
            "NetAmtPay":            self.net_amount_payable,
            "ForCur": { 
                "Currency": self.currency,
                "ForexAmt": self.forex_amount, 
                "ConvRate": self.conversion_rate
            },
            "PtuNum":   self.ptu_number
        }

        return json_data
    
    @classmethod
    def load(cls, invoice_id):
        obj = cls.objects.get(pk=invoice_id)
        return obj
