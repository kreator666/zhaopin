<template>
  <div class="publish-item-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <el-card class="form-card">
          <template #header>
            <div class="card-header">
              <h2>发布闲置物品</h2>
              <el-button type="text" @click="$router.back()">
                <el-icon><ArrowLeft /></el-icon>
                返回
              </el-button>
            </div>
          </template>
          
          <el-form 
            ref="formRef" 
            :model="form" 
            :rules="rules" 
            label-width="100px"
            class="publish-form"
          >
            <!-- 标题 -->
            <el-form-item label="物品标题" prop="title">
              <el-input 
                v-model="form.title" 
                placeholder="请输入物品标题（如：九成新iPad Pro 2021）" 
                maxlength="50"
                show-word-limit
              />
            </el-form-item>
            
            <!-- 描述 -->
            <el-form-item label="物品描述" prop="description">
              <el-input 
                v-model="form.description" 
                type="textarea" 
                :rows="4"
                placeholder="请详细描述物品的情况，包括购买时间、使用情况、是否有配件等"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
            
            <!-- 分类 -->
            <el-form-item label="物品分类" prop="category">
              <el-select v-model="form.category" placeholder="请选择物品分类" style="width: 100%">
                <el-option label="书籍教材" value="book" />
                <el-option label="数码电子" value="electronics" />
                <el-option label="自行车" value="bike" />
                <el-option label="宿舍用品" value="dorm" />
                <el-option label="票务卡券" value="ticket" />
                <el-option label="服饰鞋包" value="clothing" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
            
            <!-- 价格 -->
            <el-form-item label="售价" prop="price">
              <el-input-number 
                v-model="form.price" 
                :min="0" 
                :precision="2"
                placeholder="请输入售价"
                style="width: 200px"
              />
              <span class="price-unit">元</span>
            </el-form-item>
            
            <!-- 原价 -->
            <el-form-item label="原价">
              <el-input-number 
                v-model="form.original_price" 
                :min="0" 
                :precision="2"
                placeholder="请输入原价（选填）"
                style="width: 200px"
              />
              <span class="price-unit">元</span>
            </el-form-item>
            
            <!-- 新旧程度 -->
            <el-form-item label="新旧程度" prop="condition">
              <el-radio-group v-model="form.condition">
                <el-radio value="new">全新</el-radio>
                <el-radio value="like_new">几乎全新</el-radio>
                <el-radio value="good">良好</el-radio>
                <el-radio value="fair">一般</el-radio>
                <el-radio value="worn">较旧</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <!-- 图片上传 -->
            <el-form-item label="物品图片" prop="images">
              <el-upload
                class="image-uploader"
                :action="uploadUrl"
                :headers="uploadHeaders"
                :on-success="handleUploadSuccess"
                :on-error="handleUploadError"
                :on-remove="handleRemove"
                :file-list="fileList"
                list-type="picture-card"
                :limit="9"
                accept="image/*"
              >
                <el-icon><Plus /></el-icon>
                <template #tip>
                  <div class="el-upload__tip">
                    最多上传9张图片，支持jpg、png、gif格式
                  </div>
                </template>
              </el-upload>
            </el-form-item>
            
            <!-- 交易地点 -->
            <el-form-item label="交易地点" prop="trade_location">
              <el-input 
                v-model="form.trade_location" 
                placeholder="请输入交易地点（如：学校东门、宿舍楼下等）" 
                maxlength="100"
              />
            </el-form-item>
            
            <!-- 交易方式 -->
            <el-form-item label="交易方式" prop="trade_method">
              <el-checkbox-group v-model="form.trade_methods">
                <el-checkbox label="face_to_face">面对面交易</el-checkbox>
                <el-checkbox label="campus_delivery">校园配送</el-checkbox>
                <el-checkbox label="express">快递邮寄</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <!-- 允许议价 -->
            <el-form-item label="议价">
              <el-switch v-model="form.is_bargain_allowed" active-text="允许议价" inactive-text="不接受议价" />
            </el-form-item>
            
            <!-- 提交按钮 -->
            <el-form-item>
              <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
                发布物品
              </el-button>
              <el-button size="large" @click="$router.back()">取消</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { publishItem } from '@/api/flea'
import { uploadApi } from '@/api/upload'
import { useUserStore } from '@/stores/user'
import { ArrowLeft, Plus } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const submitting = ref(false)
const fileList = ref([])

const API_BASE_URL = 'http://localhost:5000'

const form = reactive({
  title: '',
  description: '',
  category: '',
  price: null,
  original_price: null,
  condition: 'good',
  images: [],
  trade_location: '',
  trade_methods: ['face_to_face'],
  is_bargain_allowed: true
})

const rules = {
  title: [
    { required: true, message: '请输入物品标题', trigger: 'blur' },
    { min: 2, max: 50, message: '标题长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入物品描述', trigger: 'blur' },
    { min: 10, max: 500, message: '描述长度在 10 到 500 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择物品分类', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入售价', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格不能为负数', trigger: 'blur' }
  ],
  condition: [
    { required: true, message: '请选择新旧程度', trigger: 'change' }
  ]
}

// 上传地址
const uploadUrl = computed(() => {
  return `${API_BASE_URL}/api/upload/image`
})

// 上传请求头
const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token')
  return {
    Authorization: token ? `Bearer ${token}` : ''
  }
})

// 上传成功
const handleUploadSuccess = (response, file, fileListVal) => {
  if (response && response.url) {
    // 更新 form.images
    form.images.push(response.url)
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error('图片上传失败')
  }
}

// 上传失败
const handleUploadError = (error) => {
  console.error('上传失败', error)
  ElMessage.error('图片上传失败，请重试')
}

// 移除图片
const handleRemove = (file, fileListVal) => {
  const url = file.response?.url || file.url
  const index = form.images.indexOf(url)
  if (index > -1) {
    form.images.splice(index, 1)
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        // 准备提交数据
        const submitData = {
          title: form.title,
          description: form.description,
          category: form.category,
          price: form.price,
          condition: form.condition,
          is_bargain_allowed: form.is_bargain_allowed
        }
        
        // 可选字段
        if (form.original_price !== null) {
          submitData.original_price = form.original_price
        }
        if (form.images.length > 0) {
          submitData.images = JSON.stringify(form.images)
        }
        if (form.trade_location) {
          submitData.trade_location = form.trade_location
        }
        if (form.trade_methods.length > 0) {
          submitData.trade_method = form.trade_methods.join(',')
        }
        
        await publishItem(submitData)
        ElMessage.success('发布成功！')
        router.push('/flea/my-items')
      } catch (error) {
        console.error('发布失败', error)
        ElMessage.error(error.response?.data?.error || '发布失败，请重试')
      } finally {
        submitting.value = false
      }
    }
  })
}
</script>

<style scoped>
.publish-item-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  padding: 100px 0 40px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.form-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.publish-form {
  padding: 20px 0;
}

.price-unit {
  margin-left: 10px;
  color: #666;
}

.image-uploader {
  width: 100%;
}

:deep(.el-upload--picture-card) {
  width: 100px;
  height: 100px;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 100px;
  height: 100px;
}

:deep(.el-upload__tip) {
  margin-top: 8px;
  color: #999;
  font-size: 12px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 80px 0 20px;
  }
  
  .container {
    padding: 0 10px;
  }
  
  :deep(.el-form-item__label) {
    text-align: left;
  }
  
  :deep(.el-upload--picture-card) {
    width: 80px;
    height: 80px;
  }
  
  :deep(.el-upload-list--picture-card .el-upload-list__item) {
    width: 80px;
    height: 80px;
  }
}
</style>
