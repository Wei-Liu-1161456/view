import pickle
from datetime import date, timedelta
from typing import List
from decimal import Decimal
from model import (
    Staff, Customer, CorporateCustomer,
    Order, CreditCardPayment, DebitCardPayment,
    DELIVERY_RADIUS_KM, DELIVERY_FEE
)
import sys
import os
# 将当前工作目录添加到路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_customer_distance(address: str) -> int:
    """Extract distance from customer address"""
    return int(address.split()[1])

def calculate_order_amounts(customer: Customer, base_amount: Decimal) -> tuple[Decimal, Decimal, Decimal]:
    """Calculate order amounts including delivery fee and discounts"""
    delivery_fee = Decimal('0.00')
    distance = get_customer_distance(customer.cust_address)
    
    # Check if delivery fee applies
    if distance > DELIVERY_RADIUS_KM:
        delivery_fee = DELIVERY_FEE
    
    # Apply discount if corporate customer (only to base amount, not delivery fee)
    if isinstance(customer, CorporateCustomer):
        discounted_amount = base_amount * (1 - customer.discount_rate)
    else:
        discounted_amount = base_amount
        
    total_amount = discounted_amount + delivery_fee
    
    return discounted_amount, delivery_fee, total_amount

# Create instances of the staff class
staff_member = Staff("John", "Doe", "staffJD", "12345", "Sales Department", date(2021, 1, 1), "S1000")

# Create instances of the customer class
pri_cust_member1 = Customer("Sally", "Smith", "privateSS", "12345", "Distance 10", Decimal('0.00'), Decimal('100.00'), "P1000")
pri_cust_member2 = Customer("Tom", "Brown", "privateTB", "12345", "Distance 30", Decimal('0.00'), Decimal('100.00'), "P1001")

# Create instances of the corporate customer class
co_cust_member1 = CorporateCustomer("Kim", "King", "corporateKK", "12345", "Distance 30", Decimal('0.00'), Decimal('100.00'), Decimal('0.10'), "C1000")
co_cust_member2 = CorporateCustomer("Luna", "Lory", "corporateLL", "12345", "Distance 20", Decimal('0.00'), Decimal('100.00'), Decimal('0.10'), "C1001")

# Create dictionaries to store the data
staff_members = {"S1000": staff_member}
private_customers = {"P1000": pri_cust_member1, "P1001": pri_cust_member2}
corporate_customers = {"C1000": co_cust_member1, "C1001": co_cust_member2}

def save_data(filename, data, datatype):
    """Save data to pickle file"""
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
        # print(f"{datatype} data saved to {filename}")

    # Load data
    with open("data/private_customers.pkl", 'rb') as file:
        private_customers = pickle.load(file)
    with open("data/corporate_customers.pkl", 'rb') as file:
        corporate_customers = pickle.load(file)

    # Analyze both customers
    # 显示staffs的信息
    print(staff_members)
    #显示私人客户和公司客户的信息
    print(private_customers)
    print(corporate_customers)
 

# Save all data
save_data("data/staffs.pkl", staff_members, "Staff")
print()
save_data("data/private_customers.pkl", private_customers, "Private customers")
save_data("data/corporate_customers.pkl", corporate_customers, "Corporate customers")

# Analyze the test data
# if __name__ == "__main__":
#     analyze_test_data()