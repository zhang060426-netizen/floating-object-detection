export function saveBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.style.display = 'none'
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}

export function parseContentDispositionFilename(header: string | null): string | undefined {
  if (!header) return undefined

  const encodedMatch = header.match(/filename\*\s*=\s*(?:UTF-8'')?([^;]+)/i)
  if (encodedMatch?.[1]) {
    return decodeFilename(cleanHeaderValue(encodedMatch[1]))
  }

  const quotedMatch = header.match(/filename\s*=\s*"([^"]+)"/i)
  if (quotedMatch?.[1]) return cleanFilename(quotedMatch[1])

  const plainMatch = header.match(/filename\s*=\s*([^;]+)/i)
  if (plainMatch?.[1]) return cleanFilename(cleanHeaderValue(plainMatch[1]))

  return undefined
}

function decodeFilename(value: string): string | undefined {
  try {
    return cleanFilename(decodeURIComponent(value))
  } catch {
    return cleanFilename(value)
  }
}

function cleanHeaderValue(value: string): string {
  return value.trim().replace(/^"(.*)"$/, '$1')
}

function cleanFilename(value: string): string | undefined {
  const filename = value.trim().replace(/[\\/:*?"<>|]+/g, '_')
  return filename || undefined
}
