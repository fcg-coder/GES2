import React, { useState, useRef, useEffect } from 'react';
import { ReactSVG } from 'react-svg';
import iconSrc from './map.svg';
import { getCurrentTheme } from '../themeConfig';
import { ThemeProvider } from 'styled-components';
import styled from 'styled-components';
import Sidebar from './Sidebar';

// Создаем стилизованный компонент MapContainer с использованием styled-components
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

const YourComponent = ({ initialDataUrl }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [history, setHistory] = useState([]);
    const [isMapView, setIsMapView] = useState(true);

    const loadData = (dataUrl) => {
        try {
            const randomData = generateRandomData();
            setData(randomData);
            setIsMapView(false);
        } catch (error) {
            setError(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData(initialDataUrl);
    }, [initialDataUrl]);

    const handleBackClick = () => {
        if (history.length > 0) {
            const previousData = history.pop();
            setData(previousData);
            setHistory([...history]);
        } else {
            setIsMapView(true);
        }
    };

    const handleCircleClick = (nextDataUrl) => {
        if (nextDataUrl) {
            setHistory([...history, data]);
            loadData(nextDataUrl);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    if (isMapView) return <Map />;

    const mapInternalPages = data?.map_internal_pages || [];

    return (
        <StyledSVGContainer>
            <BackButton onClick={handleBackClick}>Back</BackButton>
            <StyledSVG viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                {mapInternalPages.map((page) => (
                    <StyledCircle
                        key={page.id}
                        cx={random(10, 90)}
                        cy={random(10, 90)}
                        r={page.size}
                        size={page.size}
                        onClick={() => handleCircleClick(page.nextDataUrl)}
                    />
                ))}
            </StyledSVG>
        </StyledSVGContainer>
    );
};

const Category = ({ onClose }) => (
    <YourComponent initialDataUrl={'http://localhost:3000/data1.json'} />
);

const Map = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [showFullScreen, setShowFullScreen] = useState(false);
    const svgRef = useRef(null);
    const theme = getCurrentTheme();

    const handleMouseEnter = (event) => {
        event.target.style.fill = 'wheat';
    };

    const handleMouseLeave = (event) => {
        event.target.style.fill = '';
    };

    const handleClick = (event) => {
        const target = event.target;
        const dataUrl = target.getAttribute('data-url');
        console.log(dataUrl);
        if (dataUrl) {
            setShowFullScreen(true);
        }
    };

    const toggleSidebar = (open) => {
        setSidebarOpen(open);
    };

    const handleFullScreenClose = () => {
        setShowFullScreen(false);
    };

    return (
        <ThemeProvider theme={theme}>
            {!showFullScreen ? (
                <MapContainer>
                    <Sidebar open={sidebarOpen} toggleSidebar={toggleSidebar} />
                    <ReactSVG
                        src={iconSrc}
                        ref={svgRef}
                        className="svg-icon"
                        beforeInjection={(svg) => {
                            Array.from(svg.querySelectorAll('path')).forEach((path) => {
                                if (path.getAttribute('class') === 'cls-8') {
                               
                                    path.addEventListener('mouseenter', handleMouseEnter);
                                    path.addEventListener('mouseleave', handleMouseLeave);
                                    path.addEventListener('click', handleClick);
                                }
                            });
                        }}
                    />
                    <style>{`
            .svg-icon svg {
              transition: transform 0.3s ease-in-out;
              width: 80%;
              height: 80vh;
              margin: auto;
            }
            .svg-icon path {
              transition: fill 0.2s ease-in-out;
            }
          `}</style>
                </MapContainer>
            ) : (
                <Category onClose={handleFullScreenClose} />
            )}
        </ThemeProvider>
    );
};

export default Map;
