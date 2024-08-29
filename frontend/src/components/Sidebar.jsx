// Sidebar.js
import React, { useEffect, useRef, useState } from 'react';
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
        <LinkButton href="/backend/about/">About Us</LinkButton>
        <LinkButton href="/webgl/">VR</LinkButton>
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
            <li><a href="/backend/about/">About us</a></li>
            <li><a href="/backend/create/">Create new page</a></li>
            <li><a href="/backend/feedback/">Feedback</a></li>
            <li><a href="/webgl/">Unity</a></li>
            <li><a href="/backend/donation/">Donation</a></li>
            <li><a href="/backend/about/">About us</a></li>
            <h2>Options</h2>
            <li><a href="/backend/create/">dark mode</a></li>
          </ul>
          <ul>
            <h2>Index</h2>
            <li><a href="/backend/graph/">Graph</a></li>
            <li><a href="/backend/diagram/">Diagram</a></li>
            <li><a href="/backend/graph/">Graph</a></li>
            <li><a href="/backend/diagram/">Diagram</a></li>
          </ul>
        </div>
      </SidebarContainer>
    </>
  );
};

export default Sidebar;
