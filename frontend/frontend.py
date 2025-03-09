import sys
import requests
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, 
    QLineEdit, QTextEdit, QListWidget, QTabWidget, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class FinanceDashboard(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        """Initialize UI with dark mode and better visuals"""
        self.setWindowTitle("💰 Finance Dashboard")
        self.setGeometry(150, 80, 1280, 720)  # 16:9 Aspect Ratio (Larger View)

        # Apply Dark Mode
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-size: 14px; }
            QPushButton { background-color: #1F1F1F; border-radius: 5px; padding: 10px; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #333333; }
            QLineEdit, QTextEdit, QListWidget { background-color: #1E1E1E; border: 1px solid #333; border-radius: 5px; padding: 8px; color: #E0E0E0; }
            QTabWidget::pane { border: 1px solid #333; }
            QTabBar::tab { background: #222; padding: 10px; color: #E0E0E0; }
            QTabBar::tab:selected { background: #333; }
        """)

        layout = QVBoxLayout()

        # **Navigation Tabs**
        self.tabs = QTabWidget(self)
        self.expense_tab = QWidget()
        self.visualization_tab = QWidget()

        self.tabs.addTab(self.expense_tab, "📜 Expenses")
        self.tabs.addTab(self.visualization_tab, "📊 Visualization")

        layout.addWidget(self.tabs)

        # **Initialize Tabs**
        self.initExpenseTab()
        self.initVisualizationTab()

        self.setLayout(layout)

        # **Connect tab switch event**
        self.tabs.currentChanged.connect(self.refreshVisualizationTab)

    def initExpenseTab(self):
        """Setup the Expenses Tab"""
        tab_layout = QVBoxLayout()

        # **Input Fields**
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("💵 Enter amount (₹)")
        tab_layout.addWidget(self.amount_input)

        self.category_input = QLineEdit(self)
        self.category_input.setPlaceholderText("📂 Enter category")
        tab_layout.addWidget(self.category_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("📝 Enter description")
        tab_layout.addWidget(self.description_input)

        # **Buttons (Add & View Expenses)**
        button_layout = QHBoxLayout()

        self.add_expense_btn = QPushButton("✅ Add Expense", self)
        self.add_expense_btn.clicked.connect(self.add_expense)
        button_layout.addWidget(self.add_expense_btn)

        self.view_expenses_btn = QPushButton("📖 View Expenses", self)
        self.view_expenses_btn.clicked.connect(self.view_expenses)
        button_layout.addWidget(self.view_expenses_btn)

        tab_layout.addLayout(button_layout)

        # **Expense List**
        self.expense_list = QListWidget(self)
        tab_layout.addWidget(self.expense_list)

        self.expense_tab.setLayout(tab_layout)

    def initVisualizationTab(self):
        """Setup the Visualization Tab"""
        tab_layout = QVBoxLayout()

        # **Show Pie Chart Button**
        self.visualize_btn = QPushButton("📊 Show Pie Chart in New Window", self)
        self.visualize_btn.clicked.connect(self.show_pie_chart)
        tab_layout.addWidget(self.visualize_btn)

        # **Bar Chart (Directly in Tab)**
        self.bar_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        tab_layout.addWidget(self.bar_canvas)

        self.visualization_tab.setLayout(tab_layout)

    def refreshVisualizationTab(self):
        """Refresh bar chart when switching to the visualization tab"""
        if self.tabs.currentIndex() == 1:  # Check if Visualization tab is active
            self.fetch_and_update_bar_chart()

    def add_expense(self):
        """Send new expense data to backend & clear inputs after submission"""
        url = "http://127.0.0.1:5000/expenses"
        data = {
            "user_id": self.user_id,
            "date": "2024-03-09",
            "category": self.category_input.text().strip(),
            "amount": self.amount_input.text().strip(),
            "description": self.description_input.toPlainText().strip()
        }

        if not data["category"] or not data["amount"]:
            QMessageBox.warning(self, "⚠️ Warning", "Please fill in all required fields!")
            return

        try:
            data["amount"] = float(data["amount"])
        except ValueError:
            QMessageBox.warning(self, "⚠️ Warning", "Amount must be a number!")
            return

        response = requests.post(url, json=data)

        if response.status_code == 201:
            QMessageBox.information(self, "✅ Success", "Expense added successfully!")
            self.amount_input.clear()
            self.category_input.clear()
            self.description_input.clear()
            self.view_expenses()
        else:
            QMessageBox.warning(self, "❌ Error", "Failed to add expense.")

    def view_expenses(self):
        """Fetch and display expenses from backend"""
        url = f"http://127.0.0.1:5000/expenses/{self.user_id}"
        response = requests.get(url)

        if response.status_code == 200:
            self.expense_list.clear()
            expenses = response.json()["expenses"]
            for exp in expenses:
                self.expense_list.addItem(f"📅 {exp['date']} | {exp['category']}: ₹{exp['amount']} \n ✏️ {exp['description']}")
        else:
            QMessageBox.warning(self, "❌ Error", "Failed to fetch expenses.")

    def fetch_and_update_bar_chart(self):
        """Fetch expense data and update bar chart"""
        url = f"http://127.0.0.1:5000/visualize/{self.user_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            categories = data["categories"]
            amounts = data["amounts"]

            # **Update Bar Chart**
            self.bar_canvas.figure.clear()
            ax_bar = self.bar_canvas.figure.add_subplot(111)
            ax_bar.bar(categories, amounts, color=['#4CAF50', '#FF5733', '#FFC300', '#3498DB'])
            ax_bar.set_title("Expense Overview", color='white')
            ax_bar.set_xlabel("Category", color='white')
            ax_bar.set_ylabel("Amount", color='white')
            ax_bar.tick_params(colors='white')
            self.bar_canvas.draw()
        else:
            QMessageBox.warning(self, "❌ Error", "Failed to fetch data.")

    def show_pie_chart(self):
        """Show pie chart in a new window"""
        url = f"http://127.0.0.1:5000/visualize/{self.user_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            categories = data["categories"]
            amounts = data["amounts"]

            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
            ax.set_title("Expense Distribution", color='white')
            plt.show()
        else:
            QMessageBox.warning(self, "❌ Error", "Failed to fetch data.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_id = 1
    dashboard = FinanceDashboard(user_id)
    dashboard.show()
    sys.exit(app.exec_())
