import { request, toJsonBody } from './request'
import type { LoginResponse, UserInfo } from '../types/user'

export const LOGIN_ENDPOINT = '/api/auth/login'

export function loginApi(username: string, password: string) {
  return request<LoginResponse>(LOGIN_ENDPOINT, {
    method: 'POST',
    body: toJsonBody({ username, password }),
  })
}

export function currentUserApi() {
  return request<UserInfo>('/api/auth/me')
}
