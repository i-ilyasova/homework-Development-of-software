import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AppContext } from '../context/AppContext'
import ProductCard from '../components/ProductCard'

const mockProduct = {
  id: 1,
  title: 'Test Product',
  price: 29.99,
  description: 'Test description for the product that is long enough to be sliced',
  category: 'electronics',
  image: 'https://example.com/image.jpg',
  rating: { rate: 4.5, count: 120 },
}

function renderCard(isFavorite = jest.fn(() => false), toggleFavorite = jest.fn()) {
  return render(
    <MemoryRouter>
      <AppContext.Provider value={{ isFavorite, toggleFavorite }}>
        <ProductCard product={mockProduct} />
      </AppContext.Provider>
    </MemoryRouter>
  )
}

describe('ProductCard', () => {
  test('отображает название товара', () => {
    renderCard()
    expect(screen.getByText('Test Product')).toBeInTheDocument()
  })

  test('отображает цену товара', () => {
    renderCard()
    expect(screen.getByText('$29.99')).toBeInTheDocument()
  })

  test('отображает категорию товара', () => {
    renderCard()
    expect(screen.getByText('electronics')).toBeInTheDocument()
  })

  test('отображает рейтинг', () => {
    renderCard()
    expect(screen.getByText(/4\.5/)).toBeInTheDocument()
  })

  test('показывает кнопку «В избранное» если товар не в избранном', () => {
    renderCard(jest.fn(() => false))
    expect(screen.getByText(/В избранное/)).toBeInTheDocument()
  })

  test('показывает кнопку «В избранном» если товар уже в избранном', () => {
    renderCard(jest.fn(() => true))
    expect(screen.getByText(/В избранном/)).toBeInTheDocument()
  })

  test('вызывает toggleFavorite при нажатии кнопки избранного', () => {
    const toggleFavorite = jest.fn()
    renderCard(jest.fn(() => false), toggleFavorite)
    fireEvent.click(screen.getByText(/В избранное/))
    expect(toggleFavorite).toHaveBeenCalledTimes(1)
    expect(toggleFavorite).toHaveBeenCalledWith(mockProduct)
  })

  test('отображает изображение товара с правильным alt', () => {
    renderCard()
    const img = screen.getByRole('img', { name: 'Test Product' })
    expect(img).toBeInTheDocument()
    expect(img).toHaveAttribute('src', mockProduct.image)
  })
})
