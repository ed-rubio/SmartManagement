import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
return (
    <div className="fixed top-0 left-0 w-full">
        <nav className="w-full bg-Navbar z-50 p-4 align-top shadow-md">
            <div className="container flex justify-between items-center">
                {/* Logo */}
                <div className="text-white text-lg font-bold">
                    <Link to="/">SmartManagement</Link>
                </div>

                {/* Navigation Links */}
                <div className="flex space-x-4">
                    <Link to="/EoqPage" className="text-white hover:text-gray-200">
                        Eoq
                    </Link>
                </div>
            </div>
        </nav>
    </div>
);
};

export default Navbar;