import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <h1>Art Gallery Marketplace</h1>
      <ul className="nav-links">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/artworks/new">Add Artwork</Link>
        </li>
        <li>
          <Link to="/reviews/new">Leave a Review</Link>
        </li>
        <li>
          <Link to="/profile">User Profile</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;