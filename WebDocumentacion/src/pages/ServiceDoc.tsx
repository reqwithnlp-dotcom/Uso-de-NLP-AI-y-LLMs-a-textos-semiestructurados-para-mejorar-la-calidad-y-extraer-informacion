import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { services } from '../services/services.config'
import ErrorBoundary from '../components/ErrorBoundary'
import ProcessSimulator from '../components/ProcessSimulator'

export default function ServiceDoc() {
  const { id } = useParams()
  const service = services.find((item) => item.id === id)
  const [markdown, setMarkdown] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!service) return
    let isCancelled = false
    setIsLoading(true)
    setMarkdown('')
    setError('')

    const markdownUrl = `${import.meta.env.BASE_URL}${service.markdownPath.replace(/^\/+/, '')}`

    fetch(markdownUrl, { cache: 'no-cache' })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`No se pudo cargar la documentación (${response.status} ${response.statusText}). URL: ${markdownUrl}`)
        }
        return response.text()
      })
      .then((text) => {
        if (!isCancelled) {
          setMarkdown(text)
          setIsLoading(false)
        }
      })
      .catch((reason: Error) => {
        if (!isCancelled) {
          setError(reason.message)
          setIsLoading(false)
        }
      })

    return () => {
      isCancelled = true
    }
  }, [service])

  if (!service) {
    return (
      <section className="empty-state page-container">
        <p className="eyebrow">404 · Servicio no encontrado</p>
        <h1>Esta documentación no existe.</h1>
        <Link to="/">Volver al inicio</Link>
      </section>
    )
  }

  const contentDir = service.markdownPath.substring(0, service.markdownPath.lastIndexOf('/') + 1).replace(/^\/+/, '')

  return (
    <article className="doc-page page-container">
      <header className="doc-header">
        <p className="eyebrow">
          Servicio {String(services.indexOf(service) + 1).padStart(2, '0')} / {String(services.length).padStart(2, '0')}
        </p>
        <h1>{service.name}</h1>
        <p className="doc-description">{service.shortDescription}</p>
      </header>

      {error ? (
        <div className="error-box">
          <p><strong>Error:</strong> {error}</p>
          <button
            onClick={() => {
              setError('')
              setIsLoading(true)
              const markdownUrl = `${import.meta.env.BASE_URL}${service.markdownPath.replace(/^\/+/, '')}`
              fetch(markdownUrl, { cache: 'no-cache' })
                .then((r) => r.text())
                .then(setMarkdown)
                .catch((e: Error) => setError(e.message))
                .finally(() => setIsLoading(false))
            }}
            style={{
              marginTop: '12px',
              padding: '6px 12px',
              background: '#b14f43',
              color: '#fff',
              border: 'none',
              borderRadius: '3px',
              cursor: 'pointer',
            }}
          >
            Reintentar carga
          </button>
        </div>
      ) : isLoading ? (
        <div className="loading">Cargando documentación...</div>
      ) : markdown ? (
        <ErrorBoundary fallbackTitle="Error al procesar el formato Markdown de este servicio">
          <div className="markdown-body">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                img: ({ node: _node, src, alt, title }) => {
                  let resolvedSrc = src || ''
                  if (resolvedSrc && !resolvedSrc.startsWith('http') && !resolvedSrc.startsWith('data:') && !resolvedSrc.startsWith('/')) {
                    resolvedSrc = `${import.meta.env.BASE_URL}${contentDir}${resolvedSrc}`
                  }
                  return <img src={resolvedSrc} alt={alt || ''} title={title} />
                },
                code: ({ className, children, ...props }) => {
                  if (className === 'language-process-demo') {
                    return <ProcessSimulator serviceId={service.id} />
                  }
                  return <code className={className} {...props}>{children}</code>
                },
                pre: ({ children, ...props }) => {
                  const childArray = Array.isArray(children) ? children : [children]
                  const hasSimulator = childArray.some(
                    (c: any) => c && typeof c === 'object' && c.props && c.props.className === 'language-process-demo'
                  )
                  if (hasSimulator) {
                    return <>{children}</>
                  }
                  return <pre {...props}>{children}</pre>
                },
              }}
            >
              {markdown}
            </ReactMarkdown>

            {/* Fallback en caso de que el markdown no contenga el bloque explícito */}
            {!markdown.includes('process-demo') && (
              <div style={{ marginTop: '40px' }}>
                <h2>Simulación interactiva del proceso</h2>
                <ProcessSimulator serviceId={service.id} />
              </div>
            )}
          </div>
        </ErrorBoundary>
      ) : (
        <div className="empty-state">No hay contenido disponible para este servicio.</div>
      )}
    </article>
  )
}
