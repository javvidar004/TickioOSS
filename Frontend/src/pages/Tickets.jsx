import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'
import { StatusBadge, PriorityBadge } from '../components/StatusBadge'

export default function Tickets() {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ status: '', priority: '', category: '' })

  const fetchTickets = () => {
    const params = Object.fromEntries(Object.entries(filters).filter(([, v]) => v))
    api.get('/tickets/', { params }).then((r) => setTickets(r.data)).finally(() => setLoading(false))
  }

  useEffect(fetchTickets, [filters])

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Tickets</h1>
        <Link
          to="/tickets/new"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition text-sm font-medium"
        >
          + New Ticket
        </Link>
      </div>

      <div className="flex gap-3 mb-6 flex-wrap">
        {[
          { key: 'status', options: ['', 'open', 'in_progress', 'resolved', 'closed'] },
          { key: 'priority', options: ['', 'low', 'medium', 'high', 'critical'] },
          { key: 'category', options: ['', 'hardware', 'software', 'network', 'access', 'other'] },
        ].map(({ key, options }) => (
          <select
            key={key}
            value={filters[key]}
            onChange={(e) => setFilters({ ...filters, [key]: e.target.value })}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 capitalize"
          >
            {options.map((o) => (
              <option key={o} value={o}>{o ? o.replace('_', ' ') : `All ${key}s`}</option>
            ))}
          </select>
        ))}
      </div>

      {loading ? (
        <p className="text-gray-500 text-center py-12">Loading...</p>
      ) : tickets.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <p className="text-4xl mb-3">🎫</p>
          <p>No tickets found.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tickets.map((t) => (
            <Link
              key={t.id}
              to={`/tickets/${t.id}`}
              className="block bg-white rounded-xl shadow-sm hover:shadow-md transition p-5 border border-gray-100"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <p className="font-semibold text-gray-900 truncate">{t.title}</p>
                  <p className="text-sm text-gray-500 mt-1 truncate">{t.description}</p>
                  <p className="text-xs text-gray-400 mt-2">
                    #{t.id} · {t.category} · by {t.creator.username} · {new Date(t.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex flex-col items-end gap-1.5 shrink-0">
                  <StatusBadge status={t.status} />
                  <PriorityBadge priority={t.priority} />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
