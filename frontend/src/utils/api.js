import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  withCredentials: true // important to send/receive HttpOnly cookie
})

// response interceptor to handle 401 globally could be added here

export default api
