# 🍽️ Campus Canteen - Restaurant & Billing System

A desktop billing application built with **Python** and **Tkinter (ttk)** designed for restaurants and college canteens.

---

## 📌 Project Overview
This application fulfills all requirements of **Problem 5: Restaurant Billing System**:
1. **Interactive Menu**: Displays 10 food items across 4 categories (Meals, Snacks, Beverages, Desserts) with fixed prices.
2. **Item & Quantity Selection**: Interactive menu with category filter, search bar, and quantity controls (Spinbox with `+` / `-` buttons).
3. **Live Order Summary**: `ttk.Treeview` showing real-time items, rates, quantities, and totals, with full editing (modify quantity, remove item, clear order).
4. **Financial Calculations**: Real-time computation of Subtotal, optional Fixed Discount (manual entry or quick Student/Staff discount checkbox), and Final Payable Amount.
5. **Receipt Generation & File Handling**: Formats a structured text receipt with order ID, timestamp, itemization, and totals, with both live on-screen Preview and Save to `.txt` file functionality.
6. **Robust Exception Handling**: Thorough validation with `try...except` blocks for invalid quantities, discount amounts, and file I/O operations.

---

## 🚀 How to Run

### Requirements
- Python 3.8+ (Tkinter is included with standard Python installations on Windows/macOS).

### Launching the Application
Open a terminal (PowerShell / Command Prompt) in this directory and run:
```bash
python restaurant_billing.py
```

### Running the Automated Unit Tests
To run the automated test suite verifying all menu items, calculations, discounts, exception handling, and file operations:
```bash
python test_billing.py
```

---

## 💡 Concepts Demonstrated

| Concept | Implementation Details |
| :--- | :--- |
| **Tkinter Widgets** | `Tk`, `ttk.Frame`, `LabelFrame`, `Label`, `ttk.Entry`, `ttk.Button`, `ttk.Treeview`, `ttk.Scrollbar`, `ttk.Combobox`, `ttk.Spinbox`, `ttk.Separator`, `Toplevel` (modal dialog), `Text`, `messagebox`, `filedialog`, `simpledialog`. |
| **Dictionaries & Typing** | - `MENU_ITEMS`: Master catalog `{name: {"category": str, "price": float}}`<br>- `self.order`: Active order state typed with `TypedDict`<br>- Full static typing adhering to strict Pylance/Pyright mode (0 errors). |
| **Functions** | Clean, modular methods: `add_item_to_order()`, `modify_item_quantity()`, `remove_selected_item()`, `clear_entire_order()`, `calculate_bill()`, `apply_discount_manually()`, `generate_receipt_text()`, `save_receipt_to_file()`, `show_receipt_preview()`. |
| **Arithmetic** | Item line total ($Rate \times Qty$), Subtotal ($\sum Totals$), Discount deduction, and Final Amount ($\max(0.00, Subtotal - Discount)$) formatted to 2 decimal places. |
| **File Handling** | Generating structured ASCII text receipts and writing to file using `with open(filepath, 'w', encoding='utf-8')` with directory verification. |
| **Exception Handling** | `try...except ValueError` for non-numeric, negative, or zero quantities and invalid discount values; `try...except (IOError, OSError)` for disk/file writing operations. |

---

## 📋 Food Menu Catalog (Fixed Prices)

| Food Item | Category | Price (₹) |
| :--- | :--- | :---: |
| Veg Burger | Snacks | ₹ 80.00 |
| Cheese Pizza | Meals | ₹ 180.00 |
| Paneer Butter Masala Combo | Meals | ₹ 160.00 |
| Masala Dosa | Meals | ₹ 70.00 |
| Club Sandwich | Snacks | ₹ 65.00 |
| Crispy French Fries | Snacks | ₹ 50.00 |
| Hakka Veg Noodles | Meals | ₹ 110.00 |
| Cold Coffee with Ice Cream | Beverages | ₹ 60.00 |
| Special Masala Chai | Beverages | ₹ 25.00 |
| Warm Chocolate Brownie | Desserts | ₹ 75.00 |

---

## ⌨️ Shortcuts & User Interaction
- **Double-Click Menu Item**: Instantly adds 1 unit of that item to the order.
- **Enter on Quantity Box**: Adds the selected item with the typed quantity.
- **Double-Click Order Item**: Opens the quantity modification dialog.
- **Delete Key on Order Table**: Prompts to remove the selected order row.
- **Enter on Discount Box**: Immediately calculates and applies the new discount.
