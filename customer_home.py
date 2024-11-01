# customer_home.py

import tkinter as tk
from tkinter import ttk, messagebox
from product import Product
# from controller import Company

class CustomerHome:
    def __init__(self, root, customer, controller):
        # 拿到controller中的数据
        self.controller = controller

        self.root = root
        self.root.resizable(False, False)
        self.customer = customer
        self.root.title("FHV Company - Customer Home")
        
        # 初始化content frames字典，用于缓存不同功能区的frame
        self.content_frames = {}
        
        # 初始化当前显示的frame
        self.current_frame = None
        
        # 初始化loading提示
        self.loading_label = None
        
        self.setup_window()
        self.create_widgets()

        self.login_window = self.root.master
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_window(self):
        """设置窗口属性"""
        window_width = 1200
        window_height = 800
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        top_y = 0
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{top_y}')
        
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    def create_widgets(self):
        # Customer Profile区域
        self.profile_frame = ttk.LabelFrame(self.left_frame, text="Customer Profile", padding="10")
        self.profile_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.profile_frame, text=str(self.customer)).pack(anchor=tk.W, pady=2)

        # Function Area区域
        self.function_frame = ttk.LabelFrame(self.left_frame, text="Function Area", padding="10")
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        
        self.buttons_frame = ttk.Frame(self.function_frame)
        self.buttons_frame.pack(fill=tk.X)

        # 功能按钮配置
        self.function_buttons = {
            "Place New Order": self.place_new_order,
            "Make Payment": self.make_payment,
            "Current Orders": self.view_current_orders,
            "Previous Orders": self.view_previous_orders
        }

        for text, command in self.function_buttons.items():
            button_frame = ttk.Frame(self.buttons_frame)
            button_frame.pack(fill=tk.X, pady=3)
            ttk.Button(button_frame, text=text, command=command).pack(
                fill=tk.X, padx=5
            )

        # 底部框架
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

        # Display Area区域
        self.display_frame = ttk.LabelFrame(self.right_frame, text="Display Area", padding="10")
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 初始显示订单界面
        self.place_new_order()

    def show_loading(self):
        """显示加载提示"""
        # 如果已经存在loading label，先移除
        self.hide_loading()
        
        # 创建loading frame，确保居中显示
        loading_frame = ttk.Frame(self.display_frame)
        loading_frame.pack(expand=True)
        
        # 创建loading label
        self.loading_label = ttk.Label(
            loading_frame,
            text="Loading...",
            font=('Helvetica', 12)
        )
        self.loading_label.pack(expand=True)
        
        # 强制更新界面
        self.root.update()

    def hide_loading(self):
        """隐藏加载提示"""
        if self.loading_label:
            self.loading_label.master.destroy()  # 销毁整个loading frame
            self.loading_label = None
            # 强制更新界面
            self.root.update()

    def show_frame(self, frame_id, title, create_func=None):
        """通用frame显示方法"""
        try:
            # 显示加载提示
            self.show_loading()
            
            # 隐藏当前frame
            if self.current_frame:
                self.current_frame.pack_forget()
            
            # 更新显示区域标题
            self.display_frame.configure(text=title)
            
            # 如果frame不存在且提供了创建函数，则创建
            if frame_id not in self.content_frames and create_func:
                frame = create_func()
                if frame:  # 确保frame创建成功
                    self.content_frames[frame_id] = frame
            
            # 显示对应的frame
            if frame_id in self.content_frames:
                self.current_frame = self.content_frames[frame_id]
                # 隐藏加载提示
                self.hide_loading()
                # 显示内容frame
                self.current_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            else:
                # 如果frame创建失败，显示错误提示
                error_frame = ttk.Frame(self.display_frame)
                ttk.Label(
                    error_frame,
                    text="Failed to load the content. Please try again.",
                    foreground='red'
                ).pack(pady=10)
                error_frame.pack(fill=tk.BOTH, expand=True)
                self.current_frame = error_frame
                
        except Exception as e:
            messagebox.showerror("Error", f"Error showing frame: {str(e)}")
        finally:
            # 确保加载提示被隐藏
            self.hide_loading()

    def create_new_order_frame(self):
        """创建订单frame"""
        try:
            product_frame = ttk.Frame(self.display_frame)
            product_system = Product(product_frame, self.controller, self.customer)
            product_system.get_main_frame().pack(fill=tk.BOTH, expand=True)
            return product_frame
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize order system: {str(e)}")
            return None

    def create_payment_frame(self):
        """创建支付frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Here you can make payments for your orders...").pack(pady=10)
        return frame

    def create_current_orders_frame(self):
        """创建当前订单frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying your current orders...").pack(pady=10)
        return frame

    def create_previous_orders_frame(self):
        """创建历史订单frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying your order history...").pack(pady=10)
        return frame

    def place_new_order(self):
        """显示订单系统"""
        self.show_frame('new_order', "Place New Order", self.create_new_order_frame)
        
    def make_payment(self):
        """显示支付界面"""
        self.show_frame('payment', "Make Payment", self.create_payment_frame)
        
    def view_current_orders(self):
        """显示当前订单"""
        self.show_frame('current_orders', "Current Orders", self.create_current_orders_frame)
        
    def view_previous_orders(self):
        """显示历史订单"""
        self.show_frame('previous_orders', "Previous Orders", self.create_previous_orders_frame)
        
    def on_logout(self):
        """处理退出登录"""
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            try:
                self.root.destroy()
                self.login_window.deiconify()
            except Exception as e:
                messagebox.showerror("Error", f"Error during logout: {str(e)}")

    def on_closing(self):
        """处理窗口关闭事件"""
        if messagebox.askyesno("Quit Confirmation", "Are you sure you want to quit the application?"):
            try:
                self.root.destroy()
                self.login_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error during closing: {str(e)}")