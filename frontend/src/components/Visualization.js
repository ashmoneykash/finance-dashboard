import React from 'react';

const Visualization = ({ userId }) => {
  return (
    <div>
      <h2>Expense Visualization</h2>
      <iframe
        src={`http://127.0.0.1:5000/visualize/${userId}`}
        width="100%"
        height="500px"
        style={{ border: 'none' }}
      />
    </div>
  );
};

export default Visualization;
