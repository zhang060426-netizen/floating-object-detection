import type { FileRef } from '../types/detection'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

export function resolveFileUrl(ref?: FileRef | string | null): string {
  if (!ref) return ''
  if (typeof ref === 'string') return withBase(ref)
  if (ref.url) return withBase(ref.url)
  if (ref.bucket && ref.object_key) {
    return withBase(`/api/files/${encodeURIComponent(ref.bucket)}/${encodePath(ref.object_key)}`)
  }
  return ''
}

export function fileRefError(ref?: FileRef | string | null): string {
  if (!ref) return '后端未返回文件 URL。'
  if (typeof ref === 'string') return ''
  if (ref.url || (ref.bucket && ref.object_key)) return ''
  return '文件引用缺少 url，或缺少 bucket/object_key。'
}

function withBase(url: string): string {
  if (!url) return ''
  if (/^https?:\/\//i.test(url) || url.startsWith('blob:') || url.startsWith('data:')) return url
  const normalizedUrl = url.startsWith('/') ? url : `/${url}`
  if (!API_BASE_URL) return normalizedUrl
  if (normalizedUrl === API_BASE_URL || normalizedUrl.startsWith(`${API_BASE_URL}/`)) return normalizedUrl
  return `${API_BASE_URL}${normalizedUrl}`
}

function encodePath(path: string): string {
  return path.split('/').map(encodeURIComponent).join('/')
}
