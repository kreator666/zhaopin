<template>
  <div class="cert-form-page">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑考证信息' : '发布考证信息' }}</h2>
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
          
          <el-form-item label="考证名称" prop="name">
            <el-input 
              v-model="form.name" 
              placeholder="请输入考证名称"
              maxlength="100"
              show-word-limit
              style="width: 600px;"
            />
          </el-form-item>
          
          <el-form-item label="分类" prop="category">
            <el-select 
              v-model="form.category" 
              placeholder="请选择分类"
              style="width: 200px;"
            >
              <el-option label="语言考试" value="language" />
              <el-option label="计算机等级" value="computer" />
              <el-option label="职业资格" value="professional" />
              <el-option label="金融财会" value="finance" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="主办单位" prop="organizer">
            <el-input 
              v-model="form.organizer" 
              placeholder="请输入主办单位名称"
              style="width: 400px;"
            />
          </el-form-item>
          
          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="form.status">
              <el-radio value="upcoming">即将开始</el-radio>
              <el-radio value="ongoing">报名中</el-radio>
              <el-radio value="ended">已结束</el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
        
        <!-- 时间信息 -->
        <div class="form-section">
          <h3 class="section-title">时间信息</h3>
          
          <el-form-item label="报名开始" prop="registration_start">
            <el-date-picker
              v-model="form.registration_start"
              type="date"
              placeholder="选择报名开始日期"
              value-format="YYYY-MM-DD"
              style="width: 200px;"
            />
          </el-form-item>
          
          <el-form-item label="报名截止" prop="registration_end">
            <el-date-picker
              v-model="form.registration_end"
              type="date"
              placeholder="选择报名截止日期"
              value-format="YYYY-MM-DD"
              style="width: 200px;"
            />
          </el-form-item>
          
          <el-form-item label="考试日期" prop="exam_date">
            <el-date-picker
              v-model="form.exam_date"
              type="date"
              placeholder="选择考试日期"
              value-format="YYYY-MM-DD"
              style="width: 200px;"
            />
          </el-form-item>
        </div>
        
        <!-- 费用信息 -->
        <div class="form-section">
          <h3 class="section-title">费用信息</h3>
          
          <el-form-item label="报名费用" prop="fee">
            <el-input-number 
              v-model="form.fee" 
              :min="0"
              :precision="2"
              placeholder="0表示免费"
              style="width: 200px;"
            />
            <span class="form-unit">元</span>
            <div class="form-tip">输入 0 表示免费</div>
          </el-form-item>
          
          <el-form-item label="报名链接" prop="registration_url">
            <el-input 
              v-model="form.registration_url" 
              placeholder="请输入官方报名链接（可选）"
              style="width: 500px;"
            />
            <div class="form-tip">可选，学生端点击"立即报名"时将跳转到此链接</div>
          </el-form-item>
        </div>
        
        <!-- 详细信息 -->
        <div class="form-section">
          <h3 class="section-title">详细信息</h3>
          
          <el-form-item label="考试介绍" prop="description">
            <el-input 
              v-model="form.description" 
              type="textarea"
              :rows="6"
              placeholder="请输入考试详细介绍"
              maxlength="5000"
              show-word-limit
              style="width: 600px;"
            />
          </el-form-item>
          
          <el-form-item label="报考条件" prop="requirements">
            <el-input 
              v-model="form.requirements" 
              type="textarea"
              :rows="4"
              placeholder="请输入报考条件（可选）"
              maxlength="2000"
              show-word-limit
              style="width: 600px;"
            />
          </el-form-item>
        </div>
        
        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '发布' }}
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
import { getCertification, createCertification, updateCertification } from '@/api/training'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const formRef = ref(null)
const submitting = ref(false)

const isEdit = computed(() => {
  return !!route.params.id
})

const form = reactive({
  name: '',
  category: '',
  organizer: '',
  status: 'upcoming',
  registration_start: '',
  registration_end: '',
  exam_date: '',
  fee: null,
  registration_url: '',
  description: '',
  requirements: ''
})

const rules = {
  name: [
    { required: true, message: '请输入考证名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入考试介绍', trigger: 'blur' },
    { min: 10, max: 5000, message: '介绍长度在 10 到 5000 个字符', trigger: 'blur' }
  ]
}

// 获取详情
const fetchCertification = async () => {
  if (!isEdit.value) return
  
  const certId = route.params.id
  if (!certId) return
  
  try {
    const res = await getCertification(certId)
    const data = res.data || res
    
    form.name = data.name || ''
    form.category = data.category || ''
    form.organizer = data.organizer || ''
    form.status = data.status || 'upcoming'
    form.registration_start = data.registration_start || ''
    form.registration_end = data.registration_end || ''
    form.exam_date = data.exam_date || ''
    form.fee = data.fee !== null && data.fee !== undefined ? data.fee : null
    form.registration_url = data.registration_url || ''
    form.description = data.description || ''
    form.requirements = data.requirements || ''
  } catch (error) {
    console.error('获取考证信息失败', error)
    ElMessage.error('获取考证信息失败')
  }
}

// 返回
const goBack = () => {
  router.push('/admin/certifications')
}

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    try {
      const submitData = {
        name: form.name,
        category: form.category,
        organizer: form.organizer,
        status: form.status,
        registration_start: form.registration_start || null,
        registration_end: form.registration_end || null,
        exam_date: form.exam_date || null,
        fee: form.fee,
        registration_url: form.registration_url,
        description: form.description,
        requirements: form.requirements
      }
      
      if (isEdit.value) {
        await updateCertification(route.params.id, submitData)
        ElMessage.success('修改成功')
      } else {
        await createCertification(submitData)
        ElMessage.success('发布成功')
      }
      
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
  fetchCertification()
})
</script>

<style scoped>
.cert-form-page {
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
  border-bottom: 2px solid #E6A23C;
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
</style>
