import React, { useState } from 'react';
import Map from './components/Map';
import Kategory from './components/Kategory'; // Импорт компонента Kategory
import Footer from './components/Footer';

const App = () => {
  const [dataUrl, setDataUrl] = useState(null); // Состояние для хранения dataUrl

  // Функция для обработки клика в компоненте Map
  const handleMapClick = (pageId) => {
    setDataUrl(pageId); // Устанавливаем dataUrl в состояние
  };

  return (
    <div>
      {/* Рендерим Map или Kategory в зависимости от значения dataUrl */}
      {dataUrl === null ? (
        <Map onClick={handleMapClick} /> // Передаем функцию handleMapClick в Map
      ) : (
        <Kategory initialDataUrl={`/backend/${dataUrl}`} /> // Передаем dataUrl в Kategory через initialDataUrl
      )}
      <Footer />
    </div>
  );
};
export default App;
