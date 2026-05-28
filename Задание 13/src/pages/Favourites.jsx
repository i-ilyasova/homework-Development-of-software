import { useContext, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AppContext } from '../context/AppContext'

function FavouriteItem({ product, onRemove }) {
  const navigate = useNavigate()

  return (
    <div className="fav-item">
      <div className="fav-item__image-wrap" onClick={() => navigate(`/list/${product.id}`)}>
        <img src={product.image} alt={product.title} className="fav-item__image" />
      </div>
      <div className="fav-item__info">
        <span className="fav-item__category">{product.category}</span>
        <h3 className="fav-item__title" onClick={() => navigate(`/list/${product.id}`)}>
          {product.title}
        </h3>
        <div className="fav-item__meta">
          <span className="fav-item__price">${product.price}</span>
          <span className="fav-item__rating">★ {product.rating.rate} ({product.rating.count} отзывов)</span>
        </div>
      </div>
      <button className="fav-item__remove" onClick={() => onRemove(product)} aria-label="Удалить из избранного">
        Удалить
      </button>
    </div>
  )
}

function Favourites() {
  const { favorites, toggleFavorite } = useContext(AppContext)

  const handleRemove = useCallback(
    (product) => toggleFavorite(product),
    [toggleFavorite]
  )

  if (favorites.length === 0) {
    return (
      <div className="page page--favourites">
        <div className="page__header">
          <h1 className="page__title">Избранное</h1>
        </div>
        <div className="fav-empty">
          <div className="fav-empty__icon">🤍</div>
          <h2 className="fav-empty__title">Список избранного пуст</h2>
          <p className="fav-empty__text">Добавляйте понравившиеся товары, нажимая ♡</p>
          <Link to="/list" className="btn btn--primary">Перейти в каталог</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="page page--favourites">
      <div className="page__header">
        <h1 className="page__title">Избранное</h1>
        <p className="page__subtitle">{favorites.length} товар{favorites.length === 1 ? '' : 'а'} в списке</p>
      </div>

      <div className="fav-list">
        {favorites.map(product => (
          <FavouriteItem
            key={product.id}
            product={product}
            onRemove={handleRemove}
          />
        ))}
      </div>
    </div>
  )
}

export default Favourites
