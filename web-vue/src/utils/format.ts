import type { DetectionBBox, DetectionObject, DetectionRecord } from '../types/detection'

export function percent(value?: number | null): string {
  if (value === null || value === undefined || Number.isNaN(value)) return '-'
  return `${(value * 100).toFixed(1)}%`
}

export function formatDate(value?: string): string {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

export function recordTime(record: Pick<DetectionRecord, 'create_time' | 'created_at' | 'updated_at'>): string {
  return formatDate(record.create_time || record.created_at || record.updated_at)
}

export function targetCount(record: { target_count?: number; detection_result?: { detections?: unknown[]; summary?: { total_detections?: number } } }): number {
  return (
    record.target_count ??
    record.detection_result?.summary?.total_detections ??
    record.detection_result?.detections?.length ??
    0
  )
}

export function bboxText(detection: Pick<DetectionObject, 'bbox' | 'bbox_xyxy' | 'bbox_xywhn'>): string {
  const xyxy = normalizeNumberArray(detection.bbox?.xyxy ?? detection.bbox_xyxy)
  if (xyxy.length === 4) return `[${xyxy.map((item) => item.toFixed(0)).join(', ')}]`

  const bboxObject = detection.bbox
  const objectXyxy = normalizeObjectXyxy(bboxObject)
  if (objectXyxy.length === 4) return `[${objectXyxy.map((item) => item.toFixed(0)).join(', ')}]`

  const xywhn = normalizeNumberArray(detection.bbox?.xywhn ?? detection.bbox_xywhn)
  if (xywhn.length === 4) return `xywhn [${xywhn.map((item) => item.toFixed(4)).join(', ')}]`

  return '-'
}

function normalizeNumberArray(value?: number[]): number[] {
  return Array.isArray(value) && value.length === 4 && value.every((item) => typeof item === 'number')
    ? value
    : []
}

function normalizeObjectXyxy(bbox?: DetectionBBox): number[] {
  const values = [bbox?.x1, bbox?.y1, bbox?.x2, bbox?.y2]
  return values.every((item) => typeof item === 'number') ? (values as number[]) : []
}
