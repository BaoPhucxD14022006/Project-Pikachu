import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QComboBox,
    QCheckBox, QMessageBox, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QPixmap, QFont, QMovie
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
PATH = os.path.dirname(os.path.abspath(__file__))
class RegisterUI(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.setWindowTitle("Registration Page")

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

        self.init_ui()

    def init_ui(self):
        # Background Image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, 'images/login_images', 'register_background.jpg')
        bg_label = QLabel(self)
        bg_label.setPixmap(
            QPixmap(bg_path).scaled(
                int(1400 * self.scale_x),
                int(1000 * self.scale_y),
                Qt.KeepAspectRatioByExpanding
            )
        )
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

        # Register Frame
        frame_path = os.path.join(current_dir, 'images/login_images', 'register_frame.png')
        frame_label = QLabel(self)
        frame_label.setPixmap(
            QPixmap(frame_path).scaled(
                int(800 * self.scale_x),
                int(600 * self.scale_y),
                Qt.KeepAspectRatioByExpanding
            )
        )
        frame_label.setGeometry(
            int(450 * self.scale_x),
            int(0 * self.scale_y),
            int(1000 * self.scale_x),
            int(650 * self.scale_y),
        )

        # Main Container
        container = QWidget(self)
        container.setGeometry(
            int(500 * self.scale_x),
            int(130 * self.scale_y),
            int(400 * self.scale_x),
            int(430 * self.scale_y),
        )
        layout = QVBoxLayout(container)
        layout.setContentsMargins(
            int(25 * self.scale_x),
            int(25 * self.scale_y),
            int(25 * self.scale_x),
            int(25 * self.scale_y),
        )

        # Input Fields
        self.txt_username = self.create_label_input(container, "User Name", layout)
        self.txt_email = self.create_label_input(container, "Email", layout)
        self.cmb_gender = self.create_gender_dropdown(container, layout)
        self.txt_password = self.create_label_input(container, "Password", layout, password=True)
        self.txt_cpassword = self.create_label_input(container, "Confirm Password", layout, password=True)
        self.txt_pin = self.create_label_input(container, "PIN (6 digits)", layout)
        self.chk_terms = self.create_terms_checkbox(container, layout)

        # Buttons
        self.btn_register = self.create_button('register_button.png', 680, 560, 150, 100)
        self.add_hover_effect(self.btn_register)
        self.btn_login = self.create_button('login_button.png', 860, 560, 150, 100)
        self.add_hover_effect(self.btn_login)

    def create_label_input(self, parent, text, layout, password=False):
        widget_container = QWidget(parent)
        widget_layout = QVBoxLayout(widget_container)
        widget_layout.setSpacing(0)

        label = QLabel(text, parent)
        label.setFont(QFont("Times New Roman", int(13 * self.scale_y), QFont.Bold))
        label.setStyleSheet("color: black;")
        layout.addWidget(label)

        input_field = QLineEdit(widget_container)
        input_field.setFont(QFont("Times New Roman", int(13 * self.scale_y)))
        input_field.setStyleSheet(f"""
            QLineEdit {{
                border-image: url(./images/login_images/border_input.png) 0 0 0 0 stretch stretch;
                padding-left: {int(17 * self.scale_x)}px;
                font-size: {int(20 * self.scale_y)}px;
                color: black;
            }}
        """)
        if password:
            input_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(input_field)
        return input_field

    def create_gender_dropdown(self, container, layout):
        # Tạo widget container chứa cả label và combobox
        widget_container = QWidget(container)
        widget_layout = QVBoxLayout(widget_container)
        widget_layout.setContentsMargins(0, 0, 0, 0)

        # Label "Gender"
        label = QLabel("Gender", container)
        label.setFont(QFont("Times New Roman", int(13 * self.scale_y), QFont.Bold))
        label.setStyleSheet("color: black;")
        widget_layout.addWidget(label)

        # Combobox
        cmb_gender = QComboBox(container)
        cmb_gender.addItems(["Select", "Male", "Female", "Other"])
        cmb_gender.setStyleSheet(f"""
            QComboBox {{
                font-size: {int(18 * self.scale_y)}px;
                background-color: lightgray;
                border-image: url(./images/login_images/border_input.png) 0 0 0 0 stretch stretch;
                padding-left: {int(17 * self.scale_x)}px;
                height: {int(30 * self.scale_y)}px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                border: 1px solid lightgray;
                selection-background-color: lightblue;
                selection-color: black;
            }}
            QComboBox::drop-down {{
                border: none;
                width: {int(20 * self.scale_x)}px;
            }}
        """)
        widget_layout.addWidget(cmb_gender)

        # Thêm widget container vào layout chính
        layout.addWidget(widget_container)

        return cmb_gender


    def create_terms_checkbox(self, container, layout):
        chk_terms = QCheckBox("I Agree to the Terms & Conditions", container)
        chk_terms.setStyleSheet(f"""
            font-size: {int(13 * self.scale_y)}px;
        """)
        layout.addWidget(chk_terms)
        return chk_terms

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



class RegisterLogic(RegisterUI):
    def __init__(self):
        super().__init__()

        #Liên kết sự kiện của các nút
        self.btn_register.mousePressEvent = self.register_data
        self.btn_login.mousePressEvent = self.login_window

        # Khởi tạo hiệu ứng âm thanh
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile(os.path.join(current_dir, "sound_effect", "firstblood.wav")))
        self.click_sound.setVolume(0.5)  # Đặt âm lượng (0.0 đến 1.0)

    def play_click_sound(self):
        """Phát âm thanh khi click."""
        self.click_sound.play()

    def login_window(self, event=None):
        self.play_click_sound()  # Phát âm thanh
        # Tạo QLabel thông báo
        self.label_info = QLabel("Redirecting to Login Page...", self)
    
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
        QTimer.singleShot(1000, self.redirect_to_login)

    def redirect_to_login(self):
        self.label_info.hide()
        self.close()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f"python {os.path.join(current_dir, 'LOGIN.py')}")

    def register_data(self, event=None):
        self.play_click_sound()  # Phát âm thanh
        username = self.txt_username.text()
        email = self.txt_email.text()
        password = self.txt_password.text()
        cpassword = self.txt_cpassword.text()
        pin = self.txt_pin.text()

        if not username or not email or not password or not cpassword or not pin:
            QMessageBox.critical(self, "Error", "All fields are required!")
        elif password != cpassword:
            QMessageBox.critical(self, "Error", "Passwords do not match!")
        elif not pin.isdigit() or len(pin) != 6:
            QMessageBox.critical(self, "Error", "PIN must be a 6-digit number!")
        elif not self.chk_terms.isChecked():
            QMessageBox.critical(self, "Error", "You must agree to the terms!")
        else:
            user_data = {"username": username, "email": email, "password": password, "pin": pin}
            try:
                users = []
                if os.path.exists(f"{PATH}/saves/users.json"):
                    with open(f"{PATH}/saves/users.json", "r") as file:
                        users = json.load(file)
                if any(user["email"] == email for user in users):
                    QMessageBox.critical(self, "Error", "Email already exists!")
                else:
                    users.append(user_data)
                    with open(f"{PATH}/saves/users.json", "w") as file:
                        json.dump(users, file, indent=4)
                    self.create_new_game_for_user(email)
                    QMessageBox.information(self, "Success", "Registration successful!")
                    self.close()
                    os.system("python LOGIN.py")
            except Exception as ex:
                QMessageBox.critical(self, "Error", f"Error saving data: {str(ex)}")

    def create_new_game_for_user(self, username):
        game_state = dict()
        save_folder = "saves/save_game"
        os.makedirs(save_folder, exist_ok=True)
        save_file_path = os.path.join(save_folder, f"{username}_saved_game.json")
        with open(save_file_path, "w") as save_file:
            json.dump(game_state, save_file)
        print(f"Game file created for {username}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterLogic()
    window.show()
    sys.exit(app.exec_())
