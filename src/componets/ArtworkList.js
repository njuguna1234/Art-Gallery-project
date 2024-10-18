import React, { useEffect, useState } from 'react';

function ArtworkList() {
  const [artworks, setArtworks] = useState([]);

  useEffect(() => {
    fetch('/api/artworks')
      .then((res) => res.json())
      .then((data) => setArtworks(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h1>Artworks</h1>
      <div className="artwork-list">
        {artworks.map((artwork) => (
          <div key={artwork.id} className="artwork">
            <h2>{artwork.title}</h2>
            <p>{artwork.description}</p>
            <p>Price: ${artwork.price}</p>
            <button>Purchase</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ArtworkList;