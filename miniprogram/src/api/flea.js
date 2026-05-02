import request from './request'

// 跳蚤市场相关 API
const fleaApi = {
  // ========== 物品相关 ==========
  
  // 获取物品列表
  getItems(params = {}) {
    return request.get('/api/flea/items', params)
  },
  
  // 获取物品详情
  getItemDetail(itemId) {
    return request.get(`/api/flea/items/${itemId}`)
  },
  
  // 发布物品
  publishItem(data) {
    return request.post('/api/flea/items', data)
  },
  
  // 更新物品
  updateItem(itemId, data) {
    return request.put(`/api/flea/items/${itemId}`, data)
  },
  
  // 删除物品
  deleteItem(itemId) {
    return request.delete(`/api/flea/items/${itemId}`)
  },
  
  // 下架物品
  takeDownItem(itemId) {
    return request.post(`/api/flea/items/${itemId}/take-down`)
  },
  
  // 上架物品
  publishItemAgain(itemId) {
    return request.post(`/api/flea/items/${itemId}/publish`)
  },
  
  // 获取我的物品
  getMyItems(params = {}) {
    return request.get('/api/flea/my-items', params)
  },
  
  // ========== 求购相关 ==========
  
  // 获取求购列表
  getWanted(params = {}) {
    return request.get('/api/flea/wanted', params)
  },
  
  // 获取求购详情
  getWantedDetail(wantedId) {
    return request.get(`/api/flea/wanted/${wantedId}`)
  },
  
  // 发布求购
  publishWanted(data) {
    return request.post('/api/flea/wanted', data)
  },
  
  // 收藏物品
  toggleFavorite(itemId) {
    return request.post(`/api/flea/items/${itemId}/favorite`)
  },
  
  // 获取收藏列表
  getFavorites() {
    return request.get('/api/flea/favorites')
  }
}

export { fleaApi }
export default fleaApi
