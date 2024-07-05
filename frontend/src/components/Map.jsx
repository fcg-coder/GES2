import React from 'react';
import { ReactSVG } from 'react-svg';
import iconSrc from './map_full.svg'; // Импорт SVG файла, который содержит карту

// Компонент Map
const Map = () => {
    // Функция для обработки события наведения на путь
    const handleMouseEnter = (event) => {
        event.target.style.fill = 'red'; // Изменяем цвет заливки при наведении
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
            window.location.href = dataUrl; // Переход на другую страницу по ссылке из атрибута data-url
        }
    };

    return (
        <div style={{ width: '80%', margin: 'auto', overflow: 'hidden' }}>
            {/* Компонент ReactSVG для загрузки и отображения SVG файла */}
            <ReactSVG
                src={iconSrc}
                className="svg-icon"
                onClick={handleClick}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                beforeInjection={(svg) => {
                    // Добавление обработчиков событий к элементам <path> в SVG после вставки в DOM
                    Array.from(svg.querySelectorAll('path')).forEach((path) => {
                        path.addEventListener('mouseenter', handleMouseEnter);
                        path.addEventListener('mouseleave', handleMouseLeave);
                        path.addEventListener('click', handleClick);
                    });
                }}
            />
            <style>{`
                .svg-icon svg {
                    transition: fill 0.2s ease-in-out; /* Плавное изменение цвета заливки */
                }
            `}</style>
        </div>
    );
};

// Экспорт компонента Map как по умолчанию
export default Map;
