// Sidebar.js
import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom'; // Импортируем Link для внутренней навигации
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

  return (
    <>
      {/* Контейнер для кнопок (ссылок и кнопки меню) */}
      <ButtonContainer>
        <LinkButton to="/backend/about/">About Us</LinkButton>
        <LinkButton to="/webgl/">VR</LinkButton>
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
        <SearchBar type="text" placeholder="Search..." />

        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly' }}>
          <ul>
            <h2>FILTER</h2>
            <li><Link to="/about/">About us</Link></li>
            <li><Link to="/create/">Create new page</Link></li>
            <li><Link to="/feedback/">Feedback</Link></li>
            <li><Link to="/webgl/">Unity</Link></li>
            <li><Link to="/donation/">Donation</Link></li>
            <li><Link to="/about/">About us</Link></li>
            <h2>Options</h2>
            <li><Link to="/create/">dark mode</Link></li>
          </ul>
          <ul>
            <h2>Index</h2>
            <li><Link to="/graph">Graph</Link></li> {/* Замена ссылки на компонент Link */}
            <li><Link to="/diagram/">Diagram</Link></li>
            <li><Link to="/graph">Graph</Link></li> {/* Замена ссылки на компонент Link */}
            <li><Link to="/diagram/">Diagram</Link></li>
          </ul>
        </div>
      </SidebarContainer>
    </>
  );
};

export default Sidebar;
