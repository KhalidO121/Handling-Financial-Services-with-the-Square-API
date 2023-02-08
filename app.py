import random
import string
from square.client import Client
from pprint import pprint

client = Client(
    access_token=my_access_token,
    environment='sandbox')

# Using the Merchants API to collect merchant details.
###############################################################
def get_merchant_details(merchant_id:str):
    """Function that takes a merchant id and then prints information about that merchant.

    Args:
        merchant_id (str): id of the merchant
    """
    merchants_api = client.merchants
    result = merchants_api.retrieve_merchant(merchant_id)
    name_of_merchant = result.body['merchant']['business_name']
    country_of_merchant = result.body['merchant']['country']
    language_code = result.body['merchant']['language_code']
    
    if result.is_success():
        return("Name of business: " + name_of_merchant + "\nMerchant Country: "
               + country_of_merchant + "\nMerchant Language: " + language_code)
    elif result.is_error():
        pprint(result.errors)
        

# Using the Locations API to create, retrieve and update locations of a Square seller.
###############################################################
def create_locaton(name:str, type: str, description: str, instagram_username: str):
    """Function that creates a location for seller acount.
    
    Args:
        name (str): Name of location
        type (str): Type of location. Possible values: "MOBILE" or "PHYSICAL"
        description (str): Description of Location
        instagram_username (str): Instagram username of the location without the '@' symbol
    """
    location_api = client.locations
    result = location_api.create_location(
        body = {
        "location": {
            "name": name,
            "type": type,
            "description": description,
            "instagram_username": instagram_username
    }
  }
)
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
def update_location(id:str,new_name:str, type: str, description: str, instagram_username: str):
    """Function that updates fields of a location.

    Args:
        id (str): Location ID in the request URL
        new_name (str): New name of location
        type (str): Type of location. Possible values: "MOBILE" or "PHYSICAL"
        description (str): Description of Location
        instagram_username (str): Instagram username of the location without the '@' symbol
    """
    location_api = client.locations
    result = location_api.update_location(
        location_id = id,
        body = {
            "location" : {
                "name": new_name,
                "type": type,
                "description": description,
                "instagram_username": instagram_username
            }
        }
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)

def get_location(id:str):
    """"Function that displays information about a specific location of Square Seller.

    Args:
        id (str): Id of location
    """
    location_api = client.locations
    result = location_api.retrieve_location(
        location_id = id
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.erros)
    

def get_all_locations():
    """Function that displays information about all the locations of a Square seller."""
    location_api = client.locations
    result = location_api.list_locations()
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        

# Using the Payments API to Manage Scenarios involving payment
###############################################################
def generate_random_string():
    """Function that returns a random string of length 40

    Returns:
        str: The randomised string made up of 40 letters
    """
    return ''.join(random.choice(string.ascii_letters) for i in range(40))

# Creating different types of Payments
def create_a_card_payment(amount:int):
    """Funtion that charges credit/debit/Square Giftcard.

    Args:
        amount (int): Amount to be charged
    """
    payment_api = client.payments
    result = payment_api.create_payment(
        body = {
            "source_id": "cnon:card-nonce-ok",
            "idempotency_key": generate_random_string(),
            "amount_money": {
                "amount" : amount,
                "currency" : "GBP"
            }
        }
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)

def create_a_bank_transfer_payment(amount:int):
    """Function that charges a bank.

    Args:
        amount (int): Amount to be charged
    """
    payment_api = client.payments
    result = payment_api.create_payment(
        body = {
            "source_id": "bnon:bank-nonce-ok",
            "idempotency_key": generate_random_string(),
            "amount_money": {
                "amount" : amount,
                "currency" : "GBP"
            }
        }
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)

def create_a_cash_payment(amount_required:int, amount_supplied:int):
    """Function that registers a cash payment.

    Args:
        amount_required (int): Amount that buyer needs to pay
        amount_supplied (int): Amount that buyer supplied
    """
    payment_api = client.payments
    result = payment_api.create_payment(
        body = {
            "source_id": "CASH",
            "idempotency_key": generate_random_string(),
            "amount_money": {
                "amount" : amount_required,
                "currency" : "GBP"
            },
            "cash_details": {
                "buyer_supplied_money": {
                    "amount": amount_supplied,
                    "currency": "GBP"
                    }
                }
            }
        )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
def create_a_external_payment(amount_paid:int, source_of_payment:str, transaction_fee:int):
    """Function that registers a external payment outside of Square or seller.

    Args:
        amount_paid (int): Amount buyer paid
        source_of_payment (str): Source of this external payment
        transaction_fee (int): Transaction fee charged by external source
    """
    payment_api = client.payments
    result = payment_api.create_payment(
        body = {
            "source_id": "EXTERNAL",
            "idempotency_key": generate_random_string(),
            "amount_money": {
                "amount" : amount_paid,
                "currency" : "GBP"
            },
            "external_details": {
                "type": "OTHER",
                "source": source_of_payment,
                "source_fee_money": {
                    "amount": transaction_fee,
                    "currency": "GBP"
                    }
                }   
            }   
        )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
# Retrieving Payments:
def get_all_payments():
    """Funtion that generates a list of all the payments taken by account making the request."""
    payment_api = client.payments
    result = payment_api.list_payments()
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
def view_payment(id:str):
    """Function that fetches details of a specific payment.

    Args:
        id (str): Payment_id of the payment to fetch details of
    """
    payment_api = client.payments
    result = payment_api.get_payment(
        payment_id = id
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
    
#Refunding Payments
def refund_payment(payment_id:str,amount_to_refund:int):
    """Function that creates a refund.

    Args:
        payment_id (str): Id of payment that is to be refunded
        amount_to_refund (int): Amount to refund from original payment
    """
    payment_api = client.refunds
    result = payment_api.refund_payment(
        body = {
            "idempotency_key": generate_random_string(),
            "amount_money": {
            "amount": amount_to_refund,
            "currency": "GBP"
        },
        "payment_id": payment_id
        }
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        

def get_refund_status(id:str):
    """Function that retrieves a specific refund.

    Args:
        id (str): Id of refund to retrieve
    """
    payment_api = client.refunds
    result = payment_api.get_payment_refund(
        refund_id = id
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
def get_all_refunds():
    """Function that retrieves all refunds."""
    payment_api = client.refunds
    result = payment_api.list_payment_refunds()
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
# Using the Orders API to create and duplicate orders
###############################################################
def generate_order(id:str, tax_name:str, percentage_of_tax:str, amount_to_tax:str):
    """Function that creates an order.

    Args:
        id (str): location_id of where order is taking place
        tax_name (str): Name of tax
        percentage_of_tax (str): Percentage of tax as a int
        amount_to_tax (str): Amount to be taxed
    """
    order_api = client.orders
    result = order_api.create_order(
        body = {
            "order" : {
                "location_id": id
            },
            "taxes": [{
                "uid": generate_random_string(),
                "name": tax_name,
                "percentage": percentage_of_tax,
                "applied_money": {
                    "amount": amount_to_tax,
                    "currency": "GBP"
                    },
                "scope": "ORDER"
            }],
            "idempotency_key" : generate_random_string()
        }
    )

    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
def duplicate_order(id:str):
    """Function that creates a new order by duplicating an existing order, which will exist in DRAFT state.

    Args:
        id (str): Id of order to clone
    """
    order_api = client.orders
    result = order_api.clone_order(
        body = {
            "order_id" : id
        }
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
# Using the Invoice API to request payments for an order
###############################################################
# First thing is to have customer we are sending invoice to 
def generate_customer(customer_email_address:str):
    """Function that creates a customer.

    Args:
        customer_email_address (str): Email address of customer
    """
    customer_api = client.customers
    result = customer_api.create_customer(
        body = {
            "email_address" : customer_email_address
        }
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
def generate_invoice(order_id:str, customer_id:str):
    """Function that creates a draft invoice.

    Args:
        order_id (str): Id of associated order
        customer_id (str): Od of customer recieving the invoice
    """
    invoice_api = client.invoices
    result = invoice_api.create_invoice(
    body = {
        "invoice": {
            "order_id": order_id,
            "primary_recipient": {
                "customer_id": customer_id
            },
            "payment_requests": [{
                "request_type": "BALANCE",
                "due_date": "2030-11-14"
            }],
            "delivery_method": "EMAIL",
            "title": "Invoice for ice cream truck",
            "accepted_payment_methods": {
                "card": True,
                "square_gift_card": True
                }
            }
        }
    )
    
    if result.is_success():
        pprint(result.body)
    else:
        pprint(result.errors)
        
def send_invoice(id_of_invoice:str, version:int):
    """Function that publishes the draft invoice

    Args:
        id_of_invoice (str): Id of draft invoice to publish
        version (int): Current version of that invoice
    """
    invoice_api = client.invoices
    result = invoice_api.publish_invoice(
    invoice_id = id_of_invoice,
    body = {
        "version": version
        }   
    )

    if result.is_success():
        pprint(result.body)
    elif result.is_error():
        pprint(result.errors)



