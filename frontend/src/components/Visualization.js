import React, { useEffect, useState } from 'react';
import { visualizeExpenses } from '../services/api';

const Visualization = ({ userId }) => {
  const [chartHtml, setChartHtml] = useState('');

  useEffect(() => {
    const fetchVisualization = async () => {
      const data = await visualizeExpenses(userId);
      setChartHtml(data);
    };
    fetchVisualization();
  }, [userId]);

  return <div dangerouslySetInnerHTML={{ __html: chartHtml }} />;
};

export default Visualization;