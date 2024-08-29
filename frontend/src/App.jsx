// App.js

import React, { useState } from 'react';
import Map from './components/Map';
import Kategory from './components/Kategory'; // Импорт компонента Kategory
import Footer from './components/Footer';
import Sidebar from './components/Sidebar'; // Импорт компонента Sidebar

const App = () => {
  const [dataUrl, setDataUrl] = useState(null); // Состояние для хранения dataUrl
  const [sidebarOpen, setSidebarOpen] = useState(false); // Состояние для управления видимостью бокового меню

  // Функция для обработки клика в компоненте Map
  const handleMapClick = (pageId) => {
    setDataUrl(pageId); // Устанавливаем dataUrl в состояние
  };

  // Функция для переключения видимости бокового меню
  const toggleSidebar = (open) => {
    setSidebarOpen(open);
  };

  return (
    <div>
      {/* Вставляем компонент Sidebar */}
      <Sidebar open={sidebarOpen} toggleSidebar={toggleSidebar} />

      {/* Рендерим Map или Kategory в зависимости от значения dataUrl */}
      {dataUrl === null ? (
        <Map onClick={handleMapClick} /> // Передаем функцию handleMapClick в Map
      ) : (
        <Kategory initialDataUrl={`/backend/${dataUrl}`} /> // Передаем dataUrl в Kategory через initialDataUrl
      )}

    </div>
  );
};

export default App;
