// src/themeConfig.js

import lightTheme from './themes/lightTheme';
import darkTheme from './themes/darkTheme';

export { lightTheme, darkTheme }; // Экспортируем все темы

export const getCurrentTheme = () => lightTheme; // Это может быть изменено в зависимости от вашей логики
