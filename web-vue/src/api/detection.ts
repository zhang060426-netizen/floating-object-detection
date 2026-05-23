import { request, requestBlob } from './request'
import type {
  DashboardSummary,
  DetectionRecord,
  DetectionRecordQuery,
  ImageDetectionResponse,
  PageResult,
} from '../types/detection'

export interface DetectImageOptions {
  image: File
  modelId: string
  confidenceThreshold?: number
  saveRecord?: boolean
}

export function detectImage(options: DetectImageOptions) {
  const form = new FormData()
  form.append('image', options.image)
  form.append('model_id', options.modelId)
  if (options.confidenceThreshold !== undefined) {
    form.append('confidence_threshold', String(options.confidenceThreshold))
  }
  if (options.saveRecord !== undefined) {
    form.append('save_record', String(options.saveRecord))
  }
  return request<ImageDetectionResponse>('/api/detection/image', { method: 'POST', body: form })
}

export function fetchDetectionRecords(params?: DetectionRecordQuery) {
  return request<PageResult<DetectionRecord> | DetectionRecord[]>(withQuery('/api/detection/records', params))
}

function withQuery(path: string, params?: DetectionRecordQuery): string {
  if (!params) return path

  const query = new URLSearchParams()
  appendPositiveInteger(query, 'page', params.page)
  appendPositiveInteger(query, 'page_size', params.page_size)
  appendNonEmptyString(query, 'keyword', params.keyword)
  appendNonEmptyString(query, 'model_id', params.model_id)
  appendNonEmptyString(query, 'detection_status', params.detection_status)
  appendNonEmptyString(query, 'date_start', params.date_start)
  appendNonEmptyString(query, 'date_end', params.date_end)
  return query.size > 0 ? `${path}?${query.toString()}` : path
}

function appendPositiveInteger(query: URLSearchParams, key: string, value?: number): void {
  if (typeof value === 'number' && Number.isInteger(value) && value > 0) {
    query.set(key, String(value))
  }
}

function appendNonEmptyString(query: URLSearchParams, key: string, value?: string): void {
  if (typeof value === 'string' && value.trim()) {
    query.set(key, value.trim())
  }
}

export function fetchDetectionRecord(id: string) {
  return request<DetectionRecord>(`/api/detection/records/${encodeURIComponent(id)}`)
}

export function exportDetectionRecordWordReport(id: string) {
  return requestBlob(`/api/detection/records/${encodeURIComponent(id)}/report.docx`)
}

export function fetchDashboardSummary() {
  return request<DashboardSummary>('/api/detection/dashboard/summary')
}
