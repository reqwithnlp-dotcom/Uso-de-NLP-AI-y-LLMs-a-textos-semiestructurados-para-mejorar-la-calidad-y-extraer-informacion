import { services } from '../services/services.config'
import ServiceCard from '../components/ServiceCard'

export default function Home() {
  return (
    <section className="home-page page-container">
      <p className="eyebrow">Documentación técnica · Proyecto de investigación</p>
      <div className="home-intro">
        <div>
          <h1>Uso de <br /><em>NLP AI y LLMs</em> a textos semiestructurados.</h1>
        </div>
      </div>
      <div className="section-rule"><span>Servicios</span><span>{services.length} disponible{services.length === 1 ? '' : 's'}</span></div>
      <div className="service-grid">
        {services.map((service, index) => <ServiceCard key={service.id} service={service} index={index} />)}
      </div>
    </section>
  )
}
