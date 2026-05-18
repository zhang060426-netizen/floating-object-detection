export interface ApiEnvelope<T> {
  code: number
  message?: string
  msg?: string
  data: T
}

export interface ApiErrorPayload {
  code?: number
  message?: string
  msg?: string
}
