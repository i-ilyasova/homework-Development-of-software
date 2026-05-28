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
            Приложение оптимизировано с помощью React.memo, useMemo, useCallback
            и ленивой загрузки страниц через React.lazy + Suspense.
          </p>
        </div>

        <div className="about-section">
          <h2 className="about-section__title">Технологии</h2>
          <ul className="tech-list">
            <li className="tech-list__item"><span className="tech-badge">React 18</span> Компоненты, хуки, Context API</li>
            <li className="tech-list__item"><span className="tech-badge">React Router v6</span> Клиентская маршрутизация</li>
            <li className="tech-list__item"><span className="tech-badge">React.lazy</span> Ленивая загрузка страниц</li>
            <li className="tech-list__item"><span className="tech-badge">localStorage</span> Сохранение избранного</li>
            <li className="tech-list__item"><span className="tech-badge">Jest + RTL</span> Unit-тестирование</li>
            <li className="tech-list__item"><span className="tech-badge">Vite</span> Сборка проекта</li>
          </ul>
        </div>

        <div className="about-section">
          <h2 className="about-section__title">Функционал</h2>
          <ul className="feature-list">
            <li className="feature-list__item">✅ Каталог с поиском, фильтрами и сортировкой</li>
            <li className="feature-list__item">✅ Детальная страница товара</li>
            <li className="feature-list__item">✅ Страница избранного (/favourites)</li>
            <li className="feature-list__item">✅ localStorage — избранное между сессиями</li>
            <li className="feature-list__item">✅ Светлая / тёмная тема</li>
            <li className="feature-list__item">✅ Мемоизация и ленивая загрузка</li>
            <li className="feature-list__item">✅ Покрытие тестами Jest + RTL</li>
          </ul>
        </div>

        <div className="about-section">
          <h2 className="about-section__title">API</h2>
          <p className="about-section__text">Данные получены из открытого Fake Store API:</p>
          <code className="about-api-url">https://fakestoreapi.com</code>
          <ul className="about-endpoints" style={{ marginTop: '12px' }}>
            <li><code>GET /products</code> — список всех товаров</li>
            <li><code>GET /products/:id</code> — товар по ID</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default About
