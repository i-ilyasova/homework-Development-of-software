# Lighthouse Audit Report — ShopReact

**URL:** https://shop-react.vercel.app  
**Дата:** 2025-05-27  
**Устройство:** Desktop

## Результаты

| Метрика | Результат |
|---|---|
| **Performance** | 94 / 100 |
| **Accessibility** | 95 / 100 |
| **Best Practices** | 100 / 100 |
| **SEO** | 91 / 100 |

## Core Web Vitals

| Метрика | Значение | Оценка |
|---|---|---|
| First Contentful Paint (FCP) | 0.6 с | ✅ Хорошо |
| Largest Contentful Paint (LCP) | 1.2 с | ✅ Хорошо |
| Total Blocking Time (TBT) | 10 мс | ✅ Хорошо |
| Cumulative Layout Shift (CLS) | 0.01 | ✅ Хорошо |
| Speed Index | 0.9 с | ✅ Хорошо |

## Применённые оптимизации

### Performance
- **React.lazy + Suspense** — страницы загружаются по требованию, уменьшает initial bundle
- **React.memo** — Navbar, ProductCard, Spinner, ErrorMessage не перерисовываются без изменений пропсов
- **useMemo** — фильтрация и сортировка товаров пересчитывается только при изменении данных
- **useCallback** — функции-обработчики стабильны между рендерами
- **Кэш данных** — список товаров загружается один раз, повторные переходы в каталог не делают запрос к API
- **Vite production build** — tree-shaking, minification, code splitting

### Accessibility
- Все интерактивные элементы имеют `aria-label`
- Кнопки бургера: `aria-label="Меню"`
- Кнопка темы: `aria-label="Сменить тему"`
- Кнопка удаления из избранного: `aria-label="Удалить из избранного"`
- Контрастное соотношение цветов соответствует WCAG AA
- Семантическая разметка: `<nav>`, `<main>`, `<h1>`–`<h3>`

## Рекомендации для дальнейшей оптимизации

- Добавить `<meta name="description">` для улучшения SEO
- Указать явные размеры изображений (width/height) для снижения CLS
- Подключить Service Worker для офлайн-поддержки
