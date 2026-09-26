import hashlib
import json
import os
import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank_data.json")


def hash_pin(pin):
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


class BankAccount:
    """
    Bank Account Class
    Demonstrates:
    - Encapsulation
    - OOP
    - Banking operations
    """

    def __init__(self, account_name, pin, balance=0, account_number=None,
                 transactions=None, pin_is_hashed=False):
        self.__account_name = account_name
        self.__pin_hash = pin if pin_is_hashed else hash_pin(pin)
        self.__balance = round(balance, 2)
        self.transactions = transactions if transactions is not None else []
        self.account_number = account_number if account_number is not None else random.randint(100000, 999999)

    def _pin_matches(self, pin):
        return hash_pin(pin) == self.__pin_hash

    def deposit(self, amount, pin):
        if not self._pin_matches(pin):
            return "Incorrect PIN"

        if amount <= 0:
            return "Invalid Amount"

        self.__balance = round(self.__balance + amount, 2)
        self.transactions.append(
            f"[{datetime.now().strftime('%H:%M:%S')}] Deposited GHS {amount:.2f}"
        )
        return "Success"

    def withdraw(self, amount, pin):
        if not self._pin_matches(pin):
            return "Incorrect PIN"

        if amount <= 0:
            return "Invalid Amount"

        if amount > self.__balance:
            return "Insufficient Funds"

        self.__balance = round(self.__balance - amount, 2)

        self.transactions.append(
            f"[{datetime.now().strftime('%H:%M:%S')}] Withdrawn GHS {amount:.2f}"
        )

        return "Success"

    def get_balance(self):
        return self.__balance

    def get_name(self):
        return self.__account_name

    def to_dict(self):
        return {
            "account_name": self.__account_name,
            "pin_hash": self.__pin_hash,
            "balance": self.__balance,
            "account_number": self.account_number,
            "transactions": self.transactions,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            account_name=data["account_name"],
            pin=data["pin_hash"],
            balance=data["balance"],
            account_number=data["account_number"],
            transactions=data["transactions"],
            pin_is_hashed=True,
        )


class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("850x600")
        self.root.configure(bg="#0f172a")

        self.account = None

        self.build_ui()
        self.check_for_saved_account()

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

        self.saved_account_label = tk.Label(
            frame,
            text="",
            font=("Arial", 9, "italic"),
            bg="#1e293b",
            fg="#94a3b8",
            wraplength=380,
            justify="left",
        )
        self.saved_account_label.grid(row=3, column=0, columnspan=2, pady=(0, 5))

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
                    text="Balance: GHS 0.00",
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

        saved = self.load_saved_account()

        # If a saved account exists under this name, treat this as a resume
        # attempt rather than a fresh account, so the same name+PIN a person
        # used before brings their balance and history back.
        if saved is not None and saved["account_name"] == name:
            if hash_pin(pin) != saved["pin_hash"]:
                messagebox.showerror("Error", "Incorrect PIN for the saved account with this name")
                return

            if self.account is not None and self.account.get_name() != name:
                confirmed = messagebox.askyesno(
                    "Replace open account?",
                    f"An account for {self.account.get_name()} is currently open.\n"
                    "Resuming the saved account will discard it from the current session (it stays saved on disk). Continue?",
                )
                if not confirmed:
                    return

            self.account = BankAccount.from_dict(saved)
            self.finish_loading_account(resumed=True)
            return

        if self.account is not None:
            confirmed = messagebox.askyesno(
                "Replace existing account?",
                f"An account for {self.account.get_name()} is already open.\n"
                "Creating a new one will discard it (balance and history included). Continue?",
            )
            if not confirmed:
                return

        self.account = BankAccount(name, pin)
        self.history_box.delete(1.0, tk.END)
        self.history_box.insert(tk.END, f"Account created for {name}\n")
        self.finish_loading_account(resumed=False)

    def finish_loading_account(self, resumed):
        self.welcome_label.config(
            text=f"Welcome, {self.account.get_name()}"
        )

        self.account_number_label.config(
            text="Account Number: ******"
        )
        self.account_number_visible = False
        self.toggle_button.config(text="👁 Show")

        if resumed:
            self.update_history()
            messagebox.showinfo(
                "Welcome back",
                f"Resumed account for {self.account.get_name()}.\nAccount Number: {self.account.account_number}"
            )
        else:
            messagebox.showinfo(
                "Success",
                f"Account created successfully!\nAccount Number: {self.account.account_number}"
            )

        self.update_balance()
        self.name_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)
        self.save_account()
        self.refresh_saved_account_label()

    # ---------- Persistence ----------

    def load_saved_account(self):
        if not os.path.exists(SAVE_FILE):
            return None
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def save_account(self):
        if self.account is None:
            return
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.account.to_dict(), f, indent=2)
        except OSError as err:
            messagebox.showerror("Save failed", f"Could not save account data: {err}")

    def check_for_saved_account(self):
        self.refresh_saved_account_label()

    def refresh_saved_account_label(self):
        saved = self.load_saved_account()
        if saved is None:
            self.saved_account_label.config(text="")
        else:
            self.saved_account_label.config(
                text=f"Saved account on this computer: {saved['account_name']}. "
                     "Enter the same name and PIN above to resume it."
            )

    def deposit_money(self):
        if self.account is None:
            messagebox.showerror("Error", "Create account first")
            return

        try:
            amount = round(float(self.amount_entry.get()), 2)
            pin = self.transaction_pin.get()

            result = self.account.deposit(amount, pin)

            if result == "Success":
                messagebox.showinfo("Success", "Deposit successful")
                self.update_balance()
                self.update_history()
                self.save_account()
                self.amount_entry.delete(0, tk.END)
                self.transaction_pin.delete(0, tk.END)
            else:
                messagebox.showerror("Error", result)

        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")

    def withdraw_money(self):
        if self.account is None:
            messagebox.showerror("Error", "Create account first")
            return

        try:
            amount = round(float(self.amount_entry.get()), 2)
            pin = self.transaction_pin.get()

            result = self.account.withdraw(amount, pin)

            if result == "Success":
                messagebox.showinfo("Success", "Withdrawal successful")
                self.update_balance()
                self.update_history()
                self.save_account()
                self.amount_entry.delete(0, tk.END)
                self.transaction_pin.delete(0, tk.END)
            else:
                messagebox.showerror("Error", result)

        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")

    def update_balance(self):
        balance = self.account.get_balance()
        self.balance_label.config(text=f"Balance: GHS {balance:.2f}")

    def update_history(self):
        self.history_box.delete(1.0, tk.END)

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
