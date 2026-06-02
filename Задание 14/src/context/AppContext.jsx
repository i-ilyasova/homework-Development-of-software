import { createContext, useState, useCallback, useEffect } from 'react'

export const AppContext = createContext(null)

function loadFavourites() {
  try {
    const raw = localStorage.getItem('shop-favourites')
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export function AppProvider({ children }) {
  const [products,  setProducts]  = useState([])
  const [theme,     setTheme]     = useState('light')
  const [favorites, setFavorites] = useState(loadFavourites)

  useEffect(() => {
    localStorage.setItem('shop-favourites', JSON.stringify(favorites))
  }, [favorites])

  const toggleTheme = useCallback(() => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'))
  }, [])

  const toggleFavorite = useCallback((product) => {
    setFavorites(prev => {
      const exists = prev.some(p => p.id === product.id)
      return exists ? prev.filter(p => p.id !== product.id) : [...prev, product]
    })
  }, [])

  const isFavorite = useCallback(
    (id) => favorites.some(p => p.id === id),
    [favorites]
  )

  return (
    <AppContext.Provider
      value={{ products, setProducts, theme, toggleTheme, favorites, toggleFavorite, isFavorite }}
    >
      {children}
    </AppContext.Provider>
  )
}
