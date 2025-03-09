import sys
import requests
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, 
    QLineEdit, QTextEdit, QListWidget, QTabWidget, QHBoxLayout, QGridLayout,
    QComboBox, QDateEdit, QFrame, QSplitter, QSizePolicy
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl

# Set matplotlib style for dark theme
plt.style.use('dark_background')
mpl.rcParams['axes.edgecolor'] = '#2C3639'
mpl.rcParams['axes.labelcolor'] = '#A5C9CA'
mpl.rcParams['xtick.color'] = '#A5C9CA'
mpl.rcParams['ytick.color'] = '#A5C9CA'

# Dark green aesthetic color palette
DARK_BG = "#0F171A"
PANEL_BG = "#1A2E32"
CARD_BG = "#243B40"
ACCENT_GREEN = "#3EB489"
LIGHT_TEXT = "#E7F6F2"
MID_TEXT = "#A5C9CA"
HIGHLIGHT = "#7FFFD4"

# Chart colors - shades of green and teal
COLORS = ['#3EB489', '#2E8B57', '#20B2AA', '#008080', '#5F9EA0', '#40E0D0']

class FinanceDashboard(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
        self.initUI()

    def initUI(self):
        """Initialize UI with dark green aesthetic"""
        self.setWindowTitle("Finance Dashboard")
        self.setGeometry(150, 80, 1280, 720)  # 16:9 Aspect Ratio

        # Apply Dark Green Theme
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
            QLineEdit, QTextEdit, QListWidget, QComboBox, QDateEdit {{ 
                background-color: {PANEL_BG}; 
                border: 1px solid {CARD_BG}; 
                border-radius: 4px; 
                padding: 10px; 
                color: {LIGHT_TEXT}; 
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{ 
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
            QListWidget {{ 
                background-color: {PANEL_BG}; 
                alternate-background-color: {CARD_BG};
                border-radius: 4px;
                padding: 5px;
                border: 1px solid {CARD_BG};
            }}
            QListWidget::item {{ 
                padding: 10px; 
                border-bottom: 1px solid {CARD_BG};
            }}
            QListWidget::item:selected {{ 
                background-color: {ACCENT_GREEN}; 
                color: {DARK_BG};
            }}
            QFrame#card {{
                background-color: {CARD_BG};
                border-radius: 8px;
                padding: 15px;
            }}
            QLabel#header {{
                font-size: 18px;
                font-weight: bold;
                color: {HIGHLIGHT};
            }}
            QLabel#subheader {{
                font-size: 14px;
                color: {MID_TEXT};
            }}
            QComboBox {{
                background-color: {PANEL_BG};
                selection-background-color: {ACCENT_GREEN};
                selection-color: {DARK_BG};
            }}
            QComboBox QAbstractItemView {{
                background-color: {PANEL_BG};
                selection-background-color: {ACCENT_GREEN};
                selection-color: {DARK_BG};
            }}
            QDateEdit::drop-down {{
                background-color: {PANEL_BG};
            }}
        """)

        main_layout = QVBoxLayout()
        
        # Header with Icon and Title
        header_layout = QHBoxLayout()
        
        # Logo area with emoji
        logo_label = QLabel("💰")
        logo_label.setStyleSheet(f"font-size: 28px; color: {ACCENT_GREEN};")
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(logo_label)
        
        title_label = QLabel("Finance Dashboard")
        title_label.setObjectName("header")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        date_label = QLabel(QDate.currentDate().toString("dddd, MMMM d, yyyy"))
        date_label.setObjectName("subheader")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header_layout.addWidget(date_label)
        
        main_layout.addLayout(header_layout)
        
        # Green separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(f"background-color: {ACCENT_GREEN}; max-height: 1px;")
        main_layout.addWidget(separator)
        
        # Navigation Tabs
        self.tabs = QTabWidget(self)
        self.expense_tab = QWidget()
        self.visualization_tab = QWidget()

        self.tabs.addTab(self.expense_tab, "📝 Expenses")
        self.tabs.addTab(self.visualization_tab, "📊 Insights")

        main_layout.addWidget(self.tabs)

        # Initialize Tabs
        self.initExpenseTab()
        self.initVisualizationTab()

        self.setLayout(main_layout)

        # Connect tab switch event
        self.tabs.currentChanged.connect(self.refreshVisualizationTab)

    def initExpenseTab(self):
        """Setup the Expenses Tab with dark green aesthetic"""
        tab_layout = QVBoxLayout()
        
        # Split the expense tab into left and right panels
        expense_splitter = QSplitter(Qt.Horizontal)
        
        # LEFT PANEL: Form Card
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        form_card = QFrame(self)
        form_card.setObjectName("card")
        form_layout = QVBoxLayout(form_card)
        
        # Add a green line at the top of the card
        card_header_line = QFrame()
        card_header_line.setFrameShape(QFrame.HLine)
        card_header_line.setStyleSheet(f"background-color: {ACCENT_GREEN}; max-height: 2px;")
        form_layout.addWidget(card_header_line)
        
        form_header = QLabel("Add New Expense")
        form_header.setObjectName("header")
        form_layout.addWidget(form_header)
        
        # Date input
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        date_label.setStyleSheet(f"color: {MID_TEXT};")
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        form_layout.addLayout(date_layout)
        
        # Amount input with currency symbol
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet(f"color: {MID_TEXT};")
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount")
        currency_label = QLabel("₹")
        currency_label.setStyleSheet(f"color: {ACCENT_GREEN}; font-weight: bold;")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        amount_layout.addWidget(currency_label)
        form_layout.addLayout(amount_layout)

        # Category dropdown
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        category_label.setStyleSheet(f"color: {MID_TEXT};")
        self.category_input = QComboBox(self)
        self.category_input.addItems(self.categories)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_input)
        form_layout.addLayout(category_layout)

        # Description input
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Description:")
        desc_label.setStyleSheet(f"color: {MID_TEXT};")
        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Enter details about this expense")
        self.description_input.setMaximumHeight(80)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.description_input)
        form_layout.addLayout(desc_layout)

        # Add Expense Button
        self.add_expense_btn = QPushButton("Add Expense", self)
        self.add_expense_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_GREEN};
                color: {DARK_BG};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHT};
            }}
        """)
        self.add_expense_btn.clicked.connect(self.add_expense)
        form_layout.addWidget(self.add_expense_btn)
        
        left_layout.addWidget(form_card)
        left_layout.addStretch()
        
        # RIGHT PANEL: Expenses List
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        list_card = QFrame(self)
        list_card.setObjectName("card")
        list_layout = QVBoxLayout(list_card)
        
        # Add a green line at the top of the card
        list_header_line = QFrame()
        list_header_line.setFrameShape(QFrame.HLine)
        list_header_line.setStyleSheet(f"background-color: {ACCENT_GREEN}; max-height: 2px;")
        list_layout.addWidget(list_header_line)
        
        list_header_layout = QHBoxLayout()
        list_header = QLabel("Recent Expenses")
        list_header.setObjectName("header")
        list_header_layout.addWidget(list_header)
        
        self.view_expenses_btn = QPushButton("Refresh", self)
        self.view_expenses_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.view_expenses_btn.clicked.connect(self.view_expenses)
        self.view_expenses_btn.setMaximumWidth(120)
        list_header_layout.addWidget(self.view_expenses_btn)
        
        list_layout.addLayout(list_header_layout)
        
        # Expense List with better formatting
        self.expense_list = QListWidget(self)
        self.expense_list.setAlternatingRowColors(True)
        list_layout.addWidget(self.expense_list)
        
        right_layout.addWidget(list_card)
        
        # Add panels to splitter
        expense_splitter.addWidget(left_panel)
        expense_splitter.addWidget(right_panel)
        expense_splitter.setSizes([400, 600])  # Set initial sizes
        
        tab_layout.addWidget(expense_splitter)
        self.expense_tab.setLayout(tab_layout)
        
        # Initialize with existing expenses
        self.view_expenses()

    def initVisualizationTab(self):
        """Setup the Visualization Tab with dark green aesthetic"""
        tab_layout = QVBoxLayout()
        
        # Top header with title
        viz_header_layout = QHBoxLayout()
        viz_header = QLabel("Expense Analysis")
        viz_header.setObjectName("header")
        viz_header_layout.addWidget(viz_header)
        
        refresh_viz_btn = QPushButton("Refresh Analysis", self)
        refresh_viz_btn.setMaximumWidth(150)
        refresh_viz_btn.clicked.connect(self.refresh_visualizations)
        viz_header_layout.addWidget(refresh_viz_btn)
        
        tab_layout.addLayout(viz_header_layout)
        
        # Green separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(f"background-color: {ACCENT_GREEN}; max-height: 1px;")
        tab_layout.addWidget(separator)
        
        # Split view for charts
        charts_splitter = QSplitter(Qt.Horizontal)
        
        # Pie Chart Card
        pie_card = QFrame()
        pie_card.setObjectName("card")
        pie_layout = QVBoxLayout(pie_card)
        
        pie_header = QLabel("Expense Distribution")
        pie_header.setObjectName("subheader")
        pie_header.setAlignment(Qt.AlignCenter)
        pie_layout.addWidget(pie_header)
        
        self.pie_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        self.pie_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pie_canvas.figure.patch.set_facecolor(CARD_BG)
        pie_layout.addWidget(self.pie_canvas)
        
        charts_splitter.addWidget(pie_card)
        
        # Bar Chart Card
        bar_card = QFrame()
        bar_card.setObjectName("card")
        bar_layout = QVBoxLayout(bar_card)
        
        bar_header = QLabel("Category Comparison")
        bar_header.setObjectName("subheader")
        bar_header.setAlignment(Qt.AlignCenter)
        bar_layout.addWidget(bar_header)
        
        self.bar_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        self.bar_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bar_canvas.figure.patch.set_facecolor(CARD_BG)
        bar_layout.addWidget(self.bar_canvas)
        
        charts_splitter.addWidget(bar_card)
        
        tab_layout.addWidget(charts_splitter)

        self.visualization_tab.setLayout(tab_layout)

    def refreshVisualizationTab(self):
        """Refresh visualizations when switching to the visualization tab"""
        if self.tabs.currentIndex() == 1:  # Check if Visualization tab is active
            self.refresh_visualizations()

    def refresh_visualizations(self):
        """Update both charts with the latest data"""
        self.fetch_and_update_charts()

    def add_expense(self):
        """Send new expense data to backend & clear inputs after submission"""
        url = "http://127.0.0.1:5000/expenses"
        data = {
            "user_id": self.user_id,
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "category": self.category_input.currentText(),
            "amount": self.amount_input.text().strip(),
            "description": self.description_input.toPlainText().strip()
        }

        if not data["amount"]:
            QMessageBox.warning(self, "Warning", "Please enter an amount for your expense")
            return

        try:
            data["amount"] = float(data["amount"])
        except ValueError:
            QMessageBox.warning(self, "Warning", "Amount must be a valid number")
            return

        try:
            response = requests.post(url, json=data)

            if response.status_code == 201:
                self.amount_input.clear()
                self.date_input.setDate(QDate.currentDate())
                self.description_input.clear()
                self.view_expenses()
                QMessageBox.information(self, "Success", "Expense added successfully")
            else:
                QMessageBox.warning(self, "Error", f"Failed to add expense: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", "Could not connect to the server. Please check if the backend is running.")

    def view_expenses(self):
        """Fetch and display expenses from backend with improved formatting"""
        try:
            url = f"http://127.0.0.1:5000/expenses/{self.user_id}"
            response = requests.get(url)

            if response.status_code == 200:
                self.expense_list.clear()
                expenses = response.json()["expenses"]
                
                # Sort expenses by date (newest first)
                expenses.sort(key=lambda x: x['date'], reverse=True)
                
                for exp in expenses:
                    # Format the amount with commas for thousands
                    formatted_amount = f"₹{float(exp['amount']):,.2f}"
                    
                    # Create a more visually appealing list item
                    self.expense_list.addItem(
                        f"{exp['date']} | {exp['category']} | {formatted_amount}\n"
                        f"Description: {exp['description']}"
                    )
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch expenses")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Connection Error", "Could not connect to the server. Please check if the backend is running.")

    def fetch_and_update_charts(self):
        """Fetch expense data and update both charts with dark green styling"""
        try:
            url = f"http://127.0.0.1:5000/visualize/{self.user_id}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                categories = data["categories"]
                amounts = data["amounts"]

                # Update Pie Chart with green aesthetic
                self.pie_canvas.figure.clear()
                ax_pie = self.pie_canvas.figure.add_subplot(111)
                ax_pie.set_facecolor(CARD_BG)
                
                wedges, texts, autotexts = ax_pie.pie(
                    amounts, 
                    labels=None,  # We'll add a legend instead
                    autopct='%1.1f%%', 
                    startangle=90, 
                    colors=COLORS[:len(categories)],
                    wedgeprops={'width': 0.6, 'edgecolor': DARK_BG, 'linewidth': 1}
                )
                
                # Make percentage text visible on dark background
                for autotext in autotexts:
                    autotext.set_color(LIGHT_TEXT)
                    autotext.set_fontweight('bold')
                
                # Add a legend with green styling
                legend = ax_pie.legend(
                    wedges, 
                    categories,
                    title="Categories",
                    loc="center left",
                    bbox_to_anchor=(0.9, 0, 0.5, 1)
                )
                legend.get_title().set_color(LIGHT_TEXT)
                for text in legend.get_texts():
                    text.set_color(MID_TEXT)
                
                ax_pie.set_title("Expense Distribution", color=HIGHLIGHT, fontsize=14)
                self.pie_canvas.figure.tight_layout()
                self.pie_canvas.draw()

                # Update Bar Chart with green aesthetic
                self.bar_canvas.figure.clear()
                ax_bar = self.bar_canvas.figure.add_subplot(111)
                ax_bar.set_facecolor(CARD_BG)
                
                bars = ax_bar.bar(
                    categories, 
                    amounts, 
                    color=COLORS[:len(categories)],
                    width=0.6,
                    edgecolor=DARK_BG,
                    linewidth=1
                )
                
                # Add value labels on top of bars
                for bar in bars:
                    height = bar.get_height()
                    ax_bar.text(
                        bar.get_x() + bar.get_width()/2.,
                        height + 5,
                        f'₹{int(height):,}',
                        ha='center', 
                        va='bottom',
                        color=HIGHLIGHT
                    )
                
                # Style the bar chart with green theme
                ax_bar.set_title("Expense by Category", color=HIGHLIGHT, fontsize=14)
                ax_bar.set_xlabel("Category", color=MID_TEXT)
                ax_bar.set_ylabel("Amount (₹)", color=MID_TEXT)
                ax_bar.tick_params(colors=MID_TEXT)
                ax_bar.grid(axis='y', linestyle='--', alpha=0.3, color=PANEL_BG)
                ax_bar.spines['top'].set_visible(False)
                ax_bar.spines['right'].set_visible(False)
                ax_bar.spines['bottom'].set_color(PANEL_BG)
                ax_bar.spines['left'].set_color(PANEL_BG)
                
                self.bar_canvas.figure.tight_layout()
                self.bar_canvas.draw()
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch visualization data")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Connection Error", "Could not connect to the server. Please check if the backend is running.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better dark mode support
    user_id = 1
    dashboard = FinanceDashboard(user_id)
    dashboard.show()
    sys.exit(app.exec_())