import sys
import os
# 将当前工作目录添加到路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import messagebox, ttk
import pickle
from view.model import Person, Staff, Customer, CorporateCustomer
from customer_home import CustomerHome
from staff_home import StaffHome
# from controller import Company

class Login:
    def __init__(self, controller):
        # 拿到controller中的数据
        self.controller = controller
        self.private_customers = self.controller.private_customers
        self.corporate_customers = self.controller.corporate_customers
        self.staff_members = self.controller.staff_members

        self.root = tk.Tk()
        self.root.title("FHV Company - Login")
        # 禁止调整窗口大小
        self.root.resizable(False, False)  # 禁止水平和垂直方向的缩放
        
        self.private_customers = controller.private_customers
        self.corporate_customers = controller.corporate_customers
        self.staff_members = controller.staff_members

        # Create user interface
        self.create_widgets()

    

    # Get user information
    def get_user_info(self):
        user_info = []
        
        # Adding staff information (assumed to have only one staff)
        # if self.staff_members:
            # user_info.append(f"{self.staff_member.username}, {self.staff_member.password}")
            # Adding staff information
        for staff in self.staff_members.values():  # Changed to iterate through staffs
                user_info.append(f"{staff.username}, {staff.password}")

        # Add private customer information
        for customer in self.private_customers.values():
            user_info.append(f"{customer.username}, {customer.password}")

        # Add corporate customer information
        for customer in self.corporate_customers.values():
            user_info.append(f"{customer.username}, {customer.password}")

        return user_info


    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # 验证登录信息
        user, user_type = self.controller.user_login(username, password)
        
        if user:
            # 隐藏登录窗口
            self.root.withdraw()
            
            # 创建新窗口
            new_window = tk.Toplevel(self.root)  # 将self.root作为parent
            
            # 根据用户类型创建相应的主界面
            if user_type == "staff":
                StaffHome(new_window, user, self.controller)
            else:
                CustomerHome(new_window, user, self.controller)
        else:
            messagebox.showerror("Login Failed", 
                               "Invalid username or password.")
            
    # 关闭窗口时的操作
    def on_closing(self, window):
        """处理窗口关闭事件"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()
            self.root.destroy()

    # Exit application
    def exit_application(self):
        self.root.quit()

    def create_widgets(self):
        # Set window size
        window_width = 400
        window_height = 500

        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate window position to center it
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        # Set window position and size
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Username label and input (same line)
        frame_username = ttk.Frame(main_frame)
        frame_username.pack(pady=5)
        ttk.Label(frame_username, text="Username:").pack(side=tk.LEFT)
        self.entry_username = ttk.Entry(frame_username)
        self.entry_username.insert(0, "staffJD")  # Set default username
        self.entry_username.pack(side=tk.LEFT, padx=5)

        # Password label and input (same line)
        frame_password = ttk.Frame(main_frame)
        frame_password.pack(pady=5)
        ttk.Label(frame_password, text="Password:").pack(side=tk.LEFT)
        self.entry_password = ttk.Entry(frame_password, show="*")
        self.entry_password.insert(0, "12345") # Set default password
        self.entry_password.pack(side=tk.LEFT, padx=5)

        # Login and Exit buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Log In", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.exit_application).pack(side=tk.LEFT)

        # Display available usernames and passwords for testing
        ttk.Label(main_frame, text="Available Usernames and Passwords for Testing:").pack(pady=5)
        hint_text = tk.Text(main_frame, height=10, width=40, wrap=tk.WORD)
        hint_text.pack(pady=5)

        # Insert user info
        user_info = self.get_user_info()
        for info in user_info:
            hint_text.insert(tk.END, f"{info}\n")
        hint_text.config(state='disabled')  # Set to read-only
    def run(self):
        self.root.mainloop()
