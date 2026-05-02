import request from './request'

// 培训学习相关 API
const trainingApi = {
  // ========== 课程相关 ==========
  
  // 获取课程列表
  getCourses(params = {}) {
    return request.get('/api/training/courses', params)
  },
  
  // 获取课程详情
  getCourseDetail(courseId) {
    return request.get(`/api/training/courses/${courseId}`)
  },
  
  // 报名课程
  enrollCourse(courseId) {
    return request.post(`/api/training/courses/${courseId}/enroll`)
  },
  
  // 检查是否已报名
  checkEnrollment(courseId) {
    return request.get(`/api/training/courses/${courseId}/check-enrollment`)
  },
  
  // 获取我的课程
  getMyCourses(params = {}) {
    return request.get('/api/training/my-courses', params)
  },
  
  // 退课
  cancelEnrollment(courseId) {
    return request.post(`/api/training/courses/${courseId}/cancel`)
  },
  
  // 完成课程
  completeCourse(courseId) {
    return request.post(`/api/training/courses/${courseId}/complete`)
  },
  
  // ========== 运营端课程管理 ==========
  
  // 获取管理端课程列表
  getAdminCourses(params = {}) {
    return request.get('/api/training/admin/courses', params)
  },
  
  // 创建课程
  createCourse(data) {
    return request.post('/api/training/courses', data)
  },
  
  // 更新课程
  updateCourse(courseId, data) {
    return request.put(`/api/training/courses/${courseId}`, data)
  },
  
  // 删除课程
  deleteCourse(courseId) {
    return request.delete(`/api/training/courses/${courseId}`)
  },
  
  // ========== 学习资料相关 ==========
  
  // 获取学习资料列表
  getMaterials(params = {}) {
    return request.get('/api/training/materials', params)
  },
  
  // 获取学习资料详情
  getMaterialDetail(materialId) {
    return request.get(`/api/training/materials/${materialId}`)
  },
  
  // 上传学习资料
  uploadMaterial(data) {
    return request.post('/api/training/materials', data)
  },
  
  // 删除学习资料
  deleteMaterial(materialId) {
    return request.delete(`/api/training/materials/${materialId}`)
  },
  
  // 点赞学习资料
  likeMaterial(materialId) {
    return request.post(`/api/training/materials/${materialId}/like`)
  },
  
  // 下载学习资料（计数）
  downloadMaterial(materialId) {
    return request.post(`/api/training/materials/${materialId}/download`)
  },
  
  // 获取我的学习资料
  getMyMaterials(params = {}) {
    return request.get('/api/training/my-materials', params)
  },
  
  // ========== 考证信息相关 ==========
  
  // 获取考证信息列表
  getCertifications(params = {}) {
    return request.get('/api/training/certifications', params)
  },
  
  // 获取考证详情
  getCertificationDetail(certId) {
    return request.get(`/api/training/certifications/${certId}`)
  },
  
  // ========== 运营端考证信息管理 ==========
  
  // 获取管理端考证列表
  getAdminCertifications(params = {}) {
    return request.get('/api/training/admin/certifications', params)
  },
  
  // 创建考证信息
  createCertification(data) {
    return request.post('/api/training/certifications', data)
  },
  
  // 更新考证信息
  updateCertification(certId, data) {
    return request.put(`/api/training/certifications/${certId}`, data)
  },
  
  // 删除考证信息
  deleteCertification(certId) {
    return request.delete(`/api/training/certifications/${certId}`)
  }
}

export { trainingApi }
export default trainingApi
