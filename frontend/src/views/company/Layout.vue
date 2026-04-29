<template>
  <div class="company-layout">
    <el-container>
      <el-aside width="220px" class="sidebar">
        <div class="logo">
          <el-icon size="24" color="#409EFF"><OfficeBuilding /></el-icon>
          <span>企业管理中心</span>
        </div>
        
        <el-menu
          :default-active="$route.path"
          router
          class="company-menu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/company">
            <el-icon><HomeFilled /></el-icon>
            <span>概览</span>
          </el-menu-item>
          
          <el-menu-item index="/company/jobs">
            <el-icon><Document /></el-icon>
            <span>职位管理</span>
          </el-menu-item>
          
          <el-menu-item index="/company/applications">
            <el-icon><MessageBox /></el-icon>
            <span>收到的简历</span>
          </el-menu-item>
          
          <el-menu-item index="/company/campus-talks">
            <el-icon><School /></el-icon>
            <span>校园宣讲</span>
          </el-menu-item>
          
          <el-menu-item index="/company/courses">
            <el-icon><VideoPlay /></el-icon>
            <span>课程管理</span>
          </el-menu-item>
          
          <el-menu-item index="/company/certifications">
            <el-icon><Reading /></el-icon>
            <span>考证信息</span>
          </el-menu-item>
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
          </div>
        </el-header>
        
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

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
    router.push('/')
  }).catch(() => {})
}
</script>

<style scoped>
.company-layout {
  min-height: 100vh;
}

.company-layout :deep(.el-container) {
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

.company-menu {
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

.main-content {
  background: #f0f2f5;
  padding: 20px;
}
</style>
