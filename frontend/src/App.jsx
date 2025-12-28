import React, {useEffect} from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Login from './components/Login'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import { useDispatch } from 'react-redux'
import { fetchMe } from './store/slices/authSlice'

export default function App(){
  const dispatch = useDispatch()
  useEffect(()=>{ dispatch(fetchMe()) }, [dispatch])

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="p-4 bg-white shadow">
        <div className="max-w-4xl mx-auto flex gap-4">
          <Link to="/" className="font-semibold">Home</Link>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </div>
      </nav>
      <main className="max-w-4xl mx-auto p-4">
        <Routes>
          <Route path="/" element={<Dashboard/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/register" element={<Register/>} />
        </Routes>
      </main>
    </div>
  )
}
