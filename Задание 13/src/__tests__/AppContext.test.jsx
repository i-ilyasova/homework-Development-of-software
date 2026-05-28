import { render, screen, fireEvent } from '@testing-library/react'
import { useContext } from 'react'
import { AppProvider, AppContext } from '../context/AppContext'

const product1 = { id: 1, title: 'Product 1', price: 10, rating: { rate: 4, count: 50 } }
const product2 = { id: 2, title: 'Product 2', price: 20, rating: { rate: 3, count: 30 } }

function TestConsumer() {
  const { favorites, toggleFavorite, isFavorite, theme, toggleTheme } = useContext(AppContext)
  return (
    <div>
      <span data-testid="fav-count">{favorites.length}</span>
      <span data-testid="theme">{theme}</span>
      <span data-testid="is-fav-1">{String(isFavorite(1))}</span>
      <span data-testid="is-fav-2">{String(isFavorite(2))}</span>
      <button onClick={() => toggleFavorite(product1)}>toggle-1</button>
      <button onClick={() => toggleFavorite(product2)}>toggle-2</button>
      <button onClick={toggleTheme}>toggle-theme</button>
    </div>
  )
}

function renderConsumer() {
  return render(<AppProvider><TestConsumer /></AppProvider>)
}

describe('AppContext', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  test('начальное состояние: избранное пусто', () => {
    renderConsumer()
    expect(screen.getByTestId('fav-count').textContent).toBe('0')
  })

  test('начальная тема: light', () => {
    renderConsumer()
    expect(screen.getByTestId('theme').textContent).toBe('light')
  })

  test('toggleFavorite добавляет товар', () => {
    renderConsumer()
    fireEvent.click(screen.getByText('toggle-1'))
    expect(screen.getByTestId('fav-count').textContent).toBe('1')
    expect(screen.getByTestId('is-fav-1').textContent).toBe('true')
  })

  test('toggleFavorite удаляет уже добавленный товар', () => {
    renderConsumer()
    fireEvent.click(screen.getByText('toggle-1'))
    fireEvent.click(screen.getByText('toggle-1'))
    expect(screen.getByTestId('fav-count').textContent).toBe('0')
    expect(screen.getByTestId('is-fav-1').textContent).toBe('false')
  })

  test('можно добавить несколько товаров', () => {
    renderConsumer()
    fireEvent.click(screen.getByText('toggle-1'))
    fireEvent.click(screen.getByText('toggle-2'))
    expect(screen.getByTestId('fav-count').textContent).toBe('2')
    expect(screen.getByTestId('is-fav-2').textContent).toBe('true')
  })

  test('toggleTheme переключает тему light → dark', () => {
    renderConsumer()
    fireEvent.click(screen.getByText('toggle-theme'))
    expect(screen.getByTestId('theme').textContent).toBe('dark')
  })

  test('toggleTheme переключает тему dark → light', () => {
    renderConsumer()
    fireEvent.click(screen.getByText('toggle-theme'))
    fireEvent.click(screen.getByText('toggle-theme'))
    expect(screen.getByTestId('theme').textContent).toBe('light')
  })

  test('избранное сохраняется в localStorage', () => {
    const { unmount } = renderConsumer()
    fireEvent.click(screen.getByText('toggle-1'))
    unmount()
    renderConsumer()
    expect(screen.getByTestId('fav-count').textContent).toBe('1')
    expect(screen.getByTestId('is-fav-1').textContent).toBe('true')
  })

  test('localStorage очищается при удалении товара', () => {
    const { unmount } = renderConsumer()
    fireEvent.click(screen.getByText('toggle-1'))
    fireEvent.click(screen.getByText('toggle-1'))
    unmount()
    renderConsumer()
    expect(screen.getByTestId('fav-count').textContent).toBe('0')
  })
})
