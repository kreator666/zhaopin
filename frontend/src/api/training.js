/**
 * 培训学习相关 API
 */
import request from './request'

// ========== 课程 ==========
export const getCourses = (params = {}) => {
  return request.get('/api/training/courses', { params })
}

export const getCourse = (courseId) => {
  return request.get(`/api/training/courses/${courseId}`)
}

export const enrollCourse = (courseId) => {
  return request.post(`/api/training/courses/${courseId}/enroll`)
}

export const getMyCourses = () => {
  return request.get('/api/training/my-courses')
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
