import React, {useState} from 'react'
import api from '../utils/api'
import { useNavigate } from 'react-router-dom'

export default function Register(){
  const [name,setName]=useState('')
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const nav = useNavigate()

  async function submit(e){
    e.preventDefault()
    await api.post('/auth/register',{name,email,password})
    nav('/login')
  }

  return (
    <form onSubmit={submit} className="max-w-md mx-auto p-4 bg-white rounded shadow">
      <h2 className="text-xl mb-4">Register</h2>
      <input className="w-full p-2 border mb-2" placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
      <input className="w-full p-2 border mb-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="w-full p-2 border mb-4" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button className="px-4 py-2 bg-blue-600 text-white rounded">Register</button>
    </form>
  )
}
