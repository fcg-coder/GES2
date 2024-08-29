// SidebarStyles.js
import styled from 'styled-components';

// Стилевой компонент для бокового меню
export const SidebarContainer = styled.div`
  position: fixed;
  top: 0;
  right: 0;
  max-width: 401px; /* Ширина меню */
  width: 30%;
  height: 100%;
  background-color: #7E7BFF;
  color: white;
  transform: translateX(${props => (props.open ? '0' : '100%')});
  transition: transform 0.3s ease;
  z-index: 1000; /* Обеспечивает, что меню будет поверх других элементов */
  padding: 15px;
  overflow-y: auto; /* Добавляем скроллбар при необходимости */
  display: flex;
  flex-direction: column;
`;

// Контейнер для кнопок
export const ButtonContainer = styled.div`
  position: fixed;
  top: 40px;
  right: 40px; /* Позиция по горизонтали */
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px; /* Расстояние между кнопками */
  z-index: 1000;
    color: #0019CC;
  font-size: 20px;
  font-family: Kufam;
  
`;

// Стилевой компонент для кнопок-ссылок
export const LinkButton = styled.a`

  &:hover {
    text-decoration: underline;
  }
`;

// Стилевой компонент для кнопки открытия меню
export const MenuButton = styled.button`
  color: #0019CC;
  font-size: 20px;
  font-family: Kufam;
  border: none;
  background: transparent; /* Убираем фон */
  cursor: pointer;
  z-index: 1000; /* Обеспечивает, что кнопка будет поверх других элементов */
  opacity: ${props => (props.visible ? '1' : '0')};
  transition: opacity 0.3s ease;
`;

// Стилевой компонент для кнопки закрытия меню внутри меню
export const CloseButton = styled.button`
  background-color: transparent;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  position: absolute;
  top: 15px;
  right: 15px;
`;

// Стилевой компонент для футера
export const Footer = styled.footer`
  margin-top: 20px;
  color: white;
  font-size: 14px;

  .footerLinks {
    display: flex;
    flex-direction: row; /* Два столбца в футере */
    justify-content: space-between;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    margin-bottom: 10px;
  }

  a {
    color: white;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }
`;

// Стилевой компонент для поисковой строки
export const SearchBar = styled.input`
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: none;
  border-radius: 5px;
  outline: none;
`;
