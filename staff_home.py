import tkinter as tk
from tkinter import ttk, messagebox

class StaffHome:
    def __init__(self, root, staff):
        self.root = root
        self.root.resizable(False, False)  # 禁止水平和垂直方向的缩放
        self.staff = staff
        self.root.title("FHV Company - Staff Home")

        # 初始化content frames字典，用于缓存不同功能区的frame
        self.content_frames = {}
        
        # 初始化当前显示的frame
        self.current_frame = None

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
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        
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
        
        # 创建按钮容器框架
        self.buttons_frame = ttk.Frame(self.function_frame)
        self.buttons_frame.pack(fill=tk.X)

        # 功能按钮配置
        self.function_buttons = {
            "All Products": self.view_all_products,
            "Current Orders": self.view_current_orders,
            "Previous Orders": self.view_previous_orders,
            "All Customers": self.view_all_customers,
            "Sales Report": self.view_sales_report,
            "Popular Items": self.view_popular_items
        }

        for text, command in self.function_buttons.items():
            button = ttk.Button(self.buttons_frame, text=text, command=command)
            button.pack(fill=tk.X, pady=2, padx=5)

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

        # 初始显示欢迎消息
        self.update_display_area("Welcome", f"Welcome, {self.staff.first_name}!")

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

    def show_frame(self, frame_id, title, create_func=None):
        """通用frame显示方法"""
        try:
            # 隐藏当前frame
            if self.current_frame:
                self.current_frame.pack_forget()
            
            # 更新显示区域标题
            self.update_display_area(title)
            
            # 如果frame不存在且提供了创建函数，则创建
            if frame_id not in self.content_frames and create_func:
                frame = create_func()
                if frame:  # 确保frame创建成功
                    self.content_frames[frame_id] = frame
            
            # 显示对应的frame
            if frame_id in self.content_frames:
                self.current_frame = self.content_frames[frame_id]
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

    # 产品和订单管理功能
    def view_all_products(self):
        self.show_frame('all_products', "All Products", self.create_all_products_frame)

    def view_current_orders(self):
        self.show_frame('current_orders', "Current Orders", self.create_current_orders_frame)

    def view_previous_orders(self):
        self.show_frame('previous_orders', "Previous Orders", self.create_previous_orders_frame)

    def view_all_customers(self):
        self.show_frame('all_customers', "All Customers", self.create_all_customers_frame)

    def view_sales_report(self):
        self.show_frame('sales_report', "Sales Report", self.create_sales_report_frame)

    def view_popular_items(self):
        self.show_frame('popular_items', "Popular Items", self.create_popular_items_frame)

    def create_all_products_frame(self):
        """创建所有产品的frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying all products in the system...").pack(pady=10)
        return frame

    def create_current_orders_frame(self):
        """创建当前订单的frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying all current orders...").pack(pady=10)
        return frame

    def create_previous_orders_frame(self):
        """创建历史订单的frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying all previous orders...").pack(pady=10)
        return frame

    def create_all_customers_frame(self):
        """创建所有客户的frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying list of all customers...").pack(pady=10)
        return frame

    def create_sales_report_frame(self):
        """创建销售报告的frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying sales report...").pack(pady=10)
        return frame

    def create_popular_items_frame(self):
        """创建热门商品的frame"""
        frame = ttk.Frame(self.display_frame)
        ttk.Label(frame, text="Displaying most popular items...").pack(pady=10)
        return frame

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