"""This module saves data to files using the pickle module"""

import pickle
from datetime import date
from typing import List
from decimal import Decimal

class Person:
    '''the Person class'''
    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        '''Initializes the Person class'''
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

class Staff(Person):
    '''the Staff class'''
    def __init__(self, first_name: str, last_name: str, username: str, password: str, 
                 dept_name: str, date_joined: date,staff_ID: str):
        '''Initializes the Staff class'''
        super().__init__(first_name, last_name, username, password)
        self.dept_name = dept_name
        self.date_joined = date_joined
        self.staff_ID = staff_ID

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

class CorporateCustomer(Customer):
    '''the CorporateCustomer class'''
    def __init__(self, first_name: str, last_name: str, username: str, password: str, 
                 cust_address: str, cust_balance: Decimal, max_owing: Decimal, discount_rate: Decimal, 
                 corporate_cust_id: str):
        '''Initializes the CorporateCustomer class'''
        super().__init__(first_name, last_name, username, password, cust_address, cust_balance, max_owing, corporate_cust_id)
        self.discount_rate = discount_rate

# Create instances of the staff class
staff_member = Staff("John", "Doe", "staffJD", "12345", "Sales Department", date(2021, 1, 1), "S1000")

# Create instances of the customer class
pri_cust_member1 = Customer("Sally", "Smith", "privateSS", "12345", "Distance 10", Decimal('0.00'), Decimal('100.00'), "P1000")
pri_cust_member2 = Customer("Tom", "Brown", "privateTB", "12345", "Distance 30", Decimal('0.00'), Decimal('100.00'), "P1001")

# Create instances of the corporate customer class
co_cust_member1 = CorporateCustomer("Kim", "King", "corporateKK", "12345", "Distance 20", Decimal('0.00'), Decimal('100.00'), Decimal('0.10'), "C1000")
co_cust_member2 = CorporateCustomer("Luna", "Lory", "corporateLL", "12345", "Distance 40", Decimal('0.00'), Decimal('100.00'), Decimal('0.10'), "C1001")

# Create a dictionary to store the private customers
private_customers = {"P1000" : pri_cust_member1, "P1001" : pri_cust_member2}

# Create a dictionary to store the corporate customers
corporate_customers = {"C1000" : co_cust_member1, "C1001" : co_cust_member2}

# method to save data to a file
def save_data(filename, data, datatype):
      with open(filename, 'wb') as file:
        pickle.dump(data, file)
        print(f"{datatype} data saved to {filename}")

# Store staff to staff.pkl
save_data("data/staffs.pkl", staff_member, "Staff")

# Store private customers to private_customers.pkl
save_data("data/private_customers.pkl", private_customers, "Private customers")

# Store corporate customers to corporate_customers.pkl
save_data("data/corporate_customers.pkl", corporate_customers, "Corporate customers")