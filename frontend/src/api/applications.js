import request from './request'

export const applicationsApi = {
  // 投递简历
  apply(data) {
    return request.post('/api/applications', data)
  },
  
  // 获取我的投递记录
  getMyApplications(params = {}) {
    return request.get('/api/applications/my', { params })
  },
  
  // 获取收到的简历（HR）
  getReceivedApplications(params = {}) {
    return request.get('/api/applications/received', { params })
  },
  
  // 更新投递状态
  updateStatus(id, data) {
    return request.put(`/api/applications/${id}`, data)
  }
}
