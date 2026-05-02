import request from './request'

// 认证相关 API
const authApi = {
  // 登录
  login(data) {
    return request.post('/api/auth/login', data)
  },
  
  // 注册
  register(data) {
    return request.post('/api/auth/register', data)
  },
  
  // 获取当前用户信息
  getCurrentUser() {
    return request.get('/api/auth/me')
  },
  
  // 修改密码
  changePassword(data) {
    return request.post('/api/auth/change-password', data)
  }
}

export { authApi }
export default authApi
