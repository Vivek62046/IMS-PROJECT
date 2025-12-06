from tkinter import *
from tkinter import messagebox
import os
import sqlite3
from PIL import Image, ImageTk
import dashboard  # Make sure this file/module exists
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random



class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page | Inventory Management System")
       # self.root.geometry("400x300+500+200")
        #self.root.resizable(False, False)
        #self.root.configure(bg="white")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="Cyan")

       # ================== Variables ==================
        self.employee_id = StringVar()
        self.password_var = StringVar()

        # ================== Images ==================
        self.phone_image = ImageTk.PhotoImage(file=r"C:\Users\DELL\Desktop\Inventory-Management-System-main\images\phone.png")
        lbl_phone = Label(self.root, image=self.phone_image, bd=0, bg="white")
        lbl_phone.place(x=200, y=50)

        # ================== Login Frame ==================
        login_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_Frame.place(x=650, y=90, width=350, height=460)

        title = Label(login_Frame, text="Login System", font=("times new roman", 30, "bold"), bg="white").place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_Frame, text="Employee ID", font=("times new roman", 15, "bold"), bg="white", fg="#767171").place(x=50, y=100)
        Entry(login_Frame, textvariable=self.employee_id, font=("times new roman", 15), bg="lightyellow").place(x=50, y=140, width=250)

        lbl_pass = Label(login_Frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="#767171").place(x=50, y=200)
        Entry(login_Frame, textvariable=self.password_var, show="*", font=("times new roman", 15), bg="lightyellow").place(x=50, y=240, width=250)

        btn_login = Button(login_Frame, text="Log in", command=self.login, font=("times new roman", 15), bg="blue", fg="white", bd=0, cursor="hand2")
        btn_login.place(x=50, y=300, width=210, height=35)

        hr = Label(login_Frame, bg="green").place(x=50, y=370, width=250, height=2)
        or_ = Label(login_Frame, text="OR", bg="white", fg="green", font=("times new roman", 15, "bold")).place(x=150, y=355)

        btn_forget = Button(login_Frame, text="Forget Password?", command=self.forget_window, font=("times new roman", 13), bg="white", fg="black", bd=0, cursor="hand2")
        btn_forget.place(x=100, y=390)

        # ================== Animated Images ==================
        self.im1 = ImageTk.PhotoImage(file=r"C:\Users\DELL\Desktop\Inventory-Management-System-main\images\im1.png")
        self.im2 = ImageTk.PhotoImage(file=r"C:\Users\DELL\Desktop\Inventory-Management-System-main\images\im2.png")
        self.im3 = ImageTk.PhotoImage(file=r"C:\Users\DELL\Desktop\Inventory-Management-System-main\images\im3.png")

        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)

        self.animate()

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        try:
            if self.employee_id.get() == "" or self.password_var.get() == "":
                messagebox.showerror('Error', "All fields are required", parent=self.root)
                return

            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            cur.execute("SELECT utype FROM employee WHERE eid=? AND pass=?", (self.employee_id.get(), self.password_var.get()))
            user = cur.fetchone()
            con.close()

            if user is None:
                messagebox.showerror('Error', "Invalid Username or Password", parent=self.root)
            else:
                messagebox.showinfo("Success", f"Welcome {user[0]}", parent=self.root)
                self.root.destroy()
                if user[0] == "Admin":
                    os.system("python dashboard.py")
                else:
                    os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


 # ************************ Forget Password ****************
    def forgot_password(self):
        if self.employee_id.get() == "":
            messagebox.showerror("Error", "Please enter your Employee ID first", parent=self.root)
            return

        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT pass FROM employee WHERE eid=?", (self.employee_id.get(),))
            result = cur.fetchone()
            if result:
                messagebox.showinfo("Password Recovery", f"Your password is: {result[0]}", parent=self.root)
            else:
                messagebox.showerror("Error", "Employee ID not found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

# Forget Window 
    def forget_window(self):
        if self.employee_id.get() == "":
           messagebox.showerror("Error", "Please enter your Employee ID", parent=self.root)
           return

        try:
            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            cur.execute("SELECT eid FROM employee WHERE eid=?", (self.employee_id.get(),))
            result = cur.fetchone()
            con.close()

            if result is None:
               messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
               return

        # Create Password Reset Window
            self.var_New_Pass = StringVar()
            self.var_Conf_Pass = StringVar()

            self.forget_win = Toplevel(self.root)
            self.forget_win.title('Reset Password')
            self.forget_win.geometry('400x300+500+150')
            self.forget_win.focus_force()

            Label(self.forget_win, text='Reset Password', font=('goudy old style', 18, 'bold'), bg="#3f51b5", fg="white").pack(side=TOP, fill=X)

            Label(self.forget_win, text='New Password', font=('times new roman', 15)).place(x=20, y=80)
            Entry(self.forget_win, textvariable=self.var_New_Pass, show="*", font=('times new roman', 15), bg='lightyellow').place(x=180, y=80, width=180)

            Label(self.forget_win, text='Confirm Password', font=('times new roman', 15)).place(x=20, y=130)
            Entry(self.forget_win, textvariable=self.var_Conf_Pass, show="*", font=('times new roman', 15), bg='lightyellow').place(x=180, y=130, width=180)

            Button(self.forget_win, text="Reset", command=self.reset_password, font=("times new roman", 15), bg="green", fg="white").place(x=150, y=200)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


 # Reset Password
    def reset_password(self):
        if self.var_New_Pass.get() != self.var_Conf_Pass.get():
           messagebox.showerror("Error", "Passwords do not match", parent=self.forget_win)
           return

        try:
            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            cur.execute("UPDATE employee SET pass=? WHERE eid=?", (self.var_New_Pass.get(), self.employee_id.get()))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Password reset successfully", parent=self.forget_win)
            self.forget_win.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.forget_win)
         


if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
