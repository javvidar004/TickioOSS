import { useEffect, useState } from 'react'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'

export default function AdminUsers() {
  const { user: me } = useAuth()
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(null)

  const fetchUsers = () => {
    api.get('/users/').then((r) => setUsers(r.data)).finally(() => setLoading(false))
  }

  useEffect(fetchUsers, [])

  const updateUser = async (id, data) => {
    setSaving(id)
    try {
      await api.put(`/users/${id}`, data)
      fetchUsers()
    } finally {
      setSaving(null)
    }
  }

  const deleteUser = async (id) => {
    if (!confirm('Delete this user?')) return
    await api.delete(`/users/${id}`)
    fetchUsers()
  }

  if (loading) return <div className="p-8 text-center text-gray-500">Loading users...</div>

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">User Management</h1>
      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b">
            <tr>
              {['ID', 'Username', 'Email', 'Role', 'Active', 'Joined', 'Actions'].map((h) => (
                <th key={h} className="text-left px-4 py-3 font-semibold text-gray-600">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y">
            {users.map((u) => (
              <tr key={u.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-gray-400">#{u.id}</td>
                <td className="px-4 py-3 font-medium">{u.username}</td>
                <td className="px-4 py-3 text-gray-600">{u.email}</td>
                <td className="px-4 py-3">
                  <select
                    value={u.role}
                    disabled={u.id === me.id}
                    onChange={(e) => updateUser(u.id, { role: e.target.value })}
                    className="border rounded px-2 py-0.5 text-sm disabled:opacity-50"
                  >
                    {['user', 'agent', 'admin'].map((r) => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                </td>
                <td className="px-4 py-3">
                  <button
                    disabled={u.id === me.id}
                    onClick={() => updateUser(u.id, { is_active: !u.is_active })}
                    className={`px-2 py-0.5 rounded text-xs font-medium disabled:opacity-40 ${
                      u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'
                    }`}
                  >
                    {u.is_active ? 'Active' : 'Inactive'}
                  </button>
                </td>
                <td className="px-4 py-3 text-gray-400">
                  {new Date(u.created_at).toLocaleDateString()}
                </td>
                <td className="px-4 py-3">
                  <button
                    disabled={u.id === me.id}
                    onClick={() => deleteUser(u.id)}
                    className="text-red-500 hover:text-red-700 text-xs disabled:opacity-30"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
