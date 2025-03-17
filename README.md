# **Finance Dashboard**  
📊 **Personal Finance Tracking & Visualization**  

## **📌 Project Overview**  
The **AshmoneyKash Finance Dashboard** is a **Python-based** expense tracking application with **data visualization**. It allows users to **log expenses, track spending habits, and visualize financial trends** using an intuitive **GUI (PyQt5)** and a secure **Flask API**.  

## **✨ Features**  

### 🔐 **User Authentication**  
✔ Secure **Signup & Login** using Flask & SQLAlchemy  
✔ Separate data for each user  

### 💰 **Expense Tracking**  
✔ Add, edit, and delete expenses  
✔ Store **amount, category, date, and description**  
✔ View past expenses in an interactive list  

### 📊 **Data Visualization**  
✔ **Pie Chart & Bar Chart** for spending breakdown  
✔ Identify spending trends over time  

### 🎨 **User-Friendly GUI**  
✔ Modern, **easy-to-use PyQt5** interface  
✔ Smooth navigation with multiple tabs  

---

## **🛠 Tech Stack**  

- **Frontend:** PyQt5 (Desktop GUI)  
- **Backend:** Flask (API)  
- **Database:** SQLite with SQLAlchemy  
- **Data Visualization:** Matplotlib  

---

## **📂 Project Structure**  
```
ashmoneykash-finance-dashboard/
├── README.md
├── backend/
│   ├── app.py            # Flask backend
│   ├── instance/
│   │   └── finance.db    # SQLite database
└── frontend/
    ├── frontend.py       # PyQt5 main dashboard
    ├── login.py          # User authentication
```

---

## **🚀 How to Run the Project**  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/your-username/finance-dashboard.git
cd finance-dashboard
```

### **2️⃣ Set Up the Backend**  
```sh
cd backend
pip install -r requirements.txt
python app.py
```

### **3️⃣ Launch the Frontend**  
```sh
cd frontend
python frontend.py
```

### **4️⃣ Access the Dashboard**  
The PyQt5 app will open, allowing you to **log in and start tracking expenses!**  

---

## **🤝 Contributing**  
Want to enhance this project? Feel free to submit **issues or pull requests**!  

---

## **📜 License**  
This project is licensed under the **MIT License**.  

💡 **Manage your finances smarter – start tracking today!** 🚀  
