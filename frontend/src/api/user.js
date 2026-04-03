/**
 * 用户相关 API
 */
import request from './request'

// 获取用户资料
export const getUserProfile = (userId) => {
  return request.get(`/api/users/${userId}`)
}

// 获取当前用户资料
export const getMyProfile = () => {
  return request.get('/api/users/me')
}

// 更新个人资料
export const updateProfile = (data) => {
  return request.put('/api/users/me', data)
}

// 关注用户
export const followUser = (userId) => {
  return request.post(`/api/users/${userId}/follow`)
}

// 取消关注
export const unfollowUser = (userId) => {
  return request.delete(`/api/users/${userId}/follow`)
}

// 获取粉丝列表
export const getFollowers = (userId, params = {}) => {
  return request.get(`/api/users/${userId}/followers`, { params })
}

// 获取关注列表
export const getFollowing = (userId, params = {}) => {
  return request.get(`/api/users/${userId}/following`, { params })
}

// 获取用户动态
export const getUserActivities = (userId, params = {}) => {
  return request.get(`/api/users/${userId}/activities`, { params })
}

// 添加技能
export const addSkill = (data) => {
  return request.post('/api/users/me/skills', data)
}

// 删除技能
export const deleteSkill = (skillId) => {
  return request.delete(`/api/users/me/skills/${skillId}`)
}

// 搜索用户
export const searchUsers = (params) => {
  return request.get('/api/users/search', { params })
}
