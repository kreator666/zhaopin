<template>
  <div class="publish-post">
    <el-input
      v-model="content"
      type="textarea"
      :rows="4"
      placeholder="分享你的校园生活..."
      maxlength="500"
      show-word-limit
      resize="none"
    />
    
    <!-- 图片预览 -->
    <div v-if="imageList.length > 0" class="image-preview">
      <div v-for="(img, idx) in imageList" :key="idx" class="preview-item">
        <img :src="img" alt="" />
        <el-icon class="delete-btn" @click="removeImage(idx)"><Close /></el-icon>
      </div>
      <div v-if="imageList.length < 9" class="add-image" @click="triggerUpload">
        <el-icon><Plus /></el-icon>
      </div>
    </div>
    
    <!-- 投票选项 -->
    <div v-if="props.type === 'poll'" class="poll-options">
      <div v-for="(option, idx) in pollOptions" :key="idx" class="poll-item">
        <el-input v-model="pollOptions[idx]" :placeholder="`选项 ${idx + 1}`" maxlength="50" />
        <el-icon v-if="pollOptions.length > 2" class="remove-btn" @click="removePollOption(idx)"><Delete /></el-icon>
      </div>
      <el-button v-if="pollOptions.length < 6" text @click="addPollOption">
        <el-icon><Plus /></el-icon>添加选项
      </el-button>
    </div>
    
    <!-- 话题标签 -->
    <div v-if="selectedTopics.length > 0" class="selected-topics">
      <el-tag
        v-for="topic in selectedTopics"
        :key="topic"
        closable
        type="primary"
        @close="removeTopic(topic)"
      >
        #{{ topic }}
      </el-tag>
    </div>
    
    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="tools">
        <el-tooltip content="添加图片" placement="top">
          <el-icon :class="{ active: imageList.length > 0 }" @click="triggerUpload"><Picture /></el-icon>
        </el-tooltip>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          multiple
          style="display: none"
          @change="handleFileChange"
        />
        
        <el-tooltip content="添加话题" placement="top">
          <el-icon :class="{ active: selectedTopics.length > 0 }" @click="showTopicSelector = true"><ChatLineRound /></el-icon>
        </el-tooltip>
        
        <el-tooltip content="@好友" placement="top">
          <el-icon @click="showMentionSelector = true"><User /></el-icon>
        </el-tooltip>
        
        <el-tooltip content="添加投票" placement="top">
          <el-icon :class="{ active: props.type === 'poll' }" @click="togglePoll"><PieChart /></el-icon>
        </el-tooltip>
        
        <el-tooltip content="添加位置" placement="top">
          <el-icon><Location /></el-icon>
        </el-tooltip>
      </div>
      
      <el-button 
        type="primary" 
        :loading="publishing"
        :disabled="!canPublish"
        @click="handlePublish"
      >
        发布
      </el-button>
    </div>
    
    <!-- 话题选择器 -->
    <el-dialog v-model="showTopicSelector" title="选择话题" width="400px">
      <div class="topic-search">
        <el-input v-model="topicSearch" placeholder="搜索话题" prefix-icon="Search" />
      </div>
      <div class="hot-topics">
        <p class="section-title">热门话题</p>
        <div class="topic-tags">
          <el-tag
            v-for="topic in filteredTopics"
            :key="topic"
            :type="selectedTopics.includes(topic) ? 'primary' : 'info'"
            @click="toggleTopic(topic)"
            class="topic-tag"
          >
            #{{ topic }}
          </el-tag>
        </div>
      </div>
      <template #footer>
        <el-button @click="showTopicSelector = false">取消</el-button>
        <el-button type="primary" @click="showTopicSelector = false">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- @好友选择器 -->
    <el-dialog v-model="showMentionSelector" title="@好友" width="400px">
      <el-input v-model="mentionSearch" placeholder="搜索好友" prefix-icon="Search" />
      <div class="friend-list">
        <div 
          v-for="friend in filteredFriends" 
          :key="friend.id" 
          class="friend-item"
          @click="mentionFriend(friend)"
        >
          <el-avatar :size="40" :src="friend.avatar_url" />
          <span>{{ friend.username }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Picture,
  ChatLineRound,
  User,
  PieChart,
  Location,
  Plus,
  Close,
  Delete,
  Search
} from '@element-plus/icons-vue'
import { socialApi } from '@/api/social'
import { uploadApi } from '@/api/upload'

const props = defineProps({
  type: {
    type: String,
    default: 'text'
  }
})

const emit = defineEmits(['success', 'cancel'])

const content = ref('')
const imageList = ref([])
const selectedTopics = ref([])
const pollOptions = ref(['', ''])
const publishing = ref(false)
const fileInput = ref(null)
const showTopicSelector = ref(false)
const showMentionSelector = ref(false)
const topicSearch = ref('')
const mentionSearch = ref('')

const hotTopics = ['春招经验分享', '考研复试交流', '实习内推', '毕业季', '校园生活', '二手闲置', '失物招领', '组队学习']

const mockFriends = [
  { id: 1, username: '张三', avatar_url: '' },
  { id: 2, username: '李四', avatar_url: '' },
  { id: 3, username: '王五', avatar_url: '' }
]

const canPublish = computed(() => {
  if (props.type === 'poll') {
    return content.value.trim() && pollOptions.value.every(o => o.trim())
  }
  return content.value.trim() || imageList.value.length > 0
})

const filteredTopics = computed(() => {
  if (!topicSearch.value) return hotTopics
  return hotTopics.filter(t => t.includes(topicSearch.value))
})

const filteredFriends = computed(() => {
  if (!mentionSearch.value) return mockFriends
  return mockFriends.filter(f => f.username.includes(mentionSearch.value))
})

const triggerUpload = () => {
  if (imageList.value.length >= 9) {
    ElMessage.warning('最多上传9张图片')
    return
  }
  fileInput.value.click()
}

const handleFileChange = async (e) => {
  const files = Array.from(e.target.files)
  if (files.length + imageList.value.length > 9) {
    ElMessage.warning('最多上传9张图片')
    return
  }
  
  for (const file of files) {
    if (!file.type.startsWith('image/')) {
      ElMessage.warning(`${file.name} 不是图片文件`)
      continue
    }
    if (file.size > 5 * 1024 * 1024) {
      ElMessage.warning(`${file.name} 超过5MB限制`)
      continue
    }
    
    try {
      const res = await uploadApi.uploadImage(file)
      const data = res.data || res
      imageList.value.push(data.url)
    } catch (error) {
      console.error('上传失败', error)
      ElMessage.error('图片上传失败')
    }
  }
  
  e.target.value = ''
}

const removeImage = (idx) => {
  imageList.value.splice(idx, 1)
}

const toggleTopic = (topic) => {
  const idx = selectedTopics.value.indexOf(topic)
  if (idx > -1) {
    selectedTopics.value.splice(idx, 1)
  } else {
    if (selectedTopics.value.length < 3) {
      selectedTopics.value.push(topic)
    } else {
      ElMessage.warning('最多添加3个话题')
    }
  }
}

const removeTopic = (topic) => {
  const idx = selectedTopics.value.indexOf(topic)
  if (idx > -1) selectedTopics.value.splice(idx, 1)
}

const addPollOption = () => {
  if (pollOptions.value.length < 6) {
    pollOptions.value.push('')
  }
}

const removePollOption = (idx) => {
  pollOptions.value.splice(idx, 1)
}

const togglePoll = () => {
  emit('update:type', props.type === 'poll' ? 'text' : 'poll')
}

const mentionFriend = (friend) => {
  content.value += `@${friend.username} `
  showMentionSelector.value = false
}

const handlePublish = async () => {
  if (!canPublish.value) return
  
  publishing.value = true
  try {
    const data = {
      content: content.value,
      post_type: props.type === 'poll' ? 'poll' : (imageList.value.length > 0 ? 'image' : 'text'),
      images: imageList.value.length > 0 ? JSON.stringify(imageList.value) : null,
      tags: selectedTopics.value.length > 0 ? JSON.stringify(selectedTopics.value) : null
    }
    
    if (props.type === 'poll') {
      data.poll_options = JSON.stringify(pollOptions.value.map((text, idx) => ({
        id: idx,
        text,
        votes: 0
      })))
    }
    
    await socialApi.createPost(data)
    ElMessage.success('发布成功')
    emit('success')
    
    // 重置表单
    content.value = ''
    imageList.value = []
    selectedTopics.value = []
    pollOptions.value = ['', '']
  } catch (error) {
    console.error('发布失败', error)
    ElMessage.error(error.response?.data?.error || '发布失败')
  } finally {
    publishing.value = false
  }
}
</script>

<style scoped>
.publish-post {
  padding: 10px 0;
}

.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}

.preview-item {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.delete-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 20px;
  height: 20px;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-image {
  width: 100px;
  height: 100px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #909399;
}

.add-image:hover {
  border-color: #409eff;
  color: #409eff;
}

.poll-options {
  margin: 16px 0;
}

.poll-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.poll-item .el-input {
  flex: 1;
}

.remove-btn {
  cursor: pointer;
  color: #f56c6c;
}

.selected-topics {
  margin: 16px 0;
}

.selected-topics .el-tag {
  margin-right: 8px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}

.tools {
  display: flex;
  gap: 16px;
}

.tools .el-icon {
  font-size: 20px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s;
}

.tools .el-icon:hover {
  color: #409eff;
  transform: scale(1.1);
}

.tools .el-icon.active {
  color: #409eff;
}

.topic-search {
  margin-bottom: 16px;
}

.section-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
}

.topic-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-tag {
  cursor: pointer;
}

.friend-list {
  max-height: 300px;
  overflow-y: auto;
}

.friend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
}

.friend-item:hover {
  background: #f5f7fa;
}
</style>
