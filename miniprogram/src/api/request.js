// API 基础配置
const BASE_URL = 'http://localhost:5000'

// 获取 token
const getToken = () => {
  return uni.getStorageSync('token')
}

// 基础请求封装
const request = (options) => {
  return new Promise((resolve, reject) => {
    const token = getToken()
    
    const header = {
      'Content-Type': 'application/json'
    }
    
    if (token) {
      header['Authorization'] = `Bearer ${token}`
    }
    
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        ...header,
        ...options.header
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 未授权，清除 token 并跳转登录
          uni.removeStorageSync('token')
          uni.removeStorageSync('userInfo')
          
          // 提示登录
          uni.showToast({
            title: '请先登录',
            icon: 'none'
          })
          
          setTimeout(() => {
            uni.navigateTo({
              url: '/pages/login/index'
            })
          }, 1500)
          
          reject(res.data)
        } else if (res.statusCode === 403) {
          uni.showToast({
            title: res.data?.error || '无权访问',
            icon: 'none'
          })
          reject(res.data)
        } else {
          uni.showToast({
            title: res.data?.error || '请求失败',
            icon: 'none'
          })
          reject(res.data)
        }
      },
      fail: (err) => {
        console.error('请求失败:', err)
        uni.showToast({
          title: '网络错误，请检查网络连接',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

// GET 请求
const get = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'GET',
    data,
    ...options
  })
}

// POST 请求
const post = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'POST',
    data,
    ...options
  })
}

// PUT 请求
const put = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'PUT',
    data,
    ...options
  })
}

// DELETE 请求
const del = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'DELETE',
    data,
    ...options
  })
}

// 上传文件
const uploadFile = (url, filePath, name = 'file', extraData = {}) => {
  return new Promise((resolve, reject) => {
    const token = getToken()
    
    uni.uploadFile({
      url: BASE_URL + url,
      filePath: filePath,
      name: name,
      formData: extraData,
      header: token ? {
        'Authorization': `Bearer ${token}`
      } : {},
      success: (res) => {
        if (res.statusCode === 200) {
          try {
            const data = JSON.parse(res.data)
            resolve(data)
          } catch (e) {
            resolve(res.data)
          }
        } else {
          reject(res)
        }
      },
      fail: (err) => {
        console.error('上传失败:', err)
        uni.showToast({
          title: '上传失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

export default {
  request,
  get,
  post,
  put,
  delete: del,
  uploadFile,
  BASE_URL
}
