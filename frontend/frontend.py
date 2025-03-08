import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QListWidget,
    QLineEdit, QFormLayout, QDialog, QDialogButtonBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AddExpenseDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Add Expense")

        # Create form layout
        layout = QFormLayout()

        # Add input fields
        self.date_input = QLineEdit()
        self.category_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.description_input = QLineEdit()

        layout.addRow("Date (YYYY-MM-DD):", self.date_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Amount (₹):", self.amount_input)
        layout.addRow("Description:", self.description_input)

        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)
        self.setLayout(layout)

    def get_expense_data(self):
        return {
            "date": self.date_input.text(),
            "category": self.category_input.text(),
            "amount": float(self.amount_input.text()),
            "description": self.description_input.text()
        }


class FinanceDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Finance Dashboard")
        self.setGeometry(100, 100, 800, 600)

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
        self.refresh_button = QPushButton("Refresh Expenses")
        self.refresh_button.clicked.connect(self.fetch_expenses)
        layout.addWidget(self.refresh_button)

        # Add a button to add expenses
        self.add_button = QPushButton("Add Expense")
        self.add_button.clicked.connect(self.open_add_expense_dialog)
        layout.addWidget(self.add_button)

        # Add a chart
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set the layout
        central_widget.setLayout(layout)

    def open_add_expense_dialog(self):
        dialog = AddExpenseDialog()
        if dialog.exec_() == QDialog.Accepted:
            expense_data = dialog.get_expense_data()
            self.add_expense(expense_data)

    def add_expense(self, expense_data):
        try:
            response = requests.post("http://127.0.0.1:5000/expenses", json=expense_data)
            if response.status_code == 201:
                self.fetch_expenses()  # Refresh the expense list
            else:
                self.expense_list.addItem("Failed to add expense.")
        except Exception as e:
            self.expense_list.addItem(f"Error: {str(e)}")

    def fetch_expenses(self):
        # Fetch expenses from the Flask backend
        try:
            response = requests.get("http://127.0.0.1:5000/expenses/1")  # Replace with your API endpoint
            if response.status_code == 200:
                expenses = response.json().get("expenses", [])
                self.expense_list.clear()
                for expense in expenses:
                    self.expense_list.addItem(f"{expense['date']} - {expense['category']} - ₹{expense['amount']}")
                self.plot_expenses(expenses)
            else:
                self.expense_list.addItem("Failed to fetch expenses.")
        except Exception as e:
            self.expense_list.addItem(f"Error: {str(e)}")

    def plot_expenses(self, expenses):
        # Clear the previous plot
        self.figure.clear()

        # Prepare data for the chart
        categories = {}
        for expense in expenses:
            category = expense['category']
            amount = expense['amount']
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        # Create a bar chart
        ax = self.figure.add_subplot(111)
        ax.bar(categories.keys(), categories.values())
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Expenses by Category")

        # Refresh the canvas
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceDashboard()
    window.show()
    sys.exit(app.exec_())