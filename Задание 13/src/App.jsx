import { Routes, Route } from 'react-router-dom'
import { useContext, lazy, Suspense } from 'react'
import { AppContext } from './context/AppContext'
import Navbar from './components/Navbar'
import Spinner from './components/Spinner'

const Home       = lazy(() => import('./pages/Home'))
const List       = lazy(() => import('./pages/List'))
const Details    = lazy(() => import('./pages/Details'))
const About      = lazy(() => import('./pages/About'))
const Favourites = lazy(() => import('./pages/Favourites'))

function App() {
  const { theme } = useContext(AppContext)

  return (
    <div data-theme={theme} className="app">
      <Navbar />
      <main className="main-content">
        <Suspense fallback={<Spinner text="Загрузка страницы..." />}>
          <Routes>
            <Route path="/"           element={<Home />} />
            <Route path="/list"       element={<List />} />
            <Route path="/list/:id"   element={<Details />} />
            <Route path="/favourites" element={<Favourites />} />
            <Route path="/about"      element={<About />} />
          </Routes>
        </Suspense>
      </main>
    </div>
  )
}

export default App
