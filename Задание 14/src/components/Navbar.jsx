import { NavLink, useNavigate } from 'react-router-dom'
import { useContext, useState, memo } from 'react'
import { AppContext } from '../context/AppContext'
import { AuthContext } from '../context/AuthContext'
import { useNetworkStatus } from '../hooks/useNetworkStatus'

function Navbar() {
  const { theme, toggleTheme, favorites } = useContext(AppContext)
  const { user, logout, isAuth }          = useContext(AuthContext)
  const isOnline                          = useNetworkStatus()
  const navigate                          = useNavigate()
  const [menuOpen, setMenuOpen]           = useState(false)

  const linkClass = ({ isActive }) =>
    isActive ? 'navbar__link navbar__link--active' : 'navbar__link'

  const close = () => setMenuOpen(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

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

      {isAuth && (
        <ul className={`navbar__links ${menuOpen ? 'navbar__links--open' : ''}`}>
          <li><NavLink to="/"           className={linkClass} end    onClick={close}>Главная</NavLink></li>
          <li><NavLink to="/list"       className={linkClass}        onClick={close}>Каталог</NavLink></li>
          <li>
            <NavLink to="/favourites"   className={linkClass}        onClick={close}>
              Избранное
              {favorites.length > 0 && (
                <span className="navbar__link-badge">{favorites.length}</span>
              )}
            </NavLink>
          </li>
          <li><NavLink to="/about"      className={linkClass}        onClick={close}>О нас</NavLink></li>
        </ul>
      )}

      <div className="navbar__actions">
        <span className={`network-dot ${isOnline ? 'network-dot--online' : 'network-dot--offline'}`}
          title={isOnline ? 'Онлайн' : 'Офлайн'}
        />

        {isAuth ? (
          <>
            <span className="navbar__user">
              <span className="navbar__user-avatar">
                {user.name.charAt(0).toUpperCase()}
              </span>
              <span className="navbar__user-name">{user.name}</span>
            </span>
            <button className="btn btn--ghost btn--sm" onClick={handleLogout}>
              Выйти
            </button>
          </>
        ) : (
          <NavLink to="/login" className="btn btn--primary btn--sm">Войти</NavLink>
        )}

        <button className="theme-toggle" onClick={toggleTheme} aria-label="Сменить тему">
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
      </div>
    </nav>
  )
}

export default memo(Navbar)
