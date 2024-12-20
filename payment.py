import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from decimal import Decimal, ROUND_DOWN

class Payment:
    def __init__(self, parent, controller=None):
        """
        Initialize Payment class
        parent: parent window widget
        controller: controller instance for managing data and callbacks
        """
        try:
            self.controller = controller
            self.main_frame = ttk.LabelFrame(parent, text="Payment Information")
            
            self._init_variables()
            
            # Create notebook for payment methods
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
            
            # Create frames for different payment methods
            self.account_frame = ttk.Frame(self.notebook)
            self.credit_frame = ttk.Frame(self.notebook)
            self.debit_frame = ttk.Frame(self.notebook)
            
            # Add frames to notebook
            self.notebook.add(self.account_frame, text='Charge to Account')
            self.notebook.add(self.credit_frame, text='Credit Card')
            self.notebook.add(self.debit_frame, text='Debit Card')
            
            # Setup UI for each payment method
            self._setup_order_summary()
            self._setup_account_payment()
            self._setup_credit_payment()
            self._setup_debit_payment()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Error initializing payment system: {str(e)}")
            raise

    def _init_variables(self):
        """Initialize all variables"""
        # Order amount variables
        self.subtotal_var = tk.StringVar(value="$0.00")
        self.discount_var = tk.StringVar(value="$0.00")
        self.delivery_fee_var = tk.StringVar(value="$0.00")
        self.total_amount_var = tk.StringVar(value="$0.00")
        
        # Credit Card variables
        self.credit_card_number = tk.StringVar()
        self.credit_card_type = tk.StringVar()
        self.credit_expiry_month = tk.StringVar()
        self.credit_expiry_year = tk.StringVar()
        self.credit_cvv = tk.StringVar()
        self.credit_holder = tk.StringVar()
        
        # Debit Card variables
        self.debit_bank_name = tk.StringVar()
        self.debit_card_number = tk.StringVar()

    def _setup_order_summary(self):
        """Setup order summary section"""
        for frame in [self.account_frame, self.credit_frame, self.debit_frame]:
            info_frame = ttk.LabelFrame(frame, text="Order Summary")
            info_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Display current date
            current_date = date.today().strftime("%Y-%m-%d")
            ttk.Label(info_frame, text=f"Date: {current_date}").grid(
                row=0, column=0, columnspan=2, sticky='w', padx=5, pady=2
            )
            
            # Display order amount details
            ttk.Label(info_frame, text="Subtotal:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(info_frame, textvariable=self.subtotal_var).grid(row=1, column=1, sticky='e', padx=5, pady=2)
            
            ttk.Label(info_frame, text="Discount:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(info_frame, textvariable=self.discount_var).grid(row=2, column=1, sticky='e', padx=5, pady=2)
            
            ttk.Label(info_frame, text="Delivery Fee:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(info_frame, textvariable=self.delivery_fee_var).grid(row=3, column=1, sticky='e', padx=5, pady=2)
            
            ttk.Separator(info_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=2)
            
            ttk.Label(info_frame, text="Total Amount:").grid(row=5, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(info_frame, textvariable=self.total_amount_var).grid(row=5, column=1, sticky='e', padx=5, pady=2)

    def _setup_account_payment(self):
        """Setup charge to account payment section"""
        main_container = ttk.Frame(self.account_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        message = "The amount will be charged to your account.\nPlease confirm to proceed."
        ttk.Label(main_container, text=message, justify=tk.CENTER).pack(pady=20)
        
        button_frame = ttk.Frame(main_container)
        button_frame.pack(side=tk.BOTTOM, pady=10)
        
        ttk.Button(button_frame, text="Confirm Payment",
                  command=self._confirm_account_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel",
                  command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _setup_credit_payment(self):
        """Setup credit card payment section"""
        main_container = ttk.Frame(self.credit_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Card Number with validation
        ttk.Label(main_container, text="Card Number:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        card_frame = ttk.Frame(main_container)
        card_frame.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        
        vcmd = (self.main_frame.register(self._validate_card_input), '%P')
        ttk.Entry(
            card_frame,
            textvariable=self.credit_card_number,
            validate='key',
            validatecommand=vcmd
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(card_frame, text="(16 digits)").pack(side=tk.LEFT, padx=5)
        
        # Card Type
        ttk.Label(main_container, text="Card Type:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Combobox(
            main_container,
            textvariable=self.credit_card_type,
            values=['VISA', 'MasterCard', 'American Express'],
            state='readonly'
        ).grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Expiry Date
        ttk.Label(main_container, text="Expiry Date:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        date_frame = ttk.Frame(main_container)
        date_frame.grid(row=2, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Combobox(
            date_frame,
            textvariable=self.credit_expiry_month,
            values=[f"{i:02d}" for i in range(1, 13)],
            width=5,
            state='readonly'
        ).pack(side=tk.LEFT, padx=2)
        ttk.Combobox(
            date_frame,
            textvariable=self.credit_expiry_year,
            values=[str(i) for i in range(2025, 2035)],
            width=6,
            state='readonly'
        ).pack(side=tk.LEFT, padx=2)
        
        # CVV with validation
        ttk.Label(main_container, text="CVV:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        cvv_frame = ttk.Frame(main_container)
        cvv_frame.grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        vcmd_cvv = (self.main_frame.register(self._validate_cvv_input), '%P')
        ttk.Entry(
            cvv_frame,
            textvariable=self.credit_cvv,
            width=5,
            validate='key',
            validatecommand=vcmd_cvv
        ).pack(side=tk.LEFT)
        ttk.Label(cvv_frame, text="(3 digits)").pack(side=tk.LEFT, padx=5)
        
        # Card Holder
        ttk.Label(main_container, text="Card Holder:").grid(row=4, column=0, sticky='w', padx=5, pady=2)
        ttk.Entry(
            main_container,
            textvariable=self.credit_holder
        ).grid(row=4, column=1, sticky='ew', padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Confirm Payment",
                  command=self._confirm_credit_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel",
                  command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _setup_debit_payment(self):
        """Setup debit card payment section"""
        main_container = ttk.Frame(self.debit_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bank selection
        ttk.Label(main_container, text="Bank Name:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Combobox(
            main_container,
            textvariable=self.debit_bank_name,
            values=['Bank A', 'Bank B', 'Bank C'],
            state='readonly'
        ).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        
        # Card Number with validation
        ttk.Label(main_container, text="Card Number:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        card_frame = ttk.Frame(main_container)
        card_frame.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        vcmd = (self.main_frame.register(self._validate_card_input), '%P')
        ttk.Entry(
            card_frame,
            textvariable=self.debit_card_number,
            validate='key',
            validatecommand=vcmd
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(card_frame, text="(16 digits)").pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Confirm Payment",
                  command=self._confirm_debit_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel",
                  command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _validate_card_input(self, new_val):
        """Validate card number input - only allow digits up to 16"""
        if not new_val:  # Allow deletion
            return True
        return new_val.isdigit() and len(new_val) <= 16

    def _validate_cvv_input(self, new_val):
        """Validate CVV input - only allow digits up to 3"""
        if not new_val:  # Allow deletion
            return True
        return new_val.isdigit() and len(new_val) <= 3

    def _confirm_credit_payment(self):
        """Handle credit card payment confirmation"""
        try:
            # 获取表单值
            card_type = self.credit_card_type.get()
            card_number = self.credit_card_number.get()
            cvv = self.credit_cvv.get()
            holder = self.credit_holder.get()
            month = self.credit_expiry_month.get()
            year = self.credit_expiry_year.get()
            
            # Validate required fields
            if not all([card_type, card_number, cvv, holder, month, year]):
                messagebox.showwarning("Validation Error", "Please fill in all required fields")
                return
            
            # Validate exact length
            if len(card_number) != 16:
                messagebox.showwarning("Validation Error", "Card number must be exactly 16 digits")
                return
                
            if len(cvv) != 3:
                messagebox.showwarning("Validation Error", "CVV must be exactly 3 digits")
                return
            
            if hasattr(self.controller, 'temp_order_data'):
                payment_date = date.today()
                card_expiry_date = date(int(year), int(month), 1)
                
                # 调用check_out_with_payment方法时传入所有必要参数
                success = self.controller.temp_order_data['user'].check_out_with_payment(
                    order_data=self.controller.temp_order_data,
                    payment_method="credit",
                    card_number=card_number,
                    card_type=card_type,
                    card_expiry_date=card_expiry_date,  # 使用正确的date对象
                    cvv=cvv,
                    card_holder=holder
                )
                
                if success:
                    messagebox.showinfo("Success", "Credit card payment processed successfully.")
                    self._on_cancel()
                else:
                    messagebox.showerror("Error", f"The current balance is owing too much, \nplease settle the outstanding balance -${self.controller.user.cust_balance.quantize(Decimal('0.00'), rounding=ROUND_DOWN)} first")

            else:
                raise ValueError("Order data not found. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing credit card payment: {str(e)}")

    def _confirm_debit_payment(self):
        """Handle debit card payment confirmation"""
        try:
            # 获取表单值
            bank_name = self.debit_bank_name.get()
            card_number = self.debit_card_number.get()
            
            # Validate required fields
            if not bank_name:
                messagebox.showwarning("Validation Error", "Please select a bank")
                return
            
            if not card_number:
                messagebox.showwarning("Validation Error", "Please enter card number")
                return
            
            # Validate exact length
            if len(card_number) != 16:
                messagebox.showwarning("Validation Error", "Card number must be exactly 16 digits")
                return
            
            if hasattr(self.controller, 'temp_order_data'):
                # 调用check_out_with_payment方法时传入所有必要参数
                success = self.controller.temp_order_data['user'].check_out_with_payment(
                    order_data=self.controller.temp_order_data,
                    payment_method="debit",
                    bank_name=bank_name,
                    debit_card_num=card_number
                )
                
                if success:
                    messagebox.showinfo("Success", "Debit card payment processed successfully.")
                    self._on_cancel()
                else:
                    messagebox.showerror("Error", f"The current balance is owing too much, \nplease settle the outstanding balance -${self.controller.user.cust_balance.quantize(Decimal('0.00'), rounding=ROUND_DOWN)} first")
            else:
                raise ValueError("Order data not found. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing debit card payment: {str(e)}")

    def _confirm_account_payment(self):
        """Handle account payment confirmation"""
        try:
            if hasattr(self.controller, 'temp_order_data'):
                # 调用check_out_with_payment方法时传入所有必要参数
                success = self.controller.temp_order_data['user'].check_out_with_payment(
                    order_data=self.controller.temp_order_data,
                    payment_method="account"
                )
                
                if success:
                    messagebox.showinfo("Success", "Payment has been charged to your account.")
                    self._on_cancel()
                else:
                    messagebox.showerror("Error", f"The current balance is owing too much, \nplease settle the outstanding balance -${self.controller.user.cust_balance.quantize(Decimal('0.00'), rounding=ROUND_DOWN)} first")
            else:
                raise ValueError("Order data not found. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing account payment: {str(e)}")

    def _on_cancel(self):
        """Handle payment cancellation"""
        self.main_frame.destroy()

    def set_order_amounts(self, subtotal: Decimal, discount: Decimal, delivery_fee: Decimal, total: Decimal):
        """Set the order amount display"""
        self.subtotal_var.set(f"${subtotal:.2f}")
        self.discount_var.set(f"-${discount:.2f}")
        self.delivery_fee_var.set(f"${delivery_fee:.2f}")
        self.total_amount_var.set(f"${total:.2f}")

    def get_main_frame(self):
        """Return main frame for integration with other interfaces"""
        return self.main_frame
    
    def _on_cancel(self):
        """Handle payment cancellation.
        Properly cleanup and close the payment window.
        """
        try:
            # Get the toplevel window containing this payment frame
            payment_window = self.main_frame.master
            
            # Release the grab before destroying the window
            payment_window.grab_release()
            
            # Destroy the window
            payment_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during payment cancellation: {str(e)}")


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Payment System")
#     root.geometry("500x600")
    
#     # Create payment app instance
#     payment_app = Payment(root)
    
#     # Set example order amounts
#     payment_app.set_order_amounts(
#         Decimal('100.00'),
#         Decimal('5.00'),
#         Decimal('10.00'),
#         Decimal('105.00')
#     )
    
#     # Pack main frame
#     payment_app.get_main_frame().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
#     # Start main loop
#     root.mainloop()