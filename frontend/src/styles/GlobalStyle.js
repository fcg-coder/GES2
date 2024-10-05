// src/styles/GlobalStyle.js
import { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  body {
    background-color: ${props => props.theme.background};
    color: ${props => props.theme.color};
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
  }
  // Другие глобальные стили
`;

export default GlobalStyle;
