import request from './request'

export const jobsApi = {
  // 获取职位列表
  getList(params = {}) {
    return request.get('/api/jobs', { params })
  },
  
  // 获取职位详情
  getDetail(id) {
    return request.get(`/api/jobs/${id}`)
  },
  
  // 发布职位
  create(data) {
    return request.post('/api/jobs', data)
  },
  
  // 更新职位
  update(id, data) {
    return request.put(`/api/jobs/${id}`, data)
  },
  
  // 删除职位
  delete(id) {
    return request.delete(`/api/jobs/${id}`)
  },
  
  // 获取我发布的职位
  getMyJobs(params = {}) {
    return request.get('/api/jobs/my', { params })
  }
}
