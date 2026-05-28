import { useNavigate } from 'react-router-dom'
import { useContext } from 'react'
import { AppContext } from '../context/AppContext'

function ProductCard({ product }) {
  const navigate = useNavigate()
  const { isFavorite, toggleFavorite } = useContext(AppContext)
  const fav = isFavorite(product.id)

  return (
    <div className="product-card">
      <div
        className="product-card__image-wrap"
        onClick={() => navigate(`/list/${product.id}`)}
      >
        <img src={product.image} alt={product.title} className="product-card__image" />
        <span className="product-card__category">{product.category}</span>
      </div>
      <div className="product-card__body">
        <h3
          className="product-card__title"
          onClick={() => navigate(`/list/${product.id}`)}
        >
          {product.title}
        </h3>
        <p className="product-card__desc">
          {product.description.slice(0, 90)}…
        </p>
        <div className="product-card__footer">
          <span className="product-card__price">${product.price}</span>
          <span className="product-card__rating">
            ★ {product.rating.rate}
            <span className="product-card__rating-count">({product.rating.count})</span>
          </span>
        </div>
        <button
          className={`product-card__fav ${fav ? 'product-card__fav--active' : ''}`}
          onClick={() => toggleFavorite(product)}
        >
          {fav ? '❤ В избранном' : '♡ В избранное'}
        </button>
      </div>
    </div>
  )
}

export default ProductCard
