import sys
import json
import hashlib
import re
from datetime import datetime
from typing import Optional, Tuple

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QCheckBox,
    QSizePolicy, QGraphicsDropShadowEffect, QStackedWidget
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, 
    QSequentialAnimationGroup, pyqtProperty, QSize
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QLinearGradient, 
    QPainter, QBrush, QPen, QPixmap, QIcon,
    QFontDatabase, QPainterPath
)

# Load custom fonts (optional - you can use system fonts)
def load_fonts():
    try:
        QFontDatabase.addApplicationFont(":/fonts/poppins.ttf")
    except:
        pass  # Use system fonts if custom fonts not available

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Animation properties
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 100, 255, 80))
        self.shadow.setOffset(0, 3)
        self.setGraphicsEffect(self.shadow)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.animate_press()
        super().mousePressEvent(event)
    
    def animate_press(self):
        original_geometry = self.geometry()
        pressed_geometry = original_geometry.adjusted(2, 2, -2, -2)
        
        self._animation.stop()
        self._animation.setStartValue(original_geometry)
        self._animation.setEndValue(pressed_geometry)
        self._animation.start()

class ModernInputField(QFrame):
    def __init__(self, placeholder="", is_password=False, icon=None, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            ModernInputField {
                background-color: rgba(255, 255, 255, 30);
                border: 2px solid rgba(255, 255, 255, 50);
                border-radius: 10px;
                padding: 0px 15px;
            }
            ModernInputField:focus {
                border: 2px solid rgba(100, 150, 255, 150);
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Icon label (optional)
        self.icon_label = QLabel()
        if icon:
            self.icon_label.setPixmap(icon.pixmap(20, 20))
            self.icon_label.setFixedSize(20, 20)
            layout.addWidget(self.icon_label)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: white;
                font-size: 14px;
                font-weight: 500;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 150);
            }
        """)
        
        if is_password:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn = QPushButton()
            self.toggle_btn.setCheckable(True)
            self.toggle_btn.setFixedSize(30, 30)
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    color: white;
                    font-size: 18px;
                }
            """)
            self.toggle_btn.setText("👁")
            self.toggle_btn.clicked.connect(self.toggle_password_visibility)
            layout.addWidget(self.input_field)
            layout.addWidget(self.toggle_btn)
        else:
            layout.addWidget(self.input_field)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #ff4757; font-size: 12px;")
        self.error_label.setVisible(False)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self)
        self.main_layout.addWidget(self.error_label)
        self.main_layout.setSpacing(5)
        
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        
    def toggle_password_visibility(self):
        if self.toggle_btn.isChecked():
            self.input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("👁")
        else:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("👁")
    
    def text(self):
        return self.input_field.text()
    
    def setText(self, text):
        self.input_field.setText(text)
    
    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(bool(message))
        self.setStyleSheet("""
            ModernInputField {
                background-color: rgba(255, 255, 255, 30);
                border: 2px solid #ff4757;
                border-radius: 10px;
                padding: 0px 15px;
            }
        """)
    
    def clear_error(self):
        self.error_label.setVisible(False)
        self.setStyleSheet("""
            ModernInputField {
                background-color: rgba(255, 255, 255, 30);
                border: 2px solid rgba(255, 255, 255, 50);
                border-radius: 10px;
                padding: 0px 15px;
            }
        """)

class GradientLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#00b4db"))
        gradient.setColorAt(1, QColor("#0083b0"))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        
        # Draw text with gradient
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        
        self.title_label = GradientLabel("Welcome Back")
        self.title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.title_label.setFixedHeight(40)
        
        self.subtitle_label = QLabel("Sign in to your account")
        self.subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 14px;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        main_layout.addLayout(header_layout)
        
        # Input fields
        input_layout = QVBoxLayout()
        input_layout.setSpacing(20)
        
        # Username/Email field
        self.username_field = ModernInputField("Email or Username")
        input_layout.addWidget(self.username_field.container)
        
        # Password field
        self.password_field = ModernInputField("Password", is_password=True)
        input_layout.addWidget(self.password_field.container)
        
        # Remember me and Forgot password
        options_layout = QHBoxLayout()
        
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: rgba(255, 255, 255, 200);
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid rgba(255, 255, 255, 100);
            }
            QCheckBox::indicator:checked {
                background-color: #0083b0;
                border: 2px solid #0083b0;
            }
        """)
        
        self.forgot_button = QPushButton("Forgot Password?")
        self.forgot_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #00b4db;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #0083b0;
            }
        """)
        self.forgot_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        options_layout.addWidget(self.forgot_button)
        input_layout.addLayout(options_layout)
        
        main_layout.addLayout(input_layout)
        
        # Login button
        self.login_button = AnimatedButton("Sign In")
        self.login_button.setFixedHeight(50)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b4db, stop:1 #0083b0);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00c6ff, stop:1 #0099cc);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0099cc, stop:1 #007399);
            }
        """)
        self.login_button.clicked.connect(self.validate_login)
        main_layout.addWidget(self.login_button)
        
        # Sign up section
        signup_layout = QHBoxLayout()
        signup_layout.setSpacing(5)
        
        signup_label = QLabel("Don't have an account?")
        signup_label.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 14px;")
        
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #00b4db;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #0083b0;
                text-decoration: underline;
            }
        """)
        self.signup_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        signup_layout.addStretch()
        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(self.signup_button)
        signup_layout.addStretch()
        
        main_layout.addLayout(signup_layout)
        
        self.setLayout(main_layout)
    
    def setup_animations(self):
        # Title animation
        self.title_animation = QPropertyAnimation(self.title_label, b"geometry")
        self.title_animation.setDuration(1000)
        self.title_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
    def validate_login(self):
        username = self.username_field.text().strip()
        password = self.password_field.text()
        
        # Clear previous errors
        self.username_field.clear_error()
        self.password_field.clear_error()
        
        # Validate inputs
        if not username:
            self.username_field.set_error("Please enter your email or username")
            return False
        
        if not password:
            self.password_field.set_error("Please enter your password")
            return False
        
        # Simulate login validation
        if self.authenticate_user(username, password):
            self.show_success_message()
            return True
        else:
            self.password_field.set_error("Invalid username or password")
            return False
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Simulate user authentication"""
        # In a real application, this would check against a database
        # For demo purposes, using hardcoded credentials
        demo_credentials = {
            "admin@example.com": "Admin@123",
            "user@example.com": "User@123"
        }
        
        return username in demo_credentials and demo_credentials[username] == password
    
    def show_success_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Login Successful")
        msg.setText("You have successfully logged in!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Customize message box
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        msg.exec()

class SignupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        title_label = GradientLabel("Create Account")
        title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Join our community today")
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 14px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(20)
        
        # Input fields
        self.name_field = ModernInputField("Full Name")
        layout.addWidget(self.name_field.container)
        
        self.email_field = ModernInputField("Email Address")
        layout.addWidget(self.email_field.container)
        
        self.password_field = ModernInputField("Password", is_password=True)
        layout.addWidget(self.password_field.container)
        
        self.confirm_field = ModernInputField("Confirm Password", is_password=True)
        layout.addWidget(self.confirm_field.container)
        
        # Sign up button
        self.signup_button = AnimatedButton("Create Account")
        self.signup_button.setFixedHeight(50)
        self.signup_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b4db, stop:1 #0083b0);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00c6ff, stop:1 #0099cc);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0099cc, stop:1 #007399);
            }
        """)
        self.signup_button.clicked.connect(self.validate_signup)
        layout.addWidget(self.signup_button)
        
        # Back to login
        self.back_button = QPushButton("Already have an account? Sign In")
        self.back_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #00b4db;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #0083b0;
                text-decoration: underline;
            }
        """)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def validate_signup(self):
        # Get input values
        name = self.name_field.text().strip()
        email = self.email_field.text().strip()
        password = self.password_field.text()
        confirm_password = self.confirm_field.text()
        
        # Clear previous errors
        self.name_field.clear_error()
        self.email_field.clear_error()
        self.password_field.clear_error()
        self.confirm_field.clear_error()
        
        # Validate inputs
        valid = True
        
        if not name:
            self.name_field.set_error("Please enter your full name")
            valid = False
        
        if not email:
            self.email_field.set_error("Please enter your email")
            valid = False
        elif not self.is_valid_email(email):
            self.email_field.set_error("Please enter a valid email address")
            valid = False
        
        if not password:
            self.password_field.set_error("Please enter a password")
            valid = False
        elif len(password) < 6:
            self.password_field.set_error("Password must be at least 6 characters")
            valid = False
        
        if password != confirm_password:
            self.confirm_field.set_error("Passwords do not match")
            valid = False
        
        if valid:
            self.show_success_message()
    
    def is_valid_email(self, email):
        """Simple email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def show_success_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Registration Successful")
        msg.setText("Account created successfully!\nYou can now login with your credentials.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        msg.exec()

class ModernLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Login UI")
        self.setFixedSize(450, 600)
        
        # Set window flags for modern look
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create central widget with gradient background
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container with shadow and rounded corners
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f2027, stop:1 #203a43, stop:2 #2c5364);
                border-radius: 20px;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.container.setGraphicsEffect(shadow)
        
        # Stacked widget for multiple pages
        self.stacked_widget = QStackedWidget()
        
        # Create pages
        self.login_page = LoginPage()
        self.signup_page = SignupPage()
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)
        
        # Container layout
        container_layout = QVBoxLayout(self.container)
        container_layout.addWidget(self.stacked_widget)
        
        # Add container to main layout
        main_layout.addWidget(self.container)
        
        # Connect signals
        self.login_page.signup_button.clicked.connect(self.show_signup)
        self.signup_page.back_button.clicked.connect(self.show_login)
        
        # Add window controls
        self.add_window_controls()
    
    def add_window_controls(self):
        # Create title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background: transparent;")
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        # Title
        title_label = QLabel("Modern Login")
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Window controls
        close_button = QPushButton("✕")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 18px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background: rgba(255, 0, 0, 100);
            }
        """)
        close_button.clicked.connect(self.close)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        minimize_button = QPushButton("─")
        minimize_button.setFixedSize(30, 30)
        minimize_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 18px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 50);
            }
        """)
        minimize_button.clicked.connect(self.showMinimized)
        minimize_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        title_layout.addWidget(minimize_button)
        title_layout.addWidget(close_button)
        
        # Add title bar to container layout
        self.container.layout().insertWidget(0, title_bar)
        
        # Make window draggable
        self.draggable = True
        self.old_pos = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.draggable:
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        self.old_pos = None
    
    def show_signup(self):
        self.stacked_widget.setCurrentWidget(self.signup_page)
    
    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

def main():
    load_fonts()
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set palette for dark theme
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 40))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(40, 40, 50))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 60))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(70, 70, 80))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 180, 219))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)
    
    window = ModernLoginWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()