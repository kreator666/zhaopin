import request from './request'

export const uploadApi = {
  // 上传图片
  uploadImage(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 上传头像
  uploadAvatar(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/upload/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 上传封面
  uploadCover(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/upload/cover', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
