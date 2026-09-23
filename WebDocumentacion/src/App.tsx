import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import ServiceDoc from './pages/ServiceDoc'
import ErrorBoundary from './components/ErrorBoundary'

function App() {
  return (
    <Layout>
      <ErrorBoundary fallbackTitle="Error al cargar la vista solicitada">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/servicio/:id" element={<ServiceDoc />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </ErrorBoundary>
    </Layout>
  )
}

export default App
