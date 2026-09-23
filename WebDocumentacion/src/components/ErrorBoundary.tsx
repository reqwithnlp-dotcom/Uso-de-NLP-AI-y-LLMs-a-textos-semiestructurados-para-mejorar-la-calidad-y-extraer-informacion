import { Component, type ErrorInfo, type ReactNode } from 'react'
import { Link } from 'react-router-dom'

interface Props {
  children: ReactNode
  fallbackTitle?: string
}

interface State {
  hasError: boolean
  error: Error | null
}

export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary capturó un error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <section className="error-boundary-box page-container">
          <p className="eyebrow">Error de Renderizado</p>
          <h2>{this.props.fallbackTitle || 'Ocurrió un error al cargar esta sección.'}</h2>
          <div className="error-box" style={{ marginTop: '16px', marginBottom: '24px' }}>
            <code>{this.state.error?.message || 'Error desconocido'}</code>
          </div>
          <div style={{ display: 'flex', gap: '16px' }}>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              style={{
                background: '#173c35',
                color: '#fff',
                padding: '10px 18px',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontFamily: 'inherit',
                fontWeight: 600,
              }}
            >
              Reintentar
            </button>
            <Link
              to="/"
              style={{
                padding: '10px 18px',
                color: '#173c35',
                fontWeight: 600,
                textDecoration: 'underline',
              }}
            >
              Volver al inicio
            </Link>
          </div>
        </section>
      )
    }

    return this.props.children
  }
}
