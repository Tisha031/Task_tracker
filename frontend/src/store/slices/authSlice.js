import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../../utils/api'

export const fetchMe = createAsyncThunk('auth/fetchMe', async () => {
  const res = await api.get('/auth/me')
  return res.data
})

const slice = createSlice({
  name: 'auth',
  initialState: { user: null, status: 'idle' },
  reducers: {
    setUser(state, action){ state.user = action.payload }
  },
  extraReducers: (builder) => {
    builder.addCase(fetchMe.fulfilled, (state, action) => {
      state.user = action.payload
    })
  }
})

export const { setUser } = slice.actions
export default slice.reducer
