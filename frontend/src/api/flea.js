/**
 * 跳蚤市场相关 API
 */
import request from './request'

// ========== 物品 ==========
export const getFleaItems = (params = {}) => {
  return request.get('/flea/items', { params })
}

export const getFleaItem = (itemId) => {
  return request.get(`/flea/items/${itemId}`)
}

export const publishItem = (data) => {
  return request.post('/flea/items', data)
}

export const updateItem = (itemId, data) => {
  return request.put(`/flea/items/${itemId}`, data)
}

export const favoriteItem = (itemId) => {
  return request.post(`/flea/items/${itemId}/favorite`)
}

export const getMyItems = () => {
  return request.get('/flea/my-items')
}

// ========== 求购 ==========
export const getWanteds = (params = {}) => {
  return request.get('/flea/wanted', { params })
}

export const createWanted = (data) => {
  return request.post('/flea/wanted', data)
}

export const getMyWanteds = () => {
  return request.get('/flea/my-wanteds')
}
