<template>
  <div class="job-form-page">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑职位' : '发布职位' }}</h2>
    </div>
    
    <el-card>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="职位名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入职位名称" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最低薪资（K）">
              <el-input-number v-model="form.salary_min" :min="0" :max="1000" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="最高薪资（K）">
              <el-input-number v-model="form.salary_max" :min="0" :max="1000" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="工作地点">
              <el-input v-model="form.location" placeholder="如：北京、上海" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="工作类型">
              <el-select v-model="form.job_type" style="width: 100%">
                <el-option label="全职" value="full_time" />
                <el-option label="兼职" value="part_time" />
                <el-option label="实习" value="intern" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="经验要求">
              <el-input v-model="form.experience" placeholder="如：3-5年" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="学历要求">
          <el-input v-model="form.education" placeholder="如：本科及以上" />
        </el-form-item>
        
        <el-form-item label="职位描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="6" 
            placeholder="详细描述职位的工作内容、职责等"
          />
        </el-form-item>
        
        <el-form-item label="任职要求">
          <el-input 
            v-model="form.requirements" 
            type="textarea" 
            :rows="6" 
            placeholder="描述对应聘者的技能、经验等要求"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '立即发布' }}
          </el-button>
          <el-button size="large" @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { jobsApi } from '@/api/jobs'

const route = useRoute()
const router = useRouter()

const formRef = ref(null)
const submitting = ref(false)
const loading = ref(false)

const isEdit = computed(() => !!route.params.id)

const form = reactive({
  title: '',
  salary_min: null,
  salary_max: null,
  location: '',
  job_type: 'full_time',
  experience: '',
  education: '',
  description: '',
  requirements: ''
})

const rules = {
  title: [{ required: true, message: '请输入职位名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入职位描述', trigger: 'blur' }]
}

const fetchJobDetail = async () => {
  if (!isEdit.value) return
  
  loading.value = true
  try {
    const res = await jobsApi.getDetail(route.params.id)
    Object.assign(form, res)
  } catch (error) {
    console.error('获取职位详情失败', error)
    ElMessage.error('职位不存在')
    router.push('/company/jobs')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    if (isEdit.value) {
      await jobsApi.update(route.params.id, form)
      ElMessage.success('职位更新成功')
    } else {
      await jobsApi.create(form)
      ElMessage.success('职位发布成功')
    }
    router.push('/company/jobs')
  } catch (error) {
    console.error('提交失败', error)
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.push('/company/jobs')
}

onMounted(() => {
  fetchJobDetail()
})
</script>

<style scoped>
.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}
</style>
