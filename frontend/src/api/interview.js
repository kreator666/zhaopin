/**
 * 面试经验、宣讲会相关 API
 */
import request from './request'

// ========== 面试经验 ==========
export const getInterviewExperiences = (params = {}) => {
  return request.get('/api/interview/experiences', { params })
}

export const getInterviewExperience = (expId) => {
  return request.get(`/api/interview/experiences/${expId}`)
}

export const createInterviewExperience = (data) => {
  return request.post('/api/interview/experiences', data)
}

export const markHelpful = (expId) => {
  return request.post(`/api/interview/experiences/${expId}/helpful`)
}

// ========== 校园宣讲会 ==========
export const getCampusTalks = (params = {}) => {
  return request.get('/api/interview/campus-talks', { params })
}

export const getCampusTalk = (talkId) => {
  return request.get(`/api/interview/campus-talks/${talkId}`)
}

// ========== 企业宣讲会管理 ==========
export const getMyCampusTalks = (params = {}) => {
  return request.get('/api/interview/my/campus-talks', { params })
}

export const createCampusTalk = (data) => {
  return request.post('/api/interview/campus-talks', data)
}

export const updateCampusTalk = (talkId, data) => {
  return request.put(`/api/interview/campus-talks/${talkId}`, data)
}

export const deleteCampusTalk = (talkId) => {
  return request.delete(`/api/interview/campus-talks/${talkId}`)
}
