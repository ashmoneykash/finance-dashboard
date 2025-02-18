import React, { useState } from 'react';
import { addExpense } from '../services/api';

const AddExpense = ({ userId }) => {
  const [formData, setFormData] = useState({
    date: '',
    category: '',
    amount: '',
    description: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addExpense({ ...formData, user_id: userId });
    alert('Expense added successfully!');
    setFormData({ date: '', category: '', amount: '', description: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="date"
        value={formData.date}
        onChange={(e) => setFormData({ ...formData, date: e.target.value })}
        required
      />
      <input
        type="text"
        placeholder="Category"
        value={formData.category}
        onChange={(e) => setFormData({ ...formData, category: e.target.value })}
        required
      />
      <input
        type="number"
        placeholder="Amount"
        value={formData.amount}
        onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
        required
      />
      <input
        type="text"
        placeholder="Description"
        value={formData.description}
        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
      />
      <button type="submit">Add Expense</button>
    </form>
  );
};

export default AddExpense;