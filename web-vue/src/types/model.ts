export interface PublishedModel {
  id: string
  name: string
  base_model?: string
  weight_path?: string
  status?: string
  is_dev_placeholder?: boolean
}
