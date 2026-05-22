import { ElMessage } from 'element-plus'
import router from '../router'
import { clearToken, getToken } from '../stores/user'
import type { ApiEnvelope } from '../types/api'
import { parseContentDispositionFilename } from '../utils/download'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

const REASON_LABELS: Record<string, string> = {
  bad_request: '请求参数或上传文件不符合要求',
  invalid_image: '上传文件不是可识别图片',
  unsupported_image_type: '不支持的图片类型',
  dependency_unavailable: '后端推理依赖不可用',
  weight_missing: '模型权重不可读或不存在',
  model_not_found: '模型不存在或未发布',
  unauthorized: '登录状态无效',
}

export class ApiClientError extends Error {
  code?: number
  status?: number
  detail?: unknown

  constructor(message: string, code?: number, status?: number, detail?: unknown) {
    super(message)
    this.name = 'ApiClientError'
    this.code = code
    this.status = status
    this.detail = detail
  }
}

export interface BlobResponse {
  blob: Blob
  filename?: string
}

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = buildAuthHeaders(init)

  let response: Response
  try {
    response = await fetch(resolveApiUrl(path), { ...init, headers })
  } catch {
    throw new ApiClientError('无法连接后端 Flask API，请确认 smoke 服务已启动。')
  }

  const text = await response.text()
  const payload = text ? safeJson<unknown>(text, response.status) : undefined

  if (response.status === 401) {
    clearToken()
    ElMessage.error('登录已失效，请重新登录')
    await router.replace({ path: '/login', query: { redirect: router.currentRoute.value.fullPath } })
    throw new ApiClientError(readableError(payload, '登录已失效'), 401, response.status, payload)
  }

  const envelope = isEnvelope<T>(payload) ? payload : undefined

  if (!response.ok) {
    throw new ApiClientError(readableError(payload, `请求失败：HTTP ${response.status}`), envelope?.code, response.status, payload)
  }

  if (envelope && typeof envelope.code === 'number') {
    const ok = envelope.code === 0 || envelope.code === 200
    if (!ok) {
      throw new ApiClientError(readableError(envelope, '接口返回失败'), envelope.code, response.status, envelope)
    }
    return envelope.data
  }

  return payload as T
}

export async function requestBlob(path: string, init: RequestInit = {}): Promise<BlobResponse> {
  const headers = buildAuthHeaders(init)

  let response: Response
  try {
    response = await fetch(resolveApiUrl(path), { ...init, headers })
  } catch {
    throw new ApiClientError('无法连接后端 Flask API，请确认 smoke 服务已启动。')
  }

  if (response.status === 401) {
    const payload = await readErrorPayload(response)
    clearToken()
    ElMessage.error('登录已失效，请重新登录')
    await router.replace({ path: '/login', query: { redirect: router.currentRoute.value.fullPath } })
    throw new ApiClientError(readableError(payload, '登录已失效'), 401, response.status, payload)
  }

  if (!response.ok) {
    const payload = await readErrorPayload(response)
    const envelope = isEnvelope<unknown>(payload) ? payload : undefined
    throw new ApiClientError(readableError(payload, `请求失败：HTTP ${response.status}`), envelope?.code, response.status, payload)
  }

  const contentType = response.headers.get('Content-Type') || ''
  if (contentType.toLowerCase().includes('application/json')) {
    const payload = await response.json() as unknown
    const envelope = isEnvelope<unknown>(payload) ? payload : undefined
    throw new ApiClientError(readableError(payload, '接口返回失败'), envelope?.code, response.status, payload)
  }

  return {
    blob: await response.blob(),
    filename: parseContentDispositionFilename(response.headers.get('Content-Disposition')),
  }
}

export function toJsonBody(value: unknown): BodyInit {
  return JSON.stringify(value)
}

function buildAuthHeaders(init: RequestInit): Headers {
  const token = getToken()
  const headers = new Headers(init.headers)

  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (!(init.body instanceof FormData) && init.body !== undefined && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  return headers
}

function resolveApiUrl(path: string): string {
  if (/^https?:\/\//i.test(path)) return path
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  if (!API_BASE_URL) return normalizedPath
  if (normalizedPath === API_BASE_URL || normalizedPath.startsWith(`${API_BASE_URL}/`)) return normalizedPath
  return `${API_BASE_URL}${normalizedPath}`
}

async function readErrorPayload(response: Response): Promise<unknown> {
  const text = await response.text()
  if (!text) return undefined

  try {
    return JSON.parse(text) as unknown
  } catch {
    return text.trim() || undefined
  }
}

function safeJson<T>(text: string, status?: number): T {
  try {
    return JSON.parse(text) as T
  } catch {
    const snippet = text.trim().slice(0, 160)
    throw new ApiClientError(snippet ? `后端返回非 JSON 响应：${snippet}` : '后端返回的 JSON 格式无效', undefined, status)
  }
}

function isEnvelope<T>(value: unknown): value is ApiEnvelope<T> {
  return Boolean(value && typeof value === 'object' && ('code' in value || 'data' in value || 'msg' in value || 'message' in value))
}

function readableError(value: unknown, fallback: string): string {
  if (typeof value === 'string') return value || fallback
  if (!value || typeof value !== 'object') return fallback
  const record = value as Record<string, unknown>
  const direct = firstString(record.message, record.msg)
  const error = record.error && typeof record.error === 'object' ? (record.error as Record<string, unknown>) : undefined
  const data = record.data && typeof record.data === 'object' ? (record.data as Record<string, unknown>) : undefined
  const reason = firstString(record.reason, error?.reason, data?.reason)
  const field = firstString(error?.field, data?.field)
  const parts = [direct || fallback]
  const reasonText = reason ? (REASON_LABELS[reason] ? `${REASON_LABELS[reason]} (${reason})` : reason) : ''
  if (reasonText && reasonText !== parts[0]) parts.push(`原因：${reasonText}`)
  if (field) parts.push(`字段：${field}`)
  return parts.join('；')
}

function firstString(...values: unknown[]): string {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim()
  }
  return ''
}
