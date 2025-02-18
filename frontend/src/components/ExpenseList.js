import React, { useEffect, useState } from 'react';
import { getExpenses } from '../services/api';

const ExpenseList = ({ userId }) => {
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    const fetchExpenses = async () => {
      const data = await getExpenses(userId);
      setExpenses(data.expenses);
    };
    fetchExpenses();
  }, [userId]);

  return (
    <div>
      <h2>Expenses</h2>
      <ul>
        {expenses.map((expense) => (
          <li key={expense.id}>
            {expense.date} - {expense.category} - ${expense.amount} - {expense.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ExpenseList;