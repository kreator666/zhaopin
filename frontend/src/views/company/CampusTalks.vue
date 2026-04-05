<template>
  <div class="company-campus-talks">
    <Navbar />
    
    <div class="main-content" style="padding-top: 60px;">
      <div class="page-header">
        <div class="container">
          <h1>校园宣讲会管理</h1>
          <p>发布和管理您的校园宣讲会</p>
        </div>
      </div>
      
      <div class="container">
        <el-card shadow="hover" class="toolbar-card">
          <div class="toolbar">
            <el-button type="primary" @click="showDialog = true">
              <el-icon><Plus /></el-icon>发布宣讲会
            </el-button>
          </div>
        </el-card>
        
        <el-card shadow="hover" v-loading="loading">
          <el-table :data="talks" stripe>
            <el-table-column prop="title" label="宣讲主题" min-width="200" />
            <el-table-column prop="school_name" label="目标学校" width="150" />
            <el-table-column label="开始时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.start_time) }}
              </template>
            </el-table-column>
            <el-table-column prop="location" label="地点" width="150" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="statusType(row.status)">{{ statusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="浏览量" width="100">
              <template #default="{ row }">
                {{ row.view_count || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" text @click="editTalk(row)">编辑</el-button>
                <el-button type="danger" size="small" text @click="deleteTalk(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="talks.length === 0 && !loading" description="暂无宣讲会" />
          
          <div class="pagination" v-if="total > 0">
            <el-pagination
              v-model:current-page="page"
              :page-size="perPage"
              :total="total"
              layout="prev, pager, next"
              @current-change="fetchTalks"
            />
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 发布/编辑弹窗 -->
    <el-dialog
      v-model="showDialog"
      :title="isEdit ? '编辑宣讲会' : '发布宣讲会'"
      width="600px"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="宣讲主题" prop="title">
          <el-input v-model="form.title" placeholder="请输入宣讲主题" maxlength="200" show-word-limit />
        </el-form-item>
        
        <el-form-item label="目标学校" prop="school_name">
          <el-select
            v-model="form.school_name"
            filterable
            allow-create
            placeholder="选择或输入学校名称"
            style="width: 100%"
          >
            <el-option
              v-for="school in commonSchools"
              :key="school"
              :label="school"
              :value="school"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择开始时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选填"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="宣讲地点" prop="location">
          <el-input v-model="form.location" placeholder="如：学校大礼堂、线上直播链接等" />
        </el-form-item>
        
        <el-form-item label="报名链接">
          <el-input v-model="form.registration_url" placeholder="选填，外部报名页面链接" />
        </el-form-item>
        
        <el-form-item label="宣讲介绍">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="介绍宣讲会内容、流程、福利等"
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ isEdit ? '保存' : '发布' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import {
  getMyCampusTalks,
  createCampusTalk,
  updateCampusTalk,
  deleteCampusTalk
} from '@/api/interview'

const loading = ref(false)
const talks = ref([])
const page = ref(1)
const perPage = ref(10)
const total = ref(0)
const showDialog = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({
  id: null,
  title: '',
  school_name: '',
  start_time: '',
  end_time: '',
  location: '',
  description: '',
  registration_url: ''
})

const rules = {
  title: [{ required: true, message: '请输入宣讲主题', trigger: 'blur' }],
  school_name: [{ required: true, message: '请输入目标学校', trigger: 'blur' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  location: [{ required: true, message: '请输入宣讲地点', trigger: 'blur' }]
}

const commonSchools = [
  '清华大学', '北京大学', '复旦大学', '上海交通大学', '浙江大学',
  '南京大学', '中国科学技术大学', '华中科技大学', '武汉大学', '西安交通大学',
  '中山大学', '哈尔滨工业大学', '北京航空航天大学', '同济大学', '中国人民大学'
]

const fetchTalks = async () => {
  loading.value = true
  try {
    const res = await getMyCampusTalks({
      page: page.value,
      per_page: perPage.value
    })
    const data = res.data || res
    talks.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取宣讲会列表失败', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const statusType = (status) => {
  const types = { upcoming: 'primary', ongoing: 'success', ended: 'info' }
  return types[status] || 'info'
}

const statusText = (status) => {
  const texts = { upcoming: '即将开始', ongoing: '进行中', ended: '已结束' }
  return texts[status] || status
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const resetForm = () => {
  form.id = null
  form.title = ''
  form.school_name = ''
  form.start_time = ''
  form.end_time = ''
  form.location = ''
  form.description = ''
  form.registration_url = ''
  isEdit.value = false
}

const editTalk = (row) => {
  isEdit.value = true
  Object.assign(form, row)
  showDialog.value = true
}

const deleteTalk = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该宣讲会吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteCampusTalk(row.id)
    ElMessage.success('删除成功')
    fetchTalks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateCampusTalk(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createCampusTalk(form)
      ElMessage.success('发布成功')
    }
    showDialog.value = false
    resetForm()
    fetchTalks()
  } catch (error) {
    console.error('提交失败', error)
    ElMessage.error(error.response?.data?.error || '操作失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchTalks()
})
</script>

<style scoped>
.company-campus-talks {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: #fff;
  padding: 40px 0;
  text-align: center;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
}

.page-header p {
  margin: 0;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.toolbar-card {
  margin: 24px 0;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
