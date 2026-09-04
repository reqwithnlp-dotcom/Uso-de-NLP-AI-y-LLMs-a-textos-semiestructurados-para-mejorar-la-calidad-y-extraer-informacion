import { Link } from 'react-router-dom'
import type { ServiceConfig } from '../services/services.config'

export default function ServiceCard({ service, index }: { service: ServiceConfig; index: number }) {
  return (
    <Link className="service-card" to={`/servicio/${service.id}`}>
      <span className="card-index">{String(index + 1).padStart(2, '0')}</span>
      <h2>{service.name}</h2>
      <p>{service.shortDescription}</p>
      <span className="card-arrow">↗</span>
    </Link>
  )
}
