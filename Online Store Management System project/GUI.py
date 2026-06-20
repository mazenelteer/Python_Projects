from Data import Basket_Of_Products
from Log_In import Log_In
from Add_Product_To_Basket import Add_Product_To_Basket
from Remove_Product_From_Basket import Remove_Product_From_Basket
from Total_Price import Total_Price
from Display_Products import Display_Products

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

EMOJI = {
    "milk":"🥛","bread":"🍞","eggs":"🥚","rice":"🍚","sugar":"🍬","salt":"🧂",
    "flour":"🌾","pasta":"🍝","noodles":"🍜","cornflakes":"🥣","oats":"🌾",
    "honey":"🍯","jam":"🫙","butter":"🧈","cheese":"🧀","cream":"🥛",
    "chicken":"🍗","beef":"🥩","fish":"🐟","shrimp":"🦐","tuna":"🐟","salmon":"🐠",
    "apple":"🍎","banana":"🍌","orange":"🍊","grapes":"🍇","mango":"🥭",
    "pineapple":"🍍","watermelon":"🍉","potato":"🥔","tomato":"🍅","onion":"🧅",
    "garlic":"🧄","carrot":"🥕","cucumber":"🥒","pepper":"🫑","eggplant":"🍆",
    "lettuce":"🥬","spinach":"🥬","broccoli":"🥦","cabbage":"🥬","peas":"🫛",
    "beans":"🫘","lentils":"🫘","chickpeas":"🫘","olive_oil":"🫒","sunflower_oil":"🌻",
    "vinegar":"🫙","soy_sauce":"🫙","ketchup":"🍅","mayonnaise":"🥄","mustard":"🌭",
    "chocolate":"🍫","biscuits":"🍪","cake":"🎂","ice_cream":"🍦","chips":"🥔",
    "popcorn":"🍿","cola":"🥤","orange_juice":"🍊","apple_juice":"🍏","water":"💧",
    "sparkling_water":"💧","energy_drink":"⚡","coffee":"☕","tea":"🍵",
    "green_tea":"🍵","sugar_free_soda":"🥤","detergent":"🧴","dish_soap":"🧴",
    "hand_soap":"🧼","shampoo":"🧴","toothpaste":"🪥","toothbrush":"🪥",
    "paper_towels":"🧻","trash_bags":"🗑️",
}

G="#0F3D2E"; G2="#1D9E75"; GL="#E1F5EE"
W="#FFFFFF"; BG="#F7F8FA"; BD="#E5E7EB"
TX="#1A1A2E"; MU="#6B7280"; RD="#EF4444"

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Store Management System")
        self.geometry("1150x700")
        self.configure(bg=BG)

        self.login_obj   = Log_In()
        self.add_obj     = Add_Product_To_Basket()
        self.remove_obj  = Remove_Product_From_Basket()
        self.total_obj   = Total_Price()
        self.disp_obj    = Display_Products()

        self.users        = {}   
        self.cur_user     = None
        self.cat_var      = None
        self.search_var   = tk.StringVar()
        self.search_var.trace("w", lambda *_: self._render_products())

        self._build_sidebar()
        self._build_pages()
        self._show("products")

    # sidebar
     
    def _build_sidebar(self):
        sb = tk.Frame(self, bg=G, width=210)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Label(sb, text="🛒 Fresh Market", bg=G, fg=W,
                 font=("Helvetica",13,"bold"), pady=16).pack()
        ttk.Separator(sb).pack(fill="x")

        self._nav = {}
        for key, icon, lbl in [("products","🏪","Products"),
                                ("basket",  "🛒","Basket"),
                                ("orders",  "📦","Orders"),
                                ("users",   "👥","Users")]:
            f = tk.Frame(sb, bg=G, cursor="hand2")
            f.pack(fill="x")
            l = tk.Label(f, text=f"  {icon}  {lbl}", bg=G, fg=W,
                         font=("Helvetica",11), anchor="w", pady=10)
            l.pack(fill="x")
            for w in (f, l):
                w.bind("<Button-1>", lambda e, k=key: self._show(k))
                w.bind("<Enter>",  lambda e, f=f, l=l: [f.config(bg=G2), l.config(bg=G2)])
                w.bind("<Leave>",  lambda e, k=key, f=f, l=l: self._nav_leave(k,f,l))
            self._nav[key] = (f, l)

        ttk.Separator(sb).pack(fill="x", pady=6)
        self.badge = tk.Label(sb, text="Basket: 0 · $0", bg=G, fg=GL,
                              font=("Helvetica",9))
        self.badge.pack()

        bot = tk.Frame(sb, bg="#0a2a1e")
        bot.pack(side="bottom", fill="x")
        tk.Label(bot, text="Current User", bg="#0a2a1e", fg=GL,
                 font=("Helvetica",8), pady=2).pack()
        self.uname_lbl = tk.Label(bot, text="Guest", bg="#0a2a1e", fg=W,
                                  font=("Helvetica",10,"bold"))
        self.uname_lbl.pack()
        tk.Button(bot, text="Switch User", bg=G2, fg=W, bd=0,
                  font=("Helvetica",8), pady=4, cursor="hand2",
                  command=lambda: self._show("users")).pack(fill="x", padx=8, pady=6)

    def _nav_leave(self, key, f, l):
        c = G2 if getattr(self,"_page","") == key else G
        f.config(bg=c); l.config(bg=c)

    # pages container

    def _build_pages(self):
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(fill="both", expand=True)
        self.pages = {}
        for n in ("products","basket","orders","users"):
            self.pages[n] = tk.Frame(self.main, bg=BG)
        self._build_products_page()
        self._build_basket_page()
        self._build_orders_page()
        self._build_users_page()

    def _show(self, name):
        self._page = name
        for k,(f,l) in self._nav.items():
            c = G2 if k==name else G
            f.config(bg=c); l.config(bg=c)
        for f in self.pages.values(): f.pack_forget()
        self.pages[name].pack(fill="both", expand=True)
        getattr(self, f"_render_{name}")()

    # products page

    def _build_products_page(self):
        p = self.pages["products"]

        top = tk.Frame(p, bg=W, pady=8)
        top.pack(fill="x")
        tk.Label(top, text="🏪  Products", bg=W, fg=TX,
                 font=("Helvetica",13,"bold")).pack(side="left", padx=14)
        sf = tk.Frame(top, bg=BD)
        sf.pack(side="right", padx=14)
        tk.Label(sf, text="🔍", bg=BD).pack(side="left", padx=5)
        tk.Entry(sf, textvariable=self.search_var, bd=0, bg=BD, fg=TX,
                 font=("Helvetica",10), width=16,
                 insertbackground=TX).pack(side="left", pady=5, padx=4)

        self.cat_row = tk.Frame(p, bg=BG)
        self.cat_row.pack(fill="x", padx=10, pady=5)

        outer = tk.Frame(p, bg=BG)
        outer.pack(fill="both", expand=True, padx=10)
        self.pcanvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=self.pcanvas.yview)
        self.pgrid = tk.Frame(self.pcanvas, bg=BG)
        self.pgrid.bind("<Configure>",
            lambda e: self.pcanvas.configure(scrollregion=self.pcanvas.bbox("all")))
        self.pcanvas.create_window((0,0), window=self.pgrid, anchor="nw")
        self.pcanvas.configure(yscrollcommand=vsb.set)
        self.pcanvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.pcanvas.bind_all("<MouseWheel>",
            lambda e: self.pcanvas.yview_scroll(-1*(e.delta//120),"units"))

    def _render_products(self):
        for w in self.pgrid.winfo_children(): w.destroy()
        q = self.search_var.get().lower()
        items = [(n, p) for n, p in self.disp_obj.data.items()
            if q in n]
        COLS = 6
        for i, (name, price) in enumerate(items):
            r, c = divmod(i, COLS)
            card = tk.Frame(self.pgrid, bg=W, width=155, height=128,
                            highlightbackground=BD, highlightthickness=1,
                            cursor="hand2")
            card.grid(row=r, column=c, padx=4, pady=4)
            card.grid_propagate(False)
            tk.Label(card, text=EMOJI.get(name,"🛍"), bg=GL,
                     font=("Helvetica",25), width=6, pady=3).pack(fill="x")
            tk.Label(card, text=name.replace("_"," ").title(),
                     bg=W, fg=TX, font=("Helvetica",8,"bold"),
                     wraplength=130).pack()
            tk.Label(card, text=f"${price}", bg=W, fg=G2,
                     font=("Helvetica",10,"bold")).pack()
            tk.Button(card, text="+ Add", bg=G2, fg=W, bd=0,
                      font=("Helvetica",8), pady=2, cursor="hand2",
                      command=lambda n=name: self._add_product(n)).pack(
                          fill="x", padx=8, pady=3)

    # basket page

    def _build_basket_page(self):
        p = self.pages["basket"]
        tk.Label(p, text="🛒  My Basket", bg=BG, fg=TX,
                 font=("Helvetica",13,"bold")).pack(anchor="w", padx=14, pady=10)

        mid = tk.Frame(p, bg=BG)
        mid.pack(fill="both", expand=True, padx=14)

        self.blist = tk.Frame(mid, bg=BG)
        self.blist.pack(side="left", fill="both", expand=True)

        rf = tk.Frame(mid, bg=W, width=190,
                      highlightbackground=BD, highlightthickness=1)
        rf.pack(side="right", fill="y", padx=(12,0))
        rf.pack_propagate(False)
        tk.Label(rf, text="Summary", bg=W, fg=TX,
                 font=("Helvetica",11,"bold"), pady=10).pack()
        ttk.Separator(rf).pack(fill="x")
        self.total_lbl = tk.Label(rf, text="$0", bg=W, fg=G2,
                                  font=("Helvetica",22,"bold"), pady=8)
        self.total_lbl.pack()
        self.items_lbl = tk.Label(rf, text="0 items", bg=W, fg=MU,
                                  font=("Helvetica",9))
        self.items_lbl.pack()
        tk.Button(rf, text="✓  Place Order", bg=G2, fg=W, bd=0,
                  font=("Helvetica",10,"bold"), pady=9, cursor="hand2",
                  command=self._place_order).pack(fill="x", padx=10, pady=14, side="bottom")
        tk.Button(rf, text="🗑  Clear All", bg=BG, fg=RD, bd=0,
                  font=("Helvetica",9), cursor="hand2",
                  command=self._clear_basket).pack(side="bottom", pady=4)

    def _render_basket(self):
        for w in self.blist.winfo_children(): w.destroy()
        if not Basket_Of_Products:
            tk.Label(self.blist, text="🛒\n\nBasket is empty",
                     bg=BG, fg=MU, font=("Helvetica",13)).pack(pady=60)
        for name, price in Basket_Of_Products.items():
            row = tk.Frame(self.blist, bg=W,
                           highlightbackground=BD, highlightthickness=1)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=EMOJI.get(name,"🛍"), bg=GL,
                     font=("Helvetica",16), width=3, pady=7).pack(side="left")
            tk.Label(row, text=name.replace("_"," ").title(),
                     bg=W, fg=TX, font=("Helvetica",10,"bold")).pack(
                         side="left", padx=10)
            tk.Label(row, text=f"${price}", bg=W, fg=G2,
                     font=("Helvetica",10,"bold")).pack(side="right", padx=55)
            tk.Button(row, text="✕", bg=W, fg=RD, bd=0,
                      font=("Helvetica",10), cursor="hand2",
                      command=lambda n=name: self._remove_product(n)).pack(
                          side="right", padx=10)
            
        total = self.total_obj.calculate_Total_price()
        self.total_lbl.config(text=f"${total}")
        self.items_lbl.config(text=f"{len(Basket_Of_Products)} items")
        self._update_badge()

    # orders page

    def _build_orders_page(self):
        p = self.pages["orders"]
        tk.Label(p, text="📦  Order History", bg=BG, fg=TX,
                 font=("Helvetica",13,"bold")).pack(anchor="w", padx=14, pady=10)

        ff = tk.Frame(p, bg=BG)
        ff.pack(fill="x", padx=14, pady=(0,6))
        tk.Label(ff, text="Filter by user:", bg=BG, fg=MU,
                 font=("Helvetica",9)).pack(side="left")
        self.order_filter = tk.StringVar(value="All")
        self.order_combo  = ttk.Combobox(ff, textvariable=self.order_filter,
                                         state="readonly", width=18)
        self.order_combo.pack(side="left", padx=8)
        tk.Button(ff, text="Apply", bg=G2, fg=W, bd=0,
                  font=("Helvetica",9), padx=10, cursor="hand2",
                  command=self._render_orders).pack(side="left")

        cols = ("user","items","total","time")
        self.order_tree = ttk.Treeview(p, columns=cols, show="headings",
                                       selectmode="browse")
        for col, w, lbl in [("user",150,"User"),("items",370,"Items"),
                              ("total",80,"Total"),("time",150,"Time")]:
            self.order_tree.heading(col, text=lbl)
            self.order_tree.column(col, width=w)
        vsb = ttk.Scrollbar(p, orient="vertical", command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=vsb.set)
        self.order_tree.pack(fill="both", expand=True, padx=14, pady=(0,10))
        vsb.pack(side="right", fill="y")

    def _render_orders(self):
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)
        filt = self.order_filter.get()
        for uname, udata in self.users.items():
            if filt != "All" and filt != uname: continue
            for o in udata["orders"]:
                self.order_tree.insert("", "end", values=(
                    uname,
                    ", ".join(o["items"]),
                    f"${o['total']}",
                    o["time"],
                ))
        self.order_combo["values"] = ["All"] + list(self.users.keys())

    # users page

    def _build_users_page(self):
        p = self.pages["users"]
        tk.Label(p, text="👥  Users", bg=BG, fg=TX,
                 font=("Helvetica",13,"bold")).pack(anchor="w", padx=14, pady=10)

        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", padx=14)

        form = tk.Frame(top, bg=W, highlightbackground=BD, highlightthickness=1,
                        padx=14, pady=12)
        form.pack(side="left", fill="y")
        tk.Label(form, text="Add / Login User", bg=W, fg=TX,
                 font=("Helvetica",10,"bold")).grid(row=0, column=0,
                                                     columnspan=2, pady=(0,8))
        for i, (lbl, attr) in enumerate([("Name:","_un"), ("ID:","_uid")], 1):
            tk.Label(form, text=lbl, bg=W, fg=MU,
                     font=("Helvetica",9)).grid(row=i, column=0, sticky="w")
            e = tk.Entry(form, font=("Helvetica",10), bg=BG, fg=TX,
                         relief="flat", highlightbackground=BD,
                         highlightthickness=1, insertbackground=TX, width=16)
            e.grid(row=i, column=1, padx=6, pady=3, ipady=4)
            setattr(self, attr, e)
        tk.Button(form, text="Login as this User", bg=G2, fg=W, bd=0,
                  font=("Helvetica",9,"bold"), pady=6, cursor="hand2",
                  command=self._login_user).grid(row=3, column=0, columnspan=2,
                                                  sticky="ew", pady=(8,0))

        # users list

        rf = tk.Frame(top, bg=BG)
        rf.pack(side="left", fill="both", expand=True, padx=(14,0))
        self.user_tree = ttk.Treeview(rf, columns=("name","id","orders"),
                                      show="headings", selectmode="browse", height=8)
        for col, w, lbl in [("name",180,"Name"),("id",130,"User ID"),
                              ("orders",100,"Orders")]:
            self.user_tree.heading(col, text=lbl)
            self.user_tree.column(col, width=w)
        self.user_tree.pack(fill="both", expand=True)
        self.user_tree.bind("<Double-1>", self._select_user)
        tk.Label(rf, text="Double-click a user to switch to them",
                 bg=BG, fg=MU, font=("Helvetica",8)).pack(anchor="w", pady=2)

    def _render_users(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        for name, data in self.users.items():
            self.user_tree.insert("", "end", values=(
                ("★ " if name == self.cur_user else "") + name,
                data["id"],
                len(data["orders"]),
            ), tags=("active" if name == self.cur_user else "",))
        self.user_tree.tag_configure("active", background=GL, foreground=G)

    def _add_product(self, name):

        if self.add_obj.check_product(name):
            self._update_badge()
            self._toast(f"✓ {name.replace('_',' ').title()} added")
        else:
            messagebox.showerror("Error", "This product does not exist!")

    def _remove_product(self, name):
 
        if self.remove_obj.check_Product(name):
            self._render_basket()
            self._toast(f"✕ {name.replace('_',' ').title()} removed")

    def _clear_basket(self):
        Basket_Of_Products.clear()
        self._render_basket()

    def _place_order(self):
        if not Basket_Of_Products:
            messagebox.showwarning("Empty Basket", "Add items first!"); return
        if not self.cur_user:
            messagebox.showwarning("No User", "Please login first from Users page!"); return

        total = self.total_obj.calculate_Total_price()
        order = {
            "items": list(Basket_Of_Products.keys()),
            "total": total,
            "time":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.users[self.cur_user]["orders"].append(order)
        Basket_Of_Products.clear()
        self._render_basket()
        messagebox.showinfo("Order Placed",
                            f"✓ Order saved!\nUser: {self.cur_user}\nTotal: ${total}")

    def _login_user(self):
        name = self._un.get().strip()
        uid  = self._uid.get().strip()
        if not name or not uid:
            messagebox.showwarning("Missing", "Enter both name and ID."); return

        self.login_obj.enter_name_ID(name, uid)
        already = self.login_obj.check_in_history()   
        if name not in self.users:
            self.users[name] = {"id": uid, "orders": []}
        self.cur_user = name
        self.uname_lbl.config(text=name)
        Basket_Of_Products.clear()
        self._update_badge()
        self._render_users()
        msg = "Welcome back!" if already else f"Welcome, {name}!"
        self._toast(msg)

    def _select_user(self, event):
        sel = self.user_tree.selection()
        if not sel: return
        raw = self.user_tree.item(sel[0], "values")[0].replace("★ ", "")
        self.cur_user = raw
        self.uname_lbl.config(text=raw)
        Basket_Of_Products.clear()
        self._update_badge()
        self._render_users()
        self._toast(f"Switched to {raw}")

    def _update_badge(self):
        n = len(Basket_Of_Products)
        t = self.total_obj.calculate_Total_price()
        self.badge.config(text=f"Basket: {n} · ${t}")

    def _toast(self, msg):
        t = tk.Toplevel(self)
        t.overrideredirect(True)
        t.attributes("-topmost", True)
        x = self.winfo_x() + self.winfo_width() - 270
        y = self.winfo_y() + self.winfo_height() - 65
        t.geometry(f"250x38+{x}+{y}")
        t.configure(bg=G)
        tk.Label(t, text=msg, bg=G, fg=W,
                 font=("Helvetica",9), pady=10).pack(fill="both")
        self.after(2000, t.destroy)

GUI().mainloop()
