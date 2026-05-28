import { memo } from 'react'

function ErrorMessage({ message, onRetry }) {
  return (
    <div className="error-block">
      <div className="error-block__icon">⚠️</div>
      <h2 className="error-block__title">Что-то пошло не так</h2>
      <p className="error-block__message">{message}</p>
      {onRetry && (
        <button className="btn btn--primary" onClick={onRetry}>
          Попробовать снова
        </button>
      )}
    </div>
  )
}

export default memo(ErrorMessage)
