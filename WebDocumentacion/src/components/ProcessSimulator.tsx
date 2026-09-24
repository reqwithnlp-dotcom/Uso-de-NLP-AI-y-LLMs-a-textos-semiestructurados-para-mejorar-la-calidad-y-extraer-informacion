import { useEffect, useRef, useState } from 'react'
import { serviceSimulations } from '../services/processSimulations.data'

interface ProcessSimulatorProps {
  serviceId?: string
}

export default function ProcessSimulator({ serviceId }: ProcessSimulatorProps) {
  const simulation = serviceId ? serviceSimulations[serviceId] : undefined
  const [currentStepIndex, setCurrentStepIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  // Velocidad inicial pausada/tranquila: 3500ms
  const [speed, setSpeed] = useState<number>(3500)
  const [copied, setCopied] = useState(false)
  const timerRef = useRef<number | null>(null)

  useEffect(() => {
    // Reset state whenever serviceId changes
    setCurrentStepIndex(0)
    setIsPlaying(false)
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
  }, [serviceId])

  useEffect(() => {
    if (isPlaying) {
      timerRef.current = window.setInterval(() => {
        setCurrentStepIndex((prev) => {
          if (!simulation || prev >= simulation.steps.length - 1) {
            setIsPlaying(false)
            return prev
          }
          return prev + 1
        })
      }, speed)
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }, [isPlaying, speed, simulation])

  if (!simulation) {
    return null
  }

  const steps = simulation.steps
  const activeStep = steps[currentStepIndex] || steps[0]
  const isFirstStep = currentStepIndex === 0
  const isLastStep = currentStepIndex === steps.length - 1

  const handlePlayToggle = () => {
    if (isLastStep) {
      setCurrentStepIndex(0)
      setIsPlaying(true)
    } else {
      setIsPlaying(!isPlaying)
    }
  }

  const handleNext = () => {
    setIsPlaying(false)
    if (!isLastStep) {
      setCurrentStepIndex((prev) => prev + 1)
    }
  }

  const handlePrev = () => {
    setIsPlaying(false)
    if (!isFirstStep) {
      setCurrentStepIndex((prev) => prev - 1)
    }
  }

  const handleReset = () => {
    setIsPlaying(false)
    setCurrentStepIndex(0)
  }

  const handleCopyJson = () => {
    if (activeStep.resultPreview) {
      navigator.clipboard.writeText(JSON.stringify(activeStep.resultPreview, null, 2))
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const renderVisualResult = (data: any) => {
    if (!data) return null

    // Caso 1: Array (ej: POV Shift)
    if (Array.isArray(data)) {
      return (
        <div className="sim-visual-cards">
          {data.map((item, idx) => (
            <div key={idx} className="sim-res-card highlight">
              <div className="sim-res-card-head">
                <span className="sim-res-badge warning">Salto de Punto de Vista Detectado</span>
                <span className="sim-res-conf">Certeza: {Math.round((item.confidence || 0.85) * 100)}%</span>
              </div>
              <div className="sim-res-transition">
                <span className="sim-res-entity origin">{item.from_character?.canonical_name || 'Personaje A'}</span>
                <span className="sim-res-arrow">➔</span>
                <span className="sim-res-entity dest">{item.to_character?.canonical_name || 'Personaje B'}</span>
              </div>
              {item.evidence && (
                <div className="sim-res-evidence">
                  {item.evidence.map((ev: string, eIdx: number) => (
                    <span key={eIdx} className="sim-ev-pill">✓ {ev}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )
    }

    // Caso 2: Conectores lógicos
    if (data.connectors_found) {
      return (
        <div className="sim-visual-cards">
          <div className="sim-res-card success">
            <span className="sim-res-badge success">Conectores Encontrados: {data.total || data.connectors_found.length}</span>
            <div className="sim-pills-row">
              {data.connectors_found.map((c: any, idx: number) => (
                <div key={idx} className="sim-pill-group">
                  <span className="sim-pill-main">"{c.connector}"</span>
                  <span className="sim-pill-sub">Tipo: {c.type}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )
    }

    // Caso 3: Verbos débiles
    if (data.weak_verbs && data.suggestions) {
      return (
        <div className="sim-visual-cards">
          <div className="sim-res-card warning">
            <span className="sim-res-badge warning">Verbos Débiles Identificados ({data.total || data.weak_verbs.length})</span>
            <div className="sim-pills-row">
              {data.weak_verbs.map((v: string, idx: number) => (
                <div key={idx} className="sim-pill-group">
                  <span className="sim-pill-main weak">"{v}"</span>
                  <span className="sim-pill-sub suggest">Sugerencia: {data.suggestions[v] || 'acción directa'}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )
    }

    // Caso 4: Palabras abstractas
    if (data.results && Array.isArray(data.results)) {
      return (
        <div className="sim-visual-cards">
          <div className="sim-res-card success">
            <span className="sim-res-badge success">{data.results.length} Palabras Abstractas Detectadas</span>
            <div className="sim-chips-flow">
              {data.results.map((w: string, idx: number) => (
                <span key={idx} className="sim-chip-match">✨ {w}</span>
              ))}
            </div>
          </div>
        </div>
      )
    }

    // Caso 5: Voz pasiva
    if (typeof data.is_passive === 'boolean') {
      return (
        <div className="sim-visual-cards">
          <div className={`sim-res-card ${data.is_passive ? 'warning' : 'success'}`}>
            <span className={`sim-res-badge ${data.is_passive ? 'warning' : 'success'}`}>
              {data.is_passive ? 'Voz Pasiva Detectada (True)' : 'Voz Activa (False)'}
            </span>
            <p className="sim-res-note">
              {data.is_passive
                ? `Construcción localizada en posición de caracteres ${JSON.stringify(data.positions || [])}`
                : 'La oración no contiene estructuras verbales pasivas.'}
            </p>
          </div>
        </div>
      )
    }

    // Caso 6: Oraciones impersonales
    if (data.category && data.confidence) {
      return (
        <div className="sim-visual-cards">
          <div className="sim-res-card warning">
            <span className="sim-res-badge warning">Clasificación: {data.category.toUpperCase()}</span>
            <span className="sim-res-conf">Certeza del modelo: {Math.round(data.confidence * 100)}%</span>
            <p className="sim-res-note">Estructura sintáctica sin sujeto ejecutor definido en la oración analizada.</p>
          </div>
        </div>
      )
    }

    // Caso 7: Repetición de palabras
    if (data.repeated_words) {
      return (
        <div className="sim-visual-cards">
          <div className="sim-res-card warning">
            <span className="sim-res-badge warning">Palabras Reiteradas Detectadas</span>
            <div className="sim-pills-row">
              {data.repeated_words.map((item: any, idx: number) => (
                <div key={idx} className="sim-pill-group">
                  <span className="sim-pill-main">"{item.word}"</span>
                  <span className="sim-pill-sub">{item.count} apariciones · Posiciones {JSON.stringify(item.positions)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )
    }

    // Caso 8: Verbos modales inconsistentes
    if (data.inconsistencies) {
      return (
        <div className="sim-visual-cards">
          {data.inconsistencies.map((inc: any, idx: number) => (
            <div key={idx} className="sim-res-card warning">
              <span className="sim-res-badge warning">Inconsistencia Modal Detectada</span>
              <p className="sim-res-action">Acción compartida: <strong>"{inc.shared_action}"</strong></p>
              <div className="sim-modal-vs">
                <div className="sim-modal-case">
                  <span className="case-lbl">Caso 1</span>
                  <strong className="case-val">{inc.case_1?.modal}</strong>
                  <span className="case-cat">{inc.case_1?.category}</span>
                </div>
                <span className="sim-vs-sign">≠</span>
                <div className="sim-modal-case">
                  <span className="case-lbl">Caso 2</span>
                  <strong className="case-val">{inc.case_2?.modal}</strong>
                  <span className="case-cat">{inc.case_2?.category}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )
    }

    // Caso 9: Tiempos verbales inconsistentes
    if (data.issues && Array.isArray(data.issues)) {
      return (
        <div className="sim-visual-cards">
          {data.issues.map((iss: any, idx: number) => (
            <div key={idx} className="sim-res-card warning">
              <div className="sim-res-card-head">
                <span className="sim-res-badge warning">Código: {iss.error_code}</span>
                <span className="sim-res-conf">Posición: {iss.position}</span>
              </div>
              <p className="sim-res-note"><strong>Verbos en conflicto:</strong> "{iss.fragment}"</p>
              <p className="sim-res-desc">{iss.explanation}</p>
            </div>
          ))}
        </div>
      )
    }

    // Caso 10: Clichés
    if (data.cliches_detected) {
      return (
        <div className="sim-visual-cards">
          <div className="sim-res-card warning">
            <span className="sim-res-badge warning">Clichés y Expresiones Trilladas</span>
            <div className="sim-pills-row">
              {data.cliches_detected.map((cl: any, idx: number) => (
                <div key={idx} className="sim-pill-group">
                  <span className="sim-pill-main">"{cl.text}"</span>
                  <span className="sim-pill-sub">Sugerencia: {cl.suggestion} ({Math.round(cl.confidence * 100)}%)</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )
    }

    // Caso 11: Adverbios
    if (data.adverbs) {
      return (
        <div className="sim-visual-cards">
          <div className="sim-res-card success">
            <span className="sim-res-badge success">{data.total || data.adverbs.length} Adverbios Clasificados</span>
            <div className="sim-chips-flow">
              {data.adverbs.map((adv: any, idx: number) => (
                <div key={idx} className="sim-pill-group">
                  <span className="sim-pill-main">"{adv.word}"</span>
                  <span className="sim-pill-sub">Categoría: {adv.category}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )
    }

    // Caso 12: Puntuación inusual
    if (typeof data.unusual_punctuation === 'boolean') {
      return (
        <div className="sim-visual-cards">
          <div className={`sim-res-card ${data.unusual_punctuation ? 'warning' : 'success'}`}>
            <span className={`sim-res-badge ${data.unusual_punctuation ? 'warning' : 'success'}`}>
              {data.unusual_punctuation ? 'Puntuación Inusual Detectada: True' : 'Puntuación Correcta'}
            </span>
            {data.positions && (
              <p className="sim-res-note">Signos o delimitadores involucrados: <strong>{JSON.stringify(data.positions)}</strong></p>
            )}
          </div>
        </div>
      )
    }

    // Fallback genérico para cualquier otro objeto
    return (
      <div className="sim-visual-cards">
        <div className="sim-res-card success">
          <span className="sim-res-badge success">Procesamiento Completado</span>
          <div className="sim-generic-grid">
            {Object.entries(data).slice(0, 4).map(([k, v], idx) => (
              <div key={idx} className="sim-generic-item">
                <span className="sim-generic-k">{k}:</span>
                <strong className="sim-generic-v">{typeof v === 'object' ? JSON.stringify(v) : String(v)}</strong>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="process-simulator" aria-label="Simulador visual interactivo">
      {/* Header Bar */}
      <div className="sim-header">
        <div className="sim-title-group">
          <span className="sim-pill">PIPELINE INTERACTIVO</span>
          <h3 className="sim-title">Simulación en vivo del proceso</h3>
        </div>
        <div className="sim-speed-controls">
          <span className="sim-speed-label">Velocidad:</span>
          <button
            type="button"
            className={`sim-speed-btn ${speed === 5000 ? 'active' : ''}`}
            onClick={() => setSpeed(5000)}
            title="5 segundos por paso"
          >
            Pausada (0.5x)
          </button>
          <button
            type="button"
            className={`sim-speed-btn ${speed === 3500 ? 'active' : ''}`}
            onClick={() => setSpeed(3500)}
            title="3.5 segundos por paso"
          >
            Moderada (0.8x)
          </button>
          <button
            type="button"
            className={`sim-speed-btn ${speed === 2400 ? 'active' : ''}`}
            onClick={() => setSpeed(2400)}
            title="2.4 segundos por paso"
          >
            Estándar (1.0x)
          </button>
        </div>
      </div>

      {/* Input preview */}
      <div className="sim-sample-box">
        <span className="sim-sample-tag">Texto de entrada:</span>
        <code className="sim-sample-text">"{simulation.sampleText}"</code>
      </div>

      {/* Progress Timeline */}
      <div className="sim-timeline">
        <div
          className="sim-progress-bar"
          style={{ width: `${(currentStepIndex / (steps.length - 1)) * 100}%` }}
        />
        {steps.map((step, idx) => {
          const isDone = idx < currentStepIndex
          const isCurrent = idx === currentStepIndex
          return (
            <button
              key={step.stepNumber}
              type="button"
              className={`sim-step-node ${isCurrent ? 'active' : ''} ${isDone ? 'done' : ''}`}
              onClick={() => {
                setIsPlaying(false)
                setCurrentStepIndex(idx)
              }}
              title={step.title}
            >
              <span className="sim-node-dot">
                {isDone ? '✓' : step.stepNumber}
              </span>
              <span className="sim-node-label">{step.title}</span>
            </button>
          )
        })}
      </div>

      {/* Dynamic Stage Canvas */}
      <div className="sim-stage-card">
        <div className="sim-stage-header">
          <div className="sim-stage-badge-group">
            <span className="sim-stage-badge">{activeStep.badge}</span>
            <span className="sim-stage-counter">
              Paso {activeStep.stepNumber} de {steps.length}
            </span>
          </div>
          <h4 className="sim-stage-title">{activeStep.title}</h4>
          <p className="sim-stage-desc">{activeStep.description}</p>
        </div>

        {/* Tokens visual stage */}
        {activeStep.tokens && activeStep.tokens.length > 0 && (
          <div className="sim-tokens-container">
            {activeStep.tokens.map((token, tIdx) => (
              <div
                key={`${token.text}-${tIdx}`}
                className={`sim-token-chip status-${token.status || 'default'}`}
              >
                <span className="sim-token-text">{token.text}</span>
                {token.tag && <span className="sim-token-tag">{token.tag}</span>}
                {token.dep && <span className="sim-token-dep">{token.dep}</span>}
                {token.detail && <span className="sim-token-detail">{token.detail}</span>}
              </div>
            ))}
          </div>
        )}

        {/* Metrics Grid */}
        {activeStep.metrics && activeStep.metrics.length > 0 && (
          <div className="sim-metrics-grid">
            {activeStep.metrics.map((m, mIdx) => (
              <div key={mIdx} className="sim-metric-item">
                <span className="sim-metric-label">{m.label}</span>
                <strong className="sim-metric-val">{m.value}</strong>
              </div>
            ))}
          </div>
        )}

        {/* Annotation callout */}
        {activeStep.annotation && (
          <div className="sim-annotation-box">
            <span className="sim-annotation-icon">ℹ</span>
            <p className="sim-annotation-text">{activeStep.annotation}</p>
          </div>
        )}

        {/* Result Stage: Visual Representation First + Smaller JSON below */}
        {activeStep.resultPreview && (
          <div className="sim-result-stage">
            <div className="sim-visual-result-section">
              <span className="sim-result-section-title">Resultado de la Detección</span>
              {renderVisualResult(activeStep.resultPreview)}
            </div>

            <div className="sim-compact-json-section">
              <div className="sim-compact-json-header">
                <span className="sim-json-tag">JSON devuelto por el servicio (compacto)</span>
                <button
                  type="button"
                  className="sim-copy-btn"
                  onClick={handleCopyJson}
                >
                  {copied ? '¡Copiado!' : 'Copiar JSON'}
                </button>
              </div>
              <pre className="sim-json-block-compact">
                <code>{JSON.stringify(activeStep.resultPreview, null, 2)}</code>
              </pre>
            </div>
          </div>
        )}
      </div>

      {/* Control Buttons Footer */}
      <div className="sim-footer">
        <div className="sim-actions-left">
          <button
            type="button"
            className="sim-control-btn primary"
            onClick={handlePlayToggle}
          >
            {isPlaying ? (
              <>
                <span className="sim-btn-icon">⏸</span> Pausar
              </>
            ) : isLastStep ? (
              <>
                <span className="sim-btn-icon">↺</span> Repetir proceso
              </>
            ) : (
              <>
                <span className="sim-btn-icon">▶</span> Reproducir animación
              </>
            )}
          </button>
          <button
            type="button"
            className="sim-control-btn"
            onClick={handleReset}
            disabled={isFirstStep}
          >
            Reiniciar
          </button>
        </div>

        <div className="sim-actions-right">
          <button
            type="button"
            className="sim-control-btn"
            onClick={handlePrev}
            disabled={isFirstStep}
          >
            ← Anterior
          </button>
          <button
            type="button"
            className="sim-control-btn"
            onClick={handleNext}
            disabled={isLastStep}
          >
            Siguiente →
          </button>
        </div>
      </div>
    </div>
  )
}
