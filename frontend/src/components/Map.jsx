import React, { useEffect, useState } from 'react';
import { ReactSVG } from 'react-svg'; // Импорт компонента ReactSVG из библиотеки react-svg
import iconSrc from './map_full.svg'; // Импорт SVG файла, который содержит карту

// Компонент Map
const Map = () => {
    // Функция для обработки события наведения на путь
    const handleMouseEnter = (event) => {
        // Устанавливаем цвет заливки для элемента SVG
        event.target.style.fill = 'red'; // Замените 'red' на любой другой цвет по вашему выбору
    };

    // Функция для обработки события убирания мыши с пути
    const handleMouseLeave = (event) => {
        // Сбрасываем цвет заливки элемента SVG на его исходное значение
        event.target.style.fill = ''; // Возвращаем оригинальный цвет
    };

    // Хук состояния для отслеживания размеров окна
    const [windowDimensions, setWindowDimensions] = useState({ width: 0, height: 0 });

    // Хук эффекта для добавления обработчиков событий и отслеживания изменения размеров окна


    return (
        <div style={{ width: '80%', height: '80%' }}>
            {/* Компонент ReactSVG для загрузки и отображения SVG файла */}
            <ReactSVG
                src={iconSrc}
                className="svg-icon"
                beforeInjection={(svg) => {
                    // Перед вставкой SVG в DOM добавляем обработчики событий ко всем элементам <path>
                    Array.from(svg.querySelectorAll('path')).forEach((path) => {
                        path.addEventListener('mouseenter', handleMouseEnter);
                        path.addEventListener('mouseleave', handleMouseLeave);
                    });
                }}
            />
        </div>
    );
};

// Экспорт компонента Map как по умолчанию
export default Map;
