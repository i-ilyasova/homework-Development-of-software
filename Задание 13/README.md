# ShopReact v2

Учебное React-приложение интернет-магазина с оптимизацией, тестами и деплоем.  
Разработано в рамках курса «Разработка прототипов программных решений», ДЗ 13.

## Быстрый старт

```bash
npm install
npm run dev
```

Приложение откроется на `http://localhost:5173`.

## Команды

| Команда | Описание |
|---|---|
| `npm run dev` | Запуск dev-сервера |
| `npm run build` | Production-сборка |
| `npm run preview` | Предпросмотр production-сборки |
| `npm test` | Запуск тестов |
| `npm run test:watch` | Тесты в режиме watch |
| `npm run test:coverage` | Тесты с отчётом о покрытии |

## Деплой

Приложение задеплоено на **Vercel**:

**🔗 https://shop-react.vercel.app**

### Как задеплоить самостоятельно

**Vercel (рекомендуется):**
```bash
npm i -g vercel
npm run build
vercel deploy --prod
```

**Netlify:**
```bash
npm run build
# Перетащить папку dist/ на netlify.com/drop
```

**GitHub Pages:**
```bash
# В vite.config.js добавить: base: '/repo-name/'
npm run build
# Загрузить содержимое dist/ в ветку gh-pages
```

## Структура

```
src/
├── context/
│   └── AppContext.jsx       # Состояние: товары, тема, избранное + localStorage
├── pages/
│   ├── Home.jsx             # Главная страница
│   ├── List.jsx             # Каталог (useMemo для фильтрации)
│   ├── Details.jsx          # Страница товара
│   ├── Favourites.jsx       # Страница избранного (/favourites)
│   └── About.jsx            # О проекте
├── components/
│   ├── Navbar.jsx           # React.memo + NavLink + бейдж избранного
│   ├── ProductCard.jsx      # React.memo + useCallback
│   ├── Spinner.jsx          # React.memo
│   └── ErrorMessage.jsx     # React.memo
├── styles/
│   └── main.css             # CSS custom properties, светлая/тёмная тема
├── __tests__/
│   ├── AppContext.test.jsx   # 9 тестов: состояние, localStorage
│   ├── ProductCard.test.jsx  # 8 тестов: рендер, кнопка избранного
│   ├── Navbar.test.jsx       # 10 тестов: ссылки, тема, бейдж
│   └── Favourites.test.jsx   # 9 тестов: список, удаление, пустое состояние
├── App.jsx                  # React.lazy + Suspense для всех страниц
└── main.jsx                 # Точка входа
```

## Маршруты

| Путь | Компонент | Описание |
|---|---|---|
| `/` | `<Home />` | Главная с hero-блоком |
| `/list` | `<List />` | Каталог: поиск, фильтр, сортировка |
| `/list/:id` | `<Details />` | Детали товара: описание, рейтинг, избранное |
| `/favourites` | `<Favourites />` | Список избранных товаров |
| `/about` | `<About />` | Описание проекта |

## Оптимизации (ДЗ 13)

### Мемоизация
- **`React.memo`** — `Navbar`, `ProductCard`, `Spinner`, `ErrorMessage`
- **`useMemo`** — фильтрация и сортировка в `List.jsx`
- **`useCallback`** — обработчики в `ProductCard`, `Favourites`, `List`, `Details`

### Ленивая загрузка
- **`React.lazy` + `Suspense`** — все страницы (`Home`, `List`, `Details`, `Favourites`, `About`)
- Каждая страница выделяется в отдельный chunk при сборке

### Состояние
- **`localStorage`** — избранное сохраняется между сеансами
- **Кэш данных** — список товаров загружается один раз (Context API)

## Тесты

```
PASS  src/__tests__/AppContext.test.jsx     (9 тестов)
PASS  src/__tests__/ProductCard.test.jsx    (8 тестов)
PASS  src/__tests__/Navbar.test.jsx        (10 тестов)
PASS  src/__tests__/Favourites.test.jsx     (9 тестов)

Test Suites: 4 passed
Tests:       36 passed
```

## Lighthouse

| | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Desktop | **94** | **95** | **100** | 91 |

Подробный отчёт: [lighthouse-report.md](./lighthouse-report.md)
