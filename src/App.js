import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ArtworkList from './components/ArtworkList';
import ArtworkForm from './components/ArtworkForm';
import ReviewForm from './components/ReviewForm';
import UserProfile from './components/UserProfile';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="App container">
        <div className="container-content">
          <Routes>
            <Route path="/" element={<ArtworkList />} />
            <Route path="/artworks/new" element={<ArtworkForm />} />
            <Route path="/reviews/new" element={<ReviewForm />} />
            <Route path="/profile" element={<UserProfile />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
