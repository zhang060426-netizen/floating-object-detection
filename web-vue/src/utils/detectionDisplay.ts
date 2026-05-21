import type { DetectionArtifacts, DetectionRecord, DetectionResult, FileRef, ImageDetectionResponse } from '../types/detection'

const TIMING_DISPLAY_ITEMS = [
  { key: 'total_api_ms', label: '总耗时' },
  { key: 'model_load_ms', label: '模型加载' },
  { key: 'preprocess_ms', label: '预处理' },
  { key: 'inference_ms', label: '推理' },
  { key: 'postprocess_ms', label: '后处理' },
  { key: 'result_image_save_ms', label: '结果图保存' },
  { key: 'record_save_ms', label: '记录保存' },
] as const

export function detectionCount(result?: DetectionResult | null, record?: DetectionRecord | null): number {
  return (
    record?.target_count ??
    result?.summary?.total_detections ??
    result?.summary?.object_count ??
    result?.detections?.length ??
    0
  )
}

export function detectionStatus(result?: DetectionResult | null, response?: ImageDetectionResponse | null): string {
  const status = response?.detection_status || result?.summary?.detection_status
  if (status) return status
  return detectionCount(result) > 0 ? 'detected' : 'no_detection'
}

export function modelDisplayName(record?: DetectionRecord | null, result?: DetectionResult | null): string {
  return (
    record?.model_name ||
    record?.model?.name ||
    result?.model?.model_name ||
    result?.model?.model_id ||
    record?.model_id ||
    '-'
  )
}

export function confidenceThreshold(record?: DetectionRecord | null, result?: DetectionResult | null): number | undefined {
  return record?.confidence_threshold ?? result?.summary?.confidence_threshold ?? result?.model?.confidence_threshold
}

export function backendReason(result?: DetectionResult | null, artifacts?: DetectionArtifacts): string {
  return firstString(
    artifacts?.reason,
    result?.raw?.reason,
    result?.raw?.message,
    result?.raw?.msg,
  )
}

export function originalImageRef(record?: DetectionRecord | null, result?: DetectionResult | null): FileRef | string | null {
  const artifacts = result?.artifacts
  return (
    record?.original_image ||
    artifacts?.original_image ||
    artifactKeyRef(artifacts, 'original_image_key', 'uploads')
  )
}

export function resultImageRef(
  response?: ImageDetectionResponse | null,
  record?: DetectionRecord | null,
  result?: DetectionResult | null,
): FileRef | string | null {
  const artifacts = result?.artifacts
  return (
    response?.result_image ||
    response?.result_image_url ||
    record?.result_image ||
    record?.result_image_url ||
    artifacts?.result_image ||
    artifacts?.result_image_url ||
    artifactKeyRef(artifacts, 'result_image_key', 'results') ||
    artifactKeyRef(artifacts, 'annotated_image_key', 'results')
  )
}

export function isDevPlaceholder(result?: DetectionResult | null): boolean {
  const artifacts = result?.artifacts
  return Boolean(artifacts?.dev_placeholder || artifacts?.placeholder || result?.raw?.is_dev_placeholder)
}

export function timingDisplayItems(result?: DetectionResult | null): Array<{ key: string; label: string; value: string }> {
  const timing = result?.timing
  const legacyTiming = result?.timing_ms
  return TIMING_DISPLAY_ITEMS.reduce<Array<{ key: string; label: string; value: string }>>((items, item) => {
    const value = timing?.[item.key] ?? legacyTiming?.[item.key]
    if (typeof value === 'number' && Number.isFinite(value)) {
      items.push({ key: item.key, label: item.label, value: `${value} ms` })
    }
    return items
  }, [])
}

function artifactKeyRef(artifact: DetectionArtifacts | undefined, key: string, bucket: string): FileRef | null {
  const value = artifact?.[key]
  return typeof value === 'string' && value ? { bucket, object_key: value } : null
}

function firstString(...values: unknown[]): string {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim()
  }
  return ''
}
