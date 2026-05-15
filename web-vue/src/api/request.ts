import { ElMessage } from 'element-plus'
import router from '../router'
import { clearToken, getToken } from '../stores/user'
import type { ApiEnvelope } from '../types/api'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

export class ApiClientError extends Error {
  code?: number
  status?: number

  constructor(message: string, code?: number, status?: number) {
    super(message)
    this.name = 'ApiClientError'
    this.code = code
    this.status = status
  }
}

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getToken()
  const headers = new Headers(init.headers)

  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (!(init.body instanceof FormData) && init.body !== undefined && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers })
  } catch {
    throw new ApiClientError('无法连接后端服务，请确认 Flask API 已启动。')
  }

  const text = await response.text()
  const payload = text ? safeJson<ApiEnvelope<T>>(text) : undefined

  if (response.status === 401) {
    clearToken()
    ElMessage.error('登录已失效，请重新登录')
    await router.replace({ path: '/login', query: { redirect: router.currentRoute.value.fullPath } })
    throw new ApiClientError('登录已失效', 401, response.status)
  }

  if (!response.ok) {
    throw new ApiClientError(payload?.message || payload?.msg || `请求失败：HTTP ${response.status}`, payload?.code, response.status)
  }

  if (payload && typeof payload.code === 'number') {
    const ok = payload.code === 0 || payload.code === 200
    if (!ok) {
      throw new ApiClientError(payload.message || payload.msg || '业务请求失败', payload.code, response.status)
    }
    return payload.data
  }

  return payload as T
}

export function toJsonBody(value: unknown): BodyInit {
  return JSON.stringify(value)
}

function safeJson<T>(text: string): T {
  try {
    return JSON.parse(text) as T
  } catch {
    throw new ApiClientError('后端返回了非 JSON 响应。')
  }
}
