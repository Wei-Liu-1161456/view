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

def create_test_orders_and_payments():
    # Get today's date
    today = date.today()
    
    # Generate test dates ensuring all are in the past
    test_dates = []
    
    # This week (only past days)
    start_of_week = today - timedelta(days=today.weekday())
    for i in range(today.weekday()):
        test_day = start_of_week + timedelta(days=i)
        if test_day < today:
            test_dates.append(test_day)
    
    # Last week (2 samples)
    start_of_last_week = start_of_week - timedelta(days=7)
    test_dates.extend([
        start_of_last_week + timedelta(days=2),
        start_of_last_week + timedelta(days=4)
    ])
    
    # This month (2 samples from past days)
    start_of_month = date(today.year, today.month, 1)
    if start_of_month < today:
        test_dates.extend([
            start_of_month + timedelta(days=min(5, (today - start_of_month).days - 1)),
            start_of_month + timedelta(days=min(10, (today - start_of_month).days - 1))
        ])
    
    # Last month (2 samples)
    last_month = (today.replace(day=1) - timedelta(days=1))
    test_dates.extend([
        date(last_month.year, last_month.month, 10),
        date(last_month.year, last_month.month, 20)
    ])
    
    # Earlier this year (2 samples)
    if today.month > 2:
        test_dates.extend([
            date(today.year, today.month-2, 15),
            date(today.year, today.month-2, 25)
        ])
    
    # Past year (2 samples)
    test_dates.extend([
        today - timedelta(days=200),
        today - timedelta(days=300)
    ])

    # Sort dates in ascending order
    test_dates.sort()

    # Generate orders and payments for P1000 (private customer)
    base_amount = Decimal('50.00')
    for idx, order_date in enumerate(test_dates):
        # Calculate amounts
        order_amount, delivery_fee, total_amount = calculate_order_amounts(pri_cust_member1, base_amount)
        
        # Create order
        order = Order(pri_cust_member1, order_date, "fulfilled")  # order_number 参数虽然不用但还是要传空字符串
        order.order_amount = order_amount
        order.delivery_fee = delivery_fee
        order.total_amount = total_amount
        pri_cust_member1.list_of_orders.append(order)
        
        # Create alternating credit/debit card payments
        if idx % 2 == 0:
            payment = CreditCardPayment(
                total_amount,
                order_date,
                "4111-1111-1111-1111",
                "VISA",
                date(2025, 12, 31)
            )
        else:
            payment = DebitCardPayment(
                total_amount,
                order_date,
                "ABC Bank",
                "1234-5678-9012-3456"
            )
        pri_cust_member1.list_of_payments.append(payment)

    # Generate orders and payments for C1000 (corporate customer)
    base_amount = Decimal('100.00')
    for idx, order_date in enumerate(test_dates):
        # Calculate amounts
        order_amount, delivery_fee, total_amount = calculate_order_amounts(co_cust_member1, base_amount)
        
        # Create order
        order = Order(co_cust_member1, order_date, "fulfilled")  # 同上
        order.order_amount = order_amount
        order.delivery_fee = delivery_fee
        order.total_amount = total_amount
        co_cust_member1.list_of_orders.append(order)
        
        # Create alternating payment types
        if idx % 2 == 0:
            payment = CreditCardPayment(
                total_amount,
                order_date,
                "5555-5555-5555-5555",
                "MASTERCARD",
                date(2025, 12, 31)
            )
        else:
            payment = DebitCardPayment(
                total_amount,
                order_date,
                "XYZ Bank",
                "9876-5432-1098-7654"
            )
        co_cust_member1.list_of_payments.append(payment)

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
        print(f"{datatype} data saved to {filename}")

def analyze_test_data():
    """Load and analyze the test data"""
    def print_customer_orders(customer, customer_type):
        print(f"\n{customer_type} Customer: {customer.first_name} {customer.last_name}")
        print(f"Customer ID: {customer.cust_id}")
        print(f"Address: {customer.cust_address}")
        if isinstance(customer, CorporateCustomer):
            print(f"Discount Rate: {customer.discount_rate:.1%}")
        
        print("\nOrders:")
        for order in customer.list_of_orders:
            print(f"\nOrder {order.order_number} - Date: {order.order_date}")
            print(f"Base Amount: ${order.order_amount:.2f}")
            if order.delivery_fee > 0:
                print(f"Delivery Fee: ${order.delivery_fee:.2f}")
            print(f"Total Amount: ${order.total_amount:.2f}")
        
        print("\nPayments:")
        for payment in customer.list_of_payments:
            payment_type = "Credit Card" if isinstance(payment, CreditCardPayment) else "Debit Card"
            print(f"{payment_type} Payment - Date: {payment.payment_date}, Amount: ${payment.payment_amount:.2f}")

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
    print_customer_orders(private_customers["P1000"], "Private")
    print("\n" + "="*50)
    print_customer_orders(corporate_customers["C1000"], "Corporate")

# Create test data and save
create_test_orders_and_payments()

# Save all data
save_data("data/staffs.pkl", staff_members, "Staff")
save_data("data/private_customers.pkl", private_customers, "Private customers")
save_data("data/corporate_customers.pkl", corporate_customers, "Corporate customers")

# Analyze the test data
if __name__ == "__main__":
    analyze_test_data()