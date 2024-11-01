import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date

class AutoTreeview(ttk.Treeview):
    def __init__(self, parent, headers, data, mode="readonly", *args, **kwargs):
        """Initialize Treeview with automatic configuration"""
        super().__init__(parent, *args, **kwargs)
        
        self.mode = mode
        self["columns"] = headers
        self.heading("#0", text="", anchor="w")
        self.column("#0", width=0, stretch=tk.NO)
        
        # Configure columns
        for header in headers:
            self.heading(header, text=header, anchor="w")
            self.column(header, anchor="w", stretch=True, width=100)
        
        # Insert data
        self.update_data(data)
        
        # Configure scrollbars
        self.scroll_y = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scroll_x = ttk.Scrollbar(parent, orient="horizontal", command=self.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.config(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.pack(fill=tk.BOTH, expand=True)
        
        # Only bind events if mode is editable
        if self.mode == "editable":
            self.bind("<Double-1>", self._on_double_click)
            self.bind("<Button-3>", self._show_context_menu)
    
    def update_data(self, data):
        """Update treeview with new data"""
        # Clear existing items
        for item in self.get_children():
            self.delete(item)
        
        # Insert new data
        for row in data:
            row_values = [str(value) if value is not None else "N/A" for value in row]
            self.insert("", "end", values=row_values)
    
    def _on_double_click(self, event):
        item = self.identify_row(event.y)
        if item:
            self._process_item(item)
    
    def _show_context_menu(self, event):
        item = self.identify_row(event.y)
        if item:
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Process Order", command=lambda: self._process_item(item))
            menu.post(event.x_root, event.y_root)
    
    def _process_item(self, item_id):
        values = self.item(item_id)["values"]
        if messagebox.askyesno("Process Order", 
                             f"Process this order?\n\n"
                             f"Order ID: {values[0]}\n"
                             f"Customer: {values[1]}\n"
                             f"Date: {values[2]}\n"
                             f"Status: {values[3]}\n"
                             f"Total: {values[4]}"):
            self.delete(item_id)
            messagebox.showinfo("Success", "Order processed successfully!")

class DateSelector(ttk.Frame):
    def __init__(self, parent, label_text):
        super().__init__(parent)
        
        # Get current date
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.current_day = today.day
        
        # Create date selection frame
        date_frame = ttk.Frame(self)
        date_frame.pack(side=tk.LEFT, padx=5)
        
        # Add label
        ttk.Label(date_frame, text=label_text).pack(side=tk.LEFT, padx=5)
        
        # Year selector
        self.year_var = tk.StringVar(value=str(self.current_year))
        self.year_cb = ttk.Combobox(date_frame, textvariable=self.year_var, width=6)
        self.year_cb['values'] = list(range(2020, self.current_year + 1))
        self.year_cb.pack(side=tk.LEFT, padx=2)
        
        # Month selector
        self.month_var = tk.StringVar(value=str(self.current_month))
        self.month_cb = ttk.Combobox(date_frame, textvariable=self.month_var, width=4)
        self.month_cb['values'] = list(range(1, 13))
        self.month_cb.pack(side=tk.LEFT, padx=2)
        
        # Day selector
        self.day_var = tk.StringVar(value=str(self.current_day))
        self.day_cb = ttk.Combobox(date_frame, textvariable=self.day_var, width=4)
        self.day_cb['values'] = list(range(1, 32))
        self.day_cb.pack(side=tk.LEFT, padx=2)
        
        # Bind events
        self.month_cb.bind('<<ComboboxSelected>>', self._update_days)
        self.year_cb.bind('<<ComboboxSelected>>', self._update_days)
    
    def _update_days(self, event=None):
        """Update days based on selected month and year"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            # Get the last day of the selected month
            if month in [4, 6, 9, 11]:
                last_day = 30
            elif month == 2:
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    last_day = 29
                else:
                    last_day = 28
            else:
                last_day = 31
            
            # Update days combobox
            self.day_cb['values'] = list(range(1, last_day + 1))
            
            # Adjust day if current selection is invalid
            current_day = int(self.day_var.get())
            if current_day > last_day:
                self.day_var.set(str(last_day))
        
        except ValueError:
            pass
    
    def get_date(self):
        """Get selected date as date object"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            day = int(self.day_var.get())
            return date(year, month, day)
        except ValueError:
            return None

class SalesReportFrame(ttk.Frame):
    def __init__(self, parent, on_date_submit):
        super().__init__(parent)
        self.on_date_submit = on_date_submit
        self.create_widgets()
        
    def create_widgets(self):
        # Date selection frame
        date_frame = ttk.LabelFrame(self, text="Date Range Selection", padding="10")
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Start date selector
        self.start_date = DateSelector(date_frame, "Start Date:")
        self.start_date.pack(side=tk.LEFT)
        
        # End date selector
        self.end_date = DateSelector(date_frame, "End Date:")
        self.end_date.pack(side=tk.LEFT)
        
        # Submit button
        submit_frame = ttk.Frame(date_frame)
        submit_frame.pack(side=tk.LEFT, padx=20)
        ttk.Button(submit_frame, text="Generate Report",
                  command=self._on_submit).pack(side=tk.LEFT)
    
    def _on_submit(self):
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        
        if not start_date or not end_date:
            messagebox.showerror("Error", "Please select valid dates!")
            return
        
        # Validate dates
        if start_date > end_date:
            messagebox.showerror("Error", "Start date cannot be after end date!")
            return
        
        if end_date > date.today():
            messagebox.showerror("Error", "End date cannot be in the future!")
            return
        
        self.on_date_submit(start_date, end_date)

class StaffHome:
    def __init__(self, root, staff, controller):
        """Initialize Staff Home window"""
        self.controller = controller
        self.root = root
        self.root.resizable(False, False)
        self.staff = staff
        self.root.title("FHV Company - Staff Home")
        self.current_frame = None
        self.text_widget = None
        self.current_treeview = None
        self.setup_window()
        self.create_widgets()
        self.login_window = self.root.master
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_window(self):
        """Set up window properties and layout main frames"""
        window_width = 1200
        window_height = 700
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    def create_widgets(self):
        """Create and arrange all widgets in the window"""
        # Staff Profile area
        self.profile_frame = ttk.LabelFrame(self.left_frame, text="Staff Details", padding="10")
        self.profile_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.profile_frame, text=str(self.staff)).pack(anchor=tk.W, pady=2)

        # Function Area section
        self.function_frame = ttk.LabelFrame(self.left_frame, text="Function Area", padding="10")
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        
        self.buttons_frame = ttk.Frame(self.function_frame)
        self.buttons_frame.pack(fill=tk.X)

        # Function buttons configuration
        self.function_buttons = {
            "All Products": lambda: self.show_text_content("All Products", self.controller.staff_all_products()),
            "Current Orders": lambda: self.show_treeview_content("Current Orders", self.get_current_orders_data(), True),
            "Previous Orders": lambda: self.show_treeview_content("Previous Orders", self.get_previous_orders_data(), False),
            "All Customers": lambda: self.show_text_content("All Customers", "Customer list will be displayed here"),
            "Sales Report": self.show_sales_report,
            "Popular Items": lambda: self.show_text_content("Popular Items", "Popular items will be displayed here")
        }

        for text, command in self.function_buttons.items():
            button = ttk.Button(self.buttons_frame, text=text, command=command)
            button.pack(fill=tk.X, pady=2, padx=5)

        # Bottom frame with logout button
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

        # Display Area
        self.display_frame = ttk.LabelFrame(self.right_frame, text="Display Area", padding="10")
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        # Show welcome message
        self.show_text_content("Welcome", f"Welcome, {self.staff.first_name}!")

    def get_current_orders_data(self):
        """Get current orders data"""
        headers = ["Order ID", "Customer", "Date", "Status", "Total"]
        # Replace this with actual data from controller
        data = [
            ("ORD1001", "John Doe", "2024-11-02", "Pending", "$150.00"),
            ("ORD1002", "Jane Smith", "2024-11-02", "Processing", "$245.50"),
            ("ORD1003", "Mike Johnson", "2024-11-02", "Pending", "$89.99")
        ]
        return headers, data

    def get_previous_orders_data(self):
        """Get previous orders data"""
        headers = ["Order ID", "Customer", "Date", "Status", "Total"]
        # Replace this with actual data from controller
        data = [
            ("ORD1000", "Alice Brown", "2024-11-01", "Completed", "$120.00"),
            ("ORD999", "Bob Wilson", "2024-11-01", "Completed", "$175.25"),
            ("ORD998", "Carol White", "2024-11-01", "Cancelled", "$0.00")
        ]
        return headers, data

    def get_sales_report_data(self, start_date=None, end_date=None):
        """Get sales report data for the specified date range"""
        headers = ["Date", "Orders", "Total Sales", "Average Order Value", "Items Sold"]
        # Replace with actual data from controller based on date range
        if start_date and end_date:
            # Example data for specific date range
            data = [
                (start_date.strftime("%Y-%m-%d"), "15", "$2,250.00", "$150.00", "45"),
                (end_date.strftime("%Y-%m-%d"), "12", "$1,800.00", "$150.00", "36")
            ]
        else:
            # Default data
            data = [
                ("2024-11-01", "10", "$1,500.00", "$150.00", "30"),
                ("2024-11-02", "8", "$1,200.00", "$150.00", "24")
            ]
        return headers, data

    def show_text_content(self, title, content):
        """Display content in text widget"""
        try:
            for widget in self.display_frame.winfo_children():
                widget.destroy()
            
            ttk.Label(
                self.display_frame,
                text=title,
                font=('Helvetica', 14, 'bold')
            ).pack(pady=(0, 10))
            
            # Create text widget with scrollbars
            text_container = ttk.Frame(self.display_frame)
            text_container.pack(fill=tk.BOTH, expand=True)
            
            v_scrollbar = ttk.Scrollbar(text_container)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            h_scrollbar = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            
            text_widget = tk.Text(
                text_container,
                wrap=tk.NONE,
                width=50,
                height=20,
                yscrollcommand=v_scrollbar.set,
                xscrollcommand=h_scrollbar.set,
                font=('Helvetica', 10)
            )
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            v_scrollbar.config(command=text_widget.yview)
            h_scrollbar.config(command=text_widget.xview)
            
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying content: {str(e)}")

    def show_treeview_content(self, title, data, editable=False):
        """Display content in treeview"""
        try:
            for widget in self.display_frame.winfo_children():
                widget.destroy()
            
            # Title container
            title_frame = ttk.Frame(self.display_frame)
            title_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Title
            ttk.Label(
                title_frame,
                text=title,
                font=('Helvetica', 14, 'bold')
            ).pack(side=tk.LEFT)
            
            # Add instruction for editable treeview
            if editable:
                ttk.Label(
                    title_frame,
                    text="(Double-click or right-click to process order)",
                    font=('Helvetica', 10, 'italic'),
                    foreground='blue'
                ).pack(side=tk.LEFT, padx=(10, 0))
            
            headers, rows = data
            mode = "editable" if editable else "readonly"
            self.current_treeview = AutoTreeview(self.display_frame, headers, rows, mode=mode)

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying content: {str(e)}")

    def show_sales_report(self):
        """Display sales report with date selection"""
        try:
            # Clear existing content
            for widget in self.display_frame.winfo_children():
                widget.destroy()
            
            # Title
            ttk.Label(
                self.display_frame,
                text="Sales Report",
                font=('Helvetica', 14, 'bold')
            ).pack(pady=(0, 10))
            
            # Create and add the date selection frame
            date_selection = SalesReportFrame(self.display_frame, self.update_sales_report)
            date_selection.pack(fill=tk.X)
            
            # Add separator between date selection and report
            ttk.Separator(self.display_frame, orient='horizontal').pack(fill=tk.X, pady=10)
            
            # Create frame for treeview
            self.report_frame = ttk.Frame(self.display_frame)
            self.report_frame.pack(fill=tk.BOTH, expand=True)
            
            # Show initial report
            headers, data = self.get_sales_report_data()
            self.current_treeview = AutoTreeview(self.report_frame, headers, data, mode="readonly")

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying sales report: {str(e)}")

    def update_sales_report(self, start_date, end_date):
        """Update sales report with new date range"""
        try:
            # Get new data based on date range
            headers, data = self.get_sales_report_data(start_date, end_date)
            
            # Update treeview with new data
            if self.current_treeview:
                self.current_treeview.update_data(data)
            else:
                # Create new treeview if it doesn't exist
                self.current_treeview = AutoTreeview(self.report_frame, headers, data, mode="readonly")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating sales report: {str(e)}")

    def on_logout(self):
        """Handle logout action"""
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            self.root.destroy()
            self.login_window.deiconify()

    def on_closing(self):
        """Handle window close event"""
        if messagebox.askyesno("Quit Confirmation", "Are you sure you want to quit the application?"):
            self.root.destroy()
            self.login_window.destroy()

# # Example usage
# def main():
#     root = tk.Tk()
    
#     class DummyStaff:
#         def __init__(self):
#             self.first_name = "John"
#         def __str__(self):
#             return "John Doe - Staff ID: 1001"
    
#     class DummyController:
#         def staff_all_products(self):
#             return "Sample products list"
    
#     staff_home = StaffHome(root, DummyStaff(), DummyController())
#     root.mainloop()

# if __name__ == "__main__":
#     main()