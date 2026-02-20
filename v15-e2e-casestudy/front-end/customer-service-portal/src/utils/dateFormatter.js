/**
 * Format an ISO 8601 timestamp to a human-readable time string.
 * e.g. "10:30 AM"
 * @param {string} isoString
 * @returns {string}
 */
export const formatTime = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

/**
 * Format an ISO 8601 timestamp to a date + time string.
 * e.g. "Feb 20, 2026, 10:30 AM"
 * @param {string} isoString
 * @returns {string}
 */
export const formatDateTime = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleString([], {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Return a relative time label (e.g. "5 mins ago", "Just now").
 * @param {string} isoString
 * @returns {string}
 */
export const formatRelativeTime = (isoString) => {
  if (!isoString) return ''
  const diff = Date.now() - new Date(isoString).getTime()
  const minutes = Math.floor(diff / 60_000)
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes} min${minutes > 1 ? 's' : ''} ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} hr${hours > 1 ? 's' : ''} ago`
  const days = Math.floor(hours / 24)
  return `${days} day${days > 1 ? 's' : ''} ago`
}
