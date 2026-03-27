<template>
  <el-header class="navbar">
    <div class="container">
      <div class="logo" @click="$router.push('/')">
        <el-icon size="28" color="#409EFF"><Connection /></el-icon>
        <span>招聘求职网</span>
      </div>
      
      <nav class="nav-menu">
        <router-link to="/" exact>首页</router-link>
        <router-link to="/jobs">职位搜索</router-link>
        <template v-if="userStore.isJobSeeker">
          <router-link to="/resume">我的简历</router-link>
          <router-link to="/applications">投递记录</router-link>
        </template>
        <template v-if="userStore.isCompany">
          <router-link to="/company">企业管理</router-link>
        </template>
      </nav>
      
      <div class="user-actions">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown>
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ userStore.userInfo?.username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" @click="$router.push('/login')">登录</el-button>
          <el-button @click="$router.push('/register')">注册</el-button>
        </template>
      </div>
    </div>
  </el-header>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const router = useRouter()

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<style scoped>
.navbar {
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 0;
  height: 60px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
  cursor: pointer;
}

.nav-menu {
  flex: 1;
  display: flex;
  gap: 30px;
  margin-left: 50px;
}

.nav-menu a {
  color: #333;
  text-decoration: none;
  font-size: 15px;
  padding: 5px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  color: #409EFF;
  border-bottom-color: #409EFF;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  color: #333;
}
</style>
