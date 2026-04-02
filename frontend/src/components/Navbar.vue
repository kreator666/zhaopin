<template>
  <el-header class="navbar">
    <div class="container">
      <div class="logo" @click="$router.push('/')">
        <el-icon size="28" color="#409EFF"><Connection /></el-icon>
        <span>大学生社区</span>
      </div>
      
      <nav class="nav-menu">
        <router-link to="/" exact>首页</router-link>
        
        <!-- 求职模块 -->
        <el-dropdown>
          <span class="nav-link">求职就业<el-icon class="dropdown-icon"><ArrowDown /></el-icon></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/jobs')">职位搜索</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/interview')">面试经验</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/campus-talks')">宣讲会</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 培训学习 -->
        <el-dropdown>
          <span class="nav-link">培训学习<el-icon class="dropdown-icon"><ArrowDown /></el-icon></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/training/courses')">精品课程</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/training/materials')">学习资料</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/training/certifications')">考证信息</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 交友社交 -->
        <el-dropdown>
          <span class="nav-link">交友社交<el-icon class="dropdown-icon"><ArrowDown /></el-icon></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/social')">校友圈</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/social/circles')">兴趣圈子</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/social/events')">活动约伴</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 跳蚤市场 -->
        <router-link to="/flea">跳蚤市场</router-link>
        
        <template v-if="userStore.isPersonalUser">
          <router-link to="/resume">我的简历</router-link>
        </template>
        
        <template v-if="userStore.isCompany">
          <router-link to="/company">企业管理</router-link>
        </template>
      </nav>
      
      <div class="user-actions">
        <!-- 消息通知 -->
        <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="message-badge" v-if="userStore.isLoggedIn">
          <el-icon size="22" @click="$router.push('/messages')" class="message-icon"><Bell /></el-icon>
        </el-badge>

        <template v-if="userStore.isLoggedIn">
          <el-dropdown>
            <span class="user-info">
              <el-avatar :size="32" :src="userStore.userInfo?.avatar_url" />
              {{ userStore.userInfo?.username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push(`/profile/${userStore.userInfo?.id}`)">
                  <el-icon><User /></el-icon>个人主页
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/profile/edit')">
                  <el-icon><Edit /></el-icon>编辑资料
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/my/favorites')">
                  <el-icon><Star /></el-icon>我的收藏
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/applications')" v-if="userStore.isPersonalUser">
                  <el-icon><Document /></el-icon>投递记录
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/training/my-courses')">
                  <el-icon><Reading /></el-icon>我的课程
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/flea/my-items')">
                  <el-icon><Goods /></el-icon>我的闲置
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
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
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Connection, ArrowDown, User, Edit, Star, Document, Reading, Goods, SwitchButton, Bell } from '@element-plus/icons-vue'
import { getUnreadCount } from '@/api/social'

const userStore = useUserStore()
const router = useRouter()
const unreadCount = ref(0)

const fetchUnreadCount = async () => {
  if (!userStore.isLoggedIn) return
  try {
    const res = await getUnreadCount()
    unreadCount.value = res.data.unread_count
  } catch (error) {
    console.error('获取未读消息失败', error)
  }
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

onMounted(() => {
  fetchUnreadCount()
  // 定时刷新未读消息数
  setInterval(fetchUnreadCount, 60000)
})
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
  max-width: 1400px;
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
  gap: 24px;
  margin-left: 40px;
  align-items: center;
}

.nav-menu a,
.nav-link {
  color: #333;
  text-decoration: none;
  font-size: 15px;
  padding: 5px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-menu a:hover,
.nav-menu a.router-link-active,
.nav-link:hover {
  color: #409EFF;
  border-bottom-color: #409EFF;
}

.dropdown-icon {
  font-size: 12px;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.message-badge {
  cursor: pointer;
}

.message-icon {
  color: #666;
  transition: color 0.3s;
}

.message-icon:hover {
  color: #409EFF;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #333;
}

@media (max-width: 1200px) {
  .nav-menu {
    gap: 16px;
    margin-left: 20px;
  }
  
  .nav-menu a,
  .nav-link {
    font-size: 14px;
  }
}
</style>
