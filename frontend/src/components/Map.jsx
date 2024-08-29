import React, { useState, useRef } from 'react';
import { ReactSVG } from 'react-svg';
import iconSrc from './map.svg'; // Импорт SVG файла, который содержит карту
import { getCurrentTheme } from '../themeConfig'; // Импортируем функцию для получения текущей темы
import { ThemeProvider } from 'styled-components';
import styled from 'styled-components';

// Создаем стилизованный компонент для обертки
const MapContainer = styled.div`
  height: 100vh;
  width: 100vw;
  margin: auto;
  overflow: hidden;
  background: ${props => props.theme.backgroundColor}; // Используем тему
`;

const Map = ({ onClick }) => {
    const [scale, setScale] = useState(1);
    const [transform, setTransform] = useState('translate(0, 0) scale(1)');
    const svgRef = useRef(null);
    const theme = getCurrentTheme(); // Получаем текущую тему

    // Функция для обработки события наведения на путь
    const handleMouseEnter = (event) => {
        event.target.style.fill = 'wheat'; // Изменяем цвет заливки при наведении
    };

    // Функция для обработки события убирания мыши с пути
    const handleMouseLeave = (event) => {
        event.target.style.fill = ''; // Возвращаем оригинальный цвет заливки
    };

    // Функция для обработки события клика на путь
    const handleClick = (event) => {
        const target = event.target;
        const dataUrl = target.getAttribute('data-url');
        if (dataUrl) {
            console.log(dataUrl);
            onClick(dataUrl); // Вызываем функцию onClick, переданную из App
        }
    };

    return (
        <ThemeProvider theme={theme}>
            <MapContainer>
                {/* Компонент ReactSVG для загрузки и отображения SVG файла */}
                <ReactSVG
                    src={iconSrc}
                    ref={svgRef}
                    className="svg-icon"
                    beforeInjection={(svg) => {
                        // Добавление обработчиков событий к элементам <path> в SVG после вставки в DOM
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
                        transition: transform 0.3s ease-in-out; /* Плавное масштабирование */
                        width: 80%; /* Занимает 100% ширины */
                        height: 80vh; /* Занимает 100% высоты */
                        margin: auto;
                    }
                    .svg-icon path {
                        transition: fill 0.2s ease-in-out; /* Плавное изменение цвета заливки */
                    }
                `}</style>
            </MapContainer>
        </ThemeProvider>
    );
};

// Экспорт компонента Map как по умолчанию
export default Map;
