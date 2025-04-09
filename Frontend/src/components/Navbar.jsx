
import React from 'react';
import { Link } from 'react-router-dom';

import Logo from '../assets/logo.png'
import '../statics/Navbar.css';


function Navbar() {
  
    return (
        <nav className='main-navbar'>
            <div className='mn-section-one'>
                <img src={Logo} alt='SmartManagement' className='navbar-logo' />
                
                <Link to='/home' className='mn-link'>
                    <p className='mn-link-text'>Inicio</p>
                </Link>
                <Link to='/math' className='mn-link'>
                    <p className='mn-link-text'>Cálculo: EOQ</p>
                </Link>
                <Link to='/math' className='mn-link'>
                    <p className='mn-link-text'>Funcionamiento</p>
                </Link>
                <Link to='/math' className='mn-link'>
                    <p className='mn-link-text'>Nosotros</p>
                </Link>
            </div>

            <div className='mn-section-two'>
                <Link to='/math' className='mn-link'>
                    <p className='mn-link-text'>Mi Perfil</p>
                </Link>
                <Link to='/login' className='mn-link'>
                    <p className='mn-link-text'>Cerrar sesión</p>
                </Link>
            </div>
        </nav>
    );
};

export default Navbar;