import request from './request'

export const alumniApi = {
  // 获取校友圈列表
  getAlumniCircle(params = {}) {
    return request.get('/api/alumni/circle', { params })
  },
  
  // 获取入学年份列表
  getAlumniYears() {
    return request.get('/api/alumni/years')
  },
  
  // 获取校友圈统计
  getAlumniStats() {
    return request.get('/api/alumni/stats')
  }
}
