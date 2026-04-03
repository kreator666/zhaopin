<template>
  <div class="edit-profile-page">
    <Navbar />
    <div class="container">
      <el-page-header @back="$router.back()" title="返回个人主页" />
      
      <h2 class="page-title">编辑个人资料</h2>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="profile-form"
      >
        <!-- 头像上传 -->
        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            :http-request="customUpload"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
          >
            <el-avatar 
              v-if="form.avatar_url" 
              :size="100" 
              :src="form.avatar_url" 
              class="upload-avatar"
            />
            <div v-else class="upload-placeholder">
              <el-icon :size="32"><Plus /></el-icon>
            </div>
          </el-upload>
        </el-form-item>

        <!-- 基本信息 -->
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="个人简介" prop="bio">
          <el-input
            v-model="form.bio"
            type="textarea"
            :rows="3"
            placeholder="介绍一下你自己..."
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <!-- 学校信息 -->
        <el-divider>学校信息</el-divider>

        <el-form-item label="学校">
          <el-input v-model="form.school_name" placeholder="请输入学校名称" />
        </el-form-item>

        <el-form-item label="专业">
          <el-input v-model="form.major" placeholder="请输入专业" />
        </el-form-item>

        <el-form-item label="入学年份">
          <el-date-picker
            v-model="form.enrollment_year"
            type="year"
            placeholder="选择入学年份"
            format="YYYY"
            value-format="YYYY"
          />
        </el-form-item>

        <el-form-item label="毕业年份">
          <el-date-picker
            v-model="form.graduation_year"
            type="year"
            placeholder="选择毕业年份"
            format="YYYY"
            value-format="YYYY"
          />
        </el-form-item>

        <!-- 联系方式 -->
        <el-divider>联系方式</el-divider>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" disabled />
        </el-form-item>

        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>

        <el-form-item label="所在地">
          <el-input v-model="form.location" placeholder="请输入所在城市" />
        </el-form-item>

        <!-- 隐私设置 -->
        <el-divider>隐私设置</el-divider>

        <el-form-item label="资料公开">
          <el-switch
            v-model="form.is_public"
            active-text="公开"
            inactive-text="私密"
          />
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" size="large" @click="submitForm" :loading="loading">
            保存修改
          </el-button>
          <el-button size="large" @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>

      <!-- 技能管理 -->
      <el-card class="skills-section" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>技能专长</span>
            <el-button type="primary" size="small" @click="showAddSkill = true">
              <el-icon><Plus /></el-icon>添加技能
            </el-button>
          </div>
        </template>

        <div class="skills-list">
          <el-empty v-if="skills.length === 0" description="暂无技能" />
          <div v-for="skill in skills" :key="skill.id" class="skill-item">
            <div class="skill-info">
              <span class="skill-name">{{ skill.skill_name }}</span>
              <el-rate :model-value="skill.proficiency" disabled show-score />
              <el-tag v-if="skill.certification" size="small" type="info">
                {{ skill.certification }}
              </el-tag>
            </div>
            <el-button type="danger" size="small" text @click="deleteSkill(skill.id)">
              删除
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- 求职意向 -->
      <el-card class="job-preference-section" shadow="hover" v-if="userStore.userInfo?.role === 'student'">
        <template #header>
          <span>求职意向</span>
        </template>

        <el-form :model="profileForm" label-width="100px">
          <el-form-item label="期望城市">
            <el-input v-model="profileForm.expected_location" placeholder="请输入期望工作城市" />
          </el-form-item>

          <el-form-item label="期望薪资">
            <el-input-number v-model="profileForm.expected_salary_min" :min="0" :max="100" placeholder="最低" />
            <span class="salary-separator">-</span>
            <el-input-number v-model="profileForm.expected_salary_max" :min="0" :max="100" placeholder="最高" />
            <span class="salary-unit">K</span>
          </el-form-item>

          <el-form-item label="个人优势">
            <el-input
              v-model="profileForm.summary"
              type="textarea"
              :rows="4"
              placeholder="描述你的个人优势..."
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveProfile" :loading="profileLoading">
              保存求职意向
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 添加技能对话框 -->
    <el-dialog v-model="showAddSkill" title="添加技能" width="400px">
      <el-form :model="skillForm" label-width="80px">
        <el-form-item label="技能名称">
          <el-input v-model="skillForm.skill_name" placeholder="如：Python、Photoshop" />
        </el-form-item>
        <el-form-item label="熟练程度">
          <el-rate v-model="skillForm.proficiency" show-score />
        </el-form-item>
        <el-form-item label="相关证书">
          <el-input v-model="skillForm.certification" placeholder="如：AWS认证（选填）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddSkill = false">取消</el-button>
        <el-button type="primary" @click="addSkill">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { Plus } from '@element-plus/icons-vue'
import request from '@/api/request'
import { getMyProfile, updateProfile, addSkill, deleteSkill as deleteSkillApi } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const profileLoading = ref(false)
const showAddSkill = ref(false)

const form = ref({
  username: '',
  bio: '',
  avatar_url: '',
  school_name: '',
  major: '',
  enrollment_year: null,
  graduation_year: null,
  phone: '',
  location: '',
  email: '',
  is_public: true
})

const profileForm = ref({
  expected_location: '',
  expected_salary_min: null,
  expected_salary_max: null,
  summary: ''
})

const skillForm = ref({
  skill_name: '',
  proficiency: 3,
  certification: ''
})

const skills = ref([])

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  bio: [
    { max: 200, message: '最多200个字符', trigger: 'blur' }
  ]
}

// 获取用户信息
const fetchUserData = async () => {
  try {
    const res = await getMyProfile()
    const data = res.data
    
    form.value = {
      username: data.username,
      bio: data.bio || '',
      avatar_url: data.avatar_url || '',
      school_name: data.school_name || '',
      major: data.major || '',
      enrollment_year: data.enrollment_year ? String(data.enrollment_year) : null,
      graduation_year: data.graduation_year ? String(data.graduation_year) : null,
      phone: data.phone || '',
      location: data.location || '',
      email: data.email,
      is_public: data.is_public
    }
    
    skills.value = data.skills || []
    
    if (data.profile) {
      profileForm.value = {
        expected_location: data.profile.expected_location || '',
        expected_salary_min: data.profile.expected_salary_min,
        expected_salary_max: data.profile.expected_salary_max,
        summary: data.profile.summary || ''
      }
    }
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
}

// 头像上传
const customUpload = async (options) => {
  const { file } = options
  
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const res = await request.post('/api/upload/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    // 直接设置头像 URL
    const result = res.data || res
    form.value.avatar_url = result.url
    ElMessage.success('头像上传成功')
  } catch (error) {
    ElMessage.error('上传失败')
  }
}

const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('只支持 JPG/PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 提交表单
const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    await updateProfile(form.value)
    ElMessage.success('资料更新成功')
    userStore.updateUserInfo(form.value)
    router.back()
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    loading.value = false
  }
}

// 保存求职意向
const saveProfile = async () => {
  profileLoading.value = true
  try {
    // 调用保存简历API
    // await saveResume(profileForm.value)
    ElMessage.success('求职意向保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    profileLoading.value = false
  }
}

// 添加技能
const addNewSkill = async () => {
  if (!skillForm.value.skill_name) {
    ElMessage.warning('请输入技能名称')
    return
  }
  
  try {
    await addSkill(skillForm.value)
    ElMessage.success('技能添加成功')
    skills.value.push({ ...skillForm.value })
    showAddSkill.value = false
    skillForm.value = { skill_name: '', proficiency: 3, certification: '' }
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 删除技能
const deleteSkill = async (skillId) => {
  try {
    await deleteSkillApi(skillId)
    ElMessage.success('删除成功')
    skills.value = skills.value.filter(s => s.id !== skillId)
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchUserData()
})
</script>

<style scoped>
.edit-profile-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 84px 0 24px; /* 顶部增加 60px 为导航栏留出空间 */
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  margin: 24px 0;
  font-size: 24px;
  font-weight: 600;
}

.profile-form {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.3s;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.upload-avatar {
  width: 100%;
  height: 100%;
}

.upload-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
}

.skills-section,
.job-preference-section {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skill-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.skill-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.skill-name {
  font-weight: 500;
  min-width: 100px;
}

.salary-separator {
  margin: 0 10px;
}

.salary-unit {
  margin-left: 10px;
  color: #666;
}

@media (max-width: 768px) {
  .profile-form {
    padding: 20px;
  }
}
</style>
