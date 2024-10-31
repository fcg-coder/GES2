import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Search = ({ setResults }) => {
  const [query, setQuery] = useState('');
  const [results, setLocalResults] = useState([]); // Локальное состояние для результатов
  const [showResults, setShowResults] = useState(false); // Для управления видимостью результатов

  // Используем useEffect для выполнения поиска при каждом изменении запроса
  useEffect(() => {
    const search = async () => {
      if (query.length === 0) {
        setLocalResults([]); // Очищаем результаты, если пустой запрос
        setShowResults(false); // Скрываем результаты
        return;
      }

      setShowResults(true); // Показываем результаты
      setLocalResults([]); // Очищаем старые результаты перед новым запросом

      try {
        const response = await axios.post(`http://localhost:9200/_search`, // Поиск по всем индексам
          {
            "query": {
              "bool": {
                "should": [
                  {
                    "match_phrase_prefix": {
                      "name": {
                        "query": query.toLowerCase(), // Нечувствительность к регистру
                        "slop": 1 // Позволяет некоторую степень вариативности
                      }
                    }
                  },
                  {
                    "match": {
                      "name": {
                        "query": query.toLowerCase(), // Нечувствительность к регистру
                        "fuzziness": "AUTO" // Автоматическая нечеткость
                      }
                    }
                  }
                ]
              }
            }
          },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );

        // Проверяем ответ
        if (response.data && response.data.hits && response.data.hits.hits) {
          const formattedResults = response.data.hits.hits.map(hit => hit._source.name);
          
          // Убираем дублирующиеся результаты
          const uniqueResults = Array.from(new Set(formattedResults));
          
          // Сохраняем уникальные результаты в локальном состоянии и обновляем глобальные результаты
          setLocalResults(uniqueResults);
          setResults(uniqueResults); // Обновляем глобальные результаты
        } else {
          console.warn("Нет результатов поиска:", response.data);
          setShowResults(false); // Скрываем результаты, если нет данных
        }
      } catch (error) {
        console.error("Ошибка при поиске:", error.message);
        if (error.response) {
          console.error("Ответ сервера:", error.response.data);
        }
        setShowResults(false); // Скрываем результаты при ошибке
      }
    };

    const debounceSearch = setTimeout(() => {
      search();
    }, 300); // Дебаунс, чтобы предотвратить слишком частые запросы

    return () => clearTimeout(debounceSearch); // Очищаем таймер при изменении запроса
  }, [query]); // Запускать эффект при изменении query

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search..." 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        className="search-input"
      />
      {showResults && results.length > 0 && ( // Отображаем результаты только если они есть
        <div className="results-container">
          {results.map((result, index) => (
            <div key={index} className="result-item">{result}</div>
          ))}
        </div>
      )}
      <style jsx>{`
        .search-input {
          padding: 10px;
          font-size: 16px;
          border: 1px solid #ccc;
          border-radius: 4px;
          margin-bottom: 10px;
          transition: border-color 0.3s;
        }
        .search-input:focus {
          border-color: #007bff;
          outline: none;
        }
        .results-container {
          display: flex;
          flex-direction: column;
          gap: 10px; /* Отступы между результатами */
          opacity: 1; /* Устанавливаем начальную непрозрачность */
          transition: opacity 0.5s ease; /* Плавное исчезновение */
        }
        .result-item {
          padding: 15px;
          background-color: #2c3e50; /* Темный фон для результата */
          color: white; /* Белый текст */
          border-radius: 5px; /* Закругленные углы */
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); /* Тень для эффекта */
          opacity: 0; /* Начальное состояние - прозрачность */
          animation: fadeIn 0.5s forwards; /* Анимация плавного появления */
        }
        @keyframes fadeIn {
          to {
            opacity: 1; /* Конечное состояние - полная непрозрачность */
          }
        }
      `}</style>
    </div>
  );
};

export default Search;
