import { useEffect, useState } from 'react'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'

function StatCard({ label, value, color }) {
  return (
    <div className={`bg-white rounded-xl shadow p-6 border-l-4 ${color}`}>
      <p className="text-sm text-gray-500 uppercase tracking-wide">{label}</p>
      <p className="text-3xl font-bold mt-1">{value}</p>
    </div>
  )
}

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/tickets/dashboard').then((r) => setStats(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-8 text-center text-gray-500">Loading dashboard...</div>
  if (!stats) return null

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total" value={stats.total} color="border-blue-500" />
        <StatCard label="Open" value={stats.open} color="border-green-500" />
        <StatCard label="In Progress" value={stats.in_progress} color="border-yellow-500" />
        <StatCard label="Resolved" value={stats.resolved} color="border-purple-500" />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="font-semibold text-lg mb-4">By Priority</h2>
          {Object.entries(stats.by_priority).map(([k, v]) => (
            <div key={k} className="flex justify-between py-1.5 border-b last:border-0">
              <span className="capitalize text-gray-600">{k}</span>
              <span className="font-bold">{v}</span>
            </div>
          ))}
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="font-semibold text-lg mb-4">By Category</h2>
          {Object.entries(stats.by_category).map(([k, v]) => (
            <div key={k} className="flex justify-between py-1.5 border-b last:border-0">
              <span className="capitalize text-gray-600">{k}</span>
              <span className="font-bold">{v}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
