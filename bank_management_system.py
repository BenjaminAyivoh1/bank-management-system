import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class BankAccount:
    """
    Bank Account Class
    Demonstrates:
    - Encapsulation
    - OOP
    - Banking operations
    """

    def __init__(self, account_name, pin, balance=0):
        self.__account_name = account_name
        self.__pin = pin
        self.__balance = balance
        self.transactions = []
        self.account_number = random.randint(100000, 999999)
        
    def deposit(self, amount):
        if amount <= 0:
            return False

        self.__balance += amount
        self.transactions.append(
            f"[{datetime.now().strftime('%H:%M:%S')}] Deposited GHS {amount}"
        )
        return True

    def withdraw(self, amount, pin):
        if pin != self.__pin:
            return "Incorrect PIN"

        if amount <= 0:
            return "Invalid Amount"

        if amount > self.__balance:
            return "Insufficient Funds"

        self.__balance -= amount

        self.transactions.append(
            f"[{datetime.now().strftime('%H:%M:%S')}] Withdrawn GHS {amount}"
        )

        return "Success"

    def get_balance(self):
        return self.__balance

    def get_name(self):
        return self.__account_name


class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("850x600")
        self.root.configure(bg="#0f172a")

        self.account = None

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="BANK MANAGEMENT SYSTEM",
            font=("Arial", 24, "bold"),
            bg="#0f172a",
            fg="white",
        )
        title.pack(pady=20)

        self.main_frame = tk.Frame(self.root, bg="#1e293b", bd=3, relief="ridge")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.create_account_section()
        self.create_transaction_section()
        self.create_balance_section()
        self.create_history_section()

    def create_account_section(self):
        frame = tk.LabelFrame(
            self.main_frame,
            text="Create Account",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white",
            padx=10,
            pady=10,
        )
        frame.pack(fill="x", padx=15, pady=10)

        tk.Label(frame, text="Account Name", bg="#1e293b", fg="white").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.name_entry = tk.Entry(frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="PIN", bg="#1e293b", fg="white").grid(
            row=1, column=0, padx=10, pady=5
        )
        self.pin_entry = tk.Entry(frame, width=25, show="*")
        self.pin_entry.grid(row=1, column=1, padx=10)

        create_btn = tk.Button(
            frame,
            text="Create Account",
            bg="#22c55e",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.create_account,
        )
        create_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def create_transaction_section(self):
        frame = tk.LabelFrame(
            self.main_frame,
            text="Transactions",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white",
            padx=10,
            pady=10,
        )
        frame.pack(fill="x", padx=15, pady=10)

        tk.Label(frame, text="Amount", bg="#1e293b", fg="white").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.amount_entry = tk.Entry(frame, width=20)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(frame, text="PIN", bg="#1e293b", fg="white").grid(
            row=1, column=0, padx=10, pady=5
        )
        self.transaction_pin = tk.Entry(frame, width=20, show="*")
        self.transaction_pin.grid(row=1, column=1)

        deposit_btn = tk.Button(
            frame,
            text="Deposit",
            bg="#3b82f6",
            fg="white",
            width=15,
            command=self.deposit_money,
        )
        deposit_btn.grid(row=2, column=0, pady=10)

        withdraw_btn = tk.Button(
            frame,
            text="Withdraw",
            bg="#ef4444",
            fg="white",
            width=15,
            command=self.withdraw_money,
        )
        withdraw_btn.grid(row=2, column=1, pady=10)

    def create_balance_section(self):
        frame = tk.Frame(self.main_frame, bg="#1e293b")
        frame.pack(fill="x", padx=15, pady=10)

        self.welcome_label = tk.Label(
            frame,
            text="Welcome",
            font=("Arial", 14, "bold"),
            bg="#1e293b",
            fg="white",
        )
        self.welcome_label.pack(pady=5)

        self.account_number_visible = False

        self.account_number_label = tk.Label(
            frame,
            text="Account Number: ******",
            font=("Arial", 12),
            bg="#1e293b",
            fg="white",
        )

        self.account_number_label.pack(pady=5)

        self.toggle_button = tk.Button(
            frame,
            text="👁 Show",
            command=self.toggle_account_number,
            bg="#334155",
            fg="white",
        )
        self.toggle_button.pack(pady=5)

        self.balance_label = tk.Label(
                    frame,
                    text="Balance: GHS 0",
                    font=("Arial", 20, "bold"),
                    bg="#1e293b",
                    fg="#22c55e",
        )
        self.balance_label.pack()

    def create_history_section(self):
        frame = tk.LabelFrame(
            self.main_frame,
            text="Transaction History",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white",
            padx=10,
            pady=10,
        )
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.history_box = tk.Text(
            frame,
            height=10,
            bg="#0f172a",
            fg="white",
            font=("Consolas", 10),
        )
        self.history_box.pack(fill="both", expand=True)

    def create_account(self):
        name = self.name_entry.get()
        pin = self.pin_entry.get()

        if name == "" or pin == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        self.account = BankAccount(name, pin)

        self.welcome_label.config(
            text=f"Welcome, {self.account.get_name()}"
        )

        self.account_number_label.config(
            text="Account Number: ******"
        )

        messagebox.showinfo(
            "Success",
            f"Account created successfully!\nAccount Number: {self.account.account_number}"
        )

        self.update_balance()
        self.history_box.insert(tk.END, f"Account created for {name}\n")
        self.name_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)

    def deposit_money(self):
        if self.account is None:
            messagebox.showerror("Error", "Create account first")
            return

        try:
            amount = float(self.amount_entry.get())

            if self.account.deposit(amount):
                messagebox.showinfo("Success", "Deposit successful")
                self.update_balance()
                self.update_history()
                self.amount_entry.delete(0, tk.END)
                self.transaction_pin.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid amount")

        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")

    def withdraw_money(self):
        if self.account is None:
            messagebox.showerror("Error", "Create account first")
            return

        try:
            amount = float(self.amount_entry.get())
            pin = self.transaction_pin.get()

            result = self.account.withdraw(amount, pin)

            if result == "Success":
                messagebox.showinfo("Success", "Withdrawal successful")
                self.update_balance()
                self.update_history()
                self.amount_entry.delete(0, tk.END)
                self.transaction_pin.delete(0, tk.END)
            else:
                messagebox.showerror("Error", result)

        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")

    def update_balance(self):
        balance = self.account.get_balance()
        self.balance_label.config(text=f"Balance: GHS {balance}")

    def update_history(self):
        self.history_box.delete(1.0, tk.END)

        for transaction in self.account.transactions:
            self.history_box.insert(tk.END, transaction + "\n")

        for transaction in self.account.transactions:
            self.history_box.insert(tk.END, transaction + "\n")


    def toggle_account_number(self):

        if self.account is None:
            return

        if self.account_number_visible:

            self.account_number_label.config(
                text="Account Number: ******"
            )

            self.toggle_button.config(text="👁 Show")

            self.account_number_visible = False

        else:

            self.account_number_label.config(
                text=f"Account Number: {self.account.account_number}"
            )

            self.toggle_button.config(text="🙈 Hide")

            self.account_number_visible = True

# MAIN PROGRAM
root = tk.Tk()
app = BankManagementSystem(root)
root.mainloop()
