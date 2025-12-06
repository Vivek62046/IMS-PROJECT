from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os
import pandas as pd
import plotly.express as px
from datetime import datetime


class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | VivekAnand")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        self.blll_list=[]
        self.var_invoice=StringVar()
        #--------------- title ---------------------
        lbl_title=Label(self.root,text="View Customer Bills",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_invoice=Label(self.root,text="Invoice No.",font=("times new roman",15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="lightyellow").place(x=150,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=340,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=470,y=100,width=120,height=28)
        
        btn_report = Button(self.root, text="Show Report", command=self.sales_report,
                    font=("times new roman", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2")
        btn_report.place(x=600, y=100, width=120, height=28)
   
        #----------------- bill list -------------------
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        #--------------- bill area ----------------------
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=410,height=330)
        
        lbl_title2=Label(bill_Frame,text="Customer Bill Area",font=("goudy old style",20),bg="orange").pack(side=TOP,fill=X)
        
        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        #------------- image -----------------
        #self.bill_photo=Image.open("Inventory-Management-System/images/cat2.jpg")
        self.bill_photo=Image.open(r"C:\Users\DELL\Desktop\Inventory-Management-System-main\images\cat2.jpg")
        self.bill_photo=self.bill_photo.resize((370,300))
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)

        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=720,y=110)
        
        self.show()
#----------------------------------------------------------------------------------------------------
    def show(self):
        del self.blll_list[:]
        self.Sales_List.delete(0,END)
        for i in os.listdir(r'C:\Users\DELL\Desktop\Inventory-Management-System-main\bill'):
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.blll_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        self.bill_area.delete('1.0',END)
        fp=open(rf'C:/Users/DELL/Desktop/Inventory-Management-System-main/bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.blll_list:
                fp=open(rf'C:/Users/DELL/Desktop/Inventory-Management-System-main/billing.py/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)
# Data Analysis 
    def sales_report(self):
        try:
            bill_dir = r'C:\Users\DELL\Desktop\Inventory-Management-System-main\bill'
            sales_data = []

            for file_name in os.listdir(bill_dir):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(bill_dir, file_name)
                    with open(file_path, 'r') as f:
                       lines = f.readlines()

                    date_str = ''
                    net_pay = 0.0
                    for line in lines:
                        if 'Date:' in line:
                            try:
                                date_str = line.strip().split('Date:')[-1].strip()
                                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                            except ValueError:
                                break  # skip if invalid date
                        elif 'Net Pay' in line:
                            try:
                               net_pay = float(line.strip().split('Rs.')[-1].strip())
                            except:
                                break  # skip if net pay is invalid

                    if date_str and net_pay > 0:
                       sales_data.append({'date': date_obj.date(), 'amount': net_pay})

            if not sales_data:
               messagebox.showinfo("No Data", "No valid sales data found for analysis", parent=self.root)
               return

        # Convert to DataFrame
            df = pd.DataFrame(sales_data)
            daily_sales = df.groupby('date')['amount'].sum().reset_index()

        # Show only one plot
            fig = px.bar(
                 daily_sales,
                 x='date',
                 y='amount',
                 title='📊 Daily Sales Report',
                 labels={'date': 'Date', 'amount': 'Total Sales (Rs.)'},
                 text='amount',
                 height=500
            )

            fig.update_traces(texttemplate='₹%{text:.2f}', textposition='outside')
            fig.update_layout(
                xaxis_tickangle=-45,
                title_x=0.5,
                uniformtext_minsize=8,
                uniformtext_mode='hide',
                showlegend=False
            )

            fig.show()

        except Exception as e:
          messagebox.showerror("Error", f"Something went wrong:\n{str(e)}", parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()