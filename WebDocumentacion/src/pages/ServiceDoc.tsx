import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { services } from '../services/services.config'

export default function ServiceDoc() {
  const { id } = useParams()
  const service = services.find((item) => item.id === id)
  const [markdown, setMarkdown] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    if (!service) return
    setMarkdown('')
    setError('')
    const markdownUrl = `${import.meta.env.BASE_URL}${service.markdownPath.replace(/^\/+/, '')}`
    fetch(markdownUrl)
      .then((response) => {
        if (!response.ok) throw new Error('No se pudo cargar la documentación.')
        return response.text()
      })
      .then(setMarkdown)
      .catch((reason: Error) => setError(reason.message))
  }, [service])

  if (!service) {
    return <section className="empty-state page-container"><p className="eyebrow">404 · Servicio no encontrado</p><h1>Esta documentación no existe.</h1><Link to="/">Volver al inicio</Link></section>
  }

  return (
    <article className="doc-page page-container">
      <header className="doc-header">
        <p className="eyebrow">Servicio {String(services.indexOf(service) + 1).padStart(2, '0')} / {String(services.length).padStart(2, '0')}</p>
        <h1>{service.name}</h1>
        <p className="doc-description">{service.shortDescription}</p>
      </header>
      {error ? <div className="error-box">{error}</div> : markdown ? <div className="markdown-body"><ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown></div> : <div className="loading">Cargando documentación...</div>}
    </article>
  )
}
