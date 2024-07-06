import React, { useState, useEffect } from 'react';
import { ReactSVG } from 'react-svg';
import axios from 'axios';
import iconSrc from './map.svg'; // Импорт SVG файла, который содержит карту

// Компонент Map
const Map = ({ onClick }) => {
    const [data, setData] = useState(null);

    // useEffect(() => {
    //     axios.get('/backend/')
    //         .then(response => {
    //             setData(response.data);
    //             console.log('Data received:', response.data); // Выводим данные в консоль
    //         })
    //         .catch(error => console.error('Error fetching data:', error));
    // }, []);

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
        <div style={{ width: '80%', margin: 'auto', overflow: 'hidden' }}>
            {/* Компонент ReactSVG для загрузки и отображения SVG файла */}
            <ReactSVG
                src={iconSrc}
                className="svg-icon"
                beforeInjection={(svg) => {
                    // Добавление обработчиков событий к элементам <path> в SVG после вставки в DOM

                    // cls-8 отвечает за заливку областей
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
          transition: fill 0.2s ease-in-out; /* Плавное изменение цвета заливки */
        }
      `}</style>
        </div>
    );
};

// Экспорт компонента Map как по умолчанию
export default Map;
