import os
import json
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk  # For displaying images
import time
import threading  # Thêm mô-đun threading

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # === Background Image ===
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'images', 'back.png')
        self.bg = ImageTk.PhotoImage(file=image_path)
        bg = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # === Login Frame ===
        frame = Frame(self.root, bg="white")
        frame.place(x=480, y=100, width=400, height=500)

        # === Logo Image ===
        image_path = os.path.join(current_dir, 'images', 'side.jpg')
        self.left = ImageTk.PhotoImage(file=image_path)
        left = Label(self.root, image=self.left).place(x=250, y=250, width=230, height=230)

        # === Title ===
        title = Label(frame, text="Login Here", font=("times new roman", 20, "bold"), bg="white", fg="green").place(x=120, y=150)

        # === Email ===
        email = Label(frame, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=200)
        self.txt_email = Entry(frame, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=50, y=230, width=300)

        # === Password ===
        password = Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=270)
        self.txt_password = Entry(frame, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_password.place(x=50, y=300, width=300)

        # === Login Button ===
        btn_login = Button(frame, text="Login", font=("times new roman", 15), bg="green", fg="white", command=self.login).place(x=50, y=360, width=300)

        # === Register Button ===
        btn_register = Button(frame, text="Register", font=("times new roman", 15), bg="blue", fg="white", command=self.register_window).place(x=50, y=410, width=300)

        # === Start loading game in the background ===
        self.game_thread = threading.Thread(target=self.preload_game, daemon=True)
        self.game_thread.start()

    def preload_game(self):
        """Load the game in the background."""
        import Pikachu
        self.preloaded_game = Pikachu  # Store game reference for later use

    def login(self):
        email = self.txt_email.get()
        password = self.txt_password.get()

        try:
            with open("users.json", "r") as file:
                data = json.load(file)
                for user in data:
                    if user["email"] == email and user["password"] == password:
                        messagebox.showinfo("Success", "Login Successful!")
                        self.open_game(email)
                        return
                messagebox.showerror("Error", "Invalid Email or Password!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No registered users found!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error loading user data!")
        
    def open_game(self, email):
        """Show the game immediately after login."""
        self.root.withdraw()  # Hide login window
        if hasattr(self, "preloaded_game"):
            result = self.preloaded_game.main(email)  # Launch the preloaded game
        else:
            messagebox.showerror("Error", "Game not preloaded successfully!")
            return
        
        # Handle logout if needed
        if result == "LOG OUT":
            self.root.deiconify()

    def register_window(self):
        self.root.destroy()  # Close current window
        import register  # Open registration window

if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
