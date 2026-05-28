import { Link } from 'react-router-dom'
import { useContext } from 'react'
import { AppContext } from '../context/AppContext'

function Home() {
  const { favorites } = useContext(AppContext)

  return (
    <div className="page page--home">
      <section className="hero">
        <div className="hero__content">
          <h1 className="hero__title">
            Добро пожаловать<br />в <span className="hero__accent">ShopReact</span>
          </h1>
          <p className="hero__subtitle">
            Откройте для себя тысячи товаров по лучшим ценам.
            Удобный каталог, быстрый поиск, любимые товары в один клик.
          </p>
          <div className="hero__actions">
            <Link to="/list" className="btn btn--primary btn--lg">Перейти в каталог →</Link>
            {favorites.length > 0 && (
              <Link to="/favourites" className="btn btn--fav">
                ❤ Избранное ({favorites.length})
              </Link>
            )}
          </div>
        </div>
      </section>

      <section className="features">
        <div className="feature-card">
          <div className="feature-card__icon">🚚</div>
          <h3 className="feature-card__title">Быстрая доставка</h3>
          <p className="feature-card__text">Доставим ваш заказ в течение 1–3 рабочих дней</p>
        </div>
        <div className="feature-card">
          <div className="feature-card__icon">💳</div>
          <h3 className="feature-card__title">Безопасная оплата</h3>
          <p className="feature-card__text">SSL-шифрование и защита всех платежей</p>
        </div>
        <div className="feature-card">
          <div className="feature-card__icon">↩️</div>
          <h3 className="feature-card__title">Возврат 30 дней</h3>
          <p className="feature-card__text">Вернём деньги без лишних вопросов</p>
        </div>
        <div className="feature-card">
          <div className="feature-card__icon">⭐</div>
          <h3 className="feature-card__title">Рейтинг товаров</h3>
          <p className="feature-card__text">Реальные отзывы покупателей</p>
        </div>
      </section>
    </div>
  )
}

export default Home
