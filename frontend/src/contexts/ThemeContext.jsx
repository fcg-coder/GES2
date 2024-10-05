// src/contexts/ThemeContext.js

import React, { createContext, useContext, useState } from 'react';
import { lightTheme, darkTheme } from '../themeConfig'; // Импортируем темы

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState(lightTheme); // Начальная тема

    const changeTheme = (themeName) => {
        switch (themeName) {
            case 'light':
                setTheme(lightTheme);
                break;
            case 'dark':
                setTheme(darkTheme);
                break;
            default:
                setTheme(lightTheme);
        }
    };

    return (
        <ThemeContext.Provider value={{ theme, changeTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

export const useTheme = () => useContext(ThemeContext);
