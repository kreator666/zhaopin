<template>
  <div class="followers-page">
    <div class="container">
      <h2>{{ pageTitle }}</h2>
      
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="关注" name="following">
          <div class="users-list">
            <el-empty v-if="followingList.length === 0" description="暂无关注" />
            <div 
              v-else 
              v-for="user in followingList" 
              :key="user.id" 
              class="user-card"
              @click="viewProfile(user.id)"
            >
              <el-avatar :size="60" :src="user.avatar_url" />
              <div class="user-info">
                <h4>{{ user.username }}</h4>
                <p v-if="user.bio" class="bio">{{ user.bio }}</p>
                <div class="user-meta">
                  <el-tag v-if="user.school_name" size="small">{{ user.school_name }}</el-tag>
                  <span class="follow-time">关注于 {{ formatTime(user.follow_time) }}</span>
                </div>
              </div>
              <el-button 
                type="primary" 
                size="small"
                @click.stop="unfollow(user.id)"
              >
                已关注
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="粉丝" name="followers">
          <div class="users-list">
            <el-empty v-if="followersList.length === 0" description="暂无粉丝" />
            <div 
              v-else 
              v-for="user in followersList" 
              :key="user.id" 
              class="user-card"
              @click="viewProfile(user.id)"
            >
              <el-avatar :size="60" :src="user.avatar_url" />
              <div class="user-info">
                <h4>{{ user.username }}</h4>
                <p v-if="user.bio" class="bio">{{ user.bio }}</p>
                <div class="user-meta">
                  <el-tag v-if="user.school_name" size="small">{{ user.school_name }}</el-tag>
                </div>
              </div>
              <el-button 
                :type="user.is_following ? 'default' : 'primary'"
                size="small"
                @click.stop="toggleFollow(user)"
              >
                {{ user.is_following ? '已关注' : '+ 关注' }}
              </el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getFollowers, getFollowing, followUser, unfollowUser } from '@/api/user'

const route = useRoute()
const router = useRouter()

const activeTab = ref('following')
const followingList = ref([])
const followersList = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const userId = ref(null)

const pageTitle = computed(() => {
  return activeTab.value === 'following' ? '我的关注' : '我的粉丝'
})

const fetchData = async () => {
  try {
    const params = { page: currentPage.value, per_page: pageSize.value }
    
    if (activeTab.value === 'following') {
      const res = await getFollowing(userId.value, params)
      followingList.value = res.data.items
      total.value = res.data.total
    } else {
      const res = await getFollowers(userId.value, params)
      followersList.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

const handleTabChange = () => {
  currentPage.value = 1
  fetchData()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchData()
}

const viewProfile = (id) => {
  router.push(`/profile/${id}`)
}

const unfollow = async (id) => {
  try {
    await unfollowUser(id)
    ElMessage.success('已取消关注')
    followingList.value = followingList.value.filter(u => u.id !== id)
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const toggleFollow = async (user) => {
  try {
    if (user.is_following) {
      await unfollowUser(user.id)
      user.is_following = false
    } else {
      await followUser(user.id)
      user.is_following = true
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  // 从路由参数获取用户ID和默认标签
  userId.value = route.query.userId || 'me'
  activeTab.value = route.query.type || 'following'
  fetchData()
})
</script>

<style scoped>
.followers-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 24px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

h2 {
  margin-bottom: 24px;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.user-card:hover {
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.user-info {
  flex: 1;
}

.user-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
}

.bio {
  color: #666;
  font-size: 14px;
  margin: 0 0 8px 0;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.follow-time {
  font-size: 12px;
  color: #999;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
