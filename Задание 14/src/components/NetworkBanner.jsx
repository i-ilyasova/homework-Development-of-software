import { useState, useEffect } from 'react'
import { useNetworkStatus } from '../hooks/useNetworkStatus'

function NetworkBanner() {
  const isOnline  = useNetworkStatus()
  const [visible, setVisible] = useState(false)
  const [prev,    setPrev]    = useState(null)

  useEffect(() => {
    if (prev === null) {
      setPrev(isOnline)
      return
    }
    if (prev !== isOnline) {
      setVisible(true)
      setPrev(isOnline)
      if (isOnline) {
        const t = setTimeout(() => setVisible(false), 3000)
        return () => clearTimeout(t)
      }
    }
  }, [isOnline])

  if (!visible && isOnline) return null
  if (!visible) return null

  return (
    <div className={`network-banner network-banner--${isOnline ? 'online' : 'offline'}`}>
      {isOnline
        ? '✅ Соединение восстановлено'
        : '📡 Вы в офлайне — данные загружаются из кеша'}
    </div>
  )
}

export default NetworkBanner
