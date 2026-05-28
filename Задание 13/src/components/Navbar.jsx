import { NavLink } from 'react-router-dom'
import { useContext, useState, memo } from 'react'
import { AppContext } from '../context/AppContext'

function Navbar() {
  const { theme, toggleTheme, favorites } = useContext(AppContext)
  const [menuOpen, setMenuOpen] = useState(false)

  const linkClass = ({ isActive }) =>
    isActive ? 'navbar__link navbar__link--active' : 'navbar__link'

  const close = () => setMenuOpen(false)

  return (
    <nav className="navbar">
      <NavLink to="/" className="navbar__logo">ShopReact</NavLink>

      <button
        className={`navbar__burger ${menuOpen ? 'navbar__burger--open' : ''}`}
        onClick={() => setMenuOpen(v => !v)}
        aria-label="Меню"
      >
        <span /><span /><span />
      </button>

      <ul className={`navbar__links ${menuOpen ? 'navbar__links--open' : ''}`}>
        <li><NavLink to="/"           className={linkClass} end    onClick={close}>Главная</NavLink></li>
        <li><NavLink to="/list"       className={linkClass}        onClick={close}>Каталог</NavLink></li>
        <li>
          <NavLink to="/favourites" className={linkClass} onClick={close}>
            Избранное
            {favorites.length > 0 && (
              <span className="navbar__link-badge">{favorites.length}</span>
            )}
          </NavLink>
        </li>
        <li><NavLink to="/about"      className={linkClass}        onClick={close}>О нас</NavLink></li>
      </ul>

      <div className="navbar__actions">
        <button className="theme-toggle" onClick={toggleTheme} aria-label="Сменить тему">
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
      </div>
    </nav>
  )
}

export default memo(Navbar)
