import React, { useState } from 'react';
import Map from './components/Map';
import Kategory from './components/Kategory'; // Импорт компонента Kategory
import Footer from './components/Footer';

function App() {
  const [dataUrl, setDataUrl] = useState(null); // Состояние для хранения dataUrl

  // Функция для обработки клика в компоненте Map
  const handleMapClick = (dataUrl) => {
    setDataUrl(dataUrl); // Устанавливаем dataUrl в состояние
  };

  return (
    <div>
      {/* Рендерим Map или Kategory в зависимости от значения dataUrl */}
      {dataUrl === null ? (
        <Map onClick={handleMapClick} /> // Передаем функцию handleMapClick в Map
      ) : (
        <Kategory dataUrl={dataUrl} /> // Передаем dataUrl в Kategory
      )}
      <Footer />
    </div>
  );
}

export default App;
