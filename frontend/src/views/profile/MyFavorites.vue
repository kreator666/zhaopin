<template>
  <div>
    <Navbar />
    <div class="favorites-page">
    <div class="container">
      <h2>我的收藏</h2>
      
      <el-tabs v-model="activeTab" class="favorites-tabs">
        <el-tab-pane label="职位" name="jobs">
          <div class="favorites-list">
            <el-empty v-if="jobFavorites.length === 0" description="暂无收藏的职位" />
            <div v-else v-for="item in jobFavorites" :key="item.id" class="favorite-card">
              <div class="favorite-content">
                <h4>{{ item.title }}</h4>
                <p class="subtitle">{{ item.subtitle }}</p>
              </div>
              <el-button type="primary" text @click="viewDetail(item)">
                查看
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="课程" name="courses">
          <div class="favorites-list">
            <el-empty v-if="courseFavorites.length === 0" description="暂无收藏的课程" />
            <div v-else v-for="item in courseFavorites" :key="item.id" class="favorite-card">
              <el-image :src="item.cover" class="favorite-image" />
              <div class="favorite-content">
                <h4>{{ item.title }}</h4>
                <p class="subtitle">{{ item.provider }}</p>
              </div>
              <el-button type="primary" text @click="viewDetail(item)">
                查看
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="帖子" name="posts">
          <div class="favorites-list">
            <el-empty v-if="postFavorites.length === 0" description="暂无收藏的帖子" />
            <div v-else v-for="item in postFavorites" :key="item.id" class="favorite-card">
              <div class="favorite-content">
                <h4>{{ item.title }}</h4>
                <p class="subtitle">{{ item.author }}</p>
              </div>
              <el-button type="primary" text @click="viewDetail(item)">
                查看
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="二手" name="flea">
          <div class="favorites-list">
            <el-empty v-if="fleaFavorites.length === 0" description="暂无收藏的物品" />
            <div v-else v-for="item in fleaFavorites" :key="item.id" class="favorite-card">
              <el-image :src="item.images?.[0]" class="favorite-image" />
              <div class="favorite-content">
                <h4>{{ item.title }}</h4>
                <p class="price">¥{{ item.price }}</p>
              </div>
              <el-button type="primary" text @click="viewDetail(item)">
                查看
              </el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'

const router = useRouter()
const activeTab = ref('jobs')

const jobFavorites = ref([])
const courseFavorites = ref([])
const postFavorites = ref([])
const fleaFavorites = ref([])

const fetchFavorites = async () => {
  // TODO: 调用API获取收藏列表
}

const viewDetail = (item) => {
  // 根据类型跳转到不同详情页
  const routes = {
    jobs: `/jobs/${item.target_id}`,
    courses: `/training/courses/${item.target_id}`,
    posts: `/social/post/${item.target_id}`,
    flea: `/flea/items/${item.target_id}`
  }
  router.push(routes[activeTab.value])
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
.favorites-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 60px 0 24px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

h2 {
  margin-bottom: 24px;
}

.favorites-tabs {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
}

.favorites-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.favorite-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.favorite-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  object-fit: cover;
}

.favorite-content {
  flex: 1;
}

.favorite-content h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
}

.subtitle {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.price {
  color: #f56c6c;
  font-weight: 600;
  margin: 0;
}
</style>
