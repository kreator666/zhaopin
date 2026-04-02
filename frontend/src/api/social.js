/**
 * 社交相关 API
 */
import request from './request'

// ========== 动态 ==========
export const getFeed = (params = {}) => {
  return request.get('/social/feed', { params })
}

export const createPost = (data) => {
  return request.post('/social/posts', data)
}

export const getPost = (postId) => {
  return request.get(`/social/posts/${postId}`)
}

export const deletePost = (postId) => {
  return request.delete(`/social/posts/${postId}`)
}

export const likePost = (postId) => {
  return request.post(`/social/posts/${postId}/like`)
}

export const unlikePost = (postId) => {
  return request.delete(`/social/posts/${postId}/like`)
}

export const getComments = (postId) => {
  return request.get(`/social/posts/${postId}/comments`)
}

export const addComment = (postId, data) => {
  return request.post(`/social/posts/${postId}/comments`, data)
}

// ========== 圈子 ==========
export const getCircles = (params = {}) => {
  return request.get('/circles', { params })
}

export const getCircle = (circleId) => {
  return request.get(`/circles/${circleId}`)
}

export const createCircle = (data) => {
  return request.post('/circles', data)
}

export const joinCircle = (circleId) => {
  return request.post(`/circles/${circleId}/join`)
}

export const leaveCircle = (circleId) => {
  return request.post(`/circles/${circleId}/leave`)
}

export const getMyCircles = () => {
  return request.get('/circles/my')
}

// ========== 活动 ==========
export const getEvents = (params = {}) => {
  return request.get('/events', { params })
}

export const getEvent = (eventId) => {
  return request.get(`/events/${eventId}`)
}

export const createEvent = (data) => {
  return request.post('/events', data)
}

export const joinEvent = (eventId) => {
  return request.post(`/events/${eventId}/join`)
}

export const leaveEvent = (eventId) => {
  return request.post(`/events/${eventId}/leave`)
}

export const getMyEvents = () => {
  return request.get('/events/my')
}

// ========== 私信 ==========
export const getConversations = () => {
  return request.get('/messages/conversations')
}

export const getMessages = (userId, params = {}) => {
  return request.get(`/messages/${userId}`, { params })
}

export const sendMessage = (data) => {
  return request.post('/messages', data)
}

export const getUnreadCount = () => {
  return request.get('/messages/unread-count')
}
