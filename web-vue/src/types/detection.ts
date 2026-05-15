import type { PublishedModel } from './model'

export interface FileRef {
  bucket?: string
  object_key?: string
  url?: string
  filename?: string
}

export interface DetectionBBox {
  format?: string
  x1?: number
  y1?: number
  x2?: number
  y2?: number
  xyxy?: number[]
  xywhn?: number[]
}

export interface DetectionObject {
  detection_id?: string
  object_index?: number
  class_id: number
  class_name: string
  chinese_name?: string
  confidence: number
  bbox?: DetectionBBox
  bbox_xyxy?: number[]
  bbox_xywhn?: number[]
}

export interface DetectionResult {
  schema_version?: string
  source_type?: string
  model?: {
    model_id?: string
    model_name?: string
    base_model?: string
    confidence_threshold?: number
  }
  image?: {
    width?: number
    height?: number
    filename?: string
  }
  detections: DetectionObject[]
  summary?: {
    total_detections?: number
    has_detections?: boolean
    max_confidence?: number | null
    avg_confidence?: number | null
    confidence_threshold?: number
    by_class?: Record<string, number>
  }
  artifacts?: Record<string, unknown>
  timing?: {
    inference_ms?: number
  }
  timing_ms?: Record<string, number>
}

export interface ImageDetectionResponse {
  record_id?: string
  original_image?: FileRef
  result_image?: FileRef
  detection_result: DetectionResult
}

export interface DetectionRecord {
  id: string
  title?: string
  filename?: string
  model_id?: string
  model_name?: string
  status?: string
  create_time?: string
  created_at?: string
  updated_at?: string
  original_image?: FileRef
  result_image?: FileRef
  detection_result?: DetectionResult
  target_count?: number
  model?: PublishedModel
}

export interface PageResult<T> {
  items: T[]
  total?: number
  page?: number
  page_size?: number
}
