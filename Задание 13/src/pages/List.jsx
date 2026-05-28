import { useContext, useEffect, useState, useMemo, useCallback } from 'react'
import { AppContext } from '../context/AppContext'
import ProductCard from '../components/ProductCard'
import Spinner from '../components/Spinner'
import ErrorMessage from '../components/ErrorMessage'

const API_URL = 'https://fakestoreapi.com/products'

function List() {
  const { products, setProducts } = useContext(AppContext)
  const [loading,  setLoading]  = useState(products.length === 0)
  const [error,    setError]    = useState(null)
  const [search,   setSearch]   = useState('')
  const [category, setCategory] = useState('all')
  const [sort,     setSort]     = useState('default')

  const loadProducts = useCallback(() => {
    setLoading(true)
    setError(null)
    fetch(API_URL)
      .then(res => {
        if (!res.ok) throw new Error(`Ошибка ${res.status}: не удалось загрузить товары`)
        return res.json()
      })
      .then(data => { setProducts(data); setLoading(false) })
      .catch(err  => { setError(err.message); setLoading(false) })
  }, [setProducts])

  useEffect(() => {
    if (products.length === 0) loadProducts()
  }, [])

  const categories = useMemo(
    () => ['all', ...new Set(products.map(p => p.category))],
    [products]
  )

  const filtered = useMemo(() => {
    let result = products.filter(p => {
      const matchSearch = p.title.toLowerCase().includes(search.toLowerCase())
      const matchCat    = category === 'all' || p.category === category
      return matchSearch && matchCat
    })
    if (sort === 'price-asc')  result = [...result].sort((a, b) => a.price - b.price)
    if (sort === 'price-desc') result = [...result].sort((a, b) => b.price - a.price)
    if (sort === 'rating')     result = [...result].sort((a, b) => b.rating.rate - a.rating.rate)
    return result
  }, [products, search, category, sort])

  const resetFilters = useCallback(() => { setSearch(''); setCategory('all') }, [])

  if (loading) return <Spinner text="Загружаем каталог..." />
  if (error)   return <ErrorMessage message={error} onRetry={loadProducts} />

  return (
    <div className="page page--list">
      <div className="page__header">
        <h1 className="page__title">Каталог товаров</h1>
        <p className="page__subtitle">Найдено: {filtered.length} из {products.length}</p>
      </div>

      <div className="filters">
        <input
          type="text"
          className="filters__search"
          placeholder="Поиск по названию..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <select className="filters__select" value={sort} onChange={e => setSort(e.target.value)}>
          <option value="default">По умолчанию</option>
          <option value="price-asc">Цена: по возрастанию</option>
          <option value="price-desc">Цена: по убыванию</option>
          <option value="rating">Рейтинг: сначала лучшие</option>
        </select>
        <div className="filters__categories">
          {categories.map(cat => (
            <button
              key={cat}
              className={`filters__chip ${category === cat ? 'filters__chip--active' : ''}`}
              onClick={() => setCategory(cat)}
            >
              {cat === 'all' ? 'Все' : cat}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="no-results">
          <div className="no-results__icon">🔍</div>
          <p>Ничего не найдено по вашему запросу</p>
          <button className="btn btn--ghost" onClick={resetFilters}>Сбросить фильтры</button>
        </div>
      ) : (
        <div className="product-grid">
          {filtered.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  )
}

export default List
