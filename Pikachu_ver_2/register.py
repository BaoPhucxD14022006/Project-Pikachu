from tkinter import*
from tkinter import ttk, messagebox
from PIL import ImageTk   # pip3 install pillow
import pymysql  # pip3 install pymysql
import json
import os 

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Page")  # For Title of the page
        self.root.geometry("1350x700+0+0")    # Resolution of the page , top, bottom
        self.root.config(bg="white")

        # ===BackGround Image===
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'images', 'back.png')
        self.bg = ImageTk.PhotoImage(file=image_path)
        bg = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        # ===Side Image===
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'images', 'side.jpg')
        self.left = ImageTk.PhotoImage(file=image_path)
        left = Label(self.root, image=self.left).place(x=250, y=250, width=230, height=230)

        # ===Register Frame===
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=85, width=700, height=550)

        # ====Footer Frame=====
        footer = Frame(self.root, bg="gray")
        footer.place(x=0, y=650, relwidth=1, relheight=30)

        footer_name = Label(footer, text="Created & Developed By Saad Ahmed Salim",
                            font=("comic sans ms", 25, "bold"), bg="gray", fg="#ECF0F1").place(x=700, y=12)


        title = Label(frame1, text="Register Here", font=("times new roman", 20, "bold"), bg="white", fg="green").place(x=270, y=30)

        # --------First Row
        f_name = Label(frame1, text="First Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=220, y=100, width=250)

        # --------Second Raw
        l_name = Label(frame1, text="Last Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=140)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=220, y=140, width=250)

        # --------3rd Raw
        user_name = Label(frame1, text="User Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=180)
        self.txt_username = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_username.place(x=220, y=180, width=250)

        # -------Contact
        contact = Label(frame1, text="Contact No ", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=220)
        self.txt_contact = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=220, y=220, width=250)

        # -------Email
        email = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=260)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=220, y=260, width=250)

        # -------Age
        age = Label(frame1, text="Age", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=300)
        self.txt_age = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_age.place(x=220, y=300, width=250)

        # -------Gender
        gender = Label(frame1, text="Gender", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=340)
        self.cmb_gender = ttk.Combobox(frame1, font=("times new roman", 13), state='readonly', justify=CENTER)
        self.cmb_gender['values']=("Select", "Male", "Female", "Other")
        self.cmb_gender.place(x=220, y=340, width=250)
        self.cmb_gender.current(0)

        # ---------Password
        password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=380)
        self.txt_password = Entry(frame1, show="*", font=("times new roman", 15), bg="lightgray")
        self.txt_password.place(x=220, y=380, width=250)

        # --------Confirm Password
        cpassword = Label(frame1, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=420)
        self.txt_cpassword = Entry(frame1, show="*", font=("times new roman", 15), bg="lightgray")
        self.txt_cpassword.place(x=220, y=420, width=250)


        # --------Terms
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="I Agree the Terms & Conditions ", variable=self.var_chk, onvalue=1, offvalue=0, bg="white", font=("times new roman", 12)).place(x=50, y=460)

        # Register Button with Image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'images', 'register.jpg')
        self.btn_img = ImageTk.PhotoImage(file=image_path)
        btn_register = Button(frame1, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data).place(x=50, y=490)

        # -------Sign in Button-----
        btn_login = Button(self.root, text="Log In", command=self.login_window, font=("times new roman", 20), bd=0, cursor="hand2").place(x=320, y=480)


    def login_window(self):
        self.root.destroy()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_dir = os.path.join(current_dir, "login.py")
        os.system(" ".join(["python", current_dir]))

    def clear_data(self):
        self.txt_fname.delete(0,END)
        self.txt_lname.delete(0, END)
        self.txt_username.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_age.delete(0, END)
        self.cmb_gender.current(0)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0,END)

    def create_new_game_for_user(self, username):
        """Khởi tạo trạng thái game cho người chơi mới."""
        game_state = {
            "board": [],  # Bảng game ban đầu, có thể khởi tạo hoặc trống
            "level": 1,
            "lives": 3,
            "game_time": 0,
            "time_bonus": 0,
            "start_time": 0
        }

        save_folder = "saves"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        save_file_path = os.path.join(save_folder, f"{username}_saved_game.json")

        with open(save_file_path, "w") as save_file:
            json.dump(game_state, save_file)
        print(f"Game file created for {username}")

    def register_data(self):
        if self.txt_fname.get() == "" or self.txt_email.get() == "" or self.txt_password.get() == "" or self.txt_cpassword.get() == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
        elif self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
        else:
            user_data = {
                "fname": self.txt_fname.get(),
                "email": self.txt_email.get(),
                "password": self.txt_password.get()
            }

            try:
                data = []
                try:
                    with open("users.json", "r") as file:
                        content = file.read().strip()
                        if content:
                            data = json.loads(content)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = []

                for user in data:
                    if user["email"] == self.txt_email.get():
                        messagebox.showerror("Error", "Email already exists!", parent=self.root)
                        return

                data.append(user_data)
                with open("users.json", "w") as file:
                    json.dump(data, file, indent=4)

                # Sau khi đăng ký thành công, tạo tệp game cho người dùng
                self.create_new_game_for_user(self.txt_email.get())

                messagebox.showinfo("Success", "Registration successful!", parent=self.root)
                self.root.destroy()
                os.system("python login.py")

            except Exception as ex:
                messagebox.showerror("Error", f"Error saving data: {str(ex)}", parent=self.root)
    

root = Tk()
obj = Register(root)
root.mainloop()