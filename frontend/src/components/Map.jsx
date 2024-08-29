import React, { useState, useRef } from 'react';
// Импортируем React и необходимые хуки из 'react':
// useState - для управления состоянием в функциональном компоненте
// useRef - для создания ссылок на DOM-элементы и хранения их между рендерингами

import { ReactSVG } from 'react-svg';
// Импортируем компонент ReactSVG из 'react-svg', который позволяет загружать и отображать SVG файлы

import iconSrc from './map.svg';
// Импортируем SVG-файл 'map.svg', который будет отображен на странице. Используем его как источник изображения для компонента ReactSVG

import { getCurrentTheme } from '../themeConfig';
// Импортируем функцию getCurrentTheme из модуля '../themeConfig', которая возвращает объект темы для стилизации

import { ThemeProvider } from 'styled-components';
// Импортируем компонент ThemeProvider из 'styled-components', который позволяет применять тему ко всему компоненту

import styled from 'styled-components';
// Импортируем функцию styled из 'styled-components' для создания стилизованных компонентов

import Sidebar from './Sidebar'; // Импортируем компонент Sidebar из папки components

// Создаем стилизованный компонент MapContainer с использованием styled-components
const MapContainer = styled.div`
  height: 100vh; /* Высота контейнера - 100% высоты видимой части окна браузера */
  width: 100vw; /* Ширина контейнера - 100% ширины видимой части окна браузера */
  margin: auto; /* Автоматическое выравнивание контейнера по центру */
  overflow: hidden; /* Обрезаем содержимое, выходящее за пределы контейнера */
  background: ${props => props.theme.backgroundColor}; /* Используем свойство backgroundColor из текущей темы для установки фона */
`;

// Основной компонент Map, принимающий пропс onClick
const Map = ({ onClick }) => {
    // Используем хук useState для управления состоянием масштаба и трансформаций
    const [scale, setScale] = useState(1); // Изначальный масштаб равен 1
    const [transform, setTransform] = useState('translate(0, 0) scale(1)');
    // Хук useState для управления состоянием бокового меню
    const [sidebarOpen, setSidebarOpen] = useState(false); // Изначально боковое меню закрыто

    // Изначальное значение трансформации: перевод по осям (0, 0) и масштаб 1

    const svgRef = useRef(null);
    // Создаем ссылку на SVG элемент для последующего манипулирования с ним

    const theme = getCurrentTheme();
    // Получаем текущую тему, которая будет применена к компонентам через ThemeProvider

    // Функция для обработки события наведения мыши на путь
    const handleMouseEnter = (event) => {
        event.target.style.fill = 'wheat';
        // Меняем цвет заливки на 'wheat' при наведении мыши на элемент <path>
    };


    // Функция для переключения видимости бокового меню
    const toggleSidebar = (open) => {
        setSidebarOpen(open); // Устанавливаем состояние sidebarOpen в значение open
    };

    // Функция для обработки события убирания мыши с пути
    const handleMouseLeave = (event) => {
        event.target.style.fill = '';
        // Возвращаем оригинальный цвет заливки, когда мышь уходит с элемента <path>
    };

    // Функция для обработки клика на элемент <path>
    const handleClick = (event) => {
        const target = event.target;
        // Получаем элемент, на который кликнули
        const dataUrl = target.getAttribute('data-url');
        // Извлекаем значение атрибута 'data-url' из элемента <path>
        if (dataUrl) {
            console.log(dataUrl);
            // Выводим значение dataUrl в консоль (может быть полезно для отладки)
            onClick(dataUrl);
            // Вызываем функцию onClick, переданную через пропсы, с аргументом dataUrl
        }
    };

    return (
        <ThemeProvider theme={theme}>
            {/* Оборачиваем содержимое компонента в ThemeProvider, чтобы применить текущую тему */}
            {/* Вставляем компонент Sidebar и передаем ему состояние и функцию для управления видимостью */}
            <Sidebar open={sidebarOpen} toggleSidebar={toggleSidebar} />

            <MapContainer>
                {/* Используем стилизованный компонент MapContainer для отображения содержимого */}
                <ReactSVG
                    src={iconSrc}
                    // Передаем путь к SVG-файлу для отображения
                    ref={svgRef}
                    // Передаем ссылку на SVG элемент
                    className="svg-icon"
                    // Присваиваем класс для применения дополнительных стилей
                    beforeInjection={(svg) => {
                        // Функция beforeInjection вызывается перед вставкой SVG в DOM
                        Array.from(svg.querySelectorAll('path')).forEach((path) => {
                            // Находим все элементы <path> внутри SVG
                            if (path.getAttribute('class') === 'cls-8') {
                                // Проверяем, есть ли у элемента класс 'cls-8'
                                path.addEventListener('mouseenter', handleMouseEnter);
                                // Добавляем обработчик события наведения мыши
                                path.addEventListener('mouseleave', handleMouseLeave);
                                // Добавляем обработчик события убирания мыши
                                path.addEventListener('click', handleClick);
                                // Добавляем обработчик события клика
                            }
                        });
                    }}
                />
                <style>{`
                    .svg-icon svg {
                        transition: transform 0.3s ease-in-out; 
                        /* Плавное изменение трансформаций SVG с продолжительностью 0.3 секунды */
                        width: 80%; 
                        /* Устанавливаем ширину SVG в 80% от ширины контейнера */
                        height: 80vh; 
                        /* Устанавливаем высоту SVG в 80% от высоты видимой части окна браузера */
                        margin: auto; 
                        /* Автоматическое выравнивание SVG по центру контейнера */
                    }
                    .svg-icon path {
                        transition: fill 0.2s ease-in-out; 
                        /* Плавное изменение цвета заливки элементов <path> с продолжительностью 0.2 секунды */
                    }
                `}</style>
                {/* Стили для SVG и элементов <path> внутри него */}
            </MapContainer>
        </ThemeProvider>
    );
};

// Экспортируем компонент Map как экспорт по умолчанию
export default Map;
