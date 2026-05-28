import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AppContext } from '../context/AppContext'
import Favourites from '../pages/Favourites'

const mockProducts = [
  {
    id: 1,
    title: 'Первый товар',
    price: 19.99,
    category: 'electronics',
    image: 'https://example.com/1.jpg',
    rating: { rate: 4.2, count: 80 },
  },
  {
    id: 2,
    title: 'Второй товар',
    price: 39.99,
    category: 'clothing',
    image: 'https://example.com/2.jpg',
    rating: { rate: 3.8, count: 45 },
  },
]

function renderFavourites(favorites = [], toggleFavorite = jest.fn()) {
  return render(
    <MemoryRouter>
      <AppContext.Provider value={{ favorites, toggleFavorite }}>
        <Favourites />
      </AppContext.Provider>
    </MemoryRouter>
  )
}

describe('Favourites', () => {
  test('показывает сообщение о пустом списке', () => {
    renderFavourites([])
    expect(screen.getByText('Список избранного пуст')).toBeInTheDocument()
  })

  test('показывает ссылку на каталог при пустом списке', () => {
    renderFavourites([])
    expect(screen.getByRole('link', { name: /в каталог/i })).toBeInTheDocument()
  })

  test('отображает названия товаров', () => {
    renderFavourites(mockProducts)
    expect(screen.getByText('Первый товар')).toBeInTheDocument()
    expect(screen.getByText('Второй товар')).toBeInTheDocument()
  })

  test('отображает цены товаров', () => {
    renderFavourites(mockProducts)
    expect(screen.getByText('$19.99')).toBeInTheDocument()
    expect(screen.getByText('$39.99')).toBeInTheDocument()
  })

  test('отображает кнопки удаления для каждого товара', () => {
    renderFavourites(mockProducts)
    const removeButtons = screen.getAllByText('Удалить')
    expect(removeButtons).toHaveLength(2)
  })

  test('вызывает toggleFavorite при нажатии «Удалить»', () => {
    const toggleFavorite = jest.fn()
    renderFavourites([mockProducts[0]], toggleFavorite)
    fireEvent.click(screen.getByText('Удалить'))
    expect(toggleFavorite).toHaveBeenCalledWith(mockProducts[0])
  })

  test('отображает заголовок страницы', () => {
    renderFavourites(mockProducts)
    expect(screen.getByRole('heading', { name: /избранное/i, level: 1 })).toBeInTheDocument()
  })

  test('показывает количество товаров в подзаголовке', () => {
    renderFavourites(mockProducts)
    expect(screen.getByText(/2 товара/)).toBeInTheDocument()
  })

  test('отображает изображения товаров', () => {
    renderFavourites([mockProducts[0]])
    const img = screen.getByRole('img', { name: 'Первый товар' })
    expect(img).toHaveAttribute('src', mockProducts[0].image)
  })
})
