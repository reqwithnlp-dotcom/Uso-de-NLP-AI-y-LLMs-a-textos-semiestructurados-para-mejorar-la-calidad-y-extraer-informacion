import type { ReactNode } from 'react'
import { useTheme, type ThemeMode } from '../context/ThemeContext'

export default function ThemeToggle() {
  const { mode, resolvedTheme, setMode } = useTheme()

  const options: { id: ThemeMode; label: string; icon: ReactNode; tooltip: string }[] = [
    {
      id: 'system',
      label: 'Auto',
      tooltip: `Sistema (actual: ${resolvedTheme === 'dark' ? 'oscuro' : 'claro'})`,
      icon: (
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
          <line x1="8" y1="21" x2="16" y2="21" />
          <line x1="12" y1="17" x2="12" y2="21" />
        </svg>
      ),
    },
    {
      id: 'light',
      label: 'Claro',
      tooltip: 'Tema claro',
      icon: (
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="4" />
          <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
        </svg>
      ),
    },
    {
      id: 'dark',
      label: 'Oscuro',
      tooltip: 'Tema oscuro',
      icon: (
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      ),
    },
  ]

  return (
    <div className="theme-toggle-wrapper" aria-label="Selector de tema">
      <div className="theme-toggle-container" role="radiogroup" aria-label="Tema visual">
        {options.map((opt) => {
          const isActive = mode === opt.id
          return (
            <button
              key={opt.id}
              type="button"
              role="radio"
              aria-checked={isActive}
              title={opt.tooltip}
              className={`theme-toggle-btn${isActive ? ' active' : ''}`}
              onClick={() => setMode(opt.id)}
            >
              <span className="theme-toggle-icon">{opt.icon}</span>
              <span className="theme-toggle-label">{opt.label}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
