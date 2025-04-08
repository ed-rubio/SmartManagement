import React from 'react';
import { Outlet } from 'react-router-dom';

import Navbar from './components/UI/navbar';

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

export default App
