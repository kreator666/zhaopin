/**
 * 培训学习相关 API
 */
import request from './request'

// ========== 课程 ==========
export const getCourses = (params = {}) => {
  return request.get('/training/courses', { params })
}

export const getCourse = (courseId) => {
  return request.get(`/training/courses/${courseId}`)
}

export const enrollCourse = (courseId) => {
  return request.post(`/training/courses/${courseId}/enroll`)
}

export const getMyCourses = () => {
  return request.get('/training/my-courses')
}

// ========== 学习资料 ==========
export const getMaterials = (params = {}) => {
  return request.get('/training/materials', { params })
}

export const uploadMaterial = (data) => {
  return request.post('/training/materials', data)
}

export const downloadMaterial = (materialId) => {
  return request.post(`/training/materials/${materialId}/download`)
}

// ========== 考证信息 ==========
export const getCertifications = (params = {}) => {
  return request.get('/training/certifications', { params })
}
