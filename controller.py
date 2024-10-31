# from model import 
from typing import Dict, List
from decimal import Decimal
# from view.login import Login
import os
from decimal import ROUND_HALF_UP

# The Company class is the controller class that manages the data and the business logic of the application.
class Company:
    def __init__(self):
        '''Initializes the Company class'''
        # 初始化商品数据
        self._parse_veggies()
        self._parse_premadeboxes()

    
    # 从文件中加载产品数据
    def _parse_veggies(self):
        """解析veggies.txt获取所有蔬菜选项"""
        try:
            if not os.path.exists('static/veggies.txt'):
                raise FileNotFoundError("static/veggies.txt file not found")
                
            with open('static/veggies.txt', 'r') as f:
                lines = f.readlines()
            
            # 初始化蔬菜列表
            self.all_veggies_list = []  # 所有蔬菜列表(供box contents使用)
            self.veggies_weight_list = []  # weight类蔬菜列表
            self.veggies_unit_list = []    # unit类蔬菜列表
            self.veggies_pack_list = []    # pack类蔬菜列表
            
            # 解析数据
            current_type = None
            for line in lines:
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                    
                if line.startswith('['):
                    current_type = line[1:-1]  # 移除[]
                elif '=' in line and current_type:
                    name, price = line.split('=')
                    name = name.strip()
                    price_decimal = Decimal(price.strip()).quantize(
                        Decimal('0.01'), rounding=ROUND_HALF_UP
                    )
                    formatted_item = f"{name} - ${float(price_decimal):.2f}"
                    
                    # 添加到总列表
                    self.all_veggies_list.append(formatted_item)
                    
                    # 添加到对应类型列表
                    if 'weight/kg' in name:
                        self.veggies_weight_list.append(formatted_item)
                    elif 'unit' in name:
                        self.veggies_unit_list.append(formatted_item)
                    elif 'pack' in name:
                        self.veggies_pack_list.append(formatted_item)

            print(self.all_veggies_list)
        
        except FileNotFoundError as e:
            print(f"File Error: {str(e)}")
            raise
                        
        # except FileNotFoundError as e:
        #     messagebox.showerror("File Error", str(e))
        #     raise
        # except Exception as e:
        #     messagebox.showerror("Error", f"Error parsing veggies.txt: {str(e)}")
        #     raise
    
    def _parse_premadeboxes(self):
        """解析premadeboxes.txt获取盒子配置"""
        try:
            if not os.path.exists('static/premadeboxes.txt'):
                raise FileNotFoundError("static/premadeboxes.txt file not found")
                
            with open('static/premadeboxes.txt', 'r') as f:
                lines = f.readlines()
            
            # 初始化盒子配置
            self.smallbox_default_dict = {'price': Decimal('0'), 'contents': []}
            self.mediumbox_default_dict = {'price': Decimal('0'), 'contents': []}
            self.largebox_default_dict = {'price': Decimal('0'), 'contents': []}
            
            current_size = None
            for line in lines:
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                    
                if line.startswith('['):
                    current_size = line[1:-1].lower()
                elif '=' in line and current_size:
                    key, value = line.split('=')
                    key = key.lower()
                    
                    if key == 'price':
                        # 保存价格
                        box_dict = getattr(self, f"{current_size}box_default_dict")
                        box_dict['price'] = Decimal(value.strip()).quantize(
                            Decimal('0.01'), rounding=ROUND_HALF_UP
                        )
                    elif key.startswith('item'):
                        # 保存内容项
                        box_dict = getattr(self, f"{current_size}box_default_dict")
                        box_dict['contents'].append(value.strip())
                        
        except FileNotFoundError as e:
            print(f"File Error: {str(e)}")
            raise

    # 从view/login.py中得到登录用户数据, 并根据用户数据从pickle文件中加载对应的用户object
    def get_user(self, username, user_type):
        '''Get the user object based on the username and password'''
        if user_type == "staff":
            # 在staff.pkl中查找staff object
            for staff in self.staff_members.values():
                if staff.username == username:
                    self.user = staff
        if user_type == "private":
            # 在private_customers.pkl中查找private customer object
            for private_customer in self.private_customers.values():
                if private_customer.username == username:
                    self.private_customers = private_customer
        if user_type == "corporate":
            # 在corporate_customers.pkl中查找corporate customer object
            for corporate_customer in self.corporate_customers.values():
                if corporate_customer.username == username:
                    self.user = corporate_customer


# Create Tkinter window
if __name__ == "__main__":
    company = Company()
    
    # login = Login(company)
    # login.run()
    # login.root.mainloop()
    # login.root.destroy()