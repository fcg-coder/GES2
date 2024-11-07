import React, { useState, useEffect } from 'react';
import Endcategory from './Endcategory';

const Subcategory = ({ initialDataUrl, onClose }) => {
    const [data, setData] = useState(null); // Начальное состояние - нет данных
    const [isMapView, setIsMapView] = useState(true); // Статус отображения карты
    const [showFullScreen, setShowFullScreen] = useState(false); // Состояние для полноэкранного режима
    const [currentSubcategoryId, setCurrentSubcategoryId] = useState(null); // Для хранения текущего ID подкатегории

    // Функция для загрузки данных с указанного URL
    const loadData = async (nextDataUrl) => {
        try {
            const response = await fetch(`/api/${nextDataUrl}`); // Запрос к API
            const data = await response.json(); // Разбор JSON ответа
            setData(data); // Сохранение данных в состояние
        } catch (error) {
            console.error('Error fetching data:', error); // Ошибка загрузки данных
        }
    };

    // Хук useEffect для загрузки данных с initialDataUrl
    useEffect(() => {
        if (initialDataUrl) {
            loadData(initialDataUrl); // Загружаем данные при первом рендере или изменении initialDataUrl
        }
    }, [initialDataUrl]); // Зависимость от initialDataUrl

    // Обработчик для клика на круг
    const handleCircleClick = (nextDataUrl, flagForInternalRecordings, id) => {
        setCurrentSubcategoryId(id); // Устанавливаем текущий ID подкатегории
        if (flagForInternalRecordings === true) {
            loadData(nextDataUrl); // Если флаг true, загружаем данные с того же URL
        } else {
            setShowFullScreen(true); // Меняем состояние на true для перехода в полноэкранный режим
        }
    };

    // Проверяем данные о подкатегориях
    const subcategories = data?.subcategories || [];

    // Отображение в полноэкранном режиме или не в нем
    return (
        <div>
            {!showFullScreen ? (
                // Если showFullScreen == false, отображаем карту и круги
                <div>
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        {subcategories.map((subcategory) => (
                            <g key={subcategory.id}>
                                {/* Круг с текстом внутри */}
                                <circle
                                    cx={Math.random() * 80 + 10} // Случайное положение по оси X
                                    cy={Math.random() * 80 + 10} // Случайное положение по оси Y
                                    r={15} // Радиус круга (достаточно для текста)
                                    fill="none" // Круг без заливки
                                    stroke="black" // Черная обводка
                                    strokeWidth="2" // Толщина обводки
                                    onClick={() => handleCircleClick(subcategory.id, subcategory.flagForInternalRecordings, subcategory.id)} // При клике изменяем состояние
                                />
                                <text
                                    x={Math.random() * 80 + 10} // Позиция по X для текста (та же, что и у круга)
                                    y={Math.random() * 80 + 10} // Позиция по Y для текста (та же, что и у круга)
                                    textAnchor="middle"
                                    alignmentBaseline="middle"
                                    fontSize="5"
                                    fill="black"
                                    onClick={(e) => {
                                        e.stopPropagation(); // Предотвращаем клик на круг
                                        handleCircleClick(subcategory.id, subcategory.flagForInternalRecordings, subcategory.id); // Также обрабатываем клик на текст
                                    }}
                                >
                                    {subcategory.nameOfCategory}
                                </text>
                            </g>
                        ))}
                    </svg>
                </div>
            ) : (
                // Если showFullScreen == true, показываем компонент Endcategory
                <Endcategory subcategoryId={currentSubcategoryId} onClose={() => setShowFullScreen(false)} />
            )}
        </div>
    );
};

export default Subcategory;
