import { defineStore } from 'pinia'
import { currentUserApi, loginApi } from '../api/auth'
import type { UserInfo } from '../types/user'

const TOKEN_KEY = 'floating_objects_jwt'
const USER_KEY = 'floating_objects_user'

export function getToken(): string {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

function readUser(): UserInfo | null {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as UserInfo
  } catch {
    return null
  }
}

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getToken(),
    user: readUser() as UserInfo | null,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    async login(username: string, password: string) {
      const data = await loginApi(username, password)
      this.token = data.token
      this.user = data.user
      localStorage.setItem(TOKEN_KEY, data.token)
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))
    },
    async hydrate() {
      this.token = getToken()
      this.user = readUser()
      if (this.token && !this.user) {
        this.user = await currentUserApi()
        localStorage.setItem(USER_KEY, JSON.stringify(this.user))
      }
    },
    logout() {
      this.token = ''
      this.user = null
      clearToken()
    },
  },
})
