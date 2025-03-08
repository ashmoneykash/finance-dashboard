import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QListWidget

class FinanceDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Finance Dashboard")
        self.setGeometry(100, 100, 600, 400)

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Add a label
        self.label = QLabel("Expenses:")
        layout.addWidget(self.label)

        # Add a list to display expenses
        self.expense_list = QListWidget()
        layout.addWidget(self.expense_list)

        # Add a button to refresh expenses
        self.button = QPushButton("Refresh Expenses")
        self.button.clicked.connect(self.fetch_expenses)
        layout.addWidget(self.button)

        # Set the layout
        central_widget.setLayout(layout)

    def fetch_expenses(self):
        # Fetch expenses from the Flask backend
        try:
            response = requests.get("http://127.0.0.1:5000/expenses/1")  # Replace with your API endpoint
            if response.status_code == 200:
                expenses = response.json().get("expenses", [])
                self.expense_list.clear()
                for expense in expenses:
                    self.expense_list.addItem(f"{expense['date']} - {expense['category']} - ₹{expense['amount']}")
            else:
                self.expense_list.addItem("Failed to fetch expenses.")
        except Exception as e:
            self.expense_list.addItem(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceDashboard()
    window.show()
    sys.exit(app.exec_())