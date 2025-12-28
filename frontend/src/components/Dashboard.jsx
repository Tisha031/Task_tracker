import React, {useEffect, useState} from 'react'
import api from '../utils/api'

export default function Dashboard(){
  const [tasks,setTasks]=useState([])
  const [title,setTitle]=useState('')

  async function load(){
    const res = await api.get('/tasks')
    setTasks(res.data)
  }
  useEffect(()=>{ load() }, [])

  async function add(e){
    e.preventDefault()
    await api.post('/tasks', {title})
    setTitle('')
    load()
  }

  return (
    <div>
      <h2 className="text-2xl mb-4">Tasks</h2>
      <form onSubmit={add} className="mb-4 flex gap-2">
        <input className="flex-1 p-2 border rounded" value={title} onChange={e=>setTitle(e.target.value)} placeholder="Task title" />
        <button className="px-4 py-2 bg-blue-600 text-white rounded">Add</button>
      </form>
      <ul className="space-y-2">
        {tasks.map(t=> <li key={t.id} className="p-3 bg-white rounded shadow">{t.title} <span className="text-sm text-gray-500">- {t.status}</span></li>)}
      </ul>
    </div>
  )
}
