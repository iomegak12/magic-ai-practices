/**
 * Reusable loading spinner component.
 * @param {object} props
 * @param {string} [props.size='md']    - 'sm' | 'md' | 'lg'
 * @param {string} [props.label]        - Screen-reader label
 * @param {boolean} [props.overlay]     - If true, renders as a full-overlay loader
 */
const Loader = ({ size = 'md', label = 'Loading...', overlay = false }) => {
  const sizeClass = size === 'sm' ? 'spinner-border-sm' : ''

  const spinner = (
    <div className={`spinner-border text-primary ${sizeClass}`} role="status">
      <span className="visually-hidden">{label}</span>
    </div>
  )

  if (overlay) {
    return (
      <div
        className="d-flex align-items-center justify-content-center"
        style={{ position: 'absolute', inset: 0, background: 'rgba(255,255,255,0.6)', zIndex: 10 }}
      >
        {spinner}
      </div>
    )
  }

  return (
    <div className="d-flex align-items-center justify-content-center py-3">
      {spinner}
    </div>
  )
}

export default Loader
