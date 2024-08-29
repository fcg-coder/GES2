import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';

// Стилевой компонент для контейнера SVG
const StyledSVGContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
`;

// Стилевой компонент для SVG
const StyledSVG = styled.svg`
  width: 80%;
  height: 80%;
`;

// Стилевой компонент для круга
const StyledCircle = styled.circle`
  fill: white;
  stroke: ${props => getColor(props.size)};
  stroke-width: 0.75;

  &:hover {
    fill: wheat;
  }
`;

// Функция для определения цвета по размеру
const getColor = (size) => {
    if (size < 3) return 'red';
    else if (size < 6) return 'blue';
    else if (size < 9) return 'green';
    else return 'yellow';
};

// Основной компонент
const YourComponent = ({ initialDataUrl }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(initialDataUrl);
                setData(response.data);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        if (initialDataUrl) {
            fetchData();
        }
    }, [initialDataUrl]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    const mapInternalPages = data?.map_internal_pages || [];

    // Функция для генерации случайного числа в диапазоне
    const random = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

    // Функция для обработки клика по кругу
    const handleCircleClick = (id) => {
        console.log(`Circle with id ${id} clicked`);
        // Добавьте здесь логику для обработки клика по кругу
    };

    return (
        <StyledSVGContainer>
            <StyledSVG viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                {mapInternalPages.map(page => (
                    <StyledCircle
                        key={page.id}
                        cx={random(10, 90)}
                        cy={random(10, 90)}
                        r={page.size}
                        size={page.size}
                        onClick={() => handleCircleClick(page.id)}
                    />
                ))}
            </StyledSVG>
        </StyledSVGContainer>
    );
};

export default YourComponent;
