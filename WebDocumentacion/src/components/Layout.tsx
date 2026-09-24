import type { ReactNode } from 'react'
import { useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'
import ThemeToggle from './ThemeToggle'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { pathname } = useLocation()
  const isHome = pathname === '/'

  return (
    <div className={`app-shell${isHome ? ' app-shell--no-sidebar' : ''}`}>
      <ThemeToggle />
      {!isHome && <Sidebar />}
      <main className="main-content">{children}</main>
    </div>
  )
}


