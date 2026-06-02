import { createContext, useState, useCallback } from 'react'

export const AuthContext = createContext(null)

const MOCK_USERS = [
  { id: 1, email: 'user@example.com',  password: 'password123', name: 'Алиса' },
  { id: 2, email: 'admin@shop.ru',     password: 'admin123',    name: 'Администратор' },
]

const TOKEN_KEY = 'shop-token'
const USER_KEY  = 'shop-user'

function createToken(user) {
  const payload = {
    sub:   user.id,
    email: user.email,
    name:  user.name,
    exp:   Date.now() + 24 * 60 * 60 * 1000,
  }
  return btoa(JSON.stringify(payload))
}

function parseToken(token) {
  try {
    const payload = JSON.parse(atob(token))
    if (payload.exp < Date.now()) return null
    return payload
  } catch {
    return null
  }
}

function loadUser() {
  const token = localStorage.getItem(TOKEN_KEY)
  if (!token) return null
  const payload = parseToken(token)
  if (!payload) {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    return null
  }
  return payload
}

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(loadUser)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  const login = useCallback((email, password) => {
    setLoading(true)
    setError(null)
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const found = MOCK_USERS.find(
          (u) => u.email === email && u.password === password
        )
        if (found) {
          const token   = createToken(found)
          const payload = parseToken(token)
          localStorage.setItem(TOKEN_KEY, token)
          localStorage.setItem(USER_KEY, JSON.stringify(payload))
          setUser(payload)
          setLoading(false)
          resolve(payload)
        } else {
          const msg = 'Неверный email или пароль'
          setError(msg)
          setLoading(false)
          reject(new Error(msg))
        }
      }, 800)
    })
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setUser(null)
    setError(null)
  }, [])

  const clearError = useCallback(() => setError(null), [])

  return (
    <AuthContext.Provider value={{ user, loading, error, login, logout, clearError, isAuth: !!user }}>
      {children}
    </AuthContext.Provider>
  )
}
