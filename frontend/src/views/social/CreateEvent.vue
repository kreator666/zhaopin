<template>
  <div class="create-event-page">
    <Navbar />
    
    <div class="container" style="padding-top: 80px;">
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <h2>{{ isEdit ? '编辑活动' : '发布活动' }}</h2>
          </div>
        </template>
        
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          class="event-form"
        >
          <!-- 活动标题 -->
          <el-form-item label="活动标题" prop="title">
            <el-input
              v-model="form.title"
              placeholder="给你的活动起个吸引人的标题"
              maxlength="50"
              show-word-limit
            />
          </el-form-item>
          
          <!-- 活动类型 -->
          <el-form-item label="活动类型" prop="event_type">
            <div class="type-selector">
              <div
                v-for="type in eventTypes"
                :key="type.value"
                class="type-item"
                :class="{ active: form.event_type === type.value }"
                @click="form.event_type = type.value"
              >
                <el-icon :size="24">
                  <component :is="type.icon" />
                </el-icon>
                <span>{{ type.label }}</span>
              </div>
            </div>
          </el-form-item>
          
          <!-- 活动时间 -->
          <div class="form-row">
            <el-form-item label="开始时间" prop="start_time" class="half">
              <el-date-picker
                v-model="form.start_time"
                type="datetime"
                placeholder="选择开始时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DDTHH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
            
            <el-form-item label="结束时间" prop="end_time" class="half">
              <el-date-picker
                v-model="form.end_time"
                type="datetime"
                placeholder="选择结束时间（可选）"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DDTHH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </div>
          
          <!-- 活动地点 -->
          <el-form-item label="活动地点" prop="location">
            <el-input
              v-model="form.location"
              placeholder="请输入详细地址"
            >
              <template #prefix>
                <el-icon><Location /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <!-- 费用设置 -->
          <div class="form-row">
            <el-form-item label="费用类型" prop="fee_type" class="half">
              <el-select v-model="form.fee_type" style="width: 100%">
                <el-option label="免费" value="free" />
                <el-option label="AA制" value="aa" />
                <el-option label="固定费用" value="fixed" />
              </el-select>
            </el-form-item>
            
            <el-form-item 
              label="费用金额" 
              prop="fee_amount" 
              class="half"
              v-if="form.fee_type === 'fixed'"
            >
              <el-input-number
                v-model="form.fee_amount"
                :min="0"
                :precision="2"
                :step="10"
                style="width: 100%"
              >
                <template #append>元</template>
              </el-input-number>
            </el-form-item>
          </div>
          
          <!-- 人数限制 -->
          <el-form-item label="人数限制" prop="max_participants">
            <el-input-number
              v-model="form.max_participants"
              :min="1"
              :max="1000"
              placeholder="0表示不限"
              style="width: 200px"
            />
            <span class="form-tip">0 表示不限制人数</span>
          </el-form-item>
          
          <!-- 活动封面 -->
          <el-form-item label="活动封面">
            <el-upload
              class="cover-uploader"
              :action="uploadUrl"
              :headers="uploadHeaders"
              :show-file-list="false"
              :on-success="handleCoverSuccess"
              :before-upload="beforeCoverUpload"
            >
              <img v-if="form.cover_image" :src="form.cover_image" class="cover-preview" />
              <div v-else class="cover-placeholder">
                <el-icon :size="32"><Plus /></el-icon>
                <span>上传封面图</span>
                <span class="tip">建议尺寸 800x400</span>
              </div>
            </el-upload>
          </el-form-item>
          
          <!-- 活动详情 -->
          <el-form-item label="活动详情" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              :rows="6"
              placeholder="详细介绍活动内容、注意事项、联系方式等..."
              maxlength="2000"
              show-word-limit
            />
          </el-form-item>
          
          <!-- 提交按钮 -->
          <el-form-item>
            <div class="form-actions">
              <el-button @click="goBack">取消</el-button>
              <el-button type="primary" @click="submitForm" :loading="submitting">
                {{ isEdit ? '保存修改' : '发布活动' }}
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Plus, Location, Basketball, Reading, Food, MapLocation, 
  VideoPlay, UserFilled, More 
} from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { socialApi } from '@/api/social'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 判断是否为编辑模式
const isEdit = computed(() => !!route.params.id)
const eventId = computed(() => route.params.id)

// 上传配置
const uploadUrl = 'http://localhost:5000/api/upload/image'
const uploadHeaders = {
  Authorization: `Bearer ${localStorage.getItem('token') || ''}`
}

// 活动类型（带图标）
const eventTypes = [
  { value: 'sports', label: '运动健身', icon: 'Basketball' },
  { value: 'study', label: '学习交流', icon: 'Reading' },
  { value: 'dining', label: '聚餐美食', icon: 'Food' },
  { value: 'travel', label: '旅行户外', icon: 'MapLocation' },
  { value: 'game', label: '游戏娱乐', icon: 'VideoPlay' },
  { value: 'party', label: '社交聚会', icon: 'UserFilled' },
  { value: 'other', label: '其他', icon: 'More' }
]

// 表单数据
const formRef = ref()
const form = reactive({
  title: '',
  event_type: 'other',
  start_time: '',
  end_time: '',
  location: '',
  fee_type: 'free',
  fee_amount: 0,
  max_participants: null,
  cover_image: '',
  description: ''
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入活动标题', trigger: 'blur' },
    { min: 2, max: 50, message: '标题长度 2-50 个字符', trigger: 'blur' }
  ],
  event_type: [
    { required: true, message: '请选择活动类型', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入活动地点', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入活动详情', trigger: 'blur' }
  ]
}

const submitting = ref(false)

// 获取活动详情（编辑模式）
const fetchEvent = async () => {
  if (!isEdit.value) return
  
  try {
    const res = await socialApi.getEvent(eventId.value)
    const data = res.data
    
    // 填充表单
    Object.assign(form, {
      title: data.title,
      event_type: data.event_type,
      start_time: data.start_time,
      end_time: data.end_time,
      location: data.location,
      fee_type: data.fee_type,
      fee_amount: (data.fee_amount || 0) / 100,
      max_participants: data.max_participants,
      cover_image: data.cover_image,
      description: data.description
    })
  } catch (err) {
    console.error('获取活动详情失败:', err)
    ElMessage.error('获取活动详情失败')
    router.push('/social/events')
  }
}

// 封面上传成功
const handleCoverSuccess = (res) => {
  form.cover_image = res.url
  ElMessage.success('封面上传成功')
}

// 封面上传前检查
const beforeCoverUpload = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isJpgOrPng) {
    ElMessage.error('只支持 JPG/PNG 格式')
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB')
  }
  return isJpgOrPng && isLt5M
}

// 提交表单
const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  
  try {
    // 构建提交数据
    const data = {
      title: form.title,
      event_type: form.event_type,
      start_time: form.start_time,
      end_time: form.end_time || null,
      location: form.location,
      fee_type: form.fee_type,
      fee_amount: form.fee_type === 'fixed' ? Math.round(form.fee_amount * 100) : 0,
      max_participants: form.max_participants || null,
      cover_image: form.cover_image,
      description: form.description
    }
    
    if (isEdit.value) {
      await socialApi.updateEvent(eventId.value, data)
      ElMessage.success('活动更新成功')
    } else {
      await socialApi.createEvent(data)
      ElMessage.success('活动发布成功')
    }
    
    router.push('/social/events')
  } catch (err) {
    console.error('提交失败:', err)
    ElMessage.error(err.response?.data?.error || '提交失败')
  } finally {
    submitting.value = false
  }
}

// 返回
const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchEvent()
})
</script>

<style scoped>
.create-event-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 40px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.event-form {
  padding: 20px 0;
}

/* 类型选择器 */
.type-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.type-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  border: 2px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 80px;
}

.type-item:hover {
  border-color: #c0c4cc;
}

.type-item.active {
  border-color: #67c23a;
  background: #f0f9eb;
  color: #67c23a;
}

.type-item span {
  font-size: 13px;
}

/* 表单行 */
.form-row {
  display: flex;
  gap: 20px;
}

.form-row .half {
  flex: 1;
}

.form-tip {
  margin-left: 12px;
  font-size: 13px;
  color: #999;
}

/* 封面上传 */
.cover-uploader {
  width: 100%;
}

.cover-uploader :deep(.el-upload) {
  width: 100%;
}

.cover-preview {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.cover-placeholder {
  width: 100%;
  height: 200px;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #8c939d;
  cursor: pointer;
  transition: all 0.3s;
}

.cover-placeholder:hover {
  border-color: #409eff;
  color: #409eff;
}

.cover-placeholder span {
  margin-top: 8px;
  font-size: 14px;
}

.cover-placeholder .tip {
  font-size: 12px;
  color: #c0c4cc;
}

/* 提交按钮 */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .type-selector {
    justify-content: center;
  }
  
  .type-item {
    padding: 12px 16px;
    min-width: 60px;
  }
}
</style>
