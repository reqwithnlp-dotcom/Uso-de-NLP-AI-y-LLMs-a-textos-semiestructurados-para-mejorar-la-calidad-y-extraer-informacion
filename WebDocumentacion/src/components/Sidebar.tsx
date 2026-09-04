import { NavLink, useLocation } from 'react-router-dom'
import { services } from '../services/services.config'

export default function Sidebar() {
  const { pathname } = useLocation()
  const isServicePage = pathname.startsWith('/servicio/')

  return (
    <aside className="sidebar">
      <div className="brand-mark">NLP / DOCS</div>
      <div className="sidebar-heading">
        <span>Servicios</span>
        <span className="service-count">{services.length.toString().padStart(2, '0')}</span>
      </div>
      <nav aria-label="Servicios disponibles">
        {services.map((service) => (
          <NavLink
            key={service.id}
            to={`/servicio/${service.id}`}
            className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
          >
            <span className="link-index">{String(services.indexOf(service) + 1).padStart(2, '0')}</span>
            <span>{service.name}</span>
          </NavLink>
        ))}
      </nav>
      {isServicePage && <NavLink to="/" className="home-link">← Inicio</NavLink>}
    </aside>
  )
}
