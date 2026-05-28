import { useParams, useNavigate } from 'react-router-dom'
import { useContext, useEffect, useState, useCallback } from 'react'
import { AppContext } from '../context/AppContext'
import Spinner from '../components/Spinner'
import ErrorMessage from '../components/ErrorMessage'

function Details() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { products, toggleFavorite, isFavorite } = useContext(AppContext)

  const cached = products.find(p => p.id === Number(id))
  const [product,     setProduct]     = useState(cached || null)
  const [loading,     setLoading]     = useState(!cached)
  const [error,       setError]       = useState(null)
  const [addedToCart, setAddedToCart] = useState(false)

  const loadProduct = useCallback(() => {
    setLoading(true)
    setError(null)
    fetch(`https://fakestoreapi.com/products/${id}`)
      .then(res => {
        if (!res.ok) throw new Error(`Товар #${id} не найден`)
        return res.json()
      })
      .then(data  => { setProduct(data); setLoading(false) })
      .catch(err  => { setError(err.message); setLoading(false) })
  }, [id])

  useEffect(() => {
    if (!cached) loadProduct()
  }, [id])

  const handleAddToCart = useCallback(() => {
    setAddedToCart(true)
    setTimeout(() => setAddedToCart(false), 2000)
  }, [])

  if (loading) return <Spinner text="Загружаем товар..." />
  if (error)   return <ErrorMessage message={error} onRetry={loadProduct} />
  if (!product) return null

  const fav   = isFavorite(product.id)
  const stars = Math.round(product.rating.rate)

  return (
    <div className="page page--details">
      <button className="btn btn--ghost btn--sm" onClick={() => navigate(-1)}>← Назад</button>

      <div className="product-detail">
        <div className="product-detail__gallery">
          <div className="product-detail__image-wrap">
            <img src={product.image} alt={product.title} className="product-detail__image" />
          </div>
        </div>

        <div className="product-detail__info">
          <span className="product-detail__category">{product.category}</span>
          <h1 className="product-detail__title">{product.title}</h1>

          <div className="product-detail__rating">
            <div className="rating-stars">
              {Array.from({ length: 5 }, (_, i) => (
                <span key={i} className={i < stars ? 'star star--filled' : 'star'}>★</span>
              ))}
            </div>
            <span className="rating-value">{product.rating.rate}</span>
            <span className="rating-count">{product.rating.count} отзывов</span>
          </div>

          <p className="product-detail__price">${product.price}</p>
          <p className="product-detail__desc">{product.description}</p>

          <div className="product-detail__actions">
            <button
              className={`btn btn--primary btn--lg ${addedToCart ? 'btn--success' : ''}`}
              onClick={handleAddToCart}
            >
              {addedToCart ? '✓ Добавлено!' : 'В корзину'}
            </button>
            <button
              className={`btn btn--fav ${fav ? 'btn--fav--active' : ''}`}
              onClick={() => toggleFavorite(product)}
            >
              {fav ? '❤ В избранном' : '♡ Добавить в избранное'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Details
