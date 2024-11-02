import tkinter as tk
from tkinter import ttk, messagebox
from product import Product
from payment import Payment
from decimal import Decimal


class AutoTreeview(ttk.Treeview):
    def __init__(self, parent, headers, data, controller=None, mode="readonly", *args, **kwargs):
        """Initialize Treeview with automatic configuration.
        
        Args:
            parent: The parent widget that will contain this Treeview
            headers: List of column headers for the Treeview
            data: Initial data to populate the Treeview
            controller: Optional controller to handle user interactions
            mode: Mode of the Treeview; can be "readonly" or "editable"
            *args, **kwargs: Additional arguments passed to the parent class
        """
        super().__init__(parent, *args, **kwargs)
        
        self.controller = controller
        self.mode = mode
        self["columns"] = headers
        self.heading("#0", text="", anchor="w")
        self.column("#0", width=0, stretch=tk.NO)
        
        for header in headers:
            self.heading(header, text=header, anchor="w")
            if header == "Items":
                self.column(header, anchor="w", stretch=True, width=300, minwidth=200)
            else:
                self.column(header, anchor="w", stretch=True, width=100)
        
        self.tooltip = None
        self.bind('<Motion>', self._on_motion)
        self.bind('<Leave>', self._on_leave)
        
        self.update_data(data)
        
        # Configure scrollbars
        self.scroll_y = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scroll_x = ttk.Scrollbar(parent, orient="horizontal", command=self.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.config(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.pack(fill=tk.BOTH, expand=True)
        
        if self.mode == "editable":
            self.bind("<Double-1>", self._on_double_click)
            self.bind("<Button-3>", self._show_context_menu)

    def _on_motion(self, event):
        """Handle mouse motion events to show tooltips.
        
        Args:
            event: Mouse event containing position information
        """
        cell = self.identify_row(event.y)
        if cell and self.identify_column(event.x) == '#5':  # Items column
            values = self.item(cell)['values']
            if values and len(values) >= 5:
                if not self.tooltip:
                    self.tooltip = tk.Toplevel()
                    self.tooltip.wm_overrideredirect(True)
                    self.tooltip_label = tk.Label(
                        self.tooltip,
                        justify=tk.LEFT,
                        background="#ffffe0",
                        relief='solid',
                        borderwidth=1
                    )
                    self.tooltip_label.pack()

                x, y, _, _ = self.bbox(cell, '#5')
                x_root = event.x_root + 10
                y_root = event.y_root + 10
                self.tooltip_label.config(text=str(values[4]))
                self.tooltip.geometry(f"+{x_root}+{y_root}")
                self.tooltip.deiconify()
        elif self.tooltip:
            self.tooltip.withdraw()

    def _on_leave(self, event):
        """Handle mouse leave events to hide tooltips.
        
        Args:
            event: Mouse event containing position information
        """
        if self.tooltip:
            self.tooltip.withdraw()

    def update_data(self, data):
        """Update the Treeview with new data."""
        for item in self.get_children():
            self.delete(item)
        
        for row in data:
            row_values = []
            for i, value in enumerate(row):
                if value is None:
                    row_values.append("N/A")
                elif i == 4:
                    row_values.append(str(value))
                else:
                    row_values.append(str(value))
            self.insert("", "end", values=row_values)

    # def update_data(self, data):
    #     """Update the Treeview with new data."""
    #     for item in self.get_children():
    #         self.delete(item)
        
    #     for row in data:
    #         row_values = []
    #         for i, value in enumerate(row):
    #             if value is None:
    #                 row_values.append("N/A")
    #             elif i == 4:
    #                 row_values.append(str(value))
    #             else:
    #                 row_values.append(str(value))
    #         self.insert("", "end", values=row_values)


class CustomerHome:
    def __init__(self, root, customer, controller):
        """Initialize CustomerHome interface.
        
        Args:
            root: Root window widget
            customer: Customer instance
            controller: Controller instance for managing data and callbacks
        """
        self.controller = controller
        self.root = root
        self.root.resizable(False, False)
        self.customer = customer
        self.root.title("FHV Company - Customer Home")
        
        self.content_frames = {}
        self.current_frame = None
        self.current_treeview = None
        self.loading_label = None
        
        self.setup_window()
        self.create_widgets()

        self.login_window = self.root.master
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_window(self):
        """Setup window layout and frames"""
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
        """Create and setup all widgets"""
        # Customer Profile Area
        self.profile_frame = ttk.LabelFrame(self.left_frame, text="Customer Profile", padding="10")
        self.profile_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.profile_frame, text=str(self.customer)).pack(anchor=tk.W, pady=2)

        # Function Area
        self.function_frame = ttk.LabelFrame(self.left_frame, text="Function Area", padding="10")
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        
        self.buttons_frame = ttk.Frame(self.function_frame)
        self.buttons_frame.pack(fill=tk.X)

        # Function buttons
        self.function_buttons = {
            "Place New Order": self.place_new_order,
            "Make Payment": self.make_payment,
            "Current Orders": self.view_current_orders,
            "Previous Orders": self.view_previous_orders
        }

        for text, command in self.function_buttons.items():
            button_frame = ttk.Frame(self.buttons_frame)
            button_frame.pack(fill=tk.X, pady=3)
            ttk.Button(button_frame, text=text, command=command).pack(fill=tk.X, padx=5)

        # Bottom frame
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

    def show_frame(self, frame_id, title, create_func=None):
        """Generic method to display frames"""
        try:
            self.show_loading()
            
            # Clear display area
            for widget in self.display_frame.winfo_children():
                widget.pack_forget()
            
            self.display_frame.configure(text=title)
            
            if frame_id not in self.content_frames and create_func:
                frame = create_func()
                if frame:
                    self.content_frames[frame_id] = frame
            
            if frame_id in self.content_frames:
                self.current_frame = self.content_frames[frame_id]
                self.hide_loading()
                self.current_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            else:
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
            self.hide_loading()

    def show_loading(self):
        """Display loading indicator"""
        self.hide_loading()
        loading_frame = ttk.Frame(self.display_frame)
        loading_frame.pack(expand=True)
        self.loading_label = ttk.Label(
            loading_frame,
            text="Loading...",
            font=('Helvetica', 12)
        )
        self.loading_label.pack(expand=True)
        self.root.update()

    def hide_loading(self):
        """Hide loading indicator"""
        if self.loading_label:
            self.loading_label.master.destroy()
            self.loading_label = None
            self.root.update()

    def create_new_order_frame(self):
        """Create order frame"""
        try:
            product_frame = ttk.Frame(self.display_frame)
            product_system = Product(product_frame, self.controller, self.customer)
            product_system.bind_payment_callback(self.show_payment_window)  # Bind payment callback
            product_system.get_main_frame().pack(fill=tk.BOTH, expand=True)
            return product_frame
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize order system: {str(e)}")
            return None

    def show_payment_window(self, order_data):
        """Display payment window as modal dialog"""
        try:
            payment_window = tk.Toplevel(self.root)
            payment_window.title("Payment")
            
            window_width = 500
            window_height = 600
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = int((screen_width/2) - (window_width/2))
            y = int((screen_height/2) - (window_height/2))
            payment_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
            
            payment_window.transient(self.root)
            payment_window.grab_set()
            payment_window.resizable(False, False)
            
            payment_system = Payment(payment_window, self.controller)
            if order_data:
                payment_system.set_order_amounts(
                    order_data['subtotal'],
                    order_data['discount'],
                    order_data['delivery_fee'],
                    order_data['total']
                )
            
            payment_frame = payment_system.get_main_frame()
            payment_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Override payment window's protocol for proper cleanup
            def on_payment_window_close():
                payment_window.grab_release()
                payment_window.destroy()
                
            payment_window.protocol("WM_DELETE_WINDOW", on_payment_window_close)
            self.root.wait_window(payment_window)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error showing payment window: {str(e)}")

    def get_current_orders_data(self):
        """Get current orders data from controller"""
        headers = ["Order ID", "Customer", "Date", "Status", "Items", 
                  "Subtotal", "Delivery Fee", "Total Amount"]
        
        data = []
        for order_number, order in self.controller.customer_current_orders(self.customer).items():
            data.append((
                order_number, order["Customer"], order["Date"], order["Status"], 
                order["Items"], order["Subtotal"], order["Delivery Fee"], order["Total Amount"]
            ))
        return headers, data

    def get_previous_orders_data(self):
        """Get previous orders data from controller"""
        headers = ["Order ID", "Customer", "Date", "Status", "Items", 
                  "Subtotal", "Delivery Fee", "Total Amount"]
        
        data = []
        for order_number, order in self.controller.customer_previous_orders(self.customer).items():
            data.append((
                order_number, order["Customer"], order["Date"], order["Status"], 
                order["Items"], order["Subtotal"], order["Delivery Fee"], order["Total Amount"]
            ))
        return headers, data

    def show_treeview_content(self, title, data):
        """Display content in treeview"""
        try:
            for widget in self.display_frame.winfo_children():
                widget.pack_forget()
            
            title_frame = ttk.Frame(self.display_frame)
            title_frame.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Label(
                title_frame,
                text=title,
                font=('Helvetica', 14, 'bold')
            ).pack(side=tk.LEFT)
            
            headers, rows = data
            self.current_treeview = AutoTreeview(
                self.display_frame, 
                headers, 
                rows, 
                self.controller
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying content: {str(e)}")

    def place_new_order(self):
        """Display order system"""
        self.show_frame('new_order', "Place New Order", self.create_new_order_frame)
        
    def make_payment(self):
        """Display payment interface - currently not implemented"""
        pass
        
    def view_current_orders(self):
        """Display current orders in treeview"""
        self.show_treeview_content("Current Orders", self.get_current_orders_data())

    def view_previous_orders(self):
        """Display previous orders in treeview"""
        self.show_treeview_content("Previous Orders", self.get_previous_orders_data())
        
    def on_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            try:
                self.root.destroy()
                self.login_window.deiconify()
            except Exception as e:
                messagebox.showerror("Error", f"Error during logout: {str(e)}")

    def on_closing(self):
        """Handle window closing"""
        if messagebox.askyesno("Quit Confirmation", "Are you sure you want to quit the application?"):
            try:
                self.root.destroy()
                self.login_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error during closing: {str(e)}")