import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return (
    <div style={{ color: '#fff', background: '#0a0a0a', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <h1>DFC Website — Coming Soon</h1>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
