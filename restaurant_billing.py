"""
Problem 5: Restaurant / College-Canteen Billing System
Demonstrates: Tkinter widgets, dictionaries, functions, arithmetic, file handling, exception handling.
"""
from __future__ import annotations
import os, datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from typing import TypedDict, cast

CURRENCY: str = "₹"


class MenuItem(TypedDict):
    category: str
    price: float


class OrderItem(TypedDict):
    price: float
    quantity: int
    total: float


MENU_ITEMS: dict[str, MenuItem] = {
    "Veg Burger": {"category": "Snacks", "price": 80.00},
    "Cheese Pizza": {"category": "Meals", "price": 180.00},
    "Paneer Butter Masala Combo": {"category": "Meals", "price": 160.00},
    "Masala Dosa": {"category": "Meals", "price": 70.00},
    "Club Sandwich": {"category": "Snacks", "price": 65.00},
    "Crispy French Fries": {"category": "Snacks", "price": 50.00},
    "Hakka Veg Noodles": {"category": "Meals", "price": 110.00},
    "Cold Coffee with Ice Cream": {"category": "Beverages", "price": 60.00},
    "Special Masala Chai": {"category": "Beverages", "price": 25.00},
    "Warm Chocolate Brownie": {"category": "Desserts", "price": 75.00},
}


class RestaurantBillingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title("Campus Canteen - Billing System")
        self.root.geometry("1060x680")
        self.root.minsize(920, 600)
        self.order: dict[str, OrderItem] = {}

        self._init_styles()
        self._build_header()
        self._build_main_ui()
        self._build_status_bar()
        self.filter_menu()

    def _init_styles(self) -> None:
        self.style: ttk.Style = ttk.Style()
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        self.style.configure(".", font=("Segoe UI", 10))
        self.style.configure("Treeview", rowheight=25, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        self.style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), background="#1e3a8a", foreground="white")
        self.style.configure("Success.TButton", font=("Segoe UI", 9, "bold"), background="#059669", foreground="white")
        self.style.configure("Danger.TButton", font=("Segoe UI", 9, "bold"), background="#dc2626", foreground="white")
        self.style.map("Primary.TButton", background=[("active", "#2563eb")])
        self.style.map("Success.TButton", background=[("active", "#10b981")])
        self.style.map("Danger.TButton", background=[("active", "#ef4444")])

    def _build_header(self) -> None:
        hdr = tk.Frame(self.root, bg="#1e3a8a", padx=14, pady=10)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="🍽️ Campus Canteen", font=("Segoe UI", 16, "bold"), bg="#1e3a8a", fg="white").pack(side=tk.LEFT)
        tk.Label(hdr, text="• Order & Billing System", font=("Segoe UI", 10, "italic"), bg="#1e3a8a", fg="#93c5fd").pack(side=tk.LEFT, padx=10)
        tk.Label(hdr, text=datetime.datetime.now().strftime("%d-%b-%Y"), font=("Segoe UI", 10, "bold"), bg="#1e3a8a", fg="white").pack(side=tk.RIGHT)

    def _build_main_ui(self) -> None:
        main = tk.Frame(self.root, padx=10, pady=8)
        main.pack(fill=tk.BOTH, expand=True)

        # Left Panel: Food Menu
        left = tk.LabelFrame(main, text=" 📋 Food Menu ", font=("Segoe UI", 10, "bold"), padx=8, pady=8)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        f_bar = tk.Frame(left)
        f_bar.pack(fill=tk.X, pady=(0, 6))
        tk.Label(f_bar, text="Category:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.category_var: tk.StringVar = tk.StringVar(value="All Categories")
        self.cat_combo: ttk.Combobox = ttk.Combobox(f_bar, textvariable=self.category_var, values=["All Categories", "Meals", "Snacks", "Beverages", "Desserts"], state="readonly", width=14)
        self.cat_combo.pack(side=tk.LEFT, padx=6)
        self.cat_combo.bind("<<ComboboxSelected>>", lambda _e: self.filter_menu())
        tk.Label(f_bar, text="Search:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(6, 2))
        self.search_var: tk.StringVar = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        ttk.Entry(f_bar, textvariable=self.search_var, width=12).pack(side=tk.LEFT, fill=tk.X, expand=True)

        m_frame = tk.Frame(left)
        m_frame.pack(fill=tk.BOTH, expand=True)
        self.menu_tree: ttk.Treeview = ttk.Treeview(m_frame, columns=("name", "cat", "price"), show="headings", selectmode="browse")
        self.menu_tree.heading("name", text="Item")
        self.menu_tree.column("name", width=175, anchor="w")
        self.menu_tree.heading("cat", text="Category")
        self.menu_tree.column("cat", width=85, anchor="center")
        self.menu_tree.heading("price", text=f"Price ({CURRENCY})")
        self.menu_tree.column("price", width=75, anchor="e")

        m_scroll: ttk.Scrollbar = ttk.Scrollbar(m_frame, orient=tk.VERTICAL, command=self._scroll_menu)
        self.menu_tree.configure(yscrollcommand=m_scroll.set)
        self.menu_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        m_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu_tree.bind("<<TreeviewSelect>>", self._on_menu_select)
        self.menu_tree.bind("<Double-1>", lambda _e: self.add_item_to_order())

        add_box = tk.LabelFrame(left, text=" Add Item ", font=("Segoe UI", 9, "bold"), padx=6, pady=6)
        add_box.pack(fill=tk.X, pady=(6, 0))
        self.selected_item_label: tk.Label = tk.Label(add_box, text="Click an item in the menu table", fg="#64748b", font=("Segoe UI", 9, "italic"))
        self.selected_item_label.pack(anchor=tk.W, pady=(0, 4))

        q_row = tk.Frame(add_box)
        q_row.pack(fill=tk.X)
        tk.Label(q_row, text="Quantity:").pack(side=tk.LEFT)
        self.qty_var: tk.StringVar = tk.StringVar(value="1")
        self.qty_spinbox: ttk.Spinbox = ttk.Spinbox(q_row, from_=1, to=99, textvariable=self.qty_var, width=5, justify=tk.CENTER)
        self.qty_spinbox.pack(side=tk.LEFT, padx=4)
        self.qty_spinbox.bind("<Return>", lambda _e: self.add_item_to_order())
        ttk.Button(q_row, text="➖", width=3, command=lambda: self._adj_qty(-1)).pack(side=tk.LEFT, padx=1)
        ttk.Button(q_row, text="➕", width=3, command=lambda: self._adj_qty(1)).pack(side=tk.LEFT, padx=1)
        ttk.Button(q_row, text="➕ Add to Order", style="Primary.TButton", command=self.add_item_to_order).pack(side=tk.RIGHT)

        # Right Panel: Order Summary & Billing
        right = tk.LabelFrame(main, text=" 🛒 Order Summary & Billing ", font=("Segoe UI", 10, "bold"), padx=8, pady=8)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        c_row = tk.Frame(right)
        c_row.pack(fill=tk.X, pady=(0, 6))
        tk.Label(c_row, text="Customer:").pack(side=tk.LEFT)
        self.cust_name_var: tk.StringVar = tk.StringVar(value="Walk-in Guest")
        ttk.Entry(c_row, textvariable=self.cust_name_var, width=15).pack(side=tk.LEFT, padx=4)
        tk.Label(c_row, text="Table:").pack(side=tk.LEFT, padx=(6, 2))
        self.table_no_var: tk.StringVar = tk.StringVar(value="T-01")
        ttk.Entry(c_row, textvariable=self.table_no_var, width=6).pack(side=tk.LEFT)

        o_frame = tk.Frame(right)
        o_frame.pack(fill=tk.BOTH, expand=True)
        self.order_tree: ttk.Treeview = ttk.Treeview(o_frame, columns=("item", "price", "qty", "tot"), show="headings", selectmode="browse")
        self.order_tree.heading("item", text="Item")
        self.order_tree.column("item", width=160, anchor="w")
        self.order_tree.heading("price", text=f"Rate ({CURRENCY})")
        self.order_tree.column("price", width=70, anchor="e")
        self.order_tree.heading("qty", text="Qty")
        self.order_tree.column("qty", width=45, anchor="center")
        self.order_tree.heading("tot", text=f"Total ({CURRENCY})")
        self.order_tree.column("tot", width=75, anchor="e")

        o_scroll: ttk.Scrollbar = ttk.Scrollbar(o_frame, orient=tk.VERTICAL, command=self._scroll_order)
        self.order_tree.configure(yscrollcommand=o_scroll.set)
        self.order_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        o_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.order_tree.bind("<Double-1>", lambda _e: self.modify_item_quantity())
        self.order_tree.bind("<Delete>", lambda _e: self.remove_selected_item())

        m_row = tk.Frame(right)
        m_row.pack(fill=tk.X, pady=4)
        ttk.Button(m_row, text="✏️ Change Qty", command=self.modify_item_quantity).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(m_row, text="🗑️ Remove", command=self.remove_selected_item).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(m_row, text="🔄 Clear Order", style="Danger.TButton", command=self.clear_entire_order).pack(side=tk.RIGHT)

        # Billing Summary Box
        b_box = tk.LabelFrame(right, text=" Bill Summary ", font=("Segoe UI", 9, "bold"), padx=8, pady=6)
        b_box.pack(fill=tk.X, pady=(4, 6))

        r0 = tk.Frame(b_box); r0.pack(fill=tk.X, pady=1)
        tk.Label(r0, text="Subtotal:").pack(side=tk.LEFT)
        self.lbl_subtotal: tk.Label = tk.Label(r0, text=f"{CURRENCY} 0.00", font=("Segoe UI", 10, "bold"))
        self.lbl_subtotal.pack(side=tk.RIGHT)

        r1 = tk.Frame(b_box); r1.pack(fill=tk.X, pady=1)
        tk.Label(r1, text=f"Fixed Discount ({CURRENCY}):").pack(side=tk.LEFT)
        self.discount_var: tk.StringVar = tk.StringVar(value="0.00")
        d_ent = ttk.Entry(r1, textvariable=self.discount_var, width=8, justify=tk.RIGHT)
        d_ent.pack(side=tk.LEFT, padx=6)
        d_ent.bind("<Return>", lambda _e: self.calculate_bill())
        ttk.Button(r1, text="Apply", width=6, command=self.calculate_bill).pack(side=tk.LEFT)

        self.student_discount_applied: tk.BooleanVar = tk.BooleanVar(value=False)
        tk.Checkbutton(b_box, text="Student / Staff Special (-₹30)", variable=self.student_discount_applied,
                       command=self._on_toggle_preset_discount, font=("Segoe UI", 8)).pack(anchor=tk.W)

        ttk.Separator(b_box, orient="horizontal").pack(fill=tk.X, pady=4)

        r2 = tk.Frame(b_box); r2.pack(fill=tk.X, pady=1)
        tk.Label(r2, text="FINAL PAYABLE:", font=("Segoe UI", 11, "bold"), fg="#1e3a8a").pack(side=tk.LEFT)
        self.lbl_final_payable: tk.Label = tk.Label(r2, text=f"{CURRENCY} 0.00", font=("Segoe UI", 12, "bold"), fg="#059669")
        self.lbl_final_payable.pack(side=tk.RIGHT)

        a_row = tk.Frame(right)
        a_row.pack(fill=tk.X)
        ttk.Button(a_row, text="🧾 Save Receipt", style="Success.TButton", command=self.save_receipt_to_file).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(a_row, text="👁️ Preview", style="Primary.TButton", command=self.show_receipt_preview).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(a_row, text="🆕 Reset", command=self.reset_entire_app).pack(side=tk.RIGHT)

    def _build_status_bar(self) -> None:
        self.status_var: tk.StringVar = tk.StringVar(value="Ready. Welcome to Campus Canteen!")
        tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 9), bg="#e2e8f0", fg="#475569", anchor=tk.W, padx=10, pady=2).pack(side=tk.BOTTOM, fill=tk.X)

    def _scroll_menu(self, *args: object) -> None:
        getattr(self.menu_tree, "yview")(*args)

    def _scroll_order(self, *args: object) -> None:
        getattr(self.order_tree, "yview")(*args)

    def _on_search_change(self, *args: object) -> None:
        self.filter_menu()

    def _adj_qty(self, delta: int) -> None:
        try:
            self.qty_var.set(str(max(1, int(self.qty_var.get().strip()) + delta)))
        except ValueError:
            self.qty_var.set("1")

    def _on_menu_select(self, event: object = None) -> None:
        sel = self.menu_tree.selection()
        if sel:
            item_data = cast(tuple[str, str, str], self.menu_tree.item(sel[0], "values"))
            name, _, price = item_data
            self.selected_item_label.config(text=f"Selected: {name} ({CURRENCY} {price})", fg="#1e3a8a", font=("Segoe UI", 9, "bold"))

    def filter_menu(self) -> None:
        self.menu_tree.delete(*self.menu_tree.get_children())
        cat = self.category_var.get()
        q = self.search_var.get().strip().lower()
        for name, d in MENU_ITEMS.items():
            if (cat == "All Categories" or d["category"] == cat) and (not q or q in name.lower()):
                self.menu_tree.insert("", tk.END, values=(name, d["category"], f"{d['price']:.2f}"))

    def add_item_to_order(self) -> None:
        sel = self.menu_tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an item from the menu table.")
            return
        item_vals = cast(tuple[str, str, str], self.menu_tree.item(sel[0], "values"))
        name = item_vals[0]
        try:
            qty = int(self.qty_var.get().strip())
            if qty <= 0: raise ValueError("Quantity must be greater than zero.")
        except ValueError as err:
            messagebox.showerror("Invalid Quantity", f"Please enter a valid positive integer.\n\nDetails: {err}")
            self.qty_var.set("1")
            return

        price = MENU_ITEMS[name]["price"]
        prev_qty = self.order[name]["quantity"] if name in self.order else 0
        curr_qty = prev_qty + qty
        self.order[name] = {"price": price, "quantity": curr_qty, "total": curr_qty * price}
        self.qty_var.set("1")
        self.refresh_order_display()
        self.calculate_bill()
        self.status_var.set(f"Added {qty}x '{name}' to order.")

    def modify_item_quantity(self) -> None:
        sel = self.order_tree.selection()
        if not sel:
            messagebox.showwarning("Selection Required", "Please select an item in the order summary.")
            return
        row_vals = cast(tuple[str, str, str, str], self.order_tree.item(sel[0], "values"))
        name = row_vals[0]
        ans = simpledialog.askstring("Change Quantity", f"Enter new quantity for '{name}' (0 to remove):", parent=self.root)
        if ans is None: return
        try:
            new_qty = int(ans.strip())
            if new_qty < 0: raise ValueError("Quantity cannot be negative.")
        except ValueError as err:
            messagebox.showerror("Invalid Input", f"Please enter a valid non-negative integer.\n\nDetails: {err}")
            return

        if new_qty == 0:
            self.order.pop(name, None)
            self.status_var.set(f"Removed '{name}' from order.")
        else:
            self.order[name]["quantity"] = new_qty
            self.order[name]["total"] = new_qty * self.order[name]["price"]
            self.status_var.set(f"Updated '{name}' quantity to {new_qty}.")
        self.refresh_order_display()
        self.calculate_bill()

    def remove_selected_item(self) -> None:
        sel = self.order_tree.selection()
        if not sel: return
        row_vals = cast(tuple[str, str, str, str], self.order_tree.item(sel[0], "values"))
        name = row_vals[0]
        if messagebox.askyesno("Confirm Removal", f"Remove '{name}' from order?", parent=self.root):
            self.order.pop(name, None)
            self.refresh_order_display()
            self.calculate_bill()
            self.status_var.set(f"Removed '{name}' from order.")

    def clear_entire_order(self) -> None:
        if self.order and messagebox.askyesno("Clear Order", "Clear all items from current order?", parent=self.root):
            self.order.clear()
            self.refresh_order_display()
            self.calculate_bill()
            self.status_var.set("Order cleared.")

    def refresh_order_display(self) -> None:
        self.order_tree.delete(*self.order_tree.get_children())
        for name, d in self.order.items():
            self.order_tree.insert("", tk.END, values=(name, f"{d['price']:.2f}", d["quantity"], f"{d['total']:.2f}"))

    def _on_toggle_preset_discount(self) -> None:
        self.discount_var.set("30.00" if self.student_discount_applied.get() else "0.00")
        self.calculate_bill()

    def calculate_bill(self) -> tuple[float, float, float]:
        subtotal: float = sum(d["total"] for d in self.order.values())
        try:
            discount_val: float = float(self.discount_var.get().strip() or "0")
            if discount_val < 0: discount_val = 0.0
        except ValueError:
            discount_val = 0.0
        payable: float = max(0.0, subtotal - discount_val)
        self.lbl_subtotal.config(text=f"{CURRENCY} {subtotal:.2f}")
        self.lbl_final_payable.config(text=f"{CURRENCY} {payable:.2f}")
        return subtotal, discount_val, payable

    def generate_receipt_text(self) -> str:
        subtotal, discount, payable = self.calculate_bill()
        now = datetime.datetime.now()
        cust = self.cust_name_var.get().strip() or "Walk-in Guest"
        table = self.table_no_var.get().strip() or "T-01"
        lines: list[str] = [
            "=" * 52,
            "                 CAMPUS CANTEEN                 ",
            "          Student Centre, University Road       ",
            "                Tel: +91 98765 43210            ",
            "=" * 52,
            f"Receipt No : {now.strftime('REC%Y%m%d%H%M%S')}",
            f"Date & Time: {now.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Customer   : {cust}",
            f"Table/Token: {table}",
            "-" * 52,
            f"{'Item Description':<26}{'Rate':>8}{'Qty':>6}{'Total':>12}",
            "-" * 52,
        ]
        for name, d in self.order.items():
            lines.append(f"{name[:25]:<26}{d['price']:>8.2f}{d['quantity']:>6}{d['total']:>12.2f}")
        lines.extend([
            "-" * 52,
            f"{'Subtotal:':<36}{CURRENCY} {subtotal:>12.2f}",
            f"{'Fixed Discount:':<36}-{CURRENCY} {discount:>11.2f}",
            "=" * 52,
            f"{'FINAL PAYABLE AMOUNT:':<36}{CURRENCY} {payable:>12.2f}",
            "=" * 52,
            "                Payment Status: PAID                ",
            "           Thank you for dining with us!            ",
            "=" * 52,
        ])
        return "\n".join(lines)

    def save_receipt_to_file(self) -> None:
        if not self.order:
            messagebox.showwarning("Empty Order", "Cannot save receipt for an empty order.")
            return
        fpath = filedialog.asksaveasfilename(
            parent=self.root, title="Save Receipt",
            initialfile=f"Receipt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            defaultextension=".txt", filetypes=[("Text Files (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")]
        )
        if not fpath: return
        try:
            folder = os.path.dirname(fpath)
            if folder: os.makedirs(folder, exist_ok=True)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(self.generate_receipt_text())
            messagebox.showinfo("Receipt Saved", f"Receipt saved successfully to:\n\n{fpath}")
            self.status_var.set(f"Receipt saved: {os.path.basename(fpath)}")
        except (IOError, OSError) as err:
            messagebox.showerror("Save Error", f"Failed to save receipt file:\n\n{err}")

    def show_receipt_preview(self) -> None:
        if not self.order:
            messagebox.showwarning("Empty Order", "Order is empty. Add items to preview receipt.")
            return
        win = tk.Toplevel(self.root)
        win.title("Receipt Preview")
        win.geometry("500x540")
        txt = tk.Text(win, font=("Consolas", 10), padx=8, pady=8)
        txt.insert(tk.END, self.generate_receipt_text())
        txt.config(state=tk.DISABLED)
        txt.pack(fill=tk.BOTH, expand=True)
        btn_bar = tk.Frame(win, pady=6)
        btn_bar.pack(fill=tk.X)
        ttk.Button(btn_bar, text="💾 Save to File", style="Success.TButton", command=lambda: [win.destroy(), self.save_receipt_to_file()]).pack(side=tk.LEFT, padx=12)
        ttk.Button(btn_bar, text="Close", command=win.destroy).pack(side=tk.RIGHT, padx=12)

    def reset_entire_app(self) -> None:
        if self.order and not messagebox.askyesno("Reset Order", "Start a new order? Unsaved items will be cleared."):
            return
        self.order.clear()
        self.discount_var.set("0.00")
        self.student_discount_applied.set(False)
        self.cust_name_var.set("Walk-in Guest")
        self.table_no_var.set("T-01")
        self.qty_var.set("1")
        self.selected_item_label.config(text="Click an item in the menu table", fg="#64748b", font=("Segoe UI", 9, "italic"))
        self.refresh_order_display()
        self.calculate_bill()
        self.status_var.set("Ready for a new order.")


def main() -> None:
    root = tk.Tk()
    RestaurantBillingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
