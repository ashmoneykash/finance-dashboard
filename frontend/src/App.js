import React, { useState } from 'react';
import AddExpense from './components/AddExpense';
import ExpenseList from './components/ExpenseList';
import Visualization from './components/Visualization';

const App = () => {
  const [userId, setUserId] = useState(1); // Hardcoded for now

  return (
    <div>
      <h1>Personal Finance Dashboard</h1>
      <AddExpense userId={userId} />
      <ExpenseList userId={userId} />
      <Visualization userId={userId} />
    </div>
  );
};

export default App;