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
