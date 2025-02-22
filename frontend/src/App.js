import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import AddExpense from './components/AddExpense';
import ExpenseList from './components/ExpenseList';
import Visualization from './components/Visualization';
import './App.css';

const App = () => {
  const [userId, setUserId] = useState(null); // Track the logged-in user

  return (
    <Router>
      <div className="App">
        <h1>Personal Finance Dashboard</h1>
        <Routes>
          <Route
            path="/login"
            element={userId ? <Navigate to="/" /> : <Login setUserId={setUserId} />}
          />
          <Route
            path="/register"
            element={userId ? <Navigate to="/" /> : <Register setUserId={setUserId} />}
          />
          <Route
            path="/"
            element={
              userId ? (
                <>
                  <AddExpense userId={userId} />
                  <ExpenseList userId={userId} />
                  <Visualization userId={userId} />
                </>
              ) : (
                <Navigate to="/login" />
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;