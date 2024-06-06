import React from "react";
import {Navbar, NavbarBrand, NavbarCollapse, NavbarLink, NavbarToggle} from "flowbite-react";
import {Link, useLocation} from "react-router-dom";

const Header = () => {
    const location = useLocation()

    const isActive = (href:string) => {
        return location.pathname === href;

    }

    return (
        <Navbar fluid rounded>
            <NavbarBrand as={Link} to="/">
                <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">WS</span>
            </NavbarBrand>
            <NavbarToggle />
            <NavbarCollapse>
                <NavbarLink as={Link} to="/scans/initiate" active={isActive("/scans/initiate")}>
                    Initiate New Scan
                </NavbarLink>
                <NavbarLink as={Link} to="/scans/list" active={isActive("/scans/list")}>
                    View Scans
                </NavbarLink>
            </NavbarCollapse>
        </Navbar>
    );
}

export default Header