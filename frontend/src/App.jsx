import Footer from "./components/Footer";
import { useState } from "react";

export default function App() {
  const [active, setActive] = useState("home"); 

  const handleSectionChange = (newActive) => {
    setActive(newActive);
  };

  return (
    <>
     
      <Footer />
    </>
  );
}
