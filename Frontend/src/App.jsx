
import React from 'react';
import { Routes, Route } from 'react-router-dom';

import MainLayout from './layouts/Main';
import Login from './pages/Formulario';
import Home from './pages/Home';
import MathScreen from './pages/MathScreen';
// import Presentation from './pages/Presentation';
// import Info from './pages/Info';
// import Profile from './pages/Profile';
// import Orders from './pages/Orders';


function App() {

    return (
        <Routes>
            <Route path='/login' element={<Login />} />

            <Route path='/' element={<MainLayout />}>
                <Route index element={<Home />} /> {/* Página principal */}

                <Route path='/home' element={<Home />} />
                <Route path='/math' element={<MathScreen />} />
                {/* <Route path='/presentation' element={<Presentation />} /> */}
                {/* <Route path='/info' element={<Info />} /> */}
                {/* <Route path='/profile' element={<Profile />} /> */}
                {/* <Route path='/orders' element={<Orders />} /> */}
            </Route>
        </Routes>
    );
};

export default App;