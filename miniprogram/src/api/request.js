// API 基础配置
// 检测当前运行环境
const isH5 = typeof window !== 'undefined' && typeof window.document !== 'undefined'

// H5 模式使用相对路径，依赖 Vite 代理处理跨域
// 小程序模式可以使用完整 URL（无跨域问题）
const BASE_URL = isH5 ? '' : 'http://localhost:5000'

// 获取 token
const getToken = () => {
  return uni.getStorageSync('token')
}

// 构建完整 URL
const buildUrl = (url) => {
  // H5 模式：使用相对路径（已配置 Vite 代理）
  if (isH5) {
    // 确保 URL 以 /api 开头
    if (url.startsWith('/api')) {
      return url
    }
    if (url.startsWith('/')) {
      return '/api' + url
    }
    return '/api/' + url
  }
  
  // 小程序模式：使用完整 URL
  return BASE_URL + url
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
    
    const url = buildUrl(options.url)
    
    // 调试日志
    console.log('[Request]', options.method || 'GET', url)
    console.log('[Request Data]', options.data || {})
    
    uni.request({
      url: url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        ...header,
        ...options.header
      },
      success: (res) => {
        console.log('[Response]', url, res)
        
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
        console.error('[Request Error]', url, err)
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
    
    const uploadUrl = buildUrl(url)
    
    uni.uploadFile({
      url: uploadUrl,
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
        console.error('[Upload Error]', uploadUrl, err)
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
  BASE_URL,
  isH5
}
