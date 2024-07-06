import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const StyledSVGContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
`;

const StyledSVG = styled.svg`
  width: 80%;
  height: 80%;
`;

const YourComponent = ({ initialDataUrl }) => {
    const [data, setData] = useState(null);
    const [dataUrl, setDataUrl] = useState(initialDataUrl);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`/backend/${dataUrl}/`);
                setData(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                setData(generateRandomData()); // Если есть ошибка, используем случайные данные
            }
        };

        if (dataUrl) {
            fetchData();
        } else {
            setData(generateRandomData());
        }
    }, [dataUrl]);

    // Функция для генерации случайных данных
    const generateRandomData = () => {
        const pageCount = random(2, 5); // Количество страниц
        const pages = Array.from({ length: pageCount }, (_, i) => ({
            id: i + 1,
            countOfVW: random(1, 10),
            size: random(3, 10),
            nameOfPage: `Page ${i + 1}`
        }));

        return {
            idOfPage: random(1, 100),
            nameOfPage: "MMO",
            map_internal_pages: pages,
            username: null,
            nowTime: new Date().toISOString()
        };
    };

    const mapInternalPages = data?.map_internal_pages || [];

    const random = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

    const handleCircleClick = (pageId) => {
        setDataUrl(`/map/next_page/${pageId}`);
    };

    // Функция для обработки события наведения на круг
    const handleMouseEnter = (event) => {
        event.target.style.fill = 'wheat'; // Изменяем цвет заливки при наведении
    };

    // Функция для обработки события убирания мыши с круга
    const handleMouseLeave = (event) => {
        event.target.style.fill = 'white'; // Возвращаем оригинальный цвет заливки
    };

    return (
        <StyledSVGContainer>
            <StyledSVG viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                {mapInternalPages.map(page => (
                    <circle
                        key={page.id}
                        cx={random(10, 90)}
                        cy={random(10, 90)}
                        r={page.size}
                        fill="white"
                        stroke={getColor(page.size)}
                        strokeWidth="0.75"
                        onMouseEnter={handleMouseEnter}
                        onMouseLeave={handleMouseLeave}
                        onClick={() => handleCircleClick(page.id)}
                    />
                ))}
            </StyledSVG>
        </StyledSVGContainer>
    );
};

const getColor = (size) => {
    if (size < 3) return 'red';
    else if (size < 6) return 'blue';
    else if (size < 9) return 'green';
    else return 'yellow';
};

export default YourComponent;
