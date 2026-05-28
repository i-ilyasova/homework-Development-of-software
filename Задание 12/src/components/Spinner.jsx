function Spinner({ text = 'Загрузка...' }) {
  return (
    <div className="spinner-wrap">
      <div className="spinner" />
      <p className="spinner__text">{text}</p>
    </div>
  )
}

export default Spinner
