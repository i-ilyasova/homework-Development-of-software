import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AppContext } from '../context/AppContext'
import Navbar from '../components/Navbar'

function renderNavbar(overrides = {}) {
  const ctx = {
    theme: 'light',
    toggleTheme: jest.fn(),
    favorites: [],
    ...overrides,
  }
  return render(
    <MemoryRouter>
      <AppContext.Provider value={ctx}>
        <Navbar />
      </AppContext.Provider>
    </MemoryRouter>
  )
}

describe('Navbar', () => {
  test('отображает логотип', () => {
    renderNavbar()
    expect(screen.getByText('ShopReact')).toBeInTheDocument()
  })

  test('отображает ссылку «Главная»', () => {
    renderNavbar()
    expect(screen.getByRole('link', { name: /главная/i })).toBeInTheDocument()
  })

  test('отображает ссылку «Каталог»', () => {
    renderNavbar()
    expect(screen.getByRole('link', { name: /каталог/i })).toBeInTheDocument()
  })

  test('отображает ссылку «Избранное»', () => {
    renderNavbar()
    expect(screen.getByRole('link', { name: /избранное/i })).toBeInTheDocument()
  })

  test('отображает ссылку «О нас»', () => {
    renderNavbar()
    expect(screen.getByRole('link', { name: /о нас/i })).toBeInTheDocument()
  })

  test('отображает кнопку переключения темы', () => {
    renderNavbar()
    expect(screen.getByRole('button', { name: /сменить тему/i })).toBeInTheDocument()
  })

  test('кнопка темы вызывает toggleTheme', () => {
    const toggleTheme = jest.fn()
    renderNavbar({ toggleTheme })
    fireEvent.click(screen.getByRole('button', { name: /сменить тему/i }))
    expect(toggleTheme).toHaveBeenCalledTimes(1)
  })

  test('показывает счётчик избранного при непустом списке', () => {
    const favorites = [{ id: 1 }, { id: 2 }, { id: 3 }]
    renderNavbar({ favorites })
    expect(screen.getByText('3')).toBeInTheDocument()
  })

  test('не показывает счётчик при пустом избранном', () => {
    renderNavbar({ favorites: [] })
    expect(screen.queryByText(/^\d+$/)).not.toBeInTheDocument()
  })

  test('ссылка «Избранное» ведёт на /favourites', () => {
    renderNavbar()
    const link = screen.getByRole('link', { name: /избранное/i })
    expect(link).toHaveAttribute('href', '/favourites')
  })
})
