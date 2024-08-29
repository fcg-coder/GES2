import React, { useState, useEffect } from 'react';
// Импортируем React и хуки useState и useEffect из 'react':
// useState для управления состоянием в функциональном компоненте
// useEffect для выполнения побочных эффектов, таких как загрузка данных

import axios from 'axios';
// Импортируем библиотеку axios для выполнения HTTP-запросов

import styled from 'styled-components';
// Импортируем функцию styled из 'styled-components' для создания стилизованных компонентов

// Стилевой компонент для контейнера SVG
const StyledSVGContainer = styled.div`
  display: flex; 
  /* Используем flexbox для размещения содержимого по центру */
  justify-content: center; 
  /* Центрируем содержимое по горизонтали */
  align-items: center; 
  /* Центрируем содержимое по вертикали */
  height: 100vh; 
  /* Высота контейнера - 100% высоты видимой части окна браузера */
  width: 100vw; 
  /* Ширина контейнера - 100% ширины видимой части окна браузера */
`;

// Стилевой компонент для SVG
const StyledSVG = styled.svg`
  width: 80%; 
  /* Ширина SVG составляет 80% от ширины контейнера */
  height: 80%; 
  /* Высота SVG составляет 80% от высоты контейнера */
`;

// Стилевой компонент для круга
const StyledCircle = styled.circle`
  fill: white; 
  /* Цвет заливки круга - белый */
  stroke: ${props => getColor(props.size)}; 
  /* Цвет обводки круга зависит от его размера и определяется функцией getColor */
  stroke-width: 0.75; 
  /* Ширина обводки круга - 0.75 единицы */

  &:hover { 
    /* Псевдокласс для изменения стиля при наведении мыши */
    fill: wheat; 
    /* Цвет заливки круга изменяется на 'wheat' при наведении мыши */
  }
`;

// Функция для определения цвета по размеру
const getColor = (size) => {
    if (size < 3) return 'red';
    // Если размер круга меньше 3, возвращаем цвет 'red'
    else if (size < 6) return 'blue';
    // Если размер круга меньше 6, но не меньше 3, возвращаем цвет 'blue'
    else if (size < 9) return 'green';
    // Если размер круга меньше 9, но не меньше 6, возвращаем цвет 'green'
    else return 'yellow';
    // Если размер круга 9 или больше, возвращаем цвет 'yellow'
};

// Основной компонент YourComponent, принимающий пропс initialDataUrl
const YourComponent = ({ initialDataUrl }) => {
    const [data, setData] = useState(null);
    // Состояние для хранения загруженных данных, изначально равно null
    const [loading, setLoading] = useState(true);
    // Состояние для управления индикатором загрузки, изначально равно true
    const [error, setError] = useState(null);
    // Состояние для хранения ошибки, если она возникает, изначально равно null

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(initialDataUrl);
                // Выполняем HTTP GET запрос к URL, указанному в initialDataUrl
                setData(response.data);
                // Устанавливаем загруженные данные в состояние
            } catch (error) {
                setError(error);
                // Если возникает ошибка, устанавливаем ее в состояние
            } finally {
                setLoading(false);
                // Независимо от результата запроса, устанавливаем состояние загрузки в false
            }
        };

        if (initialDataUrl) {
            fetchData();
            // Если initialDataUrl не пустой, вызываем функцию для загрузки данных
        }
    }, [initialDataUrl]);
    // useEffect с зависимостью от initialDataUrl, вызывается при изменении initialDataUrl

    if (loading) return <div>Loading...</div>;
    // Если данные еще загружаются, отображаем сообщение 'Loading...'
    if (error) return <div>Error: {error.message}</div>;
    // Если возникла ошибка, отображаем сообщение об ошибке

    const mapInternalPages = data?.map_internal_pages || [];
    // Извлекаем массив map_internal_pages из данных, если данные не загружены, используем пустой массив

    // Функция для генерации случайного числа в заданном диапазоне
    const random = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
    // Генерирует случайное число между min и max, включая оба значения

    // Функция для обработки клика по кругу
    const handleCircleClick = (id) => {
        console.log(`Circle with id ${id} clicked`);
        // Выводим в консоль сообщение о том, что круг с указанным id был кликнут
        // Добавьте здесь логику для обработки клика по кругу
    };

    return (
        <StyledSVGContainer>
            {/* Используем стилизованный контейнер для размещения SVG по центру */}
            <StyledSVG viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                {/* Определяем viewBox для SVG и пространство имен для SVG */}
                {mapInternalPages.map(page => (
                    // Проходим по каждому элементу массива mapInternalPages и отображаем круги
                    <StyledCircle
                        key={page.id}
                        // Устанавливаем уникальный ключ для каждого элемента
                        cx={random(10, 90)}
                        // Устанавливаем значение cx (координата x центра) случайным образом между 10 и 90
                        cy={random(10, 90)}
                        // Устанавливаем значение cy (координата y центра) случайным образом между 10 и 90
                        r={page.size}
                        // Устанавливаем радиус круга в соответствии с размером, указанным в данных
                        size={page.size}
                        // Передаем размер как пропс, который будет использован в стиле
                        onClick={() => handleCircleClick(page.id)}
                    // Добавляем обработчик события клика, который вызывает функцию handleCircleClick
                    />
                ))}
            </StyledSVG>
        </StyledSVGContainer>
    );
};

// Экспортируем компонент YourComponent как экспорт по умолчанию
export default YourComponent;
