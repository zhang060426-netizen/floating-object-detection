import { request } from './request'
import type { DetectionRecord, ImageDetectionResponse, PageResult } from '../types/detection'

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

export function fetchDetectionRecords() {
  return request<PageResult<DetectionRecord> | DetectionRecord[]>('/api/detection/records')
}

export function fetchDetectionRecord(id: string) {
  return request<DetectionRecord>(`/api/detection/records/${encodeURIComponent(id)}`)
}
