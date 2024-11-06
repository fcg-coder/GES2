import React, { useState, useRef, useEffect } from 'react';
import { ReactSVG } from 'react-svg';
import iconSrc from './map.svg';
import { getCurrentTheme } from '../themeConfig';
import { ThemeProvider } from 'styled-components';
import styled from 'styled-components';
import Sidebar from './Sidebar';
import Subcategory from './Subcategory';

const MapContainer = styled.div`
  height: 100vh;
  width: 100vw;
  margin: auto;
  overflow: hidden;
  background: ${(props) => props.theme.backgroundColor};
`;

const BackButton = styled.button`
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 15px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
  z-index: 1000;

  &:hover {
    background-color: #0056b3;
  }
`;

const StyledSVGContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  position: relative;
`;

const StyledSVG = styled.svg`
  width: 80%;
  height: 80%;
`;

const StyledCircle = styled.circle`
  fill: white;
  stroke: ${(props) => getColor(props.size)};
  stroke-width: 0.75;

  &:hover {
    fill: wheat;
  }
`;

const getColor = (size) => {
    if (size < 3) return 'red';
    if (size < 6) return 'blue';
    if (size < 9) return 'green';
    return 'yellow';
};

const random = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

const generateRandomData = () => {
    const numPages = random(1, 5);
    return {
        map_internal_pages: Array.from({ length: numPages }, (_, i) => ({
            id: i.toString(),
            size: random(2, 10),
            nextDataUrl: random(0, 1) ? null : `http://localhost:3000/data${i + 2}.json`,
        })),
    };
};

const Map = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [showFullScreen, setShowFullScreen] = useState(false);
    const [currentDataUrl, setCurrentDataUrl] = useState(null);
    const svgRef = useRef(null);
    const theme = getCurrentTheme();

    const handleClick = (event) => {
        const target = event.target;
        const dataUrl = target.getAttribute('data-url');
        if (dataUrl) {
            setCurrentDataUrl(dataUrl); 
            setShowFullScreen(true);
            history.pushState({ dataUrl }, '', window.location.href); // Добавляем состояние
        }
    };

    useEffect(() => {
        const handlePopState = () => {
            setShowFullScreen(false); // Возвращаемся к виду карты
        };
        window.addEventListener('popstate', handlePopState);
        return () => window.removeEventListener('popstate', handlePopState);
    }, []);

    return (
        <ThemeProvider theme={theme}>
            {!showFullScreen ? (
                <MapContainer>
                    <Sidebar open={sidebarOpen} toggleSidebar={(open) => setSidebarOpen(open)} />
                    <ReactSVG
                        src={iconSrc}
                        ref={svgRef}
                        className="svg-icon"
                        beforeInjection={(svg) => {
                            Array.from(svg.querySelectorAll('path')).forEach((path) => {
                                if (path.getAttribute('class') === 'cls-8') {
                                    path.addEventListener('mouseenter', (event) => event.target.style.fill = 'wheat');
                                    path.addEventListener('mouseleave', (event) => event.target.style.fill = '');
                                    path.addEventListener('click', handleClick); 
                                }
                            });
                        }}
                    />
                    <style>{`
            .svg-icon svg {
              transition: transform 0.3s ease-in-out;
              width: 80%;
              height: 90vh;
              margin: 5vh


            }
            .svg-icon path {
              transition: fill 0.2s ease-in-out;
            }
          `}</style>
                </MapContainer>
            ) : (
                <Subcategory initialDataUrl={currentDataUrl} onClose={() => {
                    setShowFullScreen(false); 
                    history.back(); // При закрытии возвращаемся назад
                }} />
            )}
        </ThemeProvider>
    );
};
 
export default Map;
