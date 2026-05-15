import { request } from './request'
import type { PublishedModel } from '../types/model'

export function fetchPublishedModels() {
  return request<PublishedModel[]>('/api/models/published')
}
