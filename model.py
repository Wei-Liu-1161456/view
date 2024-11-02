from datetime import date
from typing import List, Dict, Tuple, Any
from decimal import Decimal
from abc import ABC, abstractmethod
import pickle
from enum import Enum

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
    def __init__(self, first_name: str, last_name: str, username: str, password: str, 
                 dept_name: str, date_joined: date, staff_ID: str):
        super().__init__(first_name, last_name, username, password)
        self.dept_name = dept_name
        self.date_joined = date_joined
        self.staff_ID = staff_ID
    
    def __str__(self):
        return (f"Staff ID: {self.staff_ID}\n"
                f"Name: {self.first_name} {self.last_name}\n"
                f"Username: {self.username}\n"
                f"Department: {self.dept_name}\n"
                f"Date Joined: {self.date_joined}")

    def _print_order_items(self, order: 'Order'):
        """Helper method to print order items with details"""
        print(f"Items:")
        for item in order.list_of_items:
            if isinstance(item, PremadeBox):
                print(f"- {item.item_name} ({item.box_size}) (${item.price})")
                print("  Contents:")
                for content_item in item.box_content:
                    print(f"    * {content_item.item_name}")
            else:
                print(f"- {item.item_name} x {item.quantity} (${item.total_price})")


    def show_current_orders(self) -> Dict[str, Dict[str, Any]]:
        """Show all orders with 'pending' status"""
        try:
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
                # first filter out orders with pending status
                pending_orders = {k: v for k, v in orders.items() 
                                if v.order_status == OrderStatus.PENDING}
                
                # and then create the result dictionary
                current_orders = {
                    order.order_number: {
                        "Customer": f"{order.order_customer.first_name} {order.order_customer.last_name}",
                        "Date": order.order_date,
                        "Status": order.order_status.value,
                        "Items": self._get_order_items_string(order),
                        "Subtotal": order.subtotal,
                        "Delivery Fee": order.delivery_fee,
                        "Total Amount": order.total_amount
                    } 
                    for order in pending_orders.values()
                }
                
                return current_orders
        except Exception as e:
            return {"Error": f"Error loading orders: {str(e)}"}

    def _get_order_items_string(self, order) -> str:
        """Helper method to format order items as string"""
        items_str = ""
        for item in order.list_of_items:
            if hasattr(item, 'quantity'):
                items_str += f"{item.item_name} x {item.quantity} "
            else:
                items_str += f"{item.item_name} "
        return items_str

    def show_previous_orders(self) -> Dict[str, Dict[str, Any]]:
        """Show all orders with 'fulfilled' status"""
        try:
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
                # 先筛选出 fulfilled 状态的订单
                fulfilled_orders = {k: v for k, v in orders.items() 
                                if v.order_status == OrderStatus.FULFILLED}
                
                # 然后创建结果字典
                previous_orders = {
                    order.order_number: {
                        "Customer": f"{order.order_customer.first_name} {order.order_customer.last_name}",
                        "Date": order.order_date,
                        "Status": order.order_status.value,
                        "Items": self._get_order_items_string(order),
                        "Subtotal": order.subtotal,
                        "Delivery Fee": order.delivery_fee,
                        "Total Amount": order.total_amount
                    } 
                    for order in fulfilled_orders.values()
                }
                
                return previous_orders
        except Exception as e:
            return {"Error": f"Error loading orders: {str(e)}"}

    def show_all_customers(self) -> str:
        """Show all customers (both private and corporate) and return a formatted string for display.
        
        Returns:
            A formatted string containing all customer information.
        """
        try:
            # Load private customers
            with open('data/private_customers.pkl', 'rb') as file:
                private_customers = pickle.load(file)
            
            # Load corporate customers
            with open('data/corporate_customers.pkl', 'rb') as file:
                corporate_customers = pickle.load(file)
            
            # Initialize formatted strings for display
            formatted_customers = "\n=== Private Customers ===\n"
            for cust_id, customer in private_customers.items():
                formatted_customers += (
                    f"\nCustomer ID: {cust_id}\n"
                    f"Name: {customer.first_name} {customer.last_name}\n"
                    f"Address: {customer.cust_address}\n"
                    f"Balance: ${customer.cust_balance}\n"
                    f"Max Owing: ${customer.max_owing}\n"
                )
            
            formatted_customers += "\n=== Corporate Customers ===\n"
            for cust_id, customer in corporate_customers.items():
                formatted_customers += (
                    f"\nCustomer ID: {cust_id}\n"
                    f"Name: {customer.first_name} {customer.last_name}\n"
                    f"Address: {customer.cust_address}\n"
                    f"Balance: ${customer.cust_balance}\n"
                    f"Max Owing: ${customer.max_owing}\n"
                    f"Discount Rate: {customer.discount_rate * 100}%\n"
                )
            
            # Return the combined formatted string
            return formatted_customers
        except Exception as e:
            # Return an error message if loading fails
            return "Error loading customers."

    def show_sales_report(self, start_date: date, end_date: date) -> str:
        """Generate a sales report for a specific date range.
        
        This method loads orders from a pickle file, filters them based on the date range,
        and generates a formatted report string containing order details and total sales.
        
        Args:
            start_date (date): Start date of the report period
            end_date (date): End date of the report period
            
        Returns:
            str: Formatted sales report containing:
                - Report header with date range
                - Total sales amount
                - Details for each order in the date range:
                    - Order number
                    - Customer information
                    - Order date
                    - Order items
                    - Pricing details (original total, discount if applicable, final amount)
                    
        Note:
            For corporate customers, additional discount information is included.
        """
        try:
            # Load orders from pickle file
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
            
            # Filter orders within the date range
            valid_orders = [
                order for order in orders.values()
                if start_date <= order.order_date <= end_date
            ]
            
            # Calculate total sales for the period
            total_sales = sum(order.sales_amount for order in valid_orders)
            
            # Initialize report string
            report = []
            report.append(f"=== Sales Report ({start_date} to {end_date}) ===")
            report.append(f"Total Sales: ${total_sales}\n")
            
            # Add details for each order
            for order in valid_orders:
                # Order header information
                report.append(f"Order Number: {order.order_number}")
                report.append(f"Customer: {order.order_customer.first_name} {order.order_customer.last_name}")
                report.append(f"Date: {order.order_date}")
                
                # Add order items
                items_str = self._get_order_items_str(order)  # Assuming you'll create this helper method
                report.append(items_str)
                
                # Add pricing details
                if isinstance(order.order_customer, CorporateCustomer):
                    report.append(f"Original Total: ${order.subtotal}")
                    report.append(f"Discount ({order.order_customer.discount_rate * 100}%): ${order.discount}")
                report.append(f"Final Sales Amount: ${order.sales_amount}\n")
            
            # Join all report lines with newlines
            print('\'n'.join(report))
            return '\n'.join(report)
            
        except Exception as e:
            error_msg = f"Error generating sales report: {e}"
            return error_msg

    def _get_order_items_str(self, order) -> str:
        """Helper method to format order items information.
        
        Args:
            order: Order object containing items information
            
        Returns:
            str: Formatted string containing items details
        """
        items_lines = []
        items_lines.append("Items:")
        for item in order.list_of_items:
            items_lines.append(f"  - {item.quantity}x {item.product.name} (${item.price} each)")
        return '\n'.join(items_lines)

    def show_popular_products(self) -> str:
        """Show popular products based on quantity sold across different categories (veggies and premade boxes).
        
        Returns:
            A formatted string listing the popular products and their total quantities sold, sorted from high to low.
        """
        try:
            # Load orders from the pickle file
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
            
            # Initialize dictionaries to keep track of product quantities sold
            veggie_sales = {}     # For all veggie products (including those in premade boxes)
            premade_box_sales = {} # For premade boxes
            
            for order in orders.values():
                for item in order.list_of_items:
                    # Check if item is a veggie product
                    if isinstance(item, WeightedVeggie) or isinstance(item, UnitPriceVeggie) or isinstance(item, PackVeggie):
                        item_name = item.item_name
                        if isinstance(item, WeightedVeggie):
                            veggie_sales[item_name] = veggie_sales.get(item_name, 0) + item.weight
                        elif isinstance(item, UnitPriceVeggie):
                            veggie_sales[item_name] = veggie_sales.get(item_name, 0) + item.quantity
                        elif isinstance(item, PackVeggie):
                            veggie_sales[item_name] = veggie_sales.get(item_name, 0) + item.num_of_pack
                    
                    # Check if the order contains premade boxes
                    if isinstance(item, PremadeBox):
                        box_name = item.item_name
                        # Count the premade box itself
                        premade_box_sales[box_name] = premade_box_sales.get(box_name, 0) + item.quantity
                        
                        # Count the contents of the premade box
                        for content in item.box_content:
                            content_name = content.item_name
                            if isinstance(content, WeightedVeggie):
                                veggie_sales[content_name] = veggie_sales.get(content_name, 0) + content.weight
                            elif isinstance(content, UnitPriceVeggie):
                                veggie_sales[content_name] = veggie_sales.get(content_name, 0) + content.quantity
                            elif isinstance(content, PackVeggie):
                                veggie_sales[content_name] = veggie_sales.get(content_name, 0) + content.num_of_pack

            # Sort veggie sales from high to low
            sorted_veggie_sales = sorted(veggie_sales.items(), key=lambda x: x[1], reverse=True)
            
            # Sort premade box sales from high to low
            sorted_premade_box_sales = sorted(premade_box_sales.items(), key=lambda x: x[1], reverse=True)

            # Prepare formatted strings for each category
            formatted_products = "\n=== Popular Products by Category ===\n"
            
            # Format veggie sales
            formatted_products += "\n[Veggie Products]\n"
            for item_name, total_quantity in sorted_veggie_sales:
                formatted_products += f"{item_name}: {total_quantity:.2f} sold\n"

            # Format premade box sales
            formatted_products += "\n[Premade Boxes]\n"
            for box_name, quantity in sorted_premade_box_sales:
                formatted_products += f"{box_name}: {quantity} sold\n"

            # Return the formatted string for display
            return formatted_products
        
        except Exception as e:
            # Return an error message if there is an exception during processing
            return f"Error generating popular products report: {e}"


    def fulfill_order(self, order_number: str) -> bool:
        """Update order status from pending to fulfilled
        Can only be called from current orders view
        """
        try:
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
            
            order = orders.get(order_number)
            if not order:
                print(f"Order {order_number} not found")
                return False
            
            order.order_status = OrderStatus.FULFILLED
            orders[order_number] = order
            
            with open('data/orders.pkl', 'wb') as file:
                pickle.dump(orders, file)
            
            return True
        except Exception as e:
            print(f"Error fulfilling order: {e}")
            return False

class DeliveryMethod(Enum):
    PICKUP = "pickup"
    DELIVERY = "delivery"

class Customer(Person):
    def __init__(self, first_name: str, last_name: str, username: str, password: str, 
                 cust_address: str, cust_balance: Decimal, max_owing: Decimal, cust_id: str):
        super().__init__(first_name, last_name, username, password)
        self.cust_address = cust_address
        self.cust_balance = cust_balance
        self.max_owing = max_owing
        self.list_of_orders = []
        self.list_of_payments = []
        self.cust_id = cust_id
        # 新增：根据地址确定是否支持配送
        try:
            distance = int(''.join(filter(str.isdigit, self.cust_address)))
            self.can_delivery = distance <= DELIVERY_RADIUS_KM
        except ValueError:
            self.can_delivery = False

    def __str__(self) -> str:
        return (f"Customer ID: {self.cust_id}\n"
                f"Name: {self.first_name} {self.last_name}\n"
                f"Username: {self.username}\n"
                f"Address: {self.cust_address}\n"
                f"Balance: ${self.cust_balance:.2f}\n"
                f"Maximum Owing: ${self.max_owing:.2f}\n"
                f"Delivery Available: {'Yes' if self.can_delivery else 'No'}\n")


    def can_place_order(self, order_amount: Decimal) -> bool:
        """Check if customer can place order based on total amount and max owing limit"""
        try:
            with open('data/private_customers.pkl', 'rb') as file:
                customers = pickle.load(file)
                customer = customers.get(self.cust_id)
                if customer:
                    potential_balance = customer.cust_balance + order_amount
                    can_place = potential_balance <= customer.max_owing
                    print(f"Order amount: ${order_amount}")
                    print(f"Current balance: ${customer.cust_balance}")
                    print(f"Max owing: ${customer.max_owing}")
                    print(f"Can place order: {can_place}")
                    return can_place
                return False
        except Exception as e:
            print(f"Error checking order possibility: {e}")
            return False

    def make_payment(self, *, payment_amount: Decimal, payment_date: date, 
                payment_method: str, **kwargs) -> bool:
        """Make payment using credit or debit card for corporate customer"""
        try:
            # 添加支付方式验证
            if payment_method not in ["credit", "debit", "account"]:
                raise ValueError(f"Invalid payment method: {payment_method}")
                
            # 创建支付记录
            if payment_method == "credit":
                # 检查必需的信用卡参数是否都存在
                required_credit_params = ['card_number', 'card_type', 
                                        'card_expiry_date', 'cvv', 'card_holder']
                for param in required_credit_params:
                    if param not in kwargs:
                        raise ValueError(f"Missing required credit card parameter: {param}")
                        
                payment = CreditCardPayment(
                    payment_amount=payment_amount,
                    payment_date=payment_date,
                    card_number=kwargs['card_number'],
                    card_type=kwargs['card_type'],
                    card_expiry_date=kwargs['card_expiry_date'],
                    cvv=kwargs['cvv'],
                    card_holder=kwargs['card_holder']
                )
                
            elif payment_method == "debit":
                # 检查必需的借记卡参数是否都存在
                required_debit_params = ['bank_name', 'debit_card_num']
                for param in required_debit_params:
                    if param not in kwargs:
                        raise ValueError(f"Missing required debit card parameter: {param}")
                        
                payment = DebitCardPayment(
                    payment_amount=payment_amount,
                    payment_date=payment_date,
                    bank_name=kwargs['bank_name'],
                    debit_card_num=kwargs['debit_card_num']
                )

            # 更新支付记录
            with open('data/payments.pkl', 'rb') as file:
                payments = pickle.load(file)
            payments[payment.payment_id] = payment

            # 保存支付记录
            with open('data/payments.pkl', 'wb') as file:
                pickle.dump(payments, file)

            print(f"Payment successful: ${payment_amount}")
            return True

        except Exception as e:
            print(f"Error processing payment: {e}")
            return False

    def check_out_with_payment(self, items: List['Item'], delivery_method: DeliveryMethod,
                          payment_method: str, *, 
                          # credit card parameters
                          card_number: str = None,
                          card_type: str = None, 
                          card_expiry_date: date = None,
                          cvv: str = None,
                          card_holder: str = None,
                          # debit card parameters
                          bank_name: str = None,
                          debit_card_num: str = None) -> bool:
        """Process checkout with immediate payment"""
        try:
            # 1. 创建订单
            order = Order(
                order_customer=self,
                order_date=date.today(),
                delivery_method=delivery_method
            )
            order.set_items(items)

            # 2. 验证订单金额
            if not self.can_place_order(order.total_amount):
                print("Order amount exceeds available credit")
                return False

            # 3. 处理支付
            if payment_method == "account":
                # 账户支付
                if not self.charge_to_account(order.total_amount):
                    return False
            elif payment_method == "credit":
                # 信用卡支付
                if not self.make_payment(
                    payment_amount=order.total_amount,
                    payment_date=date.today(),
                    payment_method=payment_method,
                    card_number=card_number,
                    card_type=card_type,
                    card_expiry_date=card_expiry_date,
                    cvv=cvv,
                    card_holder=card_holder
                ):
                    return False
            else:  # debit
                # 借记卡支付
                if not self.make_payment(
                    payment_amount=order.total_amount,
                    payment_date=date.today(),
                    payment_method=payment_method,
                    bank_name=bank_name,
                    debit_card_num=debit_card_num
                ):
                    return False

            # 4. 保存订单
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
            with open('data/private_customers.pkl', 'rb') as file:
                customers = pickle.load(file)

            # 5. 更新订单状态
            order.order_status = OrderStatus.PENDING
            self.list_of_orders.append(order)
            orders[order.order_number] = order
            customers[self.cust_id] = self

            # 6. 保存更新
            with open('data/orders.pkl', 'wb') as file:
                pickle.dump(orders, file)
            with open('data/private_customers.pkl', 'wb') as file:
                pickle.dump(customers, file)

            print(f"Order {order.order_number} created and paid successfully")
            return True

        except Exception as e:
            print(f"Error during checkout and payment: {e}")
            return False
        
    def charge_to_account(self, amount: Decimal) -> bool:
        """Charge amount to customer account"""
        try:
            with open('data/private_customers.pkl', 'rb') as file:
                customers = pickle.load(file)
                if self.cust_id not in customers:
                    return False
                
                self.cust_balance += amount
                customers[self.cust_id] = self
                
                with open('data/private_customers.pkl', 'wb') as file:
                    pickle.dump(customers, file)
                
                print(f"Successfully charged ${amount} to account {self.cust_id}")
                return True
        except Exception as e:
            print(f"Error charging to account: {e}")
            return False

    def view_current_orders(self) -> List['Order']:
        """View customer's current (pending) orders"""
        try:
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
                current_orders = [
                    order for order in orders.values()
                    if order.order_customer.cust_id == self.cust_id 
                    and order.order_status == OrderStatus.PENDING
                ]
                print(f"\nCurrent orders for customer {self.cust_id}:")
                for order in current_orders:
                    print(f"\n{order}")
                return current_orders
        except Exception as e:
            print(f"Error viewing current orders: {e}")
            return []

    def view_previous_orders(self) -> List['Order']:
        """View customer's fulfilled orders"""
        try:
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
                previous_orders = [
                    order for order in orders.values()
                    if order.order_customer.cust_id == self.cust_id 
                    and order.order_status == OrderStatus.FULFILLED
                ]
                print(f"\nPrevious orders for customer {self.cust_id}:")
                for order in previous_orders:
                    print(f"\n{order}")
                return previous_orders
        except Exception as e:
            print(f"Error viewing previous orders: {e}")
            return []


class CorporateCustomer(Customer):
    def __init__(self, first_name: str, last_name: str, username: str, password: str, 
                 cust_address: str, cust_balance: Decimal, max_owing: Decimal, 
                 discount_rate: Decimal, corporate_cust_id: str):
        super().__init__(first_name, last_name, username, password, 
                        cust_address, cust_balance, max_owing, corporate_cust_id)
        self.discount_rate = discount_rate

    def __str__(self) -> str:
        """String representation including discount rate"""
        base_str = super().__str__()
        return base_str[:-1] + f"\nDiscount Rate: {self.discount_rate:.0%}\n"

    def can_place_order(self, order_amount: Decimal) -> bool:
        """Check if corporate customer can place order based on total amount and max owing limit"""
        try:
            with open('data/corporate_customers.pkl', 'rb') as file:  # 改用corporate文件
                customers = pickle.load(file)
                customer = customers.get(self.cust_id)
                if customer:
                    potential_balance = customer.cust_balance + order_amount
                    can_place = potential_balance <= customer.max_owing
                    print(f"Order amount: ${order_amount}")
                    print(f"Current balance: ${customer.cust_balance}")
                    print(f"Max owing: ${customer.max_owing}")
                    print(f"Can place order: {can_place}")
                    return can_place
                return False
        except Exception as e:
            print(f"Error checking order possibility: {e}")
            return False

    def check_out_with_payment(self, items: List['Item'], delivery_method: DeliveryMethod,
                          payment_method: str, *, 
                          # credit card parameters
                          card_number: str = None,
                          card_type: str = None, 
                          card_expiry_date: date = None,
                          cvv: str = None,
                          card_holder: str = None,
                          # debit card parameters
                          bank_name: str = None,
                          debit_card_num: str = None) -> bool:
        """Process checkout with immediate payment for corporate customer"""
        try:
            # 1. 创建订单
            order = Order(
                order_customer=self,
                order_date=date.today(),
                delivery_method=delivery_method
            )
            order.set_items(items)

            # 2. 验证订单金额
            if not self.can_place_order(order.total_amount):
                print("Order amount exceeds available credit limit for corporate customer")
                return False

            # 3. 处理支付
            if payment_method == "account":
                # 账户支付
                if not self.charge_to_account(order.total_amount):
                    return False
            elif payment_method == "credit":
                # 信用卡支付
                if not self.make_payment(
                    payment_amount=order.total_amount,
                    payment_date=date.today(),
                    payment_method=payment_method,
                    card_number=card_number,
                    card_type=card_type,
                    card_expiry_date=card_expiry_date,
                    cvv=cvv,
                    card_holder=card_holder
                ):
                    return False
            else:  # debit
                # 借记卡支付
                if not self.make_payment(
                    payment_amount=order.total_amount,
                    payment_date=date.today(),
                    payment_method=payment_method,
                    bank_name=bank_name,
                    debit_card_num=debit_card_num
                ):
                    return False

            # 4. 保存订单
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
            with open('data/corporate_customers.pkl', 'rb') as file:  # 这里改为corporate
                customers = pickle.load(file)

            # 5. 更新订单状态
            order.order_status = OrderStatus.PENDING
            self.list_of_orders.append(order)
            orders[order.order_number] = order
            customers[self.cust_id] = self

            # 6. 保存更新
            with open('data/orders.pkl', 'wb') as file:
                pickle.dump(orders, file)
            with open('data/corporate_customers.pkl', 'wb') as file:  # 这里改为corporate
                pickle.dump(customers, file)

            print(f"Corporate customer order {order.order_number} created and paid successfully")
            print(f"Applied discount rate: {self.discount_rate:.0%}")
            return True

        except Exception as e:
            print(f"Error during corporate checkout and payment: {e}")
            return False
        
    def charge_to_account(self, amount: Decimal) -> bool:
        """Charge amount to corporate customer account"""
        try:
            with open('data/corporate_customers.pkl', 'rb') as file:
                customers = pickle.load(file)
                if self.cust_id not in customers:
                    return False
                
                self.cust_balance += amount
                customers[self.cust_id] = self
                
                with open('data/corporate_customers.pkl', 'wb') as file:
                    pickle.dump(customers, file)
                
                print(f"Successfully charged ${amount} to corporate account {self.cust_id}")
                return True
        except Exception as e:
            print(f"Error charging to corporate account: {e}")
            return False

     #------------------后续需要删除, 只用来测试信息是否正确------------------   
    def view_current_orders(self) -> List['Order']:
            """View corporate customer's current (pending) orders"""
            try:
                with open('data/orders.pkl', 'rb') as file:
                    orders = pickle.load(file)
                    current_orders = [
                        order for order in orders.values()
                        if order.order_customer.cust_id == self.cust_id 
                        and order.order_status == OrderStatus.PENDING
                    ]
                    print(f"\nCurrent orders for corporate customer {self.cust_id}:")
                    for order in current_orders:
                        print(f"\n{order}")
                    return current_orders
            except Exception as e:
                print(f"Error viewing current orders: {e}")
                return []
    #------------------后续需要删除, 只用来测试信息是否正确------------------
    def view_previous_orders(self) -> List['Order']:
        """View corporate customer's fulfilled orders"""
        try:
            with open('data/orders.pkl', 'rb') as file:
                orders = pickle.load(file)
                previous_orders = [
                    order for order in orders.values()
                    if order.order_customer.cust_id == self.cust_id 
                    and order.order_status == OrderStatus.FULFILLED
                ]
                print(f"\nPrevious orders for corporate customer {self.cust_id}:")
                for order in previous_orders:
                    print(f"\n{order}")
                return previous_orders
        except Exception as e:
            print(f"Error viewing previous orders: {e}")
            return []


class Payment:
    payment_id = 1000
    def __init__(self, *, payment_amount: Decimal, payment_date: date):
        """Initialize Payment with keyword arguments
        Args:
            payment_amount: Amount of payment
            payment_date: Date of payment
        """
        self.payment_id = f"PAY{Payment.payment_id}"
        Payment.payment_id += 1
        self.payment_amount = Decimal(str(payment_amount))
        self.payment_date = payment_date

#==================fianal version==================
class CreditCardPayment(Payment):
    def __init__(self, *, payment_amount: Decimal, payment_date: date,
                 card_number: str, card_type: str, card_expiry_date: date,
                 cvv: str, card_holder: str):
        """Initialize CreditCardPayment with keyword arguments
        Args:
            payment_amount: Amount of payment
            payment_date: Date of payment
            card_number: Credit card number
            card_type: Type of credit card
            card_expiry_date: Card expiry date
            cvv: Card verification value
            card_holder: Name of the card holder
        """
        super().__init__(payment_amount=payment_amount, payment_date=payment_date)
        self.card_number = card_number
        self.card_type = card_type
        self.card_expiry_date = card_expiry_date
        self.cvv = cvv
        self.card_holder = card_holder

#==================fianal version==================
class DebitCardPayment(Payment):
    def __init__(self, *, payment_amount: Decimal, payment_date: date,
                 bank_name: str, debit_card_num: str):
        """Initialize DebitCardPayment with keyword arguments
        Args:
            payment_amount: Amount of payment
            payment_date: Date of payment
            bank_name: Name of the bank
            debit_card_num: Debit card number
        """
        super().__init__(payment_amount=payment_amount, payment_date=payment_date)
        self.bank_name = bank_name
        self.debit_card_num = debit_card_num

#==================fianal version==================
class OrderStatus(Enum):
    PENDING = "pending"
    FULFILLED = "fulfilled"

class DeliveryMethod(Enum):
    PICKUP = "pickup"
    DELIVERY = "delivery"
class Order:
    order_id = 1000
    def __init__(self, order_customer: 'Customer', order_date: date, delivery_method: DeliveryMethod):
        self.order_number = f"ORD{Order.order_id}"
        Order.order_id += 1
        self.order_customer = order_customer
        self.order_date = order_date
        self.order_status = OrderStatus.PENDING
        self.list_of_items: List[Item] = []
        self.delivery_method = delivery_method
        self.delivery_fee = DELIVERY_FEE if delivery_method == DeliveryMethod.DELIVERY else Decimal('0.00')
        self.subtotal = Decimal('0.00')  # 商品总价
        self.discount = Decimal('0.00')  # 企业客户折扣金额
        self.sales_amount = Decimal('0.00')  # 实际销售额
        self.total_amount = Decimal('0.00')  # 总金额

    def __str__(self) -> str:
        """String representation of the order"""
        # Initialize a list of lines with main order information
        lines = [
            f"Order Number: {self.order_number}",       # Order number
            f"Customer: {self.order_customer}",         # Customer information
            f"Order Date: {self.order_date}",           # Order date
            f"Status: {self.order_status.value}",       # Order status
            f"Delivery Method: {self.delivery_method.value}",  # Delivery method
            f"Delivery Fee: ${self.delivery_fee:.2f}",  # Delivery fee (formatted to 2 decimal places)
            "\nItems List:"                             # Items list heading
        ]
        
        # If there are items in the order, format each item with indentation
        if self.list_of_items:
            for item in self.list_of_items:
                # Split each item string into lines and add indentation for readability
                item_lines = str(item).split('\n')
                lines.extend(f"    {line}" for line in item_lines)
        else:
            # If no items, indicate that the list is empty
            lines.append("    No items")
        
        # Add the financial summary at the end
        lines.extend([
            f"\nSubtotal: ${self.subtotal:.2f}",        # Subtotal amount
            f"Discount: ${self.discount:.2f}",          # Discount amount
            f"Sales Amount: ${self.sales_amount:.2f}",  # Sales amount after discount
            f"Total Amount: ${self.total_amount:.2f}"   # Total amount due
        ])
        
        # Join all lines with newlines for a well-formatted output
        return '\n'.join(lines)
        

    def set_items(self, items: List['Item']):
        """Set all order items at once and calculate amounts"""
        self.list_of_items = items
        self.calculate_all_amounts()

    def calculate_subtotal(self):
        """Calculate subtotal from all items"""
        self.subtotal = sum(item.total_price for item in self.list_of_items)

    def calculate_discount(self):
        """Calculate discount if customer is corporate"""
        if isinstance(self.order_customer, CorporateCustomer):
            self.discount = self.subtotal * self.order_customer.discount_rate
        else:
            self.discount = Decimal('0.00')

    def calculate_sales_amount(self):
        """Calculate sales amount (subtotal - discount)"""
        self.sales_amount = self.subtotal - self.discount

    def calculate_total_amount(self):
        """Calculate final total amount including delivery fee"""
        self.total_amount = self.sales_amount + self.delivery_fee

    def calculate_all_amounts(self):
        """Calculate all amounts in the correct order"""
        self.calculate_subtotal()
        self.calculate_discount()
        self.calculate_sales_amount()
        self.calculate_total_amount()

    def __str__(self):
        """String representation of the order"""
        order_str = [
            f"Order Number: {self.order_number}",
            f"Customer: {self.order_customer.first_name} {self.order_customer.last_name}",
            f"Date: {self.order_date}",
            f"Status: {self.order_status.value}",
            f"Delivery Method: {self.delivery_method.value}",
            "\nItems:"
        ]
        
        for item in self.list_of_items:
            if isinstance(item, PremadeBox):
                order_str.append(f"- {item.item_name} ({item.box_size}) (${item.price})")
                order_str.append("  Contents:")
                for content_item in item.box_content:
                    order_str.append(f"    * {content_item.item_name}")
            else:
                order_str.append(f"- {item.item_name} x {item.quantity} (${item.total_price})")
        
        order_str.extend([
            f"\nSubtotal: ${self.subtotal}",
            f"Discount: ${self.discount}" if self.discount > 0 else "",
            f"Sales Amount: ${self.sales_amount}",
            f"Delivery Fee: ${self.delivery_fee}" if self.delivery_method == DeliveryMethod.DELIVERY else "",
            f"Total Amount: ${self.total_amount}"
        ])
        
        return "\n".join([s for s in order_str if s != ""])  # 移除空字符串

class Item(ABC):
    def __init__(self, name: str):
        # 商品的名字(/商品的类型)
        self.item_name = name
        # 商品的总价
        self.total_price = Decimal('0.00')

    @abstractmethod # 计算商品的总价
    def calculate_total(self):
        pass
    

class Veggie(Item):
    def __init__(self, veg_name: str):
        super().__init__(veg_name)
        # self.veg_name = veg_name
    
    def __str__(self):
        return f"Name: {self.item_name}\n"


class WeightedVeggie(Veggie):
    def __init__(self, veg_name: str, weight: Decimal, weight_per_kilo: Decimal):
        super().__init__(veg_name)
        # 商品的数量
        self.weight = Decimal(str(weight))
        # 商品的单价
        self.price_per_kilo = Decimal(str(weight_per_kilo))

    # 计算商品的总价
    def calculate_total(self):
        self.total_price = self.weight * self.price_per_kilo


    def __str__(self):
        return super().__str__() + f"Weight: {self.weight} kg\nPrice per kilo: ${self.price_per_kilo}"


class PackVeggie(Veggie):
    def __init__(self, veg_name: str, num_of_pack: int, price_per_pack: Decimal):
        super().__init__(veg_name)
        # 商品的数量
        self.num_of_pack = num_of_pack
        # 商品的单价
        self.price_per_pack = Decimal(str(price_per_pack))

    # 计算商品的总价
    def calculate_total(self):
        self.total_price = self.num_of_pack * self.price_per_pack

    def __str__(self):
        return super().__str__() + f"Number of packs: {self.num_of_pack}\nPrice per pack: ${self.price_per_pack}"

class UnitPriceVeggie(Veggie):
    def __init__(self, veg_name: str, quantity: int,price_per_unit: Decimal):
        super().__init__(veg_name)
        # 商品的数量
        self.quantity = quantity
        # 商品的单价
        self.price_per_unit = Decimal(str(price_per_unit))
    
    # 计算商品的总价
    def calculate_total(self):
        self.total_price = self.quantity * self.price_per_unit

    def __str__(self):
        return super().__str__() + f"Quantity: {self.quantity}\nPrice per unit: ${self.price_per_unit}"

class PremadeBox(Item):
    def __init__(self, box_size: str, quantity:int, price: Decimal):
        super().__init__(box_size)
        # box的内容
        self.box_content: List['Item'] = []
        # box的数量
        self.quantity = quantity
        # box的价格
        self.price = price

    # 设置商品的content list
    def set_content(self, content: List['Item']):
        self.box_content = content

    # 计算商品的总价
    def calculate_total(self):
        self.total_price = self.quantity * self.price

    def __str__(self):
        return (f"Box Size: {self.item_name}\n"
                f"Quantity: {self.quantity}\n"
                f"Price: ${self.price}\n"
                f"Contents: {', '.join([item.item_name for item in self.box_content])}")