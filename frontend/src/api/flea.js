/**
 * 跳蚤市场相关 API
 */
import request from './request'

// ========== 物品 ==========
export const getFleaItems = (params = {}) => {
  return request.get('/api/flea/items', { params })
}

export const getFleaItem = (itemId) => {
  return request.get(`/api/flea/items/${itemId}`)
}

export const publishItem = (data) => {
  return request.post('/api/flea/items', data)
}

export const updateItem = (itemId, data) => {
  return request.put(`/api/flea/items/${itemId}`, data)
}

export const favoriteItem = (itemId) => {
  return request.post(`/api/flea/items/${itemId}/favorite`)
}

export const getMyItems = () => {
  return request.get('/api/flea/my-items')
}

// ========== 求购 ==========
export const getWanteds = (params = {}) => {
  return request.get('/api/flea/wanted', { params })
}

export const createWanted = (data) => {
  return request.post('/api/flea/wanted', data)
}

export const getMyWanteds = () => {
  return request.get('/api/flea/my-wanteds')
}
