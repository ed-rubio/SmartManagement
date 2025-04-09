import Formulario from './routes/pages/Formulario';
import Home from './routes/pages/Home';
import { useState, useEffect } from 'react';
import './CSS/App.css';

function App() {
  // Recuperamos el usuario guardado en localStorage
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('user');
    return savedUser ? [savedUser] : [];
  });

  return (
    <div className="App">
      {
        user.length === 0
        ? <Formulario setUser={setUser} />
        : <Home user={user} setUser={setUser} />
      }
    </div>
  );
}

export default App;
