import React from 'react';
import { NavLink } from "react-router-dom";

const Header = () => {
    return (
        <div>
            <nav>
                        <NavLink
                            to="/"
                        >
                            Home
                        </NavLink>
                        {" | "} 
                    {/* <li>
                        <NavLink
                            to="time"
                        >
                            Time
                        </NavLink>
                    </li> */}
                    
                        <NavLink
                            to="search"
                        >
                            Search
                        </NavLink>
                        {" | "} 
                        <NavLink
                            to="/email"
                        >
                            Email
                        </NavLink>

            </nav>


        </div>
    );
};

export default Header;