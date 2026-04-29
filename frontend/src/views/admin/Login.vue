<template>
  <div class="admin-login-page">
    <div class="login-container">
      <div class="login-left">
        <div class="logo-section">
          <div class="logo-icon">
            <el-icon :size="60"><Setting /></el-icon>
          </div>
          <h1>运营管理中心</h1>
          <p class="subtitle">Administration Platform</p>
        </div>
        <div class="features">
          <div class="feature-item">
            <el-icon :size="24"><VideoPlay /></el-icon>
            <span>精品课程管理</span>
          </div>
          <div class="feature-item">
            <el-icon :size="24"><Document /></el-icon>
            <span>考证信息发布</span>
          </div>
          <div class="feature-item">
            <el-icon :size="24"><DataAnalysis /></el-icon>
            <span>数据统计分析</span>
          </div>
        </div>
      </div>
      
      <div class="login-right">
        <div class="login-box">
          <h2>运营员登录</h2>
          <p class="login-tip">请使用运营账号登录</p>
          
          <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
            <el-form-item label="用户名" prop="username">
              <el-input 
                v-model="form.username" 
                placeholder="请输入用户名" 
                size="large"
                clearable
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input 
                v-model="form.password" 
                type="password" 
                placeholder="请输入密码" 
                size="large"
                show-password
                @keyup.enter="handleSubmit"
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                :loading="loading"
                style="width: 100%; height: 48px; font-size: 16px;"
                @click="handleSubmit"
              >
                <el-icon v-if="!loading"><Unlock /></el-icon>
                {{ loading ? '登录中...' : '登 录' }}
              </el-button>
            </el-form-item>
          </el-form>
          
          <div class="login-footer">
            <el-divider>
              <span class="divider-text">提示</span>
            </el-divider>
            <div class="hint-box">
              <el-icon><InfoFilled /></el-icon>
              <span>默认账号：admin / admin</span>
            </div>
            <div class="back-links">
              <router-link to="/login">返回用户登录</router-link>
              <span class="link-separator">|</span>
              <router-link to="/">返回首页</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'
import { 
  Setting, VideoPlay, Document, DataAnalysis, 
  User, Lock, Unlock, InfoFilled 
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    const res = await authApi.login(form)
    const { access_token, user } = res.data
    
    // 验证是否是管理员角色
    if (user.role !== 'admin') {
      ElMessage.error('该账号不是运营管理员账号')
      loading.value = false
      return
    }
    
    userStore.setToken(access_token)
    userStore.setUserInfo(user)
    ElMessage.success('登录成功，欢迎回来！')
    
    // 跳转到运营端
    router.push('/admin')
  } catch (error) {
    const errMsg = error.response?.data?.error || '登录失败，请检查用户名和密码'
    ElMessage.error(errMsg)
    console.error('登录失败', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  position: relative;
  overflow: hidden;
}

.admin-login-page::before {
  content: '';
  position: absolute;
  width: 800px;
  height: 800px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  top: -200px;
  right: -200px;
  z-index: 0;
}

.admin-login-page::after {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  bottom: -100px;
  left: -100px;
  z-index: 0;
}

.login-container {
  display: flex;
  width: 900px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.login-left {
  width: 380px;
  padding: 50px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.logo-section {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.logo-section h1 {
  font-size: 24px;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.subtitle {
  font-size: 14px;
  opacity: 0.8;
  margin: 0;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.2);
}

.feature-item span {
  font-size: 15px;
}

.login-right {
  flex: 1;
  padding: 50px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-box {
  width: 100%;
}

.login-box h2 {
  margin: 0 0 8px 0;
  font-size: 26px;
  color: #333;
}

.login-tip {
  margin: 0 0 30px 0;
  color: #909399;
  font-size: 14px;
}

.login-footer {
  margin-top: 30px;
}

.divider-text {
  color: #c0c4cc;
  font-size: 13px;
}

.hint-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: #f4f4f5;
  border-radius: 8px;
  color: #909399;
  font-size: 14px;
  margin-bottom: 20px;
}

.hint-box .el-icon {
  color: #e6a23c;
}

.back-links {
  text-align: center;
  font-size: 14px;
}

.back-links a {
  color: #409EFF;
  text-decoration: none;
}

.back-links a:hover {
  text-decoration: underline;
}

.link-separator {
  color: #c0c4cc;
  margin: 0 10px;
}
</style>
