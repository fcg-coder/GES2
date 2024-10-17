import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom'; // Импортируем Link для внутренней навигации
import axios from 'axios'; // Импортируем axios для HTTP-запросов
import {
  SidebarContainer,
  MenuButton,
  CloseButton,
  Footer,
  SearchBar,
  ButtonContainer,
  LinkButton
} from './SidebarStyles';

const Sidebar = ({ open, toggleSidebar }) => {
  const sidebarRef = useRef(null);
  const [buttonVisible, setButtonVisible] = useState(true);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (sidebarRef.current && !sidebarRef.current.contains(event.target) && !event.target.closest('button')) {
        toggleSidebar(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [toggleSidebar]);

  useEffect(() => {
    if (open) {
      setButtonVisible(false);
    } else {
      setButtonVisible(true);
    }
  }, [open]);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    try {
      const response = await axios.get(`http://localhost:9200/<имя_индекса>/_search`, {
        headers: {
          'Content-Type': 'application/json'
        },
        data: {
          query: {
            multi_match: {
              query: query,
              fields: ["*"] // Поиск по всем полям
            }
          }
        }
      });
      
      setResults(response.data.hits.hits);
    } catch (error) {
      console.error("Ошибка при поиске:", error);
    }
  };

  return (
    <>
      {/* Контейнер для кнопок (ссылок и кнопки меню) */}
      <ButtonContainer>
        <LinkButton to="/backend/about/">About Us</LinkButton>
        <LinkButton> <a href='/webgl/'> VR </a> </LinkButton>
        <MenuButton visible={buttonVisible} onClick={() => toggleSidebar(true)}>
          MENU
        </MenuButton>
      </ButtonContainer>

      {/* Боковое меню */}
      <SidebarContainer ref={sidebarRef} open={open}>
        {/* Кнопка для закрытия меню внутри меню */}
        <CloseButton onClick={() => toggleSidebar(false)}>
          &times;
        </CloseButton>

        {/* Поисковая строка */}
        <form onSubmit={handleSearch}>
          <SearchBar 
            type="text" 
            placeholder="Search..." 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
          />
          <button type="submit">Поиск</button>
        </form>

        {/* Результаты поиска */}
        {results.length > 0 && (
          <div>
            <h2>Результаты поиска</h2>
            <ul>
              {results.map((result) => (
                <li key={result._id}>{JSON.stringify(result._source)}</li>
              ))}
            </ul>
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly' }}>
          <ul>
            <h2>FILTER</h2>
            <li><Link to="/about/">About us</Link></li>
            <li><Link to="/create/">Create new page</Link></li>
            <li><Link to="/feedback/">Feedback</Link></li>
            <li><a href='/webgl/'> Unity </a> </li>
            <li><Link to="/donation/">Donation</Link></li>
            <li><Link to="/about/">About us</Link></li>
            <h2>Options</h2>
            <li><Link to="/create/">dark mode</Link></li>
          </ul>
          <ul>
            <h2>Index</h2>
            <li><Link to="/graph">Graph</Link></li>
            <li><Link to="/diagram/">Diagram</Link></li>
            <li><Link to="/graph">Graph</Link></li>
            <li><Link to="/diagram/">Diagram</Link></li>
          </ul>
        </div>
      </SidebarContainer>
    </>
  );
};

export default Sidebar;
