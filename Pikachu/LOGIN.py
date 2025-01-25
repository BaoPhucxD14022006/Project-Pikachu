import os
import json
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QMessageBox, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QPixmap, QMovie, QColor
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
import string
import random
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
os.chdir(path)
class LoginUI(QWidget):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic

        # Set full-screen size but keep title bar
        self.setGeometry(0, 0, QApplication.primaryScreen().size().width(), QApplication.primaryScreen().size().height())

        # Fix window size to prevent resizing
        self.setFixedSize(QApplication.primaryScreen().size())

        # Keep the title bar with close button, disable maximize/minimize buttons
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowCloseButtonHint |
            Qt.CustomizeWindowHint
        )

        self.setWindowTitle("Login Page")

        # Kích thước màn hình gốc (1366x768)
        self.base_width = 1366
        self.base_height = 768

        # Tính toán hệ số tỷ lệ
        self.screen_width = QApplication.primaryScreen().size().width()
        self.screen_height = QApplication.primaryScreen().size().height()
        self.scale_x = self.screen_width / self.base_width
        self.scale_y = self.screen_height / self.base_height

        # Set kích thước cửa sổ
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Background Image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, 'images/login_images', 'login_background.png')
        bg_label = QLabel(self)
        bg_label.setPixmap(QPixmap(bg_path).scaled(
            self.screen_width, self.screen_height, Qt.KeepAspectRatioByExpanding
        ))
        bg_label.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Background GIF
        gif_path = os.path.join(current_dir, 'images/login_images', 'pikachu.gif')
        gif_label = QLabel(self)
        gif_label.setGeometry(
            int(250 * self.scale_x),
            int(500 * self.scale_y),
            int(200 * self.scale_x),
            int(100 * self.scale_y),
        )
        gif_label.setScaledContents(True)
        gif_movie = QMovie(gif_path)
        gif_label.setMovie(gif_movie)
        gif_movie.start()

        # Login Frame
        frame_path = os.path.join(current_dir, 'images/login_images', 'login_frame.png')
        frame_label = QLabel(self)
        frame_label.setPixmap(QPixmap(frame_path).scaled(
            int(840 * self.scale_x), int(600 * self.scale_y), Qt.KeepAspectRatioByExpanding
        ))
        frame_label.setGeometry(
            int(450 * self.scale_x),
            int(40 * self.scale_y),
            int(840 * self.scale_x),
            int(600 * self.scale_y),
        )

        # Main Container
        container = QWidget(self)
        container.setGeometry(
            int(450 * self.scale_x),
            int(120 * self.scale_y),
            int(520 * self.scale_x),
            int(400 * self.scale_y),
        )
        layout = QVBoxLayout(container)
        layout.setSpacing(int(10 * self.scale_y))
        layout.setContentsMargins(
            int(100 * self.scale_x), int(100 * self.scale_y), int(100 * self.scale_x), int(100 * self.scale_y)
        )

        # Email
        self.txt_email = self.create_label_input(container, "Email", layout)

        # Password
        self.txt_password = self.create_label_input(container, "Password", layout, password=True)

        # === Captcha Code ===
        self.captcha_code = self.generate_captcha()
        self.lbl_captcha = QLabel(self.captcha_code)
        self.lbl_captcha.setFont(QFont("Times New Roman", int(20 * self.scale_y), QFont.Bold))
        self.lbl_captcha.setStyleSheet("color: blue; background-color: lightgray;")
        self.lbl_captcha.setAlignment(Qt.AlignCenter)

        # Refresh Captcha Button
        btn_refresh_captcha = QLabel()
        btn_refresh_captcha.setPixmap(QPixmap("./images/login_images/refresh_icon.png").scaled(
            int(40 * self.scale_x), int(40 * self.scale_y), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        btn_refresh_captcha.setCursor(Qt.PointingHandCursor)
        btn_refresh_captcha.mousePressEvent = lambda event: self.refresh_captcha()

        # Horizontal Layout for Captcha
        captcha_layout = QHBoxLayout()
        captcha_layout.addWidget(btn_refresh_captcha)  # Thêm nút làm mới bên trái
        captcha_layout.addWidget(self.lbl_captcha)    # Thêm mã captcha
        self.txt_captcha = self.create_label_input(container, "", captcha_layout, password=False)
        # Add Horizontal Layout to Main Layout
        layout.addLayout(captcha_layout)

        # Buttons
        self.btn_login = self.create_button('login_button.png', 560, 420, 150, 100)
        self.btn_login.mousePressEvent = self.logic.login
        self.add_hover_effect(self.btn_login)

        self.btn_register = self.create_button('register_button.png', 720, 420, 150, 100)
        self.btn_register.mousePressEvent = self.logic.register_window
        self.add_hover_effect(self.btn_register)

        # Forgot Password Label
        btn_forgot = QLabel(self)
        btn_forgot.setText('<a href="#">Forgot Password?</a>')
        btn_forgot.setGeometry(
            int(950 * self.scale_x),
            int(530 * self.scale_y),
            int(170 * self.scale_x),
            int(50 * self.scale_y),
        )
        btn_forgot.setStyleSheet(f"""
            font-size: {int(18 * self.scale_y)}px;
            color: blue;
            text-decoration: underline;
        """)
        btn_forgot.setAlignment(Qt.AlignCenter)
        btn_forgot.setOpenExternalLinks(False)
        btn_forgot.setCursor(Qt.PointingHandCursor)
        btn_forgot.linkActivated.connect(self.logic.forgot_password)


    def create_label_input(self, parent, text, layout, password=False):
        label = QLabel(text, parent)
        label.setFont(QFont("Times New Roman", int(20 * self.scale_y), QFont.Bold))
        label.setStyleSheet("""
            QLabel {
                color: black;
                background: transparent;  /* Nền trong suốt để hiệu ứng bóng hoạt động */
            }
        """)
        # Áp dụng hiệu ứng bóng chữ bằng QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)  # Độ mờ của bóng
        shadow.setOffset(1, 1)   # Độ lệch của bóng
        shadow.setColor(QColor("white"))  # Màu của bóng
        label.setGraphicsEffect(shadow)
        layout.addWidget(label)
        
        if text != "":
            input_field = QLineEdit(parent)
            input_field.setFont(QFont("Times New Roman", int(15 * self.scale_y)))
            input_field.setStyleSheet(f"""
                QLineEdit {{
                    border-image: url(./images/login_images/border_input_login.png) 0 0 0 0 stretch stretch;
                    padding-left: {int(25 * self.scale_x)}px;
                    padding-right: {int(25 * self.scale_x)}px;
                    color: black;
                    height: {int(40 * self.scale_y)}px;
                }}
            """)
        else:
            input_field = QLineEdit(parent)
            input_field.setFont(QFont("Times New Roman", int(15 * self.scale_y)))
            input_field.setStyleSheet(f"""
                QLineEdit {{
                    border-image: url(./images/login_images/border_input_login.png) 0 0 0 0 stretch stretch;
                    padding-left: {int(11 * self.scale_x)}px;
                    padding-right: {int(11 * self.scale_x)}px;
                    color: black;
                    height: {int(40 * self.scale_y)}px;
                }}
            """)
        if password:
            input_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(input_field)
        return input_field

    def create_button(self, img_name, x, y, w, h):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'images/login_images', img_name)
        button = QLabel(self)
        button.setPixmap(QPixmap(image_path).scaled(
            int(w * self.scale_x), int(h * self.scale_y), Qt.KeepAspectRatio
        ))
        button.setGeometry(
            int(x * self.scale_x),
            int(y * self.scale_y),
            int(w * self.scale_x),
            int(h * self.scale_y),
        )
        return button

    def add_hover_effect(self, button):
        button.setCursor(Qt.PointingHandCursor)

    def generate_captcha(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(6))

    def refresh_captcha(self):
        self.captcha_code = self.generate_captcha()
        self.lbl_captcha.setText(self.captcha_code)



class LoginLogic:
    def __init__(self):
        self.ui = LoginUI(self)
        self.ui.show()
        self.game_thread = threading.Thread(target=self.preload_game, daemon=True)
        self.game_thread.start()

        # Khởi tạo hiệu ứng âm thanh
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile(os.path.join(current_dir, "sound_effect", "firstblood.wav")))
        self.click_sound.setVolume(0.5)  # Đặt âm lượng (0.0 đến 1.0)

    def play_click_sound(self):
        """Phát âm thanh khi click."""
        self.click_sound.play()

    def preload_game(self):
        """Load the game in the background."""
        import Pikachu
        self.preloaded_game = Pikachu

    def login(self, event=None):
        self.play_click_sound()  # Phát âm thanh
        email = self.ui.txt_email.text()
        password = self.ui.txt_password.text()
        captcha = self.ui.txt_captcha.text()

        if captcha != self.ui.captcha_code:
            QMessageBox.critical(self.ui, "Error", "Captcha is incorrect!")
            self.ui.refresh_captcha()
            return

        try:
            with open(f"{path}/saves/users.json", "r") as file:
                data = json.load(file)
                for user in data:
                    if user["email"] == email and user["password"] == password:
                        QMessageBox.information(self.ui, "Success", "Login Successful!")
                        self.open_game(email)
                        return
                QMessageBox.critical(self.ui, "Error", "Invalid Email or Password!")
        # except FileNotFoundError:
        #     QMessageBox.critical(self.ui, "Error", "No registered users found!")
        except json.JSONDecodeError:
            QMessageBox.critical(self.ui, "Error", "Error loading user data!")

    def open_game(self, email):
        self.ui.hide()
        if hasattr(self, "preloaded_game"):
            self.preloaded_game.main(email)
            result = self.preloaded_game.MainGame(email)
        else:
            QMessageBox.critical(self.ui, "Error", "Game chưa được tải thành công!")
            return

        if result == "LOG OUT":
            self.close_game()
            self.ui.show()

    def close_game(self):
        if hasattr(self, "preloaded_game"):
            self.preloaded_game.pygame.quit()

    def register_window(self, event=None):
        self.play_click_sound()  # Phát âm thanh
        # Tạo QLabel thông báo
        self.label_info = QLabel("Redirecting to Register Page...", self.ui)
    
        # Đặt vị trí ở góc trên bên phải
        self.label_info.setGeometry(1100, 50, 300, 50)  # Điều chỉnh vị trí của thông báo

        # Thêm nền màu và căn giữa chữ
        self.label_info.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 150);  /* Nền đen mờ */
                color: white;  /* Màu chữ trắng */
                font-size: 20px;
                padding: 10px;
                border-radius: 10px;  /* Viền bo tròn */
            }
        """)
        self.label_info.setAlignment(Qt.AlignCenter)  # Căn giữa nội dung thông báo

        self.label_info.show()  # Hiển thị thông báo

        # Đợi 1 giây (1000ms) rồi tự động chuyển trang
        QTimer.singleShot(1000, self.redirect_to_register)
    def add_hover_effect(self, button):
        """Thêm hiệu ứng hover cho các button."""
        button.setCursor(Qt.PointingHandCursor)  # Đổi con trỏ chuột thành nắm tay khi hover
        button.setStyleSheet("""
            QLabel:hover {
                opacity: 0.6;
            }
        """)
        button.mousePressEvent = lambda event: self.play_click_sound()  # Thêm hiệu ứng âm thanh khi click

    def redirect_to_register(self):
        self.label_info.hide()  # Ẩn thông báo sau khi hiển thị
        self.ui.close()  # Đóng cửa sổ đăng nhập
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f'python "{os.path.join(current_dir, "REGISTER.py")}"')

    def forgot_password(self, event = None):
        dialog = QDialog(self.ui)
        dialog.setWindowTitle("Forgot Password")
        dialog.setGeometry(500, 200, 400, 400)
        dialog.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(dialog)

        title = QLabel("Forgot Password")
        title.setFont(QFont("Times New Roman", 20, QFont.Bold))
        title.setStyleSheet("color: red;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        email_label = QLabel("Email")
        email_label.setFont(QFont("Times New Roman", 15, QFont.Bold))
        email_label.setStyleSheet("color: gray;")
        layout.addWidget(email_label)

        txt_email = QLineEdit()
        txt_email.setFont(QFont("Times New Roman", 15))
        txt_email.setStyleSheet("background-color: lightgray; border-radius: 5px;")
        layout.addWidget(txt_email)

        pin_label = QLabel("PIN")
        pin_label.setFont(QFont("Times New Roman", 15, QFont.Bold))
        pin_label.setStyleSheet("color: gray;")
        layout.addWidget(pin_label)

        txt_pin = QLineEdit()
        txt_pin.setFont(QFont("Times New Roman", 15))
        txt_pin.setStyleSheet("background-color: lightgray; border-radius: 5px;")
        layout.addWidget(txt_pin)

        new_password_label = QLabel("New Password")
        new_password_label.setFont(QFont("Times New Roman", 15, QFont.Bold))
        new_password_label.setStyleSheet("color: gray;")
        layout.addWidget(new_password_label)

        txt_new_password = QLineEdit()
        txt_new_password.setFont(QFont("Times New Roman", 15))
        txt_new_password.setEchoMode(QLineEdit.Password)
        txt_new_password.setStyleSheet("background-color: lightgray; border-radius: 5px;")
        layout.addWidget(txt_new_password)

        confirm_password_label = QLabel("Confirm Password")
        confirm_password_label.setFont(QFont("Times New Roman", 15, QFont.Bold))
        confirm_password_label.setStyleSheet("color: gray;")
        layout.addWidget(confirm_password_label)

        txt_confirm_password = QLineEdit()
        txt_confirm_password.setFont(QFont("Times New Roman", 15))
        txt_confirm_password.setEchoMode(QLineEdit.Password)
        txt_confirm_password.setStyleSheet("background-color: lightgray; border-radius: 5px;")
        layout.addWidget(txt_confirm_password)

        btn_reset = QPushButton("Reset Password")
        btn_reset.setFont(QFont("Times New Roman", 15, QFont.Bold))
        btn_reset.setStyleSheet("background-color: green; color: white; border-radius: 5px;")
        btn_reset.clicked.connect(lambda: self.reset_password(dialog, txt_email, txt_pin, txt_new_password, txt_confirm_password))
        layout.addWidget(btn_reset)

        dialog.exec_()

    def reset_password(self, dialog, txt_email, txt_pin, txt_new_password, txt_confirm_password):
        email = txt_email.text().strip()
        pin = txt_pin.text().strip()
        new_password = txt_new_password.text().strip()
        confirm_password = txt_confirm_password.text().strip()

        if not email or not pin or not new_password or not confirm_password:
            QMessageBox.critical(dialog, "Error", "All fields are required!")
            return

        if new_password != confirm_password:
            QMessageBox.critical(dialog, "Error", "Passwords do not match!")
            return

        try:
            with open(f"{path}/saves/users.json", "r") as file:
                users = json.load(file)

            for user in users:
                if user["email"] == email and user.get("pin") == pin:
                    user["password"] = new_password
                    with open(f"{path}/saves/users.json", "w") as file:
                        json.dump(users, file, indent=4)
                    QMessageBox.information(dialog, "Success", "Password reset successfully!")
                    dialog.accept()
                    return

            QMessageBox.critical(dialog, "Error", "Invalid email or PIN!")

        except FileNotFoundError:
            QMessageBox.critical(dialog, "Error", "User database not found.")
        except Exception as e:
            QMessageBox.critical(dialog, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication([])
    login = LoginLogic()
    app.exec_()
