import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTabWidget, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import your main dashboard
# Make sure to update the import path based on your project structure
from frontend import FinanceDashboard

# Dark green aesthetic color palette (copied from your frontend)
DARK_BG = "#0F171A"
PANEL_BG = "#1A2E32"
CARD_BG = "#243B40"
ACCENT_GREEN = "#3EB489"
LIGHT_TEXT = "#E7F6F2"
MID_TEXT = "#A5C9CA"
HIGHLIGHT = "#7FFFD4"

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AshMoneyKash - Login')
        self.setGeometry(100, 100, 480, 600)
        
        # Apply Dark Green Theme (similar to your dashboard)
        self.setStyleSheet(f"""
            QWidget {{ 
                background-color: {DARK_BG}; 
                color: {LIGHT_TEXT}; 
                font-size: 14px; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton {{ 
                background-color: {CARD_BG}; 
                border: none; 
                border-radius: 4px; 
                padding: 12px; 
                color: {LIGHT_TEXT}; 
                font-weight: bold; 
            }}
            QPushButton:hover {{ 
                background-color: {PANEL_BG}; 
                border: 1px solid {ACCENT_GREEN};
            }}
            QPushButton:pressed {{ 
                background-color: {ACCENT_GREEN}; 
                color: {DARK_BG};
            }}
            QLineEdit {{ 
                background-color: {PANEL_BG}; 
                border: 1px solid {CARD_BG}; 
                border-radius: 4px; 
                padding: 10px; 
                color: {LIGHT_TEXT}; 
            }}
            QLineEdit:focus {{ 
                border: 1px solid {ACCENT_GREEN}; 
            }}
            QTabWidget::pane {{ 
                border: none; 
                background-color: {DARK_BG}; 
            }}
            QTabBar::tab {{ 
                background: {PANEL_BG}; 
                padding: 12px 20px; 
                color: {MID_TEXT}; 
                border-top-left-radius: 4px; 
                border-top-right-radius: 4px; 
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{ 
                background: {CARD_BG}; 
                color: {HIGHLIGHT}; 
                border-bottom: 2px solid {ACCENT_GREEN};
            }}
            QFrame#card {{
                background-color: {CARD_BG};
                border-radius: 8px;
                padding: 15px;
            }}
            QLabel#header {{
                font-size: 24px;
                font-weight: bold;
                color: {HIGHLIGHT};
            }}
            QLabel#subheader {{
                font-size: 14px;
                color: {MID_TEXT};
            }}
        """)
        
        main_layout = QVBoxLayout()
        
        # Header with Logo and Title
        header_layout = QHBoxLayout()
        
        logo_label = QLabel("💰")
        logo_label.setStyleSheet(f"font-size: 36px; color: {ACCENT_GREEN};")
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        title_label = QLabel("AshMoneyKash")
        title_label.setObjectName("header")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        main_layout.addLayout(header_layout)
        
        # Green separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(f"background-color: {ACCENT_GREEN}; max-height: 2px;")
        main_layout.addWidget(separator)
        
        subtitle = QLabel("Your Personal Finance Dashboard")
        subtitle.setObjectName("subheader")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        main_layout.addSpacing(20)
        
        # Auth Tabs (Login & Register)
        self.auth_tabs = QTabWidget()
        self.login_tab = QWidget()
        self.register_tab = QWidget()
        
        self.auth_tabs.addTab(self.login_tab, "Login")
        self.auth_tabs.addTab(self.register_tab, "Register")
        
        self.setup_login_tab()
        self.setup_register_tab()
        
        main_layout.addWidget(self.auth_tabs)
        main_layout.addStretch()
        
        # Footer
        footer_label = QLabel("© 2025 AshMoneyKash - All Rights Reserved")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet(f"color: {MID_TEXT}; font-size: 12px;")
        main_layout.addWidget(footer_label)
        
        self.setLayout(main_layout)

    def setup_login_tab(self):
        """Setup the login tab with username and password fields"""
        login_layout = QVBoxLayout()
        login_layout.setContentsMargins(40, 20, 40, 20)
        
        # Login Card
        login_card = QFrame()
        login_card.setObjectName("card")
        card_layout = QVBoxLayout(login_card)
        
        card_layout.addSpacing(10)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setStyleSheet(f"color: {MID_TEXT};")
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.login_username)
        
        card_layout.addSpacing(15)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet(f"color: {MID_TEXT};")
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.login_password)
        
        card_layout.addSpacing(25)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_GREEN};
                color: {DARK_BG};
                font-weight: bold;
                padding: 12px;
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHT};
            }}
        """)
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)
        
        card_layout.addSpacing(10)
        
        login_layout.addWidget(login_card)
        self.login_tab.setLayout(login_layout)

    def setup_register_tab(self):
        """Setup the registration tab with username and password fields"""
        register_layout = QVBoxLayout()
        register_layout.setContentsMargins(40, 20, 40, 20)
        
        # Register Card
        register_card = QFrame()
        register_card.setObjectName("card")
        card_layout = QVBoxLayout(register_card)
        
        card_layout.addSpacing(10)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setStyleSheet(f"color: {MID_TEXT};")
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.register_username)
        
        card_layout.addSpacing(15)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet(f"color: {MID_TEXT};")
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Choose a password")
        self.register_password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.register_password)
        
        card_layout.addSpacing(15)
        
        # Confirm password field
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setStyleSheet(f"color: {MID_TEXT};")
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm your password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(confirm_label)
        card_layout.addWidget(self.confirm_password)
        
        card_layout.addSpacing(25)
        
        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_GREEN};
                color: {DARK_BG};
                font-weight: bold;
                padding: 12px;
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHT};
            }}
        """)
        self.register_button.clicked.connect(self.handle_register)
        card_layout.addWidget(self.register_button)
        
        card_layout.addSpacing(10)
        
        register_layout.addWidget(register_card)
        self.register_tab.setLayout(register_layout)
        
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Warning", "Please enter both username and password")
            return
        
        # Send login request to backend
        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                user_id = data.get("user_id")
                
                # Show success message
                QMessageBox.information(self, "Success", "Login successful!")
                
                # Open the dashboard with the user's ID
                self.open_dashboard(user_id)
            else:
                error_msg = "Invalid username or password"
                if response.json().get("error"):
                    error_msg = response.json().get("error")
                QMessageBox.warning(self, "Login Failed", error_msg)
                
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Connection Error", 
                               "Could not connect to the server. Please check if the backend is running.")
    
    def handle_register(self):
        """Handle registration button click"""
        username = self.register_username.text().strip()
        password = self.register_password.text().strip()
        confirm = self.confirm_password.text().strip()
        
        if not username or not password or not confirm:
            QMessageBox.warning(self, "Warning", "Please fill in all fields")
            return
            
        if password != confirm:
            QMessageBox.warning(self, "Warning", "Passwords do not match")
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "Warning", "Password must be at least 6 characters long")
            return
            
        # Send registration request to backend
        try:
            response = requests.post(
                "http://127.0.0.1:5000/register",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 201:
                QMessageBox.information(
                    self, 
                    "Success", 
                    "Account created successfully! You can now log in."
                )
                # Switch to login tab
                self.auth_tabs.setCurrentIndex(0)
                self.login_username.setText(username)
                self.login_password.clear()
            else:
                error_msg = "Registration failed"
                if response.json().get("message"):
                    error_msg = response.json().get("message")
                QMessageBox.warning(self, "Registration Failed", error_msg)
                
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Connection Error", 
                              "Could not connect to the server. Please check if the backend is running.")
    
    def open_dashboard(self, user_id):
        """Open the finance dashboard with the user's ID"""
        self.dashboard = FinanceDashboard(user_id)
        self.dashboard.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better dark mode support
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec_())