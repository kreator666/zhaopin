import request from './request'

export const resumeApi = {
  // 获取我的简历
  getMyResume() {
    return request.get('/api/resume')
  },
  
  // 创建/更新简历
  saveResume(data) {
    return request.post('/api/resume', data)
  }
}
