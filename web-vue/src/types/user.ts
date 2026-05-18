export interface UserInfo {
  id: string
  username: string
  role: string
}

export interface LoginResponse {
  token: string
  user: UserInfo
}
