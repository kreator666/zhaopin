import request from './request'

// 用户相关 API
const userApi = {
  // 获取用户信息
  getUserInfo(userId) {
    return request.get(`/api/users/${userId}`)
  },
  
  // 获取当前用户信息
  getCurrentUser() {
    return request.get('/api/auth/me')
  },
  
  // 更新用户信息
  updateProfile(data) {
    return request.put('/api/users/profile', data)
  },
  
  // 获取我的粉丝
  getFollowers() {
    return request.get('/api/users/followers')
  },
  
  // 获取我的关注
  getFollowing() {
    return request.get('/api/users/following')
  },
  
  // 关注/取消关注用户
  toggleFollow(userId) {
    return request.post(`/api/users/${userId}/follow`)
  },
  
  // 获取收藏列表
  getFavorites() {
    return request.get('/api/users/favorites')
  },
  
  // 检查是否已关注用户
  checkFollow(userId) {
    return request.get(`/api/users/${userId}/check-follow`)
  }
}

export { userApi }
export default userApi
