import { resolveFileUrl } from '../utils/fileUrl'
import type { FileRef } from '../types/detection'

export function fileUrl(ref?: FileRef | string | null): string {
  return resolveFileUrl(ref)
}
