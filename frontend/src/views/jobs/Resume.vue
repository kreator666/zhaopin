<template>
  <div class="resume-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <el-card class="resume-card">
          <template #header>
            <div class="card-header">
              <h2>我的简历</h2>
              <el-button type="primary" @click="handleSave" :loading="saving">保存简历</el-button>
            </div>
          </template>
          
          <el-form :model="form" label-position="top" :rules="rules" ref="formRef">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="form.name" placeholder="请输入姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="性别">
                  <el-radio-group v-model="form.gender">
                    <el-radio value="男">男</el-radio>
                    <el-radio value="女">女</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="出生日期">
                  <el-date-picker
                    v-model="form.birth_date"
                    type="date"
                    placeholder="选择出生日期"
                    style="width: 100%"
                    value-format="YYYY-MM-DD"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="所在城市">
                  <el-input v-model="form.location" placeholder="请输入所在城市" />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="个人简介">
              <el-input 
                v-model="form.summary" 
                type="textarea" 
                :rows="4" 
                placeholder="简单介绍一下自己"
              />
            </el-form-item>
            
            <el-divider>工作经历</el-divider>
            
            <el-form-item>
              <el-input 
                v-model="form.experience_text" 
                type="textarea" 
                :rows="6" 
                placeholder="请填写您的工作经历，包括公司名称、职位、工作时间、工作内容等"
              />
            </el-form-item>
            
            <el-divider>教育经历</el-divider>
            
            <el-form-item>
              <el-input 
                v-model="form.education_text" 
                type="textarea" 
                :rows="6" 
                placeholder="请填写您的教育经历，包括学校名称、专业、学历、时间等"
              />
            </el-form-item>
            
            <el-form-item label="技能标签">
              <el-input 
                v-model="form.skills" 
                placeholder="多个技能用逗号分隔，如：Java, Python, Vue.js"
              />
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { resumeApi } from '@/api/resume'

const formRef = ref(null)
const saving = ref(false)
const loading = ref(false)

const form = reactive({
  name: '',
  gender: '',
  birth_date: '',
  location: '',
  summary: '',
  experience_text: '',
  education_text: '',
  skills: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
}

const fetchResume = async () => {
  loading.value = true
  try {
    const res = await resumeApi.getMyResume()
    console.log('Resume API response:', res)
    const data = res.data || res
    console.log('Resume data:', data)
    if (data && data.id) {
      // 逐个字段赋值，确保响应式正常工作
      form.name = data.name || ''
      form.gender = data.gender || ''
      form.birth_date = data.birth_date || ''
      form.location = data.location || ''
      form.summary = data.summary || ''
      form.experience_text = data.experience_text || ''
      form.education_text = data.education_text || ''
      form.skills = data.skills || ''
      console.log('Form after assign:', form)
    }
  } catch (error) {
    console.error('获取简历失败', error)
    ElMessage.error('获取简历失败')
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  saving.value = true
  try {
    await resumeApi.saveResume(form)
    ElMessage.success('简历保存成功')
  } catch (error) {
    console.error('保存失败', error)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchResume()
})
</script>

<style scoped>
.resume-page {
  min-height: 100vh;
}

.main-content {
  padding-top: 80px;
  padding-bottom: 40px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.resume-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}
</style>
