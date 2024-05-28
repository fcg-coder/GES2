// FormDistributor.js
import React from 'react';
import Blob from './FormCreator';

const generateRandomPosition = () => ({
    x: Math.random() * 800, // Генерируем случайную координату X в пределах ширины контейнера
    y: Math.random() * 600, // Генерируем случайную координату Y в пределах высоты контейнера
});

const FormDistributor = ({ onFormClick }) => { // Добавляем свойство onFormClick для обработки клика на формы
    const numForms = 5; // всегда 5 форм
    const numPoints = 100; // количество точек в каждой форме
    const numComponents = 5; // количество компонентов кривой


    const containerStyle = {
        height: '100%'
    };

    
    const handleClick = () => {
        if (typeof onFormClick === 'function') {
            onFormClick(); // Вызываем функцию обратного вызова при клике на форму
        }
    };

    return (
        <div style= {containerStyle}>
            {[...Array(numForms)].map((_, index) => {
                const { x, y } = generateRandomPosition(); // Генерируем случайные координаты
                return (
                    <div key={index} style={{ position: 'absolute', left: x, top: y }}>
                        <Blob numPoints={numPoints} numComponents={numComponents} onClick={handleClick} /> {/* Добавляем обработчик клика */}
                    </div>
                );
            })}
        </div>
    );
};

export default FormDistributor;
