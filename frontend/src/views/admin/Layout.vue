<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="220px" class="sidebar">
        <div class="logo">
          <el-icon size="24" color="#409EFF"><Setting /></el-icon>
          <span>运营管理中心</span>
        </div>
        
        <el-menu
          :default-active="$route.path"
          router
          class="admin-menu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/admin">
            <el-icon><HomeFilled /></el-icon>
            <span>概览</span>
          </el-menu-item>
          
          <el-sub-menu index="training">
            <template #title>
              <el-icon><Reading /></el-icon>
              <span>培训学习</span>
            </template>
            <el-menu-item index="/admin/courses">
              <el-icon><VideoPlay /></el-icon>
              <span>课程管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/certifications">
              <el-icon><Document /></el-icon>
              <span>考证信息</span>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
        
        <div class="sidebar-footer">
          <el-button text @click="goHome">
            <el-icon><HomeFilled /></el-icon>
            返回首页
          </el-button>
          <el-button text @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-button>
        </div>
      </el-aside>
      
      <el-container>
        <el-header class="header">
          <div class="header-right">
            <span class="username">{{ userStore.userInfo?.username }}</span>
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <el-avatar :size="32" class="avatar">
                  {{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() }}
                </el-avatar>
                <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人设置</el-dropdown-item>
                  <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 修改密码对话框 -->
    <el-dialog v-model="showPasswordDialog" title="修改密码" width="400px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入当前密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="请输入新密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" :loading="changingPassword" @click="handleChangePassword">确认修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api/auth'
import { Setting, HomeFilled, Reading, VideoPlay, Document, SwitchButton, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const showPasswordDialog = ref(false)
const changingPassword = ref(false)
const passwordFormRef = ref(null)

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const goHome = () => {
  router.push('/')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/admin/login')
  }).catch(() => {})
}

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/profile/edit')
  } else if (command === 'changePassword') {
    showPasswordDialog.value = true
  } else if (command === 'logout') {
    handleLogout()
  }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    changingPassword.value = true
    try {
      await authApi.changePassword({
        old_password: passwordForm.oldPassword,
        new_password: passwordForm.newPassword
      })
      
      ElMessage.success('密码修改成功，请重新登录')
      showPasswordDialog.value = false
      
      // 清除表单
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
      
      // 退出登录
      userStore.logout()
      router.push('/admin/login')
    } catch (error) {
      const errMsg = error.response?.data?.error || '密码修改失败'
      ElMessage.error(errMsg)
    } finally {
      changingPassword.value = false
    }
  })
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.admin-layout :deep(.el-container) {
  min-height: 100vh;
}

.sidebar {
  background-color: #304156;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #1f2d3d;
}

.admin-menu {
  flex: 1;
  border-right: none;
}

.sidebar-footer {
  padding: 15px;
  border-top: 1px solid #1f2d3d;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar-footer :deep(.el-button) {
  color: #bfcbd9;
  justify-content: flex-start;
}

.sidebar-footer :deep(.el-button:hover) {
  color: #409EFF;
}

.header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.username {
  color: #606266;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.avatar {
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
  color: #fff;
  font-weight: bold;
}

.dropdown-icon {
  margin-left: 5px;
  font-size: 12px;
  color: #909399;
}

.main-content {
  background: #f0f2f5;
  padding: 20px;
}
</style>
