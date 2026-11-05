
import json
import os
from datetime import datetime, date, timedelta

DATA_FILE = "food_items.json"
LOW_STOCK_LIMIT = 2


# Class to store details of each food item
class FoodItem:
    def __init__(self, name, category, quantity, expiry_date):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.expiry_date = expiry_date

    def display(self):
        print(
            f"Name: {self.name} | Category: {self.category} | "
            f"Quantity: {self.quantity} | Expiry Date: {self.expiry_date}"
        )

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date
        }


# Load saved food items from the JSON file
def load_items():
    items = []

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

                for item in data:
                    food = FoodItem(
                        item["name"],
                        item["category"],
                        item["quantity"],
                        item["expiry_date"]
                    )
                    items.append(food)

        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            print("Could not read the saved data. Starting with an empty list.")

    return items


# Save food items to the JSON file
def save_items(items):
    data = []

    for item in items:
        data.append(item.to_dict())

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except OSError:
        print("Error: Could not save the food items.")


# Add a new food item
def add_item(items):
    print("\n--- Add Food Item ---")

    name = input("Enter food name: ").strip()
    category = input("Enter category (Dairy, Fruits, Vegetables, etc.): ").strip()

    if name == "" or category == "":
        print("Name and category cannot be empty.")
        return

    # Check for duplicate food names
    for item in items:
        if item.name.lower() == name.lower():
            print("This food item already exists.")
            print("Please use Update Quantity to change its quantity.")
            return

    try:
        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        expiry_date = input("Enter expiry date (DD-MM-YYYY): ")

        # Check whether the date is valid
        datetime.strptime(expiry_date, "%d-%m-%Y")

        food = FoodItem(name, category, quantity, expiry_date)
        items.append(food)

        save_items(items)
        print("Food item added successfully!")

    except ValueError:
        print("Invalid input! Enter a valid quantity and date.")


# Display all food items
def view_items(items):
    print("\n--- All Food Items ---")

    if len(items) == 0:
        print("No food items available.")
        return

    for item in items:
        item.display()


# Search for a food item
def search_item(items):
    print("\n--- Search Food Item ---")

    name = input("Enter food name to search: ").strip().lower()

    found = False

    for item in items:
        if name in item.name.lower():
            item.display()
            found = True

    if not found:
        print("Food item not found.")


# Update the quantity of a food item
def update_quantity(items):
    print("\n--- Update Quantity ---")

    name = input("Enter food name: ").strip().lower()

    for item in items:
        if item.name.lower() == name:

            try:
                quantity = int(input("Enter new quantity: "))

                if quantity < 0:
                    print("Quantity cannot be negative.")
                    return

                if quantity == 0:
                    items.remove(item)
                    print("Food item removed because quantity is zero.")
                else:
                    item.quantity = quantity
                    print("Quantity updated successfully!")

                save_items(items)
                return

            except ValueError:
                print("Please enter a valid number.")
                return

    print("Food item not found.")


# Delete a food item
def delete_item(items):
    print("\n--- Delete Food Item ---")

    name = input("Enter food name to delete: ").strip().lower()

    for item in items:
        if item.name.lower() == name:
            items.remove(item)
            save_items(items)
            print("Food item deleted successfully!")
            return

    print("Food item not found.")


# Check expired and soon-to-expire food
def check_expiry(items):
    print("\n--- Expiry Check ---")

    today = date.today()
    soon_date = today + timedelta(days=3)

    expired = []
    expiring_soon = []

    for item in items:
        expiry = datetime.strptime(
            item.expiry_date, "%d-%m-%Y"
        ).date()

        if expiry < today:
            expired.append(item)

        elif today <= expiry <= soon_date:
            expiring_soon.append(item)

    print("\nExpired Food:")

    if len(expired) == 0:
        print("No expired food items.")
    else:
        for item in expired:
            item.display()

    print("\nFood Expiring Within 3 Days:")

    if len(expiring_soon) == 0:
        print("No food items expiring soon.")
    else:
        for item in expiring_soon:
            item.display()


# Show food items with low quantity
def low_stock(items):
    print("\n--- Low Stock Warning ---")

    found = False

    for item in items:
        if item.quantity <= LOW_STOCK_LIMIT:
            print(
                item.name,
                "- Only",
                item.quantity,
                "left!"
            )
            found = True

    if not found:
        print("No low-stock items. Your kitchen stock is sufficient.")


# Generate a kitchen stock report
def kitchen_report(items):
    print("\n--- Kitchen Stock Report ---")

    if len(items) == 0:
        print("No food records available.")
        return

    total_quantity = 0
    categories = set()

    for item in items:
        total_quantity += item.quantity
        categories.add(item.category)

    print("Total food items:", len(items))
    print("Total quantity in stock:", total_quantity)
    print("Different categories:", len(categories))

    print("\nCategories Available:")

    for category in categories:
        print("-", category)


# Main menu of the program
def main():
    items = load_items()

    while True:
        print("\n========== FRIDGEFRIEND ==========")
        print("1. Add Food Item")
        print("2. View All Food Items")
        print("3. Search Food Item")
        print("4. Update Quantity")
        print("5. Delete Food Item")
        print("6. Check Expiry Dates")
        print("7. Low Stock Warning")
        print("8. Kitchen Stock Report")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ")

        if choice == "1":
            add_item(items)

        elif choice == "2":
            view_items(items)

        elif choice == "3":
            search_item(items)

        elif choice == "4":
            update_quantity(items)

        elif choice == "5":
            delete_item(items)

        elif choice == "6":
            check_expiry(items)

        elif choice == "7":
            low_stock(items)

        elif choice == "8":
            kitchen_report(items)

        elif choice == "9":
            print("Thank you for using FridgeFriend!")
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 9.")


# Start the program
if __name__ == "__main__":
    main()
