import time
import random
import tkinter as tk
from tkinter import ttk
import threading

class CoffeeManager:
    """Main class to manage multiple stock resources running simultaneously."""

    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Shop Management ☕")
        self.root.geometry("500x900")
        self.root.resizable(False, False)

        # Dictionary to hold all stock management classes
        self.resources = {}

        # UI Setup
        self.setup_ui()

        # Initialize and start multiple stock managers
        self.add_resource("Coffee", CoffeeStock)
        self.add_resource("Milk", MilkStock)
        self.add_resource("Sugar", SugarStock)
        self.add_resource("Tea", TeaStock)
        self.add_resource("Cocoa", CocoaStock)
        self.add_resource("Water", WaterStock)

    def setup_ui(self):
        """Sets up UI elements for tracking multiple stock resources."""
        self.main_label = tk.Label(self.root, text="Stock Management System", font=("Arial", 16, "bold"))
        self.main_label.pack(pady=10)

        # Frame to hold stock UI elements
        self.stock_frame = tk.Frame(self.root)
        self.stock_frame.pack()

    def add_resource(self, name, stock_class):
        """Creates and starts a stock management class."""
        stock_instance = stock_class(self.stock_frame, name)
        self.resources[name] = stock_instance

        # Start stock management in a separate thread
        threading.Thread(target=stock_instance.update_stock, daemon=True).start()


class StockBase:
    """Base class for stock management."""

    def __init__(self, parent, name, initial_stock=10000, threshold=4000):
        self.name = name
        self.stock = initial_stock
        self.max_stock = initial_stock  # Keep track of the max capacity
        self.purchases = 0
        self.tick_count = 0
        self.total_10_tick_consumption = 0
        self.need_restock = False
        self.threshold = threshold

        # UI Elements
        self.label = tk.Label(parent, text=f"{self.name} Stock: {self.stock} units", font=("Arial", 12))
        self.label.pack()

        self.progress = ttk.Progressbar(parent, length=300, mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress.pack(pady=5)

        self.label_purchases = tk.Label(parent, text=f"Total Purchased: {self.purchases} units", font=("Arial", 10), fg="gray")
        self.label_purchases.pack()

        self.label_last_tick = tk.Label(parent, text="⚡ Last Tick: 0 units", font=("Arial", 10), fg="blue")
        self.label_last_tick.pack()

        self.label_10_ticks = tk.Label(parent, text="📊 Consumed in Last 10 Ticks: 0 units", font=("Arial", 10), fg="purple")
        self.label_10_ticks.pack()

    def update_stock(self):
        """Updates stock every 3 seconds in an infinite loop."""
        while True:
            consumption = random.randint(1, 1000)
            self.stock -= consumption
            self.total_10_tick_consumption += consumption
            self.tick_count += 1

            # Update UI
            self.label.config(text=f"{self.name} Stock: {self.stock} units")
            self.label_last_tick.config(text=f"⚡ Last Tick: {consumption} units")

            # Check if stock drops below threshold (flag for restocking)
            if self.stock < self.threshold and not self.need_restock:
                self.need_restock = True

            # Restock only enough to reach max stock
            elif self.need_restock:
                missing_amount = self.max_stock - self.stock  # Buy only needed amount
                self.restock(missing_amount)
                self.need_restock = False  # Reset flag

            # Every 10 ticks, display total consumption and reset counter
            if self.tick_count == 10:
                print(f"📊 {self.name} - Total Consumption Over Last 10 Ticks: {self.total_10_tick_consumption} units")
                self.label_10_ticks.config(text=f"📊 Consumed in Last 10 Ticks: {self.total_10_tick_consumption} units")
                self.total_10_tick_consumption = 0
                self.tick_count = 0

            # Update progress bar
            self.progress["value"] = (self.stock / self.max_stock) * 100
            self.update_progress_color()

            time.sleep(3)  # Simulate tick delay

    def restock(self, amount):
        """Restocks only enough to reach full capacity."""
        if amount > 0:
            print(f"📦 {self.name} Restocking {amount} units...")
            time.sleep(1)  # Simulate short delay
            self.stock += amount
            self.purchases += amount
            self.label_purchases.config(text=f"Total Purchased: {self.purchases} units")
            print(f"✅ {self.name} New stock after restocking: {self.stock} units")

    def update_progress_color(self):
        """Updates progress bar color dynamically based on stock percentage."""
        stock_percentage = (self.stock / self.max_stock) * 100

        if stock_percentage >= 70:
            self.progress.configure(style="Green.Horizontal.TProgressbar")  # Green if stock ≥ 70%
        elif 50 <= stock_percentage < 70:
            self.progress.configure(style="Orange.Horizontal.TProgressbar")  # Orange if stock is 50-69%
        else:
            self.progress.configure(style="Red.Horizontal.TProgressbar")  # Red if stock < 50%


class CoffeeStock(StockBase):
    """Handles coffee stock."""
    def __init__(self, parent, name):
        super().__init__(parent, name)


class MilkStock(StockBase):
    """Handles milk stock."""
    def __init__(self, parent, name):
        super().__init__(parent, name, initial_stock=8000, threshold=3000)


class SugarStock(StockBase):
    """Handles sugar stock."""
    def __init__(self, parent, name):
        super().__init__(parent, name, initial_stock=6000, threshold=2500)


class TeaStock(StockBase):
    """Handles tea stock."""
    def __init__(self, parent, name):
        super().__init__(parent, name, initial_stock=7000, threshold=2800)


class CocoaStock(StockBase):
    """Handles cocoa stock."""
    def __init__(self, parent, name):
        super().__init__(parent, name, initial_stock=5000, threshold=2000)


class WaterStock(StockBase):
    """Handles water stock."""
    def __init__(self, parent, name):
        super().__init__(parent, name, initial_stock=12000, threshold=5000)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()

    # Set up progress bar styles with explicit colors
    style = ttk.Style()
    style.theme_use('default')

    # Green Progress Bar (≥ 70%)
    style.configure("Green.Horizontal.TProgressbar", troughcolor="white", background="green")

    # Orange Progress Bar (50% - 69%)
    style.configure("Orange.Horizontal.TProgressbar", troughcolor="white", background="orange")

    # Red Progress Bar (< 50%)
    style.configure("Red.Horizontal.TProgressbar", troughcolor="white", background="red")

    # Start the manager
    app = CoffeeManager(root)
    root.mainloop()

