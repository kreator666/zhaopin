/**
 * 社交相关 API
 */
import request from './request'

// ========== 动态 ==========
export const getFeed = (params = {}) => {
  return request.get('/api/social/feed', { params })
}

export const createPost = (data) => {
  return request.post('/api/social/posts', data)
}

export const getPost = (postId) => {
  return request.get(`/api/social/posts/${postId}`)
}

export const deletePost = (postId) => {
  return request.delete(`/api/social/posts/${postId}`)
}

export const likePost = (postId) => {
  return request.post(`/api/social/posts/${postId}/like`)
}

export const unlikePost = (postId) => {
  return request.delete(`/api/social/posts/${postId}/like`)
}

export const getComments = (postId) => {
  return request.get(`/api/social/posts/${postId}/comments`)
}

export const addComment = (postId, data) => {
  return request.post(`/api/social/posts/${postId}/comments`, data)
}

// ========== 圈子 ==========
export const getCircles = (params = {}) => {
  return request.get('/api/circles', { params })
}

export const getCircle = (circleId) => {
  return request.get(`/api/circles/${circleId}`)
}

export const createCircle = (data) => {
  return request.post('/api/circles', data)
}

export const joinCircle = (circleId) => {
  return request.post(`/api/circles/${circleId}/join`)
}

export const leaveCircle = (circleId) => {
  return request.post(`/api/circles/${circleId}/leave`)
}

export const getMyCircles = () => {
  return request.get('/api/circles/my')
}

// ========== 活动 ==========
export const getEvents = (params = {}) => {
  return request.get('/api/events', { params })
}

export const getEvent = (eventId) => {
  return request.get(`/api/events/${eventId}`)
}

export const createEvent = (data) => {
  return request.post('/api/events', data)
}

export const joinEvent = (eventId) => {
  return request.post(`/api/events/${eventId}/join`)
}

export const leaveEvent = (eventId) => {
  return request.post(`/api/events/${eventId}/leave`)
}

export const getMyEvents = () => {
  return request.get('/api/events/my')
}

// ========== 私信 ==========
export const getConversations = () => {
  return request.get('/api/messages/conversations')
}

export const getMessages = (userId, params = {}) => {
  return request.get(`/api/messages/${userId}`, { params })
}

export const sendMessage = (data) => {
  return request.post('/api/messages', data)
}

export const getUnreadCount = () => {
  return request.get('/api/messages/unread-count')
}
