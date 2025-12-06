from tkinter import*
from PIL import Image,ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox
import plotly.express as px


class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x760+110+100")
        self.root.title("Inventory Management System | Vivek Anand")
        self.root.resizable(True, True)
        self.root.config(bg="white")

        #------------- title --------------
        # self.icon_title=PhotoImage(file="Inventory-Management-System-main/images/logo1.png")
        self.icon_title = PhotoImage(file=r"images\logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #------------ logout button -----------
        #btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2")
        btn_logout.place(x=1150, y=10, height=50, width=150)

        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #---------------- left menu ---------------
       # self.MenuLogo=Image.open("Inventory-Management-System-main/images/menu_im.png")
        self.MenuLogo=Image.open(r"images\menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=620)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)

       # self.icon_side=PhotoImage(file="Inventory-Management-System-main/images/side.png")
        self.icon_side=PhotoImage(file=r"images\side.png")
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
         # **** Data Analysis Button ******
        btn_analytics = Button(LeftMenu, text="Analytics", command=self.analytics, image=self.icon_side,
                               compound=LEFT, padx=5, anchor="w", font=("times new roman", 20, "bold"),
                               bg="white", bd=5, cursor="hand2")
        btn_analytics.pack(side=TOP, fill=X)
        #btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu, text="Exit", command=self.btn_exit, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman",20,"bold"), bg="white", bd=3, cursor="hand2")
        btn_exit.pack(side=TOP, fill=X)
        

        #----------- content ----------------
        self.lbl_employee=Label(self.root,text="Total Employee\n{ 0 }",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n{ 0 }",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category\n{ 0 }",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product\n{ 0 }",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n{ 0 }",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        #self.lbl_Analytics=Label(self.root,text="Total Analytics\n{ 0 }",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        #self.lbl_Analytics.place(x=1000,y=300,height=150,width=300)

        #------------ footer -----------------
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Developed by Deepak Kumar Singh\nFor any Technical Issues Contact: 9523941328",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()
#-------------- functions ----------------
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {str(len(product))} ]")

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {str(len(category))} ]")

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {str(len(employee))} ]")

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {str(len(supplier))} ]")
            
            bill=len(os.listdir(r"bill"))
            self.lbl_sales.config(text=f"Total Sales\n[ {str(bill)} ]")

           # cur.execute("SELECT SUM(quantity) FROM product")  # Assuming `quantity` or `stock` exists in the `product` table
           # total_products = cur.fetchone()[0]  # This will give the total quantity of products in stock
            #self.lbl_Analytics.config(text=f"Total Analytics\n[ {str(total_products)} products in stock ]")

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

# ***** Data *****
    #def analytics(self):
       # try:
           # con = sqlite3.connect(database=r'ims.db')
           # df = pd.read_sql_query("SELECT * FROM sales", con)

           # if df.empty:
               # messagebox.showinfo("Analytics", "No sales data available.", parent=self.root)
               # return

           # df['date'] = pd.to_datetime(df['date'], errors='coerce')
           # df = df.dropna(subset=['date'])

           # df['Month'] = df['date'].dt.to_period('M')
          #  monthly_sales = df.groupby('Month')['amount'].sum()

          #  monthly_sales.plot(kind='bar', title='Monthly Sales Summary', color='skyblue')
           # plt.xlabel('Month')
           # plt.ylabel('Total Sales')
          #  plt.tight_layout()
           # plt.show()

       # except Exception as ex:
          #  messagebox.showerror("Error", f"Analytics error: {str(ex)}", parent=self.root)
   # def analytics(self):
    # try:
       # con = sqlite3.connect(database=r'ims.db')
       # df = pd.read_sql_query("SELECT name, qty FROM product", con)

       # if df.empty:
           # messagebox.showinfo("Analytics", "No product data available.", parent=self.root)
           # return

       # df = df.sort_values(by='qty', ascending=False)

       # fig = px.bar(
          #  df,
          #  x='name',
           # y='qty',
            #title='Stock Quantity by Product',
            #labels={'name': 'Product Name', 'qty': 'Quantity'},
            #color='qty',
            #text='qty',
           # height=600,
           # color_continuous_scale='viridis'  # or 'blues', 'plasma', etc.
        #)

        #fig.update_traces(textposition='outside')
        #fig.update_layout(
        #    xaxis_tickangle=-45,
         #   title_x=0.5,
          #  uniformtext_minsize=8,
           # uniformtext_mode='hide'
        #)

       # fig.show()

     #except Exception as ex:
     #   messagebox.showerror ("Error", f"Analytics error: {str(ex)}", parent=self.root)
    def analytics(self):
     try:
        con = sqlite3.connect(database=r'ims.db')
        df = pd.read_sql_query("SELECT name, qty FROM product", con)

        if df.empty:
            messagebox.showinfo("Analytics", "No product data available.", parent=self.root)
            return

        # Ensure qty is numeric
        df['qty'] = pd.to_numeric(df['qty'], errors='coerce').fillna(0).astype(int)

        # Sort by quantity
        df = df.sort_values(by='qty', ascending=False)

      # === Export to Excel ===
        export_path = os.path.join(os.getcwd(), "stock_analytics_report.xlsx")
        df.to_excel(export_path, index=False)

        messagebox.showinfo("Export Success", f"Analytics report exported to:\n{export_path}", parent=self.root)

        fig = px.bar(
            df,
            x='name',
            y='qty',
            title='Stock Quantity by Product',
            labels={'name': 'Product Name', 'qty': 'Quantity'},
            color='qty',
            text='qty',
            height=600,
            color_continuous_scale='viridis'
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_tickangle=-45,
            title_x=0.5,
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )

        fig.show()

     except Exception as ex:
        messagebox.showerror("Error", f"Analytics error: {str(ex)}", parent=self.root)

    
      

  # **************Exit Function*****************

    def btn_exit(self):
        confirm = messagebox.askyesno("Inventory Management System", "Are you sure you want to exit this project?", parent=self.root)
        if confirm:
            self.root.destroy()

  # ************* LogOut **************
    def logout(self):
       confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root)
       if confirm:
            self.root.destroy()  # Closes the main dashboard
            os.system("python Login.py")
            # Optionally, import and call your login window here
            # from login import Login
            # root = Tk()
            # Login(root)
            # root.mainloop()

      

if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()