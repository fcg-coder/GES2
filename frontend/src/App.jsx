import React, { useState } from 'react'; // Импортируем React и хук useState для управления состоянием
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Импортируем компоненты маршрутизации из react-router-dom
import Map from './components/Map'; // Импортируем компонент Map из папки components


import Graph from './components/Graph'; // Импортируем компонент Graph из папки components

// Основной компонент приложения
const App = () => {
  // Хук useState для управления состоянием dataUrl
  const [dataUrl, setDataUrl] = useState(null); // Изначально dataUrl равно null


  // Функция для обработки кликов на компоненте Map
  const handleMapClick = (pageId) => {
    setDataUrl(pageId); // Обновляем состояние dataUrl с помощью переданного pageId
  };



  return (
    <Router> {/* Оборачиваем приложение в Router для поддержки маршрутизации */}
      <div>
   
        {/* Основное содержимое приложения, рендерится в зависимости от текущего маршрута */}
        <Routes>
          {/* Основной маршрут (путь "/") отображает компонент Map */}
          <Route path="/" element={<Map />} />

          {/* Маршрут "/graph" отображает компонент Graph */}
          <Route path="/graph" element={<Graph />} />

          {/* Дополнительные маршруты могут быть добавлены здесь по необходимости */}
          {/* <Route path="/some-other-route" element={<SomeOtherComponent />} /> */}
        </Routes>


      </div>
    </Router>
  );
};

// Экспортируем компонент App для использования в других частях приложения
export default App;
