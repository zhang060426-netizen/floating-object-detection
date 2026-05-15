import { request, toJsonBody } from './request'
import type { LoginResponse, UserInfo } from '../types/user'

export function loginApi(username: string, password: string) {
  return request<LoginResponse>('/api/auth/login', {
    method: 'POST',
    body: toJsonBody({ username, password }),
  })
}

export function currentUserApi() {
  return request<UserInfo>('/api/auth/me')
}
