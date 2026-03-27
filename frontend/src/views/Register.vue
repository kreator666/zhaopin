<template>
  <div class="register-page">
    <div class="register-box">
      <h2>用户注册</h2>
      
      <el-radio-group v-model="form.role" size="large" style="margin-bottom: 20px; width: 100%; justify-content: center;">
        <el-radio-button label="job_seeker">我要找工作</el-radio-button>
        <el-radio-button label="company">我要招人</el-radio-button>
      </el-radio-group>
      
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" size="large">
            <template #prefix><el-icon><User /></el-icon></template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" size="large">
            <template #prefix><el-icon><Message /></el-icon></template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" show-password>
            <template #prefix><el-icon><Lock /></el-icon></template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" size="large" show-password>
            <template #prefix><el-icon><Lock /></el-icon></template>
          </el-input>
        </el-form-item>
        
        <!-- 企业用户额外字段 -->
        <template v-if="form.role === 'company'">
          <el-divider>企业信息</el-divider>
          
          <el-form-item label="公司名称" prop="company_name">
            <el-input v-model="form.company_name" placeholder="请输入公司名称" size="large" />
          </el-form-item>
          
          <el-form-item label="所属行业">
            <el-input v-model="form.industry" placeholder="请输入所属行业" size="large" />
          </el-form-item>
          
          <el-form-item label="公司地址">
            <el-input v-model="form.company_location" placeholder="请输入公司地址" size="large" />
          </el-form-item>
          
          <el-form-item label="公司简介">
            <el-input v-model="form.company_description" type="textarea" :rows="3" placeholder="请输入公司简介" />
          </el-form-item>
        </template>
        
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" style="width: 100%" @click="handleSubmit">
            注册
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <span>已有账号？</span>
          <router-link to="/login">立即登录</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  role: 'job_seeker',
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  company_name: '',
  industry: '',
  company_location: '',
  company_description: ''
})

const validatePass2 = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ],
  company_name: [{ required: true, message: '请输入公司名称', trigger: 'blur' }]
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  // 移除confirmPassword
  const submitData = { ...form }
  delete submitData.confirmPassword
  
  loading.value = true
  try {
    const res = await authApi.register(submitData)
    userStore.setToken(res.access_token)
    userStore.setUserInfo(res.user)
    ElMessage.success('注册成功')
    router.push('/')
  } catch (error) {
    console.error('注册失败', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 0;
}

.register-box {
  width: 450px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.register-box h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
}

.form-footer a {
  color: #409EFF;
  text-decoration: none;
  margin-left: 5px;
}
</style>
