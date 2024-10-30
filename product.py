import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, ROUND_HALF_UP
import os

class Product:
    def __init__(self, parent):
        """
        初始化Product类
        parent: 父级窗口部件
        """
        try:
            # 初始化固定值
            self.small_size = 3
            self.medium_size = 4
            self.large_size = 5
            
            # 初始化商品数据
            self._parse_veggies()
            self._parse_premadeboxes()
            
            # 创建主Frame
            self.main_frame = ttk.Frame(parent)
            
            # 创建notebook
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
            
            # 创建A类和B类的frame
            self.a_frame = ttk.Frame(self.notebook)
            self.b_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.a_frame, text='Veggies')
            self.notebook.add(self.b_frame, text='Premade Boxes')
            
            # 初始化变量
            self.a_type_var = tk.StringVar(value='weight/kg')
            self.b_size_var = tk.StringVar(value='small')
            
            # 初始化界面
            self._setup_a_products()
            self._setup_b_products()
            self._setup_cart()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Error initializing product system: {str(e)}")
            raise
    
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
                        
        except FileNotFoundError as e:
            messagebox.showerror("File Error", str(e))
            raise
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing veggies.txt: {str(e)}")
            raise
    
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
            messagebox.showerror("File Error", str(e))
            raise
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing premadeboxes.txt: {str(e)}")
            raise

    def _setup_a_products(self):
        """设置A类商品(Veggies)界面"""
        # 主容器使用grid布局
        main_container = ttk.Frame(self.a_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        main_container.grid_columnconfigure(0, weight=1)
        
        # A类商品选择区域 - row 0
        type_frame = ttk.Frame(main_container)
        type_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # A类商品的Radiobuttons
        for i, a_type in enumerate(['weight/kg', 'unit', 'pack']):
            ttk.Radiobutton(
                type_frame,
                text=a_type,
                value=a_type,
                variable=self.a_type_var,
                command=self._update_a_products
            ).grid(row=0, column=i, padx=5)
        
        # Product选择区域 - row 1
        product_frame = ttk.Frame(main_container)
        product_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        product_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(product_frame, text="Product:").grid(row=0, column=0, padx=5)
        self.a_product_var = tk.StringVar()
        self.a_product_combo = ttk.Combobox(
            product_frame,
            textvariable=self.a_product_var,
            state='readonly',
            width=40
        )
        self.a_product_combo.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Quantity选择区域 - row 2
        quantity_frame = ttk.Frame(main_container)
        quantity_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Label(quantity_frame, text="Quantity:").pack(side=tk.LEFT, padx=5)
        self.a_quantity_spinbox = ttk.Spinbox(
            quantity_frame,
            from_=1,
            to=100,
            width=5,
            wrap=True,
            state='readonly'
        )
        self.a_quantity_spinbox.pack(side=tk.LEFT, padx=5)
        # 设置默认值为 1
        self.a_quantity_spinbox.set('1')
        
        # 按钮区域 - row 3
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="Add to Cart",
            command=self._add_to_cart_a
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Clear Cart",
            command=self._clear_cart
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Check Out Order",
            command=self._check_out_order
        ).pack(side=tk.LEFT, padx=5)
        
        # 填充剩余空间 - row 4
        spacer = ttk.Frame(main_container)
        spacer.grid(row=4, column=0, sticky='nsew', pady=5)
        main_container.grid_rowconfigure(4, weight=1)
        
        # 更新商品列表
        self._update_a_products()


    def _setup_b_products(self):
        """设置B类商品(Premade Boxes)界面"""
        # 主容器使用grid布局
        main_container = ttk.Frame(self.b_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        main_container.grid_columnconfigure(0, weight=1)
        
        # B类商品选择区域 - row 0
        size_frame = ttk.Frame(main_container)
        size_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        for i, size in enumerate(['small', 'medium', 'large']):
            price = getattr(self, f"{size}box_default_dict")['price']
            ttk.Radiobutton(
                size_frame,
                text=f"{size.capitalize()} (${float(price):.2f})",
                value=size,
                variable=self.b_size_var,
                command=self._update_b_contents
            ).grid(row=0, column=i, padx=5)
        
        # Contents选择区域 - row 1
        self.contents_label_frame = ttk.LabelFrame(main_container, text="Box Contents")
        self.contents_label_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # 创建内容frame
        self.contents_frame = ttk.Frame(self.contents_label_frame)
        self.contents_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.contents_frame.grid_columnconfigure(1, weight=1)
        
        # 创建固定的items标签和combobox
        self.item_widgets = []
        for i in range(5):
            label = ttk.Label(self.contents_frame, text=f"Item {i+1}:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky='w')
            
            combo = ttk.Combobox(self.contents_frame, state='readonly', width=40)
            combo['values'] = self.all_veggies_list
            combo.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            
            self.item_widgets.append((label, combo))
            
            if i >= 3:
                label.grid_remove()
                combo.grid_remove()
        
        # Quantity选择区域 - row 2
        quantity_frame = ttk.Frame(main_container)
        quantity_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Label(quantity_frame, text="Quantity:").pack(side=tk.LEFT, padx=5)
        self.b_quantity_spinbox = ttk.Spinbox(
            quantity_frame,
            from_=1,
            to=100,
            width=5,
            wrap=True,
            state='readonly'
        )
        self.b_quantity_spinbox.pack(side=tk.LEFT, padx=5)
        # 设置默认值为 1
        self.b_quantity_spinbox.set('1')
        
        
        # 按钮区域 - row 3
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="Add to Cart",
            command=self._add_to_cart_b
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Clear Cart",
            command=self._clear_cart
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Check Out Order",
            command=self._check_out_order
        ).pack(side=tk.LEFT, padx=5)
        
        # 填充剩余空间 - row 4
        spacer = ttk.Frame(main_container)
        spacer.grid(row=4, column=0, sticky='nsew', pady=5)
        main_container.grid_rowconfigure(4, weight=1)
        
        # 更新contents显示
        self._update_b_contents()

    def _setup_cart(self):
        """设置购物车界面"""
        # 创建购物车LabelFrame
        cart_frame = ttk.LabelFrame(self.main_frame, text="Cart Details")
        cart_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # 创建主容器，使用grid布局
        main_container = ttk.Frame(cart_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # 创建Treeview和Scrollbar的容器
        tree_frame = ttk.Frame(main_container)
        tree_frame.grid(row=0, column=0, sticky='nsew')
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # 创建Scrollbar (垂直和水平)
        v_scrollbar = ttk.Scrollbar(tree_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 购物车显示区域
        self.cart_tree = ttk.Treeview(
            tree_frame,
            columns=('Product', 'Quantity', 'Price', 'Subtotal', 'Contents'),
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.cart_tree.yview)
        h_scrollbar.config(command=self.cart_tree.xview)
        
        self.cart_tree.heading('Product', text='Product')
        self.cart_tree.heading('Quantity', text='Quantity')
        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.heading('Subtotal', text='Subtotal')
        self.cart_tree.heading('Contents', text='Box Contents')
        
        self.cart_tree.column('Product', width=150, minwidth=150)
        self.cart_tree.column('Quantity', width=60, minwidth=60)
        self.cart_tree.column('Price', width=100, minwidth=100)
        self.cart_tree.column('Subtotal', width=100, minwidth=100)
        self.cart_tree.column('Contents', width=400, minwidth=800)
        
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _update_a_products(self):
        """更新A类商品下拉框的内容"""
        current_type = self.a_type_var.get()
        
        # 类型名称映射
        type_mapping = {
            'weight/kg': 'weight',
            'unit': 'unit',
            'pack': 'pack'
        }
        
        # 获取对应的选项列表
        list_name = f'veggies_{type_mapping[current_type]}_list'
        options = getattr(self, list_name)
        
        if options:
            self.a_product_combo['values'] = options
            self.a_product_combo.set(options[0])
        else:
            self.a_product_combo['values'] = []
            self.a_product_combo.set('')

    def _update_b_contents(self):
        """更新B类商品的contents显示"""
        current_size = self.b_size_var.get()
        box_dict = getattr(self, f"{current_size}box_default_dict")
        num_items = getattr(self, f"{current_size}_size")
        
        # 遍历所有items
        for i, (label, combo) in enumerate(self.item_widgets):
            if i < num_items:
                # 显示并设置默认值
                label.grid()
                combo.grid()
                
                # 设置默认值（从box_dict中获取）
                default_content = box_dict['contents'][i]
                for option in self.all_veggies_list:
                    if default_content.split(' x ')[0] in option:
                        combo.set(option)
                        break
            else:
                # 隐藏
                label.grid_remove()
                combo.grid_remove()

    def _add_to_cart_a(self):
        """添加A类商品(Veggies)到购物车"""
        try:
            product = self.a_product_var.get()
            if not product:
                messagebox.showwarning("Warning", "Please select a product")
                return
                
            quantity = int(self.a_quantity_spinbox.get())
            name, price = product.split(' - $')
            price = Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            subtotal = (price * Decimal(quantity)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            self.cart_tree.insert('', 'end', values=(
                name,
                quantity,
                f"${float(price):.2f}",
                f"${float(subtotal):.2f}",
                ""  # 普通商品没有contents
            ))
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding to cart: {str(e)}")

    def _add_to_cart_b(self):
        """添加B类商品(Premade Boxes)到购物车"""
        try:
            size = self.b_size_var.get()
            quantity = int(self.b_quantity_spinbox.get())
            box_dict = getattr(self, f"{size}box_default_dict")
            price = box_dict['price']
            subtotal = (price * Decimal(quantity)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # 获取当前选择的contents
            contents = []
            num_items = getattr(self, f"{size}_size")
            for i, (_, combo) in enumerate(self.item_widgets[:num_items]):
                item_name = combo.get().split(' - $')[0]
                contents.append(f"{item_name} x 1")
            
            # 格式化contents字符串
            contents_str = ", ".join(contents)
            
            self.cart_tree.insert('', 'end', values=(
                f"{size.capitalize()} Box",
                quantity,
                f"${float(price):.2f}",
                f"${float(subtotal):.2f}",
                contents_str
            ))
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding to cart: {str(e)}")

    def _check_out_order(self):
        """提交订单，保存购物车数据"""
        try:
            # 检查购物车是否为空
            if not self.cart_tree.get_children():
                messagebox.showwarning("Warning", "Cart is empty")
                return
            
            # 保存购物车数据
            self.cart_dict = {}
            # 购物车总价
            total = Decimal('0.00')
            
            # 遍历购物车items
            for item in self.cart_tree.get_children():
                values = self.cart_tree.item(item)['values']
                
                # 解析值[Product, Quantity, Price, Subtotal, Contents]
                name = values[0]
                quantity = int(values[1])
                price = Decimal(values[2].replace('$', ''))
                subtotal = Decimal(values[3].replace('$', ''))
                contents = values[4] if values[4] else ""
                
                # 判断商品类型
                if 'Box' in name:
                    item_type = 'box'
                else:
                    # 通过商品名称判断类型
                    if 'weight/kg' in name:
                        item_type = 'weight'
                    elif 'unit' in name:
                        item_type = 'unit'
                    elif 'pack' in name:
                        item_type = 'pack'
                    else:
                        # 如果无法判断类型，记录到日志
                        print(f"Warning: Unable to determine type for item: {name}")
                        item_type = 'unknown'
                
                # 保存到字典
                self.cart_dict[str(item)] = {
                    'type': item_type,          # 商品类型：'box', 'weight', 'unit', 'pack'
                    'name': name,               # 原始完整名称
                    'quantity': quantity,       # 数量
                    'price': price,            # 单价
                    'subtotal': subtotal,      # 小计
                    'contents': contents       # 盒子内容（如果是box类型）
                }
                
                # 累计总价
                total += subtotal
                
            # 显示支付选项对话框
            response = messagebox.askyesnocancel(
                "Payment Options",
                f"Total Amount: ${float(total):.2f}\n\n"
                "Would you like to pay now?\n\n"
                " - Pay Now : Click 'Yes'\n\n"
                " - Pay Later (Charge to Account) : Click 'No'\n\n"
                " - Cancel : Click 'Cancel'"
            )
            
            if response is None:  # Cancel was clicked
                return
                
            if response:  # Yes was clicked - Pay Now
                self._clear_cart()
                # 调用父组件的回调函数来切换到支付界面
                if hasattr(self.get_main_frame().master, 'make_payment_callback'):
                    self.get_main_frame().master.make_payment_callback()
                messagebox.showinfo("Payment", f"Please proceed with the payment of ${float(total):.2f}")
            else:  # No was clicked - Pay Later
                self._clear_cart()
                messagebox.showinfo(
                    "Charge to Account", 
                    f"The amount ${float(total):.2f} has been charged to your account."
                )
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error checking out order: {str(e)}")
            # 打印详细错误信息便于调试
            import traceback
            print(f"Error details:\n{traceback.format_exc()}")
    def _get_unit_by_type(self, item_type):
        """根据商品类型返回对应的单位"""
        unit_mapping = {
            'box': 'box',
            'weight': 'kg',
            'unit': 'piece',
            'pack': 'pack',
            'unknown': 'item'
        }
        return unit_mapping.get(item_type, 'item')
    def _clear_cart(self):
        """清空购物车"""
        try:
            for item in self.cart_tree.get_children():
                self.cart_tree.delete(item)
        except Exception as e:
            messagebox.showerror("Error", f"Error clearing cart: {str(e)}")

    def get_main_frame(self):
        """返回主Frame以便集成到其他界面"""
        return self.main_frame


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("FHV Company")  # 设置窗口标题
#     root.geometry("800x600")  # 设置窗口大小
#     product_app = Product()  # 创建 Product 实例
#     product_app.main_frame.pack(fill=tk.BOTH, expand=True)  # 显示主框架
#     root.mainloop()  # 进入主循环