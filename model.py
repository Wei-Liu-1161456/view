from datetime import date
from typing import List
from decimal import Decimal
from abc import ABC, abstractmethod

# Constants for business rules
MAX_PRIVATE_CUSTOMER_OWING = Decimal('100.00')
DEFAULT_CORPORATE_DISCOUNT = Decimal('0.10')
DELIVERY_RADIUS_KM = 20
DELIVERY_FEE = Decimal('10.00')

class Person:
    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

class Staff(Person):
    def __init__(self, first_name: str, last_name: str, username: str, password: str, dept_name: str, date_joined: date,staff_ID: str):
        super().__init__(first_name, last_name, username, password)
        self.dept_name = dept_name
        self.date_joined = date_joined
        self.staff_ID = staff_ID

    def __str__(self):
        '''Return a string representation of the Staff object'''
        return (f"Staff ID: {self.staff_ID}\n"
                f"Name: {self.first_name} {self.last_name}\n"
                f"Username: {self.username}\n"
                f"Department: {self.dept_name}\n"
                f"Date Joined: {self.date_joined.isoformat()}")  # Display date in ISO format

class Customer(Person):
    def __init__(self, first_name: str, last_name: str, username: str, password: str, 
                 cust_address: str, cust_balance: Decimal, max_owing: Decimal, cust_id: str):
        '''Initializes the Customer class'''
        super().__init__(first_name, last_name, username, password)
        self.cust_address = cust_address
        self.cust_balance = cust_balance
        self.max_owing = max_owing
        self.list_of_orders = []
        self.list_of_payments = []
        self.cust_id = cust_id

    def __str__(self):
        '''Return a string representation of the Customer object'''
        return (f"Customer ID: {self.cust_id}\n"
                f"Name: {self.first_name} {self.last_name}\n"
                f"Username: {self.username}\n"
                f"Address: {self.cust_address}\n"
                f"Balance: {self.cust_balance}\n"
                f"Max Owing: {self.max_owing}")

class CorporateCustomer(Customer):
    '''the CorporateCustomer class'''
    def __init__(self, first_name: str, last_name: str, username: str, password: str, 
                 cust_address: str, cust_balance: Decimal, max_owing: Decimal, discount_rate: Decimal, 
                 corporate_cust_id: str):
        '''Initializes the CorporateCustomer class'''
        super().__init__(first_name, last_name, username, password, cust_address, cust_balance, max_owing, corporate_cust_id)
        self.discount_rate = discount_rate

    def __str__(self):
        '''Return a string representation of the CorporateCustomer object'''
        return (f"Customer ID: {self.cust_id}\n"
                f"Name: {self.first_name} {self.last_name}\n"
                f"Username: {self.username}\n"
                f"Address: {self.cust_address}\n"
                f"Balance: {self.cust_balance}\n"
                f"Max Owing: {self.max_owing}\n"
                f"Discount Rate: {self.discount_rate:.2%}")  # Display discount rate as a percentage

class Payment:
    payment_id = 1000
    def __init__(self, payment_amount: Decimal, payment_date: date):
        self.payment_id = "pay" + str(Payment.payment_id)
        Payment.payment_id += 1
        self.payment_amount = Decimal(str(payment_amount))
        self.payment_date = payment_date

class CreditCardPayment(Payment):
    def __init__(self, payment_amount: Decimal, payment_date: date,
                 card_number: str, card_type: str, card_expiry_date: date):
        super().__init__(payment_amount, payment_date)
        self.card_number = card_number
        self.card_type = card_type
        self.card_expiry_date = card_expiry_date
    
    '''
     payment = CreditCardPayment(
                total_amount,
                order_date,
                "4111-1111-1111-1111",
                "VISA",
                date(2025, 12, 31)
            )
    '''


class DebitCardPayment(Payment):
    def __init__(self, payment_amount: Decimal, payment_date: date,
                 bank_name: str, debit_card_num: str):
        super().__init__(payment_amount, payment_date)
        self.bank_name = bank_name
        self.debit_card_num = debit_card_num

class Order:
    order_id = 1000
    def __init__(self, order_customer: 'Customer', 
                 order_date: date, order_status: str):
        self.order_number = "ORD" + str(Order.order_id)
        Order.order_id += 1
        self.order_customer = order_customer
        self.order_date = order_date
        self.order_status = order_status
        self.list_of_items: List['OrderLine'] = []
        self.delivery_fee = DELIVERY_FEE
        self.discount = Decimal('0.00')
        self.delivery_fee = Decimal('0.00')
        self.total_amount = Decimal('0.00')

class OrderLine:
    def __init__(self, item_number: int):
        self.item_number = item_number
        self.an_item: 'Item' = None

class Item():
    def __init__(self):
        pass

    # @abstractmethod
    

class Veggie(Item):
    def __init__(self, veg_name: str):
        super().__init__()
        self.veg_name = veg_name

class WeightedVeggie(Veggie):
    def __init__(self, veg_name: str, weight: Decimal, weight_per_kilo: Decimal):
        super().__init__(veg_name)
        self.weight = Decimal(str(weight))
        self.weight_per_kilo = Decimal(str(weight_per_kilo))

class PackVeggie(Veggie):
    def __init__(self, veg_name: str, num_of_pack: int, price_per_pack: Decimal):
        super().__init__(veg_name)
        self.num_of_pack = num_of_pack
        self.price_per_pack = Decimal(str(price_per_pack))

class UnitPriceVeggie(Veggie):
    def __init__(self, veg_name: str, price_per_unit: Decimal, quantity: int):
        super().__init__(veg_name)
        self.price_per_unit = Decimal(str(price_per_unit))
        self.quantity = quantity

class PremadeBox(Item):
    def __init__(self, box_size: str):
        super().__init__()
        self.box_size = box_size
        self.box_content: List['Veggie'] = []