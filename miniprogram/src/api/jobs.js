import request from './request'

// 职位相关 API
const jobsApi = {
  // 获取职位列表
  getJobs(params = {}) {
    return request.get('/api/jobs', params)
  },
  
  // 获取职位详情
  getJobDetail(jobId) {
    return request.get(`/api/jobs/${jobId}`)
  },
  
  // 投递简历
  applyJob(jobId, data = {}) {
    return request.post(`/api/jobs/${jobId}/apply`, data)
  },
  
  // 收藏/取消收藏职位
  toggleFavorite(jobId) {
    return request.post(`/api/jobs/${jobId}/favorite`)
  },
  
  // 获取收藏的职位
  getFavoriteJobs() {
    return request.get('/api/jobs/favorites')
  },
  
  // 获取我的投递记录
  getMyApplications() {
    return request.get('/api/applications/me')
  },
  
  // 获取校园宣讲会列表
  getCampusTalks(params = {}) {
    return request.get('/api/campus-talks', params)
  },
  
  // 获取校园宣讲会详情
  getCampusTalkDetail(talkId) {
    return request.get(`/api/campus-talks/${talkId}`)
  },
  
  // 获取面试经验列表
  getInterviews(params = {}) {
    return request.get('/api/interviews', params)
  },
  
  // 获取面试经验详情
  getInterviewDetail(interviewId) {
    return request.get(`/api/interviews/${interviewId}`)
  }
}

// 简历相关 API
const resumeApi = {
  // 获取我的简历
  getMyResume() {
    return request.get('/api/resumes/me')
  },
  
  // 创建/更新简历
  saveResume(data) {
    return request.post('/api/resumes', data)
  }
}

export { jobsApi, resumeApi }
export default jobsApi
