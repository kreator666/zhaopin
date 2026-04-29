<template>
  <div class="course-form-page">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑课程' : '发布新课程' }}</h2>
      <el-button @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
    </div>
    
    <el-card>
      <el-form 
        ref="formRef"
        :model="form" 
        :rules="rules" 
        label-width="120px"
        :disabled="submitting"
      >
        <!-- 基本信息 -->
        <div class="form-section">
          <h3 class="section-title">基本信息</h3>
          
          <el-form-item label="课程名称" prop="title">
            <el-input 
              v-model="form.title" 
              placeholder="请输入课程名称"
              maxlength="100"
              show-word-limit
              style="width: 600px;"
            />
          </el-form-item>
          
          <el-form-item label="课程描述" prop="description">
            <el-input 
              v-model="form.description" 
              type="textarea"
              :rows="5"
              placeholder="请输入课程详细描述"
              maxlength="2000"
              show-word-limit
              style="width: 600px;"
            />
          </el-form-item>
          
          <el-form-item label="课程分类" prop="category">
            <el-select 
              v-model="form.category" 
              placeholder="请选择课程分类"
              style="width: 200px;"
            >
              <el-option label="编程开发" value="programming" />
              <el-option label="语言学习" value="language" />
              <el-option label="考试考证" value="exam_prep" />
              <el-option label="职业技能" value="career" />
              <el-option label="设计创意" value="design" />
              <el-option label="数据科学" value="data" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="课程级别" prop="level">
            <el-radio-group v-model="form.level">
              <el-radio value="beginner">入门</el-radio>
              <el-radio value="intermediate">进阶</el-radio>
              <el-radio value="advanced">高级</el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
        
        <!-- 讲师信息 -->
        <div class="form-section">
          <h3 class="section-title">讲师信息</h3>
          
          <el-form-item label="讲师姓名" prop="instructor">
            <el-input 
              v-model="form.instructor" 
              placeholder="请输入讲师姓名"
              style="width: 300px;"
            />
          </el-form-item>
          
          <el-form-item label="提供方" prop="provider">
            <el-input 
              v-model="form.provider" 
              placeholder="请输入提供方（如公司名称、培训机构等）"
              style="width: 400px;"
            />
            <div class="form-tip">企业用户默认为公司名称</div>
          </el-form-item>
        </div>
        
        <!-- 价格与时长 -->
        <div class="form-section">
          <h3 class="section-title">价格与时长</h3>
          
          <el-form-item label="课程价格" prop="price">
            <el-input-number 
              v-model="form.price" 
              :min="0"
              :precision="2"
              placeholder="0表示免费"
              style="width: 200px;"
            />
            <span class="form-unit">元</span>
            <div class="form-tip">输入 0 表示免费课程</div>
          </el-form-item>
          
          <el-form-item label="原价" prop="original_price">
            <el-input-number 
              v-model="form.original_price" 
              :min="0"
              :precision="2"
              placeholder="可选，用于显示折扣"
              style="width: 200px;"
            />
            <span class="form-unit">元</span>
            <div class="form-tip">可选，设置后显示原价与现价对比</div>
          </el-form-item>
          
          <el-form-item label="课程时长" prop="duration">
            <el-input 
              v-model="form.duration" 
              placeholder="例如：24课时、40小时、1个月"
              style="width: 300px;"
            />
          </el-form-item>
        </div>
        
        <!-- 课程封面 -->
        <div class="form-section">
          <h3 class="section-title">课程封面</h3>
          
          <el-form-item label="封面图片" prop="cover_image">
            <el-upload
              class="cover-uploader"
              :action="uploadUrl"
              :headers="uploadHeaders"
              :show-file-list="false"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              accept="image/*"
            >
              <div v-if="form.cover_image" class="cover-preview">
                <img :src="getCoverImage(form.cover_image)" class="preview-img" />
                <div class="cover-mask">
                  <el-icon><Edit /></el-icon>
                  <span>更换图片</span>
                </div>
              </div>
              <div v-else class="upload-placeholder">
                <el-icon class="upload-icon"><Plus /></el-icon>
                <span>上传封面</span>
              </div>
            </el-upload>
            <div class="form-tip">建议上传 1200 x 800 像素的图片，支持 JPG、PNG 格式</div>
          </el-form-item>
        </div>
        
        <!-- 授课形式 -->
        <div class="form-section">
          <h3 class="section-title">授课形式</h3>
          
          <el-form-item label="授课形式" prop="is_online">
            <el-radio-group v-model="form.is_online">
              <el-radio :value="true">线上课程</el-radio>
              <el-radio :value="false">线下课程</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item 
            v-if="!form.is_online" 
            label="授课地点" 
            prop="location"
          >
            <el-input 
              v-model="form.location" 
              placeholder="请输入线下授课地点"
              style="width: 400px;"
            />
          </el-form-item>
        </div>
        
        <!-- 开课时间 -->
        <div class="form-section">
          <h3 class="section-title">开课时间</h3>
          
          <el-form-item label="开课日期" prop="start_date">
            <el-date-picker
              v-model="form.start_date"
              type="date"
              placeholder="选择开课日期"
              value-format="YYYY-MM-DD"
              style="width: 200px;"
            />
          </el-form-item>
          
          <el-form-item label="结束日期" prop="end_date">
            <el-date-picker
              v-model="form.end_date"
              type="date"
              placeholder="选择结束日期（可选）"
              value-format="YYYY-MM-DD"
              style="width: 200px;"
            />
          </el-form-item>
        </div>
        
        <!-- 课程状态 -->
        <div class="form-section" v-if="isEdit">
          <h3 class="section-title">课程状态</h3>
          
          <el-form-item label="课程状态" prop="status">
            <el-radio-group v-model="form.status">
              <el-radio value="active">报名中</el-radio>
              <el-radio value="ended">已结束</el-radio>
              <el-radio value="cancelled">已取消</el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
        
        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '发布课程' }}
          </el-button>
          <el-button size="large" @click="goBack">
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getCourse, createCourse, updateCourse } from '@/api/training'
import { ArrowLeft, Plus, Edit } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const formRef = ref(null)
const submitting = ref(false)

const isEdit = computed(() => {
  return !!route.params.id
})

// 上传配置
const uploadUrl = computed(() => {
  return `${API_BASE_URL}/api/upload/cover`
})

const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token')
  return {
    Authorization: token ? `Bearer ${token}` : ''
  }
})

const form = reactive({
  title: '',
  description: '',
  category: '',
  level: 'beginner',
  instructor: '',
  provider: '',
  price: 0,
  original_price: null,
  duration: '',
  cover_image: '',
  is_online: true,
  location: '',
  start_date: '',
  end_date: '',
  status: 'active'
})

const rules = {
  title: [
    { required: true, message: '请输入课程名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入课程描述', trigger: 'blur' },
    { min: 10, max: 2000, message: '描述长度在 10 到 2000 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择课程分类', trigger: 'change' }
  ],
  level: [
    { required: true, message: '请选择课程级别', trigger: 'change' }
  ]
}

// 获取封面图片
const getCoverImage = (coverImage) => {
  if (!coverImage) {
    return ''
  }
  if (coverImage.startsWith('http')) {
    return coverImage
  }
  return `${API_BASE_URL}${coverImage}`
}

// 获取课程详情
const fetchCourseDetail = async () => {
  if (!isEdit.value) return
  
  const courseId = route.params.id
  if (!courseId) return
  
  try {
    const res = await getCourse(courseId)
    const data = res.data || res
    
    form.title = data.title || ''
    form.description = data.description || ''
    form.category = data.category || ''
    form.level = data.level || 'beginner'
    form.instructor = data.instructor || ''
    form.provider = data.provider || ''
    form.price = data.price || 0
    form.original_price = data.original_price || null
    form.duration = data.duration || ''
    form.cover_image = data.cover_image || ''
    form.is_online = data.is_online !== false
    form.location = data.location || ''
    form.start_date = data.start_date || ''
    form.end_date = data.end_date || ''
    form.status = data.status || 'active'
  } catch (error) {
    console.error('获取课程详情失败', error)
    ElMessage.error('获取课程详情失败')
  }
}

// 上传成功
const handleUploadSuccess = (response) => {
  if (response && response.url) {
    form.cover_image = response.url
    ElMessage.success('上传成功')
  } else {
    ElMessage.error('上传失败')
  }
}

// 上传失败
const handleUploadError = (error) => {
  console.error('上传失败', error)
  ElMessage.error('上传失败，请重试')
}

// 返回
const goBack = () => {
  router.push('/company/courses')
}

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    try {
      // 准备提交数据
      const submitData = {
        title: form.title,
        description: form.description,
        category: form.category,
        level: form.level,
        instructor: form.instructor,
        provider: form.provider,
        price: form.price,
        original_price: form.original_price,
        duration: form.duration,
        cover_image: form.cover_image,
        is_online: form.is_online,
        location: form.is_online ? '' : form.location,
        start_date: form.start_date || null,
        end_date: form.end_date || null
      }
      
      // 如果是企业用户且没有填写提供方，默认使用公司名称
      if (!submitData.provider && userStore.userInfo?.role === 'company' && userStore.userInfo?.company?.name) {
        submitData.provider = userStore.userInfo.company.name
      }
      
      if (isEdit.value) {
        // 编辑模式
        submitData.status = form.status
        await updateCourse(route.params.id, submitData)
        ElMessage.success('修改成功')
      } else {
        // 创建模式
        await createCourse(submitData)
        ElMessage.success('发布成功')
      }
      
      // 返回列表页
      goBack()
    } catch (error) {
      console.error('提交失败', error)
      const errMsg = error.response?.data?.error || '提交失败，请重试'
      ElMessage.error(errMsg)
    } finally {
      submitting.value = false
    }
  })
}

onMounted(() => {
  fetchCourseDetail()
})
</script>

<style scoped>
.course-form-page {
  padding-top: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 22px;
  color: #333;
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.form-section:last-of-type {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
  display: inline-block;
}

.form-unit {
  margin-left: 8px;
  color: #666;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.cover-uploader {
  display: inline-block;
}

.cover-preview {
  position: relative;
  width: 300px;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 14px;
}

.cover-preview:hover .cover-mask {
  opacity: 1;
}

.cover-mask .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.upload-placeholder {
  width: 300px;
  height: 200px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  color: #909399;
}

.upload-placeholder:hover {
  border-color: #409eff;
  color: #409eff;
}

.upload-icon {
  font-size: 36px;
  margin-bottom: 8px;
}

.upload-placeholder span {
  font-size: 14px;
}
</style>
