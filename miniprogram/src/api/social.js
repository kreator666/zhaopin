import request from './request'

// 社交相关 API
const socialApi = {
  // ========== 动态/帖子相关 ==========
  
  // 获取动态列表
  getFeed(params = {}) {
    return request.get('/api/social/feed', params)
  },
  
  // 获取动态详情
  getPostDetail(postId) {
    return request.get(`/api/social/posts/${postId}`)
  },
  
  // 发布动态
  createPost(data) {
    return request.post('/api/social/posts', data)
  },
  
  // 点赞动态
  likePost(postId) {
    return request.post(`/api/social/posts/${postId}/like`)
  },
  
  // 评论动态
  commentPost(postId, data) {
    return request.post(`/api/social/posts/${postId}/comments`, data)
  },
  
  // 删除动态
  deletePost(postId) {
    return request.delete(`/api/social/posts/${postId}`)
  },
  
  // ========== 话题相关 ==========
  
  // 获取话题列表
  getTopics(params = {}) {
    return request.get('/api/social/topics', params)
  },
  
  // 获取话题详情
  getTopicDetail(topicId) {
    return request.get(`/api/social/topics/${topicId}`)
  },
  
  // ========== 校友圈相关 ==========
  
  // 获取校友圈
  getAlumniCircle(params = {}) {
    return request.get('/api/social/alumni', params)
  },
  
  // ========== 活动相关 ==========
  
  // 获取活动列表
  getEvents(params = {}) {
    return request.get('/api/social/events', params)
  },
  
  // 获取活动详情
  getEventDetail(eventId) {
    return request.get(`/api/social/events/${eventId}`)
  },
  
  // 报名活动
  enrollEvent(eventId) {
    return request.post(`/api/social/events/${eventId}/enroll`)
  },
  
  // 创建活动
  createEvent(data) {
    return request.post('/api/social/events', data)
  },
  
  // 获取我的活动
  getMyEvents(params = {}) {
    return request.get('/api/social/events/my', params)
  },
  
  // ========== 消息相关 ==========
  
  // 获取会话列表
  getConversations() {
    return request.get('/api/messages/conversations')
  },
  
  // 获取消息历史
  getMessages(userId, params = {}) {
    return request.get(`/api/messages/${userId}`, params)
  },
  
  // 发送消息
  sendMessage(userId, data) {
    return request.post(`/api/messages/${userId}`, data)
  }
}

export { socialApi }
export default socialApi
