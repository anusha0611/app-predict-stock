import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4">
      <div className="container mx-auto flex justify-between">
        <h1 className="text-white text-xl">Stock Prediction</h1>
        <div>
          <Link to="/" className="text-white mr-4">Home</Link>
          <Link to="/stocks" className="text-white">Stocks</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
