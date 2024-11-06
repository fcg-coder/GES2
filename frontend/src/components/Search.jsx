import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Search = ({ setResults }) => {
  const [query, setQuery] = useState('');
  const [results, setLocalResults] = useState([]);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    const search = async () => {
      if (query.length === 0) {
        setLocalResults([]);
        setShowResults(false);
        return;
      }

      setShowResults(true);
      setLocalResults([]);

      try {
        const response = await axios.post(`http://localhost:9200/_search`, {
          query: {
            bool: {
              should: [
                {
                  match_phrase_prefix: {
                    name: {
                      query: query.toLowerCase(),
                      slop: 1
                    }
                  }
                },
                {
                  match: {
                    name: {
                      query: query.toLowerCase(),
                      fuzziness: "AUTO"
                    }
                  }
                }
              ]
            }
          }
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.data && response.data.hits && response.data.hits.hits) {
          const formattedResults = response.data.hits.hits.map(hit => hit._source.name);
          const uniqueResults = Array.from(new Set(formattedResults));
          setLocalResults(uniqueResults);
          setResults(uniqueResults);
        } else {
          console.warn("Нет результатов поиска:", response.data);
          setShowResults(false);
        }
      } catch (error) {
        console.error("Ошибка при поиске:", error.message);
        if (error.response) {
          console.error("Ответ сервера:", error.response.data);
        }
        setShowResults(false);
      }
    };

    const debounceSearch = setTimeout(() => {
      search();
    }, 300);

    return () => clearTimeout(debounceSearch);
  }, [query, setResults]);

  return (
    <div>
      <svg width="400" height="80" viewBox="0 0 400 80" xmlns="http://www.w3.org/2000/svg" style={{ cursor: 'text' }}>
        {/* Фон поиска */}
        <rect x="20" y="20" width="360" height="40" rx="20" fill="none" stroke="white" strokeWidth="2" />

        {/* Иконка лупы */}
        <circle cx="50" cy="40" r="10" stroke="white" strokeWidth="2" fill="none" />
        <line x1="57" y1="47" x2="65" y2="55" stroke="white" strokeWidth="2" />

        {/* Поле ввода */}
        <foreignObject x="70" y="25" width="300" height="30">
          <input
            type="text"
            placeholder="Search..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{
              width: '100%',
              height: '100%',
              fontSize: '16px',
              border: 'none',
              outline: 'none',
              background: 'transparent',
              color: 'white'
            }}
          />
        </foreignObject>
      </svg>

      {showResults && results.length > 0 && (
        <div className="results-container">
          {results.map((result, index) => (
            <div key={index} className="result-item">{result}</div>
          ))}
        </div>
      )}

      <style jsx>{`
        .results-container {
          display: flex;
          flex-direction: column;
          gap: 10px;
          opacity: 1;
          transition: opacity 0.5s ease;
          padding-top: 10px;
        }
        .result-item {
          padding: 10px 15px;
          background-color: #333;
          color: white;
          border-radius: 5px;
          font-size: 14px;
          cursor: pointer;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
          transition: background-color 0.3s ease;
          background: none;
        }
        .result-item:hover {
          background-color: #444;
        }
      `}</style>
    </div>
  );
};

export default Search;
