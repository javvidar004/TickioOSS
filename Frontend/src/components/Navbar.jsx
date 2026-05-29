import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-blue-600 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <Link to="/" className="text-xl font-bold tracking-tight">
          🎫 TickioOSS
        </Link>
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link to="/tickets" className="hover:text-blue-200 transition">Tickets</Link>
              <Link to="/tickets/new" className="hover:text-blue-200 transition">New Ticket</Link>
              {(user.role === 'admin' || user.role === 'agent') && (
                <Link to="/dashboard" className="hover:text-blue-200 transition">Dashboard</Link>
              )}
              {user.role === 'admin' && (
                <Link to="/admin/users" className="hover:text-blue-200 transition">Users</Link>
              )}
              <span className="text-blue-200 text-sm">
                {user.username} ({user.role})
              </span>
              <button
                onClick={handleLogout}
                className="bg-white text-blue-600 px-3 py-1 rounded text-sm font-medium hover:bg-blue-50 transition"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-blue-200 transition">Login</Link>
              <Link to="/register" className="bg-white text-blue-600 px-3 py-1 rounded text-sm font-medium hover:bg-blue-50 transition">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
