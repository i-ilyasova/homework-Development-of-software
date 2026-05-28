function About() {
  return (
    <div className="page page--about">
      <div className="page__header">
        <h1 className="page__title">О проекте</h1>
        <p className="page__subtitle">ShopReact — учебный интернет-магазин</p>
      </div>

      <div className="about-grid">
        <div className="about-section">
          <h2 className="about-section__title">Описание</h2>
          <p className="about-section__text">
            ShopReact — демонстрационное приложение интернет-магазина,
            разработанное в рамках курса «Разработка прототипов программных решений».
          </p>
          <p className="about-section__text">
            Проект демонстрирует ключевые концепции React: маршрутизацию,
            асинхронную загрузку данных, глобальное состояние через Context API
            и реактивный пользовательский интерфейс.
          </p>
        </div>

        <div className="about-section">
          <h2 className="about-section__title">Технологии</h2>
          <ul className="tech-list">
            <li className="tech-list__item">
              <span className="tech-badge">React 18</span>
              Компоненты, хуки, Context API
            </li>
            <li className="tech-list__item">
              <span className="tech-badge">React Router v6</span>
              Клиентская маршрутизация, NavLink
            </li>
            <li className="tech-list__item">
              <span className="tech-badge">Context API</span>
              Глобальное состояние и темы
            </li>
            <li className="tech-list__item">
              <span className="tech-badge">Fake Store API</span>
              REST API с товарами
            </li>
            <li className="tech-list__item">
              <span className="tech-badge">Vite</span>
              Сборка и запуск проекта
            </li>
          </ul>
        </div>

        <div className="about-section">
          <h2 className="about-section__title">Функционал</h2>
          <ul className="feature-list">
            <li className="feature-list__item">✅ Каталог товаров с поиском и фильтрами</li>
            <li className="feature-list__item">✅ Сортировка по цене и рейтингу</li>
            <li className="feature-list__item">✅ Детальная страница товара</li>
            <li className="feature-list__item">✅ Добавление в избранное (Context API)</li>
            <li className="feature-list__item">✅ Светлая / тёмная тема</li>
            <li className="feature-list__item">✅ Кэш данных без повторных запросов</li>
            <li className="feature-list__item">✅ Спиннер и обработка ошибок</li>
          </ul>
        </div>

        <div className="about-section">
          <h2 className="about-section__title">API</h2>
          <p className="about-section__text">
            Данные получены из открытого API Fake Store:
          </p>
          <code className="about-api-url">https://fakestoreapi.com</code>
          <p className="about-section__text" style={{ marginTop: '12px' }}>
            Эндпоинты:
          </p>
          <ul className="about-endpoints">
            <li><code>GET /products</code> — список всех товаров</li>
            <li><code>GET /products/:id</code> — товар по ID</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default About
