const STATUS_COLORS = {
  open: 'bg-green-100 text-green-800',
  in_progress: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-blue-100 text-blue-800',
  closed: 'bg-gray-100 text-gray-600',
}

const PRIORITY_COLORS = {
  low: 'bg-slate-100 text-slate-600',
  medium: 'bg-orange-100 text-orange-700',
  high: 'bg-red-100 text-red-700',
  critical: 'bg-red-600 text-white',
}

export function StatusBadge({ status }) {
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${STATUS_COLORS[status] ?? 'bg-gray-100'}`}>
      {status.replace('_', ' ')}
    </span>
  )
}

export function PriorityBadge({ priority }) {
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${PRIORITY_COLORS[priority] ?? 'bg-gray-100'}`}>
      {priority}
    </span>
  )
}
