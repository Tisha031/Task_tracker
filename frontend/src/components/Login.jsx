import React, {useState} from 'react'
import api from '../utils/api'
import { useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { fetchMe } from '../store/slices/authSlice'

export default function Login(){
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const nav = useNavigate()
  const dispatch = useDispatch()

  async function submit(e){
    e.preventDefault()
    await api.post('/auth/login',{email,password})
    // since cookie is HttpOnly, we fetch /auth/me to get user
    await dispatch(fetchMe())
    nav('/')
  }

  return (
    <form onSubmit={submit} className="max-w-md mx-auto p-4 bg-white rounded shadow">
      <h2 className="text-xl mb-4">Login</h2>
      <input className="w-full p-2 border mb-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="w-full p-2 border mb-4" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button className="px-4 py-2 bg-green-600 text-white rounded">Login</button>
    </form>
  )
}
