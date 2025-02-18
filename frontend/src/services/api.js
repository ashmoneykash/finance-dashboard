import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000'; // Replace with your backend URL

export const addExpense = async (expense) => {
  const response = await axios.post(`${API_BASE_URL}/expenses`, expense);
  return response.data;
};

export const getExpenses = async (userId) => {
  const response = await axios.get(`${API_BASE_URL}/expenses/${userId}`);
  return response.data;
};

export const visualizeExpenses = async (userId) => {
  const response = await axios.get(`${API_BASE_URL}/visualize/${userId}`);
  return response.data;
};