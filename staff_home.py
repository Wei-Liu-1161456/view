# staff_home.py

import tkinter as tk
from tkinter import ttk, messagebox

class StaffHome:
    def __init__(self, root, staff):
        self.root = root
        # 禁止调整窗口大小
        self.root.resizable(False, False)  # 禁止水平和垂直方向的缩放
        self.staff = staff
        self.root.title("FHV Company - Staff Home")
        self.setup_window()
        self.create_widgets()

        # 保存登录窗口的引用
        self.login_window = self.root.master

        # 设置窗口关闭按钮的行为
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_window(self):
        """设置窗口属性"""
        window_width = 1200
        window_height = 700
        
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
        # 创建Staff Profile区域
        self.profile_frame = ttk.LabelFrame(self.left_frame, text="Staff Details", padding="10")
        self.profile_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 添加员工信息
        ttk.Label(self.profile_frame, text=str(self.staff)).pack(anchor=tk.W, pady=2)

        # 创建Function Area区域
        self.function_frame = ttk.LabelFrame(self.left_frame, text="Function Area", padding="10")
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建按钮容器框架 - 移除expand=True
        self.buttons_frame = ttk.Frame(self.function_frame)
        self.buttons_frame.pack(fill=tk.X)
        
        # 添加功能按钮组
        # 产品和订单管理组
        group_frame1 = self.create_button_group("Products & Orders", [
            ("All Products", self.view_all_products),
            ("Current Orders", self.view_current_orders),
            ("Previous Orders", self.view_previous_orders)
        ])
        group_frame1.pack(fill=tk.X, pady=(0, 5))
        
        # 客户管理
        group_frame2 = self.create_button_group("Customer Management", [
            ("All Customers", self.view_all_customers)
        ])
        group_frame2.pack(fill=tk.X, pady=5)
        
        # Sales Report
        group_frame3 = self.create_button_group("Sales Reports", [
            ("Sales Report", self.view_sales_report),
            ("Popular Items", self.view_popular_items)
        ])

        group_frame3.pack(fill=tk.X, pady=5)

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

        # 创建Display Area区域
        self.display_frame = ttk.LabelFrame(self.right_frame, text="Display Area", padding="10")
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加欢迎消息
        ttk.Label(
            self.display_frame, 
            text=f"Welcome, {self.staff.first_name}!",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=20)
        
        ttk.Label(
            self.display_frame,
            text="Please select a function from the left menu to begin.",
            font=('Helvetica', 12)
        ).pack()

    def create_button_group(self, group_name, buttons):
        """创建按钮组"""
        group_frame = ttk.LabelFrame(self.buttons_frame, text=group_name, padding="5")
        
        for text, command in buttons:
            ttk.Button(group_frame, text=text, command=command).pack(
                fill=tk.X, pady=2, padx=5
            )
            
        return group_frame

    def update_display_area(self, title, content=""):
        """更新显示区域的内容"""
        # 清除显示区域的现有内容
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        # 添加新的标题
        ttk.Label(
            self.display_frame,
            text=title,
            font=('Helvetica', 14, 'bold')
        ).pack(pady=20)
        
        if content:
            ttk.Label(
                self.display_frame,
                text=content,
                font=('Helvetica', 12)
            ).pack(pady=10)

    # 产品和订单管理功能
    def view_all_products(self):
        self.update_display_area("All Products", "Displaying all products in the system...")
        # 实现显示所有产品的功能

    def view_current_orders(self):
        self.update_display_area("Current Orders", "Displaying all current orders...")
        # 实现显示当前订单的功能

    def view_previous_orders(self):
        self.update_display_area("Previous Orders", "Displaying all previous orders...")
        # 实现显示历史订单的功能

    # 客户管理功能
    def view_all_customers(self):
        self.update_display_area("All Customers", "Displaying list of all customers...")
        # 实现显示所有客户的功能
    

    # 销售报告功能
    def view_sales_report(self):  
        self.update_display_area("Sales Report", "Displaying sales report...")
        # 实现显示销售报告的功能

    def view_popular_items(self):
        self.update_display_area("Popular Items", "Displaying most popular items...")
        # 实现显示热门商品的功能

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