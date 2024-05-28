import React, { useState } from 'react';
import './App.css';
import Footer from "./components/Footer";
import Map from "./components/Map";

export default function App() {
  const [key, setKey] = useState(0);

  const handleClick = () => {
    setKey(prevKey => prevKey + 1);
  };

  return (
    <body>
      <Map key={key} />
      <button onClick={handleClick}>Перерисовать</button>
      <Footer />
    </body>
  );
}
