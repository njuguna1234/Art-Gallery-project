import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ArtworkList from './componets/ArtworkList';
import ArtworkForm from './componets/ArtworkForm';
import ReviewForm from './componets/ReviewForm';
import UserProfile from './componets/UserProfile';
import Navbar from './componets/Navbar';


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
