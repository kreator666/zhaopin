import request from './request'

export const authApi = {
  // 注册
  register(data) {
    return request.post('/api/auth/register', data)
  },
  
  // 登录
  login(data) {
    return request.post('/api/auth/login', data)
  },
  
  // 获取当前用户
  getCurrentUser() {
    return request.get('/api/auth/me')
  },
  
  // 修改密码
  changePassword(data) {
    return request.post('/api/auth/change-password', data)
  }
}
