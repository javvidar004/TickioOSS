import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Home() {
  const { user } = useAuth()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex items-center justify-center px-4">
      <div className="text-center max-w-xl">
        <div className="text-6xl mb-6">🎫</div>
        <h1 className="text-4xl font-bold text-gray-900 mb-3">TickioOSS</h1>
        <p className="text-lg text-gray-600 mb-8">
          Open-source IT support ticket system. Report issues, track progress, and resolve incidents fast.
        </p>
        {user ? (
          <div className="flex gap-4 justify-center">
            <Link
              to="/tickets"
              className="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              View Tickets
            </Link>
            <Link
              to="/tickets/new"
              className="border border-blue-600 text-blue-600 px-6 py-3 rounded-xl font-semibold hover:bg-blue-50 transition"
            >
              Open a Ticket
            </Link>
          </div>
        ) : (
          <div className="flex gap-4 justify-center">
            <Link
              to="/login"
              className="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="border border-blue-600 text-blue-600 px-6 py-3 rounded-xl font-semibold hover:bg-blue-50 transition"
            >
              Register
            </Link>
          </div>
        )}
        <p className="text-xs text-gray-400 mt-10">
          Built with FastAPI + React + PostgreSQL · Licensed under MIT
        </p>
      </div>
    </div>
  )
}
