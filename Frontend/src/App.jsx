
import './CSS/App.css';
import Navbar from './components/UI/navbar';
import { Outlet } from 'react-router-dom';

function App() {
  return (
    <>
    <Navbar />
    <main>
      <Outlet />
    </main>
    </>

  )
}

export default App;
