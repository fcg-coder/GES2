import React, { useState, useEffect } from 'react';

const Subcategory = ({ initialDataUrl, onClose }) => {
    // Состояния для данных и вида карты
    const [data, setData] = useState(null); // Начальное состояние - нет данных
    const [isMapView, setIsMapView] = useState(true); // Статус отображения карты

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
    const handleCircleClick = (nextDataUrl, flagForInternalRecordings) => {
        if (flagForInternalRecordings === 1) {
            loadData(nextDataUrl); // Если флаг 1, загружаем данные с того же URL
        } else {
            window.location.href = `/alternativePage/${nextDataUrl}`; // Если флаг 0, перенаправляем пользователя
        }
    };

    // Если данные еще не загружены, отображаем сообщение о загрузке
    if (!data) return <div>Loading...</div>;

    // Проверяем флаг для отображения круга или перенаправления
    const mapInternalPages = data?.map_internal_pages || [];

    // Если отображается карта, рисуем круги
    if (isMapView) {
        return (
            <div>
                {/* Компонент SVG для отображения кругов */}
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    {/* Отображаем каждый элемент данных как круг */}
                    {mapInternalPages.map((page) => (
                        <circle
                            key={page.id} // Уникальный ключ для каждого круга
                            cx={Math.random() * 80 + 10} // Случайное положение по оси X
                            cy={Math.random() * 80 + 10} // Случайное положение по оси Y
                            r={page.size} // Радиус круга, который соответствует размеру страницы
                            onClick={() => handleCircleClick(page.nextDataUrl, page.flagForInternalRecordings)} // При клике загружаем следующий набор данных
                        />
                    ))}
                </svg>
            </div>
        );
    }

    // В случае другого вида отображения (например, карты) можно вернуть другой JSX
    return (
        <div>
            <h2>Map view is disabled or alternative view</h2>
        </div>
    );
};

export default Subcategory;
