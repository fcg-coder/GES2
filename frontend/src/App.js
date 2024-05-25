import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [pages, setPages] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchPages() {
      try {
        const response = await axios.get('/backend/');
        // Проверяем, что response.data.pages является массивом
        if (Array.isArray(response.data.pages)) {
          setPages(response.data.pages);
        } else {
          // Если это не массив, устанавливаем pages как пустой массив
          setPages([]);
          setError('Data is not an array');
        }
      } catch (error) {
        console.error('Error fetching pages:', error);
        setError('Failed to fetch pages');
      }
    }

    fetchPages();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="intro">
      {pages.length > 0 ? (
        pages.map((page) => (
          <a key={page.id} href={`/pages/${page.id}`}>
            <canvas className="canvas" data-radius={page.size}>{page.nameOfPage}</canvas>
          </a>
        ))
      ) : (
        <div>No pages available</div>
      )}
      <div className="footer">
        <ul>INFORMATION
          <li>
            <a href="/about">About us</a>
          </li>
          <li>
            <a href="/create">Create new page</a>
          </li>
          <li>
            <a href="/feedback">Feedback</a>
          </li>
          <li>
            <a href="/webgl">Unity</a>
          </li>
          <li>
            <a href="/donation">Donation</a>
          </li>
        </ul>
        <ul>ALTERNATIVE VIEW
          <li>
            <a href="/graph">Graph</a>
          </li>
          <li>
            <a href="/diagram">Diagram</a>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default App;
