/**
 * 培训学习相关 API
 */
import request from './request'

// ========== 课程（学生端）==========
export const getCourses = (params = {}) => {
  return request.get('/api/training/courses', { params })
}

export const getCourse = (courseId) => {
  return request.get(`/api/training/courses/${courseId}`)
}

export const enrollCourse = (courseId) => {
  return request.post(`/api/training/courses/${courseId}/enroll`)
}

export const checkEnrollment = (courseId) => {
  return request.get(`/api/training/courses/${courseId}/check-enrollment`)
}

export const getMyCourses = (params = {}) => {
  return request.get('/api/training/my-courses', { params })
}

// ========== 课程（运营端：管理员/企业用户）==========
export const getAdminCourses = (params = {}) => {
  return request.get('/api/training/admin/courses', { params })
}

export const createCourse = (data) => {
  return request.post('/api/training/courses', data)
}

export const updateCourse = (courseId, data) => {
  return request.put(`/api/training/courses/${courseId}`, data)
}

export const deleteCourse = (courseId) => {
  return request.delete(`/api/training/courses/${courseId}`)
}

// ========== 学习资料 ==========
export const getMaterials = (params = {}) => {
  return request.get('/api/training/materials', { params })
}

export const getMaterial = (materialId) => {
  return request.get(`/api/training/materials/${materialId}`)
}

export const uploadMaterial = (data) => {
  return request.post('/api/training/materials', data)
}

export const updateMaterial = (materialId, data) => {
  return request.put(`/api/training/materials/${materialId}`, data)
}

export const deleteMaterial = (materialId) => {
  return request.delete(`/api/training/materials/${materialId}`)
}

export const downloadMaterial = (materialId) => {
  return request.post(`/api/training/materials/${materialId}/download`)
}

export const likeMaterial = (materialId) => {
  return request.post(`/api/training/materials/${materialId}/like`)
}

export const getMyMaterials = (params = {}) => {
  return request.get('/api/training/my-materials', { params })
}

// ========== 考证信息 ==========
export const getCertifications = (params = {}) => {
  return request.get('/api/training/certifications', { params })
}
