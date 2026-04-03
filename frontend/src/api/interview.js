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
