# customer_home.py

import tkinter as tk
from tkinter import ttk, messagebox
from product import Product

class CustomerHome:
    def __init__(self, root, customer):
        self.root = root
        # 禁止调整窗口大小
        self.root.resizable(False, False)
        self.customer = customer
        self.root.title("FHV Company - Customer Home")
        self.setup_window()
        self.create_widgets()

        # 保存登录窗口的引用
        self.login_window = self.root.master

        # 设置窗口关闭按钮的行为
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_window(self):
        """设置窗口属性"""
        window_width = 1000
        window_height = 600
        
        # 获取屏幕尺寸并计算窗口位置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        # 设置窗口位置和大小
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建左右分栏
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    def create_widgets(self):
        # 创建Customer Profile区域
        self.profile_frame = ttk.LabelFrame(self.left_frame, text="Customer Profile", padding="10")
        self.profile_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 添加客户信息
        ttk.Label(self.profile_frame, text=str(self.customer)).pack(anchor=tk.W, pady=2)

        # 创建Function Area区域
        self.function_frame = ttk.LabelFrame(self.left_frame, text="Function Area", padding="10")
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建按钮框架 - 移除expand=True
        self.buttons_frame = ttk.Frame(self.function_frame)
        self.buttons_frame.pack(fill=tk.X)

        # 添加功能按钮，每个按钮之间有固定间距
        buttons = [
            ("Place New Order", self.place_new_order),
            ("Make Payment", self.make_payment),
            ("Current Orders", self.view_current_orders),
            ("Previous Orders", self.view_previous_orders)
        ]

        # 为每个按钮创建独立的frame以保持一致的间距
        for text, command in buttons:
            button_frame = ttk.Frame(self.buttons_frame)
            button_frame.pack(fill=tk.X, pady=3)  # 减小按钮间距
            ttk.Button(button_frame, text=text, command=command).pack(
                fill=tk.X, padx=5
            )

        # 使用Frame包装分隔线和退出按钮，将它们推到底部
        bottom_frame = ttk.Frame(self.function_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Separator(bottom_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        self.logout_button = ttk.Button(
            bottom_frame,
            text="Log Out",
            command=self.on_logout,
            style='Accent.TButton'
        )
        self.logout_button.pack(fill=tk.X)

    

        # 创建Display Area区域并直接显示产品订单界面
        self.display_frame = ttk.LabelFrame(self.right_frame, text="Place New Order", padding="10")  # 初始标题
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 初始化并显示产品订单界面
        try:
            self.product_system = Product()  # 创建Product实例并保存引用
            product_frame = self.product_system.get_main_frame()
            product_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize order system: {str(e)}")

    def update_display_area(self, title, content=""):
        """更新显示区域的内容"""        
        # 更新显示区域标题
        self.display_frame.configure(text=title)
        
        # 清空显示区域
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        # 重新显示界面
        
    

    # 功能按钮的处理函数
    def place_new_order(self):
        """显示订单系统"""
        try:
            # 更新显示区域标题
            self.display_frame.configure(text="Place New Order")
            
            # 清空显示区域
            for widget in self.display_frame.winfo_children():
                widget.destroy()
            
            # 重新显示产品订单界面
            product_app = Product()  # 创建 Product 实例
            product_app.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # 显示主框架
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show order system: {str(e)}")
        

    def make_payment(self):
        self.update_display_area("Make Payment", "Here you can make payments for your orders...")
        # 实现付款功能

    def view_current_orders(self):
        self.update_display_area("Current Orders", "Displaying your current orders...")
        # 实现查看当前订单功能

    def view_previous_orders(self):
        self.update_display_area("Previous Orders", "Displaying your order history...")
        # 实现查看历史订单功能

    def on_logout(self):
        """处理退出登录"""
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            self.root.destroy()  # 关闭当前窗口
            self.login_window.deiconify()  # 显示登录窗口

    def on_closing(self):
        """处理窗口关闭事件"""
        if messagebox.askyesno("Quit Confirmation", "Are you sure you want to quit the application?"):
            self.root.destroy()  # 关闭当前窗口
            self.login_window.destroy()  # 关闭登录窗口