import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, ROUND_HALF_UP
import os
from my_widgts import ValidatedSpinbox
from decimal import InvalidOperation
# from controller import Company  


class Product:
    def __init__(self, parent, controller):
        """
        初始化Product类
        parent: 父级窗口部件
        """
        try:
            # 拿到controller中的数据
            self.controller = controller

            # 初始化商品数据
            # 初始化蔬菜列表
            self.all_veggies_list = self.controller.all_veggies_list  # 所有蔬菜列表(供box contents使用)
            self.veggies_weight_list = self.controller.veggies_weight_list  # weight类蔬菜列表
            self.veggies_unit_list = self.controller.veggies_unit_list    # unit类蔬菜列表
            self.veggies_pack_list = self.controller.veggies_pack_list    # pack类蔬菜列表
            # 初始化盒子配置
            self.smallbox_default_dict = self.controller.smallbox_default_dict
            self.mediumbox_default_dict = self.controller.mediumbox_default_dict
            self.largebox_default_dict = self.controller.largebox_default_dict

            # 初始化固定值
            self.small_size = 3
            self.medium_size = 4
            self.large_size = 5
            
            # 创建主Frame
            self.main_frame = ttk.Frame(parent)
            
            # 创建notebook
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
            
            # 创建A类和B类的frame
            self.veggie_frame = ttk.Frame(self.notebook)
            self.box_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.veggie_frame, text='Veggies')
            self.notebook.add(self.box_frame, text='Premade Boxes')
            
            # 初始化变量
            self.veggie_type_var = tk.StringVar(value='weight/kg')
            self.box_size_var = tk.StringVar(value='small')
            
            # 初始化界面
            self._setup_veggie_products()
            self._setup_box_products()
            self._setup_cart()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Error initializing product system: {str(e)}")
            raise
    


    def _setup_veggie_products(self):
        """设置A类商品(Veggies)界面"""
        # 主容器使用grid布局
        main_container = ttk.Frame(self.veggie_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        main_container.grid_columnconfigure(0, weight=1)
        
        # A类商品选择区域 - row 0
        type_frame = ttk.Frame(main_container)
        type_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # A类商品的Radiobuttons
        for i, veggie_type in enumerate(['weight/kg', 'unit', 'pack']):
            ttk.Radiobutton(
                type_frame,
                text=veggie_type,
                value=veggie_type,
                variable=self.veggie_type_var,
                command=self._update_veggie_products
            ).grid(row=0, column=i, padx=5)
        
        # Product选择区域 - row 1
        product_frame = ttk.Frame(main_container)
        product_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        product_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(product_frame, text="Product:").grid(row=0, column=0, padx=5)
        self.veggie_product_var = tk.StringVar()
        self.veggie_product_combo = ttk.Combobox(
            product_frame,
            textvariable=self.veggie_product_var,
            state='readonly',
            width=40
        )
        self.veggie_product_combo.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Quantity选择区域 - row 2
        quantity_frame = ttk.Frame(main_container)
        quantity_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Label(quantity_frame, text="Quantity:").pack(side=tk.LEFT, padx=5)
        
        # 使用自定义的ValidatedSpinbox
        self.veggie_quantity_spinbox = ValidatedSpinbox(quantity_frame)
        self.veggie_quantity_spinbox.model = 'float'
        self.veggie_quantity_spinbox.pack(side=tk.LEFT, padx=5)
        # 设置默认值为 1
        self.veggie_quantity_spinbox.set('1')
        
        # 按钮区域 - row 3
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="Add to Cart",
            command=self._add_veggie_to_cart
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
        self._update_veggie_products()


    def _setup_box_products(self):
        """设置B类商品(Premade Boxes)界面"""
        # 主容器使用grid布局
        main_container = ttk.Frame(self.box_frame)
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
                variable=self.box_size_var,
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
        
        # 使用自定义的ValidatedSpinbox
        self.box_quantity_spinbox = ValidatedSpinbox(quantity_frame)
        self.box_quantity_spinbox.pack(side=tk.LEFT, padx=5)
        # 设置默认值为 1
        self.box_quantity_spinbox.set('1')
        
        
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

        # 设置quantity的model
        self.box_quantity_spinbox.model = 'int'

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

    def _update_veggie_products(self):
        """更新A类商品下拉框的内容"""
        current_type = self.veggie_type_var.get()
        
        # 切换quantiy的model
        if current_type == 'weight/kg':
            self.veggie_quantity_spinbox.model = 'float'
        else:
            self.veggie_quantity_spinbox.model = 'int'

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
            self.veggie_product_combo['values'] = options
            self.veggie_product_combo.set(options[0])
        else:
            self.veggie_product_combo['values'] = []
            self.veggie_product_combo.set('')

    def _update_b_contents(self):
        """更新B类商品的contents显示"""
        current_size = self.box_size_var.get()
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


    def _add_veggie_to_cart(self):
        """Add Veggie (Class A) product to the shopping cart."""
        try:
            product = self.veggie_product_var.get()
            if not product:
                messagebox.showwarning("Warning", "Please select a product")
                return

            # Allow for decimal quantities without enforcing two decimal places
            quantity = Decimal(self.veggie_quantity_spinbox.get())
            
            # Ensure quantity is positive
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be greater than zero")
                return
            
            name, price = product.split(' - $')
            price = Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            subtotal = (price * quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            self.cart_tree.insert('', 'end', values=(
                name,
                quantity,
                f"${float(price):.2f}",
                f"${float(subtotal):.2f}",
                ""  # No contents for standard products
            ))
        except (ValueError, InvalidOperation) as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding to cart: {str(e)}")


    def _add_to_cart_b(self):
        """添加B类商品(Premade Boxes)到购物车"""
        try:
            size = self.box_size_var.get()
            quantity = int(self.box_quantity_spinbox.get())
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
        """Submit the order and save the cart data."""
        try:
            # Check if the cart is empty
            if not self.cart_tree.get_children():
                messagebox.showwarning("Warning", "Cart is empty")
                return
            
            # Initialize cart list and total
            self.cart_dict = []
            total = Decimal('0.00')
            
            # Iterate through cart items
            for item in self.cart_tree.get_children():
                values = self.cart_tree.item(item)['values']
                
                # Parse values [Product, Quantity, Price, Subtotal, Contents]
                name = values[0]
                quantity = Decimal(values[1])  # Allow decimal quantities
                price = Decimal(values[2].replace('$', ''))
                subtotal = Decimal(values[3].replace('$', ''))
                contents = values[4] if values[4] else ""
                
                # Determine the item type
                if 'Box' in name:
                    item_type = 'box'
                else:
                    # Determine the type based on the product name
                    if 'weight/kg' in name:
                        item_type = 'weight'
                    elif 'unit' in name:
                        item_type = 'unit'
                    elif 'pack' in name:
                        item_type = 'pack'
                    else:
                        # Log if the type cannot be determined
                        print(f"Warning: Unable to determine type for item: {name}")
                        item_type = 'unknown'
                
                # Create item dictionary and append to list
                cart_item = {
                    'type': item_type,          # Item type: 'box', 'weight', 'unit', 'pack'
                    'name': name,               # Original full name
                    'quantity': quantity,       # Quantity
                    'price': price,             # Unit price
                    'subtotal': subtotal,       # Subtotal
                    'contents': contents        # Box contents (if it's a box type)
                }
            
                self.cart_dict.append(cart_item)
                
                # Accumulate total price
                total += subtotal
                
            # Show payment options dialog
            response = messagebox.askyesnocancel(
                "Payment Options",
                f"Total Amount: ${float(total):.2f}\n\n"
                "Would you like to pay now?\n\n"
                " - Pay Now : Click 'Yes'\n\n"
                " - Pay Later (Charge to Account) : Click 'No'\n\n"
                " - Cancel : Click 'Cancel'"
            )
            
            # 打印订单信息
            print(self.cart_dict)

            if response is None:  # Cancel was clicked
                return
                
            if response:  # Yes was clicked - Pay Now
                self._clear_cart()
                # Call the parent component's callback to switch to the payment interface
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
            # Print detailed error information for debugging
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