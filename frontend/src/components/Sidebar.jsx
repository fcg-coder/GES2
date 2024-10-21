// Sidebar.js
import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
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
    setButtonVisible(!open);
  }, [open]);

  return (
    <>
      <ButtonContainer>
        <LinkButton to="/backend/about/">About Us</LinkButton>
        <LinkButton><a href='/webgl/'> VR </a></LinkButton>
        <MenuButton visible={buttonVisible} onClick={() => toggleSidebar(true)}>
          MENU
        </MenuButton>
      </ButtonContainer>

      <SidebarContainer ref={sidebarRef} open={open}>
   

        <Search setResults={setResults} /> {/* Встраиваем компонент поиска */}

        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly' }}>
          <ul>
            <h2>FILTER</h2>
            <li><Link to="/about/">About us</Link></li>
            <li><Link to="/create/">Create new page</Link></li>
            <li><Link to="/feedback/">Feedback</Link></li>
            <li><a href='/webgl/'> Unity </a></li>
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
