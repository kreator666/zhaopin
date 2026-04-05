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
  
  // 获取圈子列表
  getCircles(params = {}) {
    return request.get('/api/circles', { params })
  },
  
  // 获取我加入的圈子
  getMyCircles() {
    return request.get('/api/circles/my')
  },
  
  // 获取圈子详情
  getCircleDetail(circleId) {
    return request.get(`/api/circles/${circleId}`)
  },
  
  // 加入圈子
  joinCircle(circleId) {
    return request.post(`/api/circles/${circleId}/join`)
  },
  
  // 退出圈子
  leaveCircle(circleId) {
    return request.post(`/api/circles/${circleId}/leave`)
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
