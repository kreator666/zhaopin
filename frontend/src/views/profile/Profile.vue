<template>
  <div class="profile-page">
    <!-- 封面图 -->
    <div class="cover-section" :style="coverStyle">
      <div class="cover-overlay"></div>
    </div>

    <!-- 用户信息卡片 -->
    <div class="profile-header">
      <div class="container">
        <div class="user-info">
          <el-avatar 
            :size="120" 
            :src="userInfo.avatar_url || defaultAvatar"
            class="user-avatar"
          />
          <div class="user-meta">
            <h1 class="username">
              {{ userInfo.username }}
              <el-tag v-if="userInfo.student_verified" type="success" size="small">已认证</el-tag>
            </h1>
            <p class="bio">{{ userInfo.bio || '这个人很懒，还没有写简介' }}</p>
            <div class="user-tags">
              <el-tag v-if="userInfo.school_name" size="small">{{ userInfo.school_name }}</el-tag>
              <el-tag v-if="userInfo.major" size="small" type="info">{{ userInfo.major }}</el-tag>
              <el-tag v-if="graduationYear" size="small" type="warning">{{ graduationYear }}届</el-tag>
            </div>
          </div>
          <div class="user-actions">
            <template v-if="isCurrentUser">
              <el-button type="primary" @click="$router.push('/profile/edit')">
                <el-icon><Edit /></el-icon>编辑资料
              </el-button>
            </template>
            <template v-else>
              <el-button 
                :type="isFollowing ? 'default' : 'primary'"
                @click="handleFollow"
              >
                {{ isFollowing ? '已关注' : '+ 关注' }}
              </el-button>
              <el-button @click="startChat">
                <el-icon><ChatDotRound /></el-icon>私信
              </el-button>
            </template>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="user-stats">
          <div class="stat-item">
            <span class="stat-value">{{ userInfo.post_count || 0 }}</span>
            <span class="stat-label">动态</span>
          </div>
          <div class="stat-item" @click="showFollowers">
            <span class="stat-value">{{ userInfo.follower_count || 0 }}</span>
            <span class="stat-label">粉丝</span>
          </div>
          <div class="stat-item" @click="showFollowing">
            <span class="stat-value">{{ userInfo.following_count || 0 }}</span>
            <span class="stat-label">关注</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ userInfo.reputation || 0 }}</span>
            <span class="stat-label">声望</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="profile-content container">
      <el-row :gutter="24">
        <!-- 左侧栏 -->
        <el-col :xs="24" :md="8">
          <!-- 个人信息卡片 -->
          <el-card class="info-card" shadow="hover">
            <template #header>
              <span>个人信息</span>
            </template>
            <div class="info-list">
              <div class="info-item" v-if="userInfo.school_name">
                <el-icon><School /></el-icon>
                <span>{{ userInfo.school_name }}</span>
              </div>
              <div class="info-item" v-if="userInfo.major">
                <el-icon><Reading /></el-icon>
                <span>{{ userInfo.major }}</span>
              </div>
              <div class="info-item" v-if="userInfo.enrollment_year">
                <el-icon><Calendar /></el-icon>
                <span>{{ userInfo.enrollment_year }}年入学</span>
              </div>
              <div class="info-item" v-if="userInfo.location">
                <el-icon><Location /></el-icon>
                <span>{{ userInfo.location }}</span>
              </div>
              <div class="info-item" v-if="userInfo.email">
                <el-icon><Message /></el-icon>
                <span>{{ userInfo.email }}</span>
              </div>
              <div class="info-item" v-if="userInfo.phone">
                <el-icon><Phone /></el-icon>
                <span>{{ userInfo.phone }}</span>
              </div>
            </div>
          </el-card>

          <!-- 技能展示 -->
          <el-card class="skills-card" shadow="hover" v-if="skills.length > 0">
            <template #header>
              <span>技能专长</span>
            </template>
            <div class="skills-list">
              <div v-for="skill in skills" :key="skill.id" class="skill-item">
                <span class="skill-name">{{ skill.skill_name }}</span>
                <el-rate 
                  :model-value="skill.proficiency" 
                  disabled 
                  show-score
                  text-color="#ff9900"
                />
                <el-tag v-if="skill.verified" type="success" size="small">认证</el-tag>
              </div>
            </div>
          </el-card>

          <!-- 成就徽章 -->
          <el-card class="badges-card" shadow="hover" v-if="badges.length > 0">
            <template #header>
              <span>成就徽章</span>
            </template>
            <div class="badges-list">
              <el-tooltip 
                v-for="badge in badges" 
                :key="badge.id"
                :content="badge.description"
                placement="top"
              >
                <div class="badge-item">
                  <el-avatar :size="50" :src="badge.badge_icon" />
                  <span class="badge-name">{{ badge.badge_name }}</span>
                </div>
              </el-tooltip>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧栏 - 动态 -->
        <el-col :xs="24" :md="16">
          <el-tabs v-model="activeTab" class="content-tabs">
            <el-tab-pane label="动态" name="activities">
              <div class="activities-list">
                <div v-for="activity in activities" :key="activity.id" class="activity-item">
                  <div class="activity-icon">
                    <el-icon :size="20">
                      <component :is="getActivityIcon(activity.activity_type)" />
                    </el-icon>
                  </div>
                  <div class="activity-content">
                    <p class="activity-text">{{ formatActivity(activity) }}</p>
                    <span class="activity-time">{{ formatTime(activity.created_at) }}</span>
                  </div>
                </div>
                <el-empty v-if="activities.length === 0" description="暂无动态" />
              </div>
              <div class="load-more" v-if="hasMoreActivities">
                <el-button text @click="loadMoreActivities">加载更多</el-button>
              </div>
            </el-tab-pane>

            <el-tab-pane label="帖子" name="posts">
              <el-empty description="暂无帖子" />
            </el-tab-pane>

            <el-tab-pane label="求职" name="jobs" v-if="userInfo.role === 'student' || userInfo.role === 'job_seeker'">
              <div class="job-status" v-if="profile">
                <h4>求职意向</h4>
                <p v-if="profile.expected_location">期望城市：{{ profile.expected_location }}</p>
                <p v-if="profile.expected_salary_min || profile.expected_salary_max">
                  期望薪资：{{ profile.expected_salary_min }}-{{ profile.expected_salary_max }}K
                </p>
                <el-button type="primary" @click="$router.push('/resume')">
                  查看完整简历
                </el-button>
              </div>
            </el-tab-pane>

            <el-tab-pane label="收藏" name="favorites" v-if="isCurrentUser">
              <el-empty description="暂无收藏" />
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import {
  Edit,
  ChatDotRound,
  School,
  Reading,
  Calendar,
  Location,
  Message,
  Phone,
  Document,
  Star,
  Share,
  User,
  Collection,
  Trophy
} from '@element-plus/icons-vue'
import { getUserProfile, getMyProfile, followUser, unfollowUser, getUserActivities } from '@/api/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
const defaultCover = 'https://picsum.photos/1200/300'

// 数据
const userInfo = ref({})
const profile = ref(null)
const skills = ref([])
const badges = ref([])
const activities = ref([])
const isFollowing = ref(false)
const activeTab = ref('activities')
const currentPage = ref(1)
const hasMoreActivities = ref(true)

// 计算属性
const userId = computed(() => route.params.id)
const isCurrentUser = computed(() => {
  return userStore.userInfo?.id === parseInt(userId.value)
})

const coverStyle = computed(() => ({
  backgroundImage: `url(${userInfo.value.cover_url || defaultCover})`
}))

const graduationYear = computed(() => {
  if (userInfo.value.graduation_year) {
    return userInfo.value.graduation_year
  }
  if (userInfo.value.enrollment_year) {
    return userInfo.value.enrollment_year + 4
  }
  return null
})

// 方法
const fetchUserData = async () => {
  try {
    let res
    if (isCurrentUser.value) {
      res = await getMyProfile()
    } else {
      res = await getUserProfile(userId.value)
    }
    userInfo.value = res.data
    profile.value = res.data.profile
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
}

const fetchActivities = async () => {
  try {
    const res = await getUserActivities(userId.value, {
      page: currentPage.value,
      per_page: 10
    })
    if (currentPage.value === 1) {
      activities.value = res.data.items
    } else {
      activities.value.push(...res.data.items)
    }
    hasMoreActivities.value = res.data.items.length === 10
  } catch (error) {
    console.error('获取动态失败', error)
  }
}

const handleFollow = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  try {
    if (isFollowing.value) {
      await unfollowUser(userId.value)
      isFollowing.value = false
      userInfo.value.follower_count--
      ElMessage.success('已取消关注')
    } else {
      await followUser(userId.value)
      isFollowing.value = true
      userInfo.value.follower_count++
      ElMessage.success('关注成功')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const startChat = () => {
  router.push(`/messages/${userId.value}`)
}

const showFollowers = () => {
  router.push({ path: '/my/followers', query: { userId: userId.value, type: 'followers' } })
}

const showFollowing = () => {
  router.push({ path: '/my/followers', query: { userId: userId.value, type: 'following' } })
}

const loadMoreActivities = () => {
  currentPage.value++
  fetchActivities()
}

const getActivityIcon = (type) => {
  const icons = {
    post: Document,
    like: Star,
    comment: ChatDotRound,
    share: Share,
    follow: User,
    job_apply: Collection,
    training_enroll: Reading,
    flea_publish: ShoppingBag
  }
  return icons[type] || Document
}

const formatActivity = (activity) => {
  const texts = {
    post: '发布了新动态',
    like: '点赞了内容',
    comment: '发表了评论',
    share: '分享了内容',
    follow: '关注了用户',
    job_apply: '投递了简历',
    training_enroll: '报名了课程',
    flea_publish: '发布了物品'
  }
  return texts[activity.activity_type] || '进行了操作'
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

// 监听路由变化
watch(() => route.params.id, () => {
  fetchUserData()
  fetchActivities()
})

onMounted(() => {
  fetchUserData()
  fetchActivities()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.cover-section {
  height: 300px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.3) 100%);
}

.profile-header {
  background: #fff;
  padding-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: flex-end;
  margin-top: -60px;
  position: relative;
  z-index: 1;
  padding: 0 20px;
}

.user-avatar {
  border: 4px solid #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}

.user-meta {
  flex: 1;
  margin-left: 24px;
  margin-bottom: 10px;
}

.username {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.bio {
  color: #666;
  margin: 0 0 10px 0;
  font-size: 14px;
}

.user-tags {
  display: flex;
  gap: 8px;
}

.user-actions {
  margin-bottom: 10px;
  display: flex;
  gap: 10px;
}

.user-stats {
  display: flex;
  justify-content: center;
  gap: 60px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.stat-item {
  text-align: center;
  cursor: pointer;
  transition: opacity 0.3s;
}

.stat-item:hover {
  opacity: 0.7;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}

.profile-content {
  padding: 24px 20px;
}

.info-card,
.skills-card,
.badges-card {
  margin-bottom: 20px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #666;
}

.info-item .el-icon {
  font-size: 18px;
  color: #409eff;
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skill-item {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.skill-name {
  font-weight: 500;
  min-width: 80px;
}

.badges-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.badge-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.badge-name {
  font-size: 12px;
  color: #666;
}

.content-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.activity-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  margin: 0 0 8px 0;
  color: #333;
}

.activity-time {
  font-size: 12px;
  color: #999;
}

.load-more {
  text-align: center;
  margin-top: 20px;
}

.job-status {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .user-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: -40px;
  }
  
  .user-meta {
    margin-left: 0;
    margin-top: 16px;
  }
  
  .user-tags {
    justify-content: center;
  }
  
  .user-actions {
    margin-top: 16px;
  }
  
  .user-stats {
    gap: 30px;
  }
}
</style>
