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

export interface DetectionArtifacts {
  original_image?: FileRef | string
  original_image_key?: string
  result_image?: FileRef | string
  result_image_url?: string
  annotated_image_key?: string
  result_image_key?: string
  dev_placeholder?: boolean
  placeholder?: boolean
  reason?: string
  enhanced_image?: FileRef | string
  enhanced_image_url?: string
  crops?: Array<FileRef | string>
  [key: string]: unknown
}

export type DetectionStatus = 'detected' | 'no_detection' | 'failed' | string

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
    object_count?: number
    has_detections?: boolean
    has_detection?: boolean
    detection_status?: DetectionStatus
    max_confidence?: number | null
    avg_confidence?: number | null
    mean_confidence?: number | null
    confidence_threshold?: number
    by_class?: Record<string, number>
    class_counts?: Record<string, number>
  }
  artifacts?: DetectionArtifacts
  timing?: {
    total_api_ms?: number
    inference_ms?: number
    model_load_ms?: number
    preprocess_ms?: number
    postprocess_ms?: number
    result_image_save_ms?: number
    record_save_ms?: number
  }
  timing_ms?: Record<string, number>
  raw?: Record<string, unknown>
}

export interface ImageDetectionResponse {
  record_id?: string
  detection_status?: DetectionStatus
  original_image?: FileRef | string
  result_image?: FileRef | string
  result_image_url?: string
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
  original_image?: FileRef | string
  result_image?: FileRef | string
  result_image_url?: string
  detection_result?: DetectionResult
  target_count?: number
  confidence_threshold?: number
  model?: PublishedModel
}

export interface PageResult<T> {
  items?: T[]
  records?: T[]
  list?: T[]
  data?: T[]
  total?: number
  page?: number
  page_size?: number
  pageSize?: number
  current_page?: number
}

export interface DetectionRecordQuery {
  page?: number
  page_size?: number
}
