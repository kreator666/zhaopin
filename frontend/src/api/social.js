import request from './request'

// 获取未读消息数
export const getUnreadCount = () => {
  return request.get('/api/messages/unread-count')
}

export const socialApi = {
  // 获取动态流
  getFeed(params = {}) {
    return request.get('/api/social/feed', { params })
  },
  
  // 发布动态
  createPost(data) {
    return request.post('/api/social/posts', data)
  },
  
  // 获取帖子详情
  getPostDetail(postId) {
    return request.get(`/api/social/posts/${postId}`)
  },
  
  // 删除帖子
  deletePost(postId) {
    return request.delete(`/api/social/posts/${postId}`)
  },
  
  // 点赞
  likePost(postId) {
    return request.post(`/api/social/posts/${postId}/like`)
  },
  
  // 取消点赞
  unlikePost(postId) {
    return request.delete(`/api/social/posts/${postId}/like`)
  },
  
  // 获取评论
  getComments(postId, params = {}) {
    return request.get(`/api/social/posts/${postId}/comments`, { params })
  },
  
  // 添加评论
  addComment(postId, data) {
    return request.post(`/api/social/posts/${postId}/comments`, data)
  },
  
  // 删除评论
  deleteComment(postId, commentId) {
    return request.delete(`/api/social/posts/${postId}/comments/${commentId}`)
  },
  
  // 获取活动列表
  getEvents(params = {}) {
    return request.get('/api/events', { params })
  },
  
  // 获取我的活动（参加或组织）
  getMyEvents() {
    return request.get('/api/events/my')
  },
  
  // 获取活动详情
  getEventDetail(eventId) {
    return request.get(`/api/events/${eventId}`)
  },
  
  // 报名活动
  joinEvent(eventId) {
    return request.post(`/api/events/${eventId}/join`)
  },
  
  // 取消报名
  leaveEvent(eventId) {
    return request.post(`/api/events/${eventId}/leave`)
  },
  
  // ========== 兴趣话题 ==========
  // 获取话题列表
  getTopics(params = {}) {
    return request.get('/api/topics', { params })
  },
  
  // 创建话题
  createTopic(data) {
    return request.post('/api/topics', data)
  },
  
  // 获取话题详情
  getTopic(topicId) {
    return request.get(`/api/topics/${topicId}`)
  },
  
  // 更新话题
  updateTopic(topicId, data) {
    return request.put(`/api/topics/${topicId}`, data)
  },
  
  // 删除话题
  deleteTopic(topicId) {
    return request.delete(`/api/topics/${topicId}`)
  },
  
  // 关闭话题
  closeTopic(topicId) {
    return request.post(`/api/topics/${topicId}/close`)
  },
  
  // 标记已解决
  solveTopic(topicId) {
    return request.post(`/api/topics/${topicId}/solve`)
  },
  
  // 获取话题回复
  getTopicReplies(topicId) {
    return request.get(`/api/topics/${topicId}/replies`)
  },
  
  // 发表回复
  createTopicReply(topicId, data) {
    return request.post(`/api/topics/${topicId}/replies`, data)
  },
  
  // 删除回复
  deleteTopicReply(replyId) {
    return request.delete(`/api/topics/replies/${replyId}`)
  },
  
  // 采纳最佳答案
  acceptTopicReply(replyId) {
    return request.post(`/api/topics/replies/${replyId}/accept`)
  },
  
  // 获取所有标签
  getTags() {
    return request.get('/api/topics/tags')
  },
  
  // ========== 活动约伴 ==========
  // 获取活动列表
  getEvents(params = {}) {
    return request.get('/api/events', { params })
  },
  
  // 获取活动类型
  getEventTypes() {
    return request.get('/api/events/types')
  },
  
  // 创建活动
  createEvent(data) {
    return request.post('/api/events', data)
  },
  
  // 获取活动详情
  getEvent(eventId) {
    return request.get(`/api/events/${eventId}`)
  },
  
  // 更新活动
  updateEvent(eventId, data) {
    return request.put(`/api/events/${eventId}`, data)
  },
  
  // 删除活动
  deleteEvent(eventId) {
    return request.delete(`/api/events/${eventId}`)
  },
  
  // 参加活动
  joinEvent(eventId) {
    return request.post(`/api/events/${eventId}/join`)
  },
  
  // 退出活动
  leaveEvent(eventId) {
    return request.post(`/api/events/${eventId}/leave`)
  },
  
  // 获取活动参与者
  getEventParticipants(eventId) {
    return request.get(`/api/events/${eventId}/participants`)
  },
  
  // 获取活动评论
  getEventComments(eventId) {
    return request.get(`/api/events/${eventId}/comments`)
  },
  
  // 发表评论
  createEventComment(eventId, data) {
    return request.post(`/api/events/${eventId}/comments`, data)
  },
  
  // 删除评论
  deleteEventComment(commentId) {
    return request.delete(`/api/events/comments/${commentId}`)
  },
  
  // 获取我的活动
  getMyEvents(type = 'joined') {
    return request.get('/api/events/my', { params: { type } })
  },
  
  // ========== 活动签到 ==========
  // 签到
  checkInEvent(eventId, data) {
    return request.post(`/api/events/${eventId}/checkin`, data)
  },
  
  // 获取签到状态
  getCheckInStatus(eventId) {
    return request.get(`/api/events/${eventId}/checkin/status`)
  },
  
  // 获取签到列表（创建者）
  getCheckInList(eventId) {
    return request.get(`/api/events/${eventId}/checkins`)
  },
  
  // ========== 活动评价 ==========
  // 获取评价列表
  getEventReviews(eventId) {
    return request.get(`/api/events/${eventId}/reviews`)
  },
  
  // 发表评价
  createEventReview(eventId, data) {
    return request.post(`/api/events/${eventId}/reviews`, data)
  },
  
  // 获取待评价列表
  getPendingReviews(eventId) {
    return request.get(`/api/events/${eventId}/reviews/pending`)
  }
}

export const uploadApi = {
  // 上传图片
  uploadImage(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
