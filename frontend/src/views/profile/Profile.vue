<template>
  <div class="profile-page">
    <!-- 导航栏 -->
    <Navbar />
    
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
            :src="getFullImageUrl(userInfo.avatar_url) || defaultAvatar"
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

            <!-- 兴趣话题 - 显示用户发布的话题 -->
            <el-tab-pane label="兴趣话题" name="topics">
              <div class="topics-section">
                <div v-if="userTopics.length > 0" class="user-topics-list">
                  <div v-for="topic in userTopics" :key="topic.id" class="user-topic-item" @click="$router.push(`/social/topics/${topic.id}`)">
                    <h4>{{ topic.title }}</h4>
                    <p class="topic-excerpt">{{ topic.content?.substring(0, 100) }}...</p>
                    <div class="topic-meta">
                      <span><el-icon><View /></el-icon> {{ topic.view_count || 0 }}</span>
                      <span><el-icon><ChatDotRound /></el-icon> {{ topic.reply_count || 0 }}</span>
                      <span>{{ formatTime(topic.created_at) }}</span>
                    </div>
                  </div>
                </div>
                <el-empty v-else description="暂无发布的话题">
                  <el-button type="primary" @click="$router.push('/social/circles')">去发布话题</el-button>
                </el-empty>
              </div>
            </el-tab-pane>

            <!-- 求职 - 仅自己可见 -->
            <el-tab-pane label="求职" name="jobs" v-if="isCurrentUser && (userInfo.role === 'student' || userInfo.role === 'job_seeker' || userInfo.role === 'alumni')">
              <div class="job-section">
                <!-- 求职意向 -->
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
                
                <!-- 投递记录 -->
                <div class="applications-section">
                  <h4>投递记录</h4>
                  <div class="applications-list" v-if="jobApplications.length > 0">
                    <div v-for="app in jobApplications" :key="app.id" class="application-item">
                      <div class="app-job-info">
                        <h5 @click="$router.push(`/jobs/${app.job_id}`)">{{ app.job?.title || '未知职位' }}</h5>
                        <p class="company-name">{{ app.job?.company_name || '未知公司' }}</p>
                      </div>
                      <div class="app-status">
                        <el-tag :type="getStatusType(app.status)" size="small">
                          {{ getStatusText(app.status) }}
                        </el-tag>
                        <span class="app-time">{{ formatTime(app.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                  <el-empty v-else description="暂无投递记录" />
                </div>
              </div>
            </el-tab-pane>

            <!-- 活动约伴 - 显示参加或组织的活动 -->
            <el-tab-pane label="活动约伴" name="events" v-if="isCurrentUser">
              <div class="events-section">
                <div v-if="userEvents.length > 0" class="events-list">
                  <div v-for="event in userEvents" :key="event.id" class="event-item" @click="$router.push(`/social/events/${event.id}`)">
                    <div class="event-image" v-if="event.cover_image">
                      <img :src="getFullImageUrl(event.cover_image)" alt="" />
                    </div>
                    <div class="event-info">
                      <h4>{{ event.title }}</h4>
                      <p class="event-time">
                        <el-icon><Calendar /></el-icon>
                        {{ formatTime(event.start_time) }}
                      </p>
                      <p class="event-location">
                        <el-icon><Location /></el-icon>
                        {{ event.location }}
                      </p>
                      <el-tag :type="event.is_organizer ? 'success' : 'primary'" size="small">
                        {{ event.is_organizer ? '组织者' : '参与者' }}
                      </el-tag>
                    </div>
                  </div>
                </div>
                <el-empty v-else description="暂无参加的活动">
                  <el-button type="primary" @click="$router.push('/social/events')">去发现活动</el-button>
                </el-empty>
              </div>
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
  Trophy,
  ShoppingBag,
  View
} from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { getUserProfile, getMyProfile, followUser, unfollowUser, getUserActivities, getFollowing } from '@/api/user'
import { applicationsApi } from '@/api/applications'
import { socialApi } from '@/api/social'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
const defaultCover = 'https://picsum.photos/1200/300'
const API_BASE_URL = 'http://localhost:5000'

// 获取完整图片URL
const getFullImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${API_BASE_URL}${url}`
}

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
const jobApplications = ref([])
const userTopics = ref([])
const userEvents = ref([])

// 计算属性
const userId = computed(() => parseInt(route.params.id))
const isCurrentUser = computed(() => {
  if (!userStore.isLoggedIn || !userStore.userInfo?.id) return false
  return parseInt(userStore.userInfo.id) === userId.value
})

const coverStyle = computed(() => ({
  backgroundImage: `url(${getFullImageUrl(userInfo.value.cover_url) || defaultCover})`
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
    skills.value = res.data.skills || []
    badges.value = res.data.badges || []
    
    // 如果访问他人主页，检查是否已关注
    if (!isCurrentUser.value && userStore.isLoggedIn) {
      checkFollowStatus()
    }
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
}

const checkFollowStatus = async () => {
  // 确保已登录且有自己的ID
  if (!userStore.isLoggedIn || !userStore.userInfo?.id) {
    return
  }
  try {
    // 获取当前用户的关注列表，检查是否包含该用户
    const res = await getFollowing(userStore.userInfo.id, { page: 1, per_page: 1000 })
    const followingList = res.data.items || []
    isFollowing.value = followingList.some(user => user.id === userId.value)
  } catch (error) {
    console.error('获取关注状态失败', error)
  }
}

const fetchActivities = async () => {
  try {
    const res = await getUserActivities(userId.value, {
      page: currentPage.value,
      per_page: 10
    })
    const data = res.data || res
    if (currentPage.value === 1) {
      activities.value = data.items || []
    } else {
      activities.value.push(...(data.items || []))
    }
    hasMoreActivities.value = (data.items || []).length === 10
  } catch (error) {
    console.error('获取动态失败', error)
  }
}

// 获取投递记录
const fetchJobApplications = async () => {
  if (!isCurrentUser.value) return
  try {
    const res = await applicationsApi.getMyApplications({ per_page: 20 })
    const data = res.data || res
    jobApplications.value = data.items || []
  } catch (error) {
    console.error('获取投递记录失败', error)
  }
}

// 获取用户发布的兴趣话题
const fetchUserTopics = async () => {
  try {
    const res = await socialApi.getTopics({ user_id: userId.value, per_page: 100 })
    const data = res.data || res
    userTopics.value = (data.items || []).filter(t => t.user_id === userId.value)
  } catch (error) {
    console.error('获取兴趣话题失败', error)
  }
}

// 获取用户参加/组织的活动
const fetchUserEvents = async () => {
  if (!isCurrentUser.value) return
  try {
    const res = await socialApi.getMyEvents()
    const data = res.data || res
    userEvents.value = data.items || []
  } catch (error) {
    console.error('获取活动列表失败', error)
  }
}

// 投递状态样式
const getStatusType = (status) => {
  const types = {
    pending: 'info',
    accepted: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

// 投递状态文本
const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    accepted: '已通过',
    rejected: '未通过'
  }
  return texts[status] || status
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
  // 如果有具体内容，优先显示
  if (activity.content) {
    return activity.content
  }
  
  const texts = {
    post: '发布了新动态',
    like: '点赞了内容',
    comment: '发表了评论',
    share: '分享了内容',
    follow: '关注了用户',
    job_apply: '投递了职位',
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
  fetchJobApplications()
  fetchUserTopics()
  fetchUserEvents()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px; /* 为 fixed 导航栏留出空间 */
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
  gap: 16px;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 8px;
}

.activities-list::-webkit-scrollbar {
  width: 6px;
}

.activities-list::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 3px;
}

.activities-list::-webkit-scrollbar-track {
  background: #f5f7fa;
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

.job-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.job-status {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.applications-section h4,
.job-status h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.application-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background 0.3s;
}

.application-item:hover {
  background: #f0f2f5;
}

.app-job-info h5 {
  margin: 0 0 4px 0;
  color: #409eff;
  cursor: pointer;
}

.app-job-info h5:hover {
  text-decoration: underline;
}

.company-name {
  margin: 0;
  font-size: 13px;
  color: #666;
}

.app-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.app-time {
  font-size: 12px;
  color: #999;
}

/* 兴趣话题样式 */
.topics-section {
  padding: 16px 0;
}

.user-topics-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-topic-item {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.user-topic-item:hover {
  background: #e6f2ff;
}

.user-topic-item h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
}

.user-topic-item .topic-excerpt {
  margin: 0 0 12px 0;
  font-size: 13px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-topic-item .topic-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #909399;
}

.user-topic-item .topic-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 活动约伴样式 */
.events-section {
  padding: 16px 0;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.event-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.event-item:hover {
  background: #e6f2ff;
}

.event-image {
  width: 120px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.event-info {
  flex: 1;
}

.event-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
}

.event-time,
.event-location {
  margin: 4px 0;
  font-size: 13px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
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
