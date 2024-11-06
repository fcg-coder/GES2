import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios'; // Импортируем axios для запроса
import {
  SidebarContainer,
  MenuButton,
  CloseButton,
  ButtonContainer,
  LinkButton
} from './SidebarStyles';
import Search from './Search'; // Импортируем компонент поиска

const Sidebar = ({ open, toggleSidebar }) => {
  const sidebarRef = useRef(null);
  const [buttonVisible, setButtonVisible] = useState(true);
  const [pagesCount, setPagesCount] = useState(0); // Отдельное состояние для страниц
  const [categoriesCount, setCategoriesCount] = useState(0); // Отдельное состояние для категорий

  // Асинхронная функция для получения количества записей в Elasticsearch
  const fetchDataCount = async () => {
    try {
      const responseOfPages = await axios.post('http://localhost:9200/pages/_count');
      const responseOfCategories = await axios.post('http://localhost:9200/categories/_count');
      setPagesCount(responseOfPages.data.count);
      setCategoriesCount(responseOfCategories.data.count);
    } catch (error) {
      console.error("Ошибка при поиске:", error.message);
      if (error.response) {
        console.error("Ответ сервера:", error.response.data);
      }
      setPagesCount(0);
      setCategoriesCount(0);
    }
  };

  useEffect(() => {
    fetchDataCount();
  }, []);

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
    setButtonVisible(!open);
  }, [open]);

  return (
    <>
      <ButtonContainer>
        <LinkButton to="/backend/about/">About Us</LinkButton>
        <LinkButton>
          <a href='/webgl/'> VR </a>
        </LinkButton>
        <MenuButton visible={buttonVisible} onClick={() => toggleSidebar(true)}>
          MENU
        </MenuButton>
      </ButtonContainer>

      <SidebarContainer ref={sidebarRef} open={open}>
        <Search setResults={setPagesCount} /> {/* Встраиваем компонент поиска */}
        <div className="content-container">
          <div className="filters" style={{ marginBottom: '20px', width: '50%' }}>
            <h2 className="section-title">FILTERS</h2>
            <ul className="links-list">
              <li><Link to="/">HUDS</Link></li>
              <li><Link to="/">MODRPC</Link></li>
              <li><Link to="/">SOCIAL MMOs</Link></li>
              <li><Link to="/">HISTORICAL MMOs</Link></li>
              <li><Link to="/">SANDBOXES</Link></li>
              <li><Link to="/">ART PROJECTS MMOs</Link></li>
            </ul>
          </div>

          <div className="index" style={{ marginBottom: '20px', width: '50%' }}>
            <h2 className="section-title">INDEX</h2>
            <ul className="links-list">
              <li><Link to="/">2MOONS</Link></li>
              <li><Link to="/">2023 Online</Link></li>
              <li><Link to="/">3D Nature</Link></li>
              <li><Link to="/">Art Museum</Link></li>
              <li><Link to="/">SB Universe</Link></li>
            </ul>
          </div>

          <div className="options" style={{ width: '50%' }}>
            <h2 className="section-title">OPTIONS</h2>
            <ul className="links-list">
              <li><Link to="/">DARK MODE</Link></li>
            </ul>
          </div>
        </div>

        <style jsx>{`
  .content-container {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    color: white;
  }
  
  .section-title {
    font-size: 22px;
    font-weight: normal;
    color: white;
  }

  .links-list {
    list-style-type: none;
    padding: 0;
    line-height: 1.8em;
  }

  .links-list li a {
    color: white;
    text-decoration: none;
    transition: color 0.3s ease;
  }

  .links-list li a:hover {
    color: #ddd;
  }

  .filters, .index, .options {
    width: 50%;
    margin-bottom: 20px;
  }
`}</style>


        {/* Отображаем количество результатов, если они получены */}
        {pagesCount > 0 && categoriesCount > 0 && (
          <div style={{ padding: '10px', textAlign: 'center', color: 'white' }}>
            <p>Total virtual worlds: {pagesCount} in {categoriesCount} categories</p>
          </div>
        )}
      </SidebarContainer>
    </>
  );
};

export default Sidebar;
