import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'
import { StatusBadge, PriorityBadge } from '../components/StatusBadge'

export default function TicketDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [ticket, setTicket] = useState(null)
  const [comments, setComments] = useState([])
  const [commentText, setCommentText] = useState('')
  const [editStatus, setEditStatus] = useState('')
  const [editAssignee, setEditAssignee] = useState('')
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)

  const isStaff = user?.role === 'admin' || user?.role === 'agent'

  const fetchAll = () => {
    Promise.all([
      api.get(`/tickets/${id}`),
      api.get(`/tickets/${id}/comments`),
      isStaff ? api.get('/users/') : Promise.resolve({ data: [] }),
    ]).then(([t, c, u]) => {
      setTicket(t.data)
      setEditStatus(t.data.status)
      setEditAssignee(t.data.assignee?.id ?? '')
      setComments(c.data)
      setAgents(u.data.filter((u) => u.role !== 'user'))
    }).finally(() => setLoading(false))
  }

  useEffect(fetchAll, [id])

  const handleUpdate = async () => {
    await api.put(`/tickets/${id}`, {
      status: editStatus,
      assigned_to_id: editAssignee || null,
    })
    fetchAll()
  }

  const handleComment = async (e) => {
    e.preventDefault()
    if (!commentText.trim()) return
    await api.post(`/tickets/${id}/comments`, { content: commentText })
    setCommentText('')
    fetchAll()
  }

  const handleDelete = async () => {
    if (!confirm('Delete this ticket?')) return
    await api.delete(`/tickets/${id}`)
    navigate('/tickets')
  }

  if (loading) return <div className="p-8 text-center text-gray-500">Loading...</div>
  if (!ticket) return null

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <button onClick={() => navigate(-1)} className="text-blue-600 hover:underline text-sm mb-4 block">
        ← Back
      </button>

      <div className="bg-white rounded-xl shadow p-6 mb-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <h1 className="text-xl font-bold">{ticket.title}</h1>
            <p className="text-sm text-gray-500 mt-1">
              #{ticket.id} · {ticket.category} · by {ticket.creator.username} · {new Date(ticket.created_at).toLocaleDateString()}
            </p>
          </div>
          <div className="flex flex-col items-end gap-1.5 shrink-0">
            <StatusBadge status={ticket.status} />
            <PriorityBadge priority={ticket.priority} />
          </div>
        </div>
        <p className="text-gray-700 whitespace-pre-wrap">{ticket.description}</p>

        {ticket.assignee && (
          <p className="mt-4 text-sm text-gray-500">Assigned to: <strong>{ticket.assignee.username}</strong></p>
        )}

        {isStaff && (
          <div className="mt-6 pt-4 border-t flex flex-wrap gap-3 items-end">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Status</label>
              <select
                value={editStatus}
                onChange={(e) => setEditStatus(e.target.value)}
                className="border rounded px-2 py-1 text-sm"
              >
                {['open', 'in_progress', 'resolved', 'closed'].map((s) => (
                  <option key={s} value={s}>{s.replace('_', ' ')}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Assign to</label>
              <select
                value={editAssignee}
                onChange={(e) => setEditAssignee(e.target.value)}
                className="border rounded px-2 py-1 text-sm"
              >
                <option value="">Unassigned</option>
                {agents.map((a) => (
                  <option key={a.id} value={a.id}>{a.username}</option>
                ))}
              </select>
            </div>
            <button
              onClick={handleUpdate}
              className="bg-blue-600 text-white px-4 py-1.5 rounded text-sm hover:bg-blue-700 transition"
            >
              Save
            </button>
            {user.role === 'admin' && (
              <button
                onClick={handleDelete}
                className="bg-red-500 text-white px-4 py-1.5 rounded text-sm hover:bg-red-600 transition ml-auto"
              >
                Delete
              </button>
            )}
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="font-semibold text-lg mb-4">Comments ({comments.length})</h2>
        <div className="space-y-4 mb-6">
          {comments.map((c) => (
            <div key={c.id} className="bg-gray-50 rounded-lg p-4">
              <div className="flex justify-between text-sm text-gray-500 mb-2">
                <strong className="text-gray-800">{c.author.username}</strong>
                <span>{new Date(c.created_at).toLocaleString()}</span>
              </div>
              <p className="text-gray-700 whitespace-pre-wrap">{c.content}</p>
            </div>
          ))}
          {comments.length === 0 && <p className="text-gray-400 text-sm">No comments yet.</p>}
        </div>
        <form onSubmit={handleComment} className="flex gap-3">
          <textarea
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            placeholder="Add a comment..."
            rows={2}
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition self-end"
          >
            Post
          </button>
        </form>
      </div>
    </div>
  )
}
