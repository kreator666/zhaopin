<template>
  <div class="event-list-item" @click="$emit('click')">
    <el-image 
      :src="event.cover_image || defaultCover" 
      fit="cover"
      class="item-cover"
    >
      <template #error>
        <div class="cover-fallback">
          <el-icon :size="32"><Calendar /></el-icon>
        </div>
      </template>
    </el-image>
    
    <div class="item-content">
      <h4 class="item-title">{{ event.title }}</h4>
      
      <div class="item-meta">
        <span><el-icon><Calendar /></el-icon> {{ formatDate(event.start_time) }}</span>
        <span><el-icon><Location /></el-icon> {{ event.location }}</span>
      </div>
      
      <div class="item-footer">
        <el-tag :type="statusType" size="small">{{ statusText }}</el-tag>
        <span class="participant-count">{{ event.current_participants }} 人参加</span>
      </div>
    </div>
    
    <div v-if="isCreator" class="item-badge">发起人</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Calendar, Location } from '@element-plus/icons-vue'

const props = defineProps({
  event: {
    type: Object,
    required: true
  },
  isCreator: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])

const defaultCover = 'https://placehold.co/200x120/667eea/ffffff?text=Event'

const statusType = computed(() => {
  const map = {
    open: 'success',
    full: 'danger',
    ongoing: 'warning',
    ended: 'info',
    cancelled: 'info'
  }
  return map[props.event.status] || 'info'
})

const statusText = computed(() => {
  const map = {
    open: '报名中',
    full: '已满员',
    ongoing: '进行中',
    ended: '已结束',
    cancelled: '已取消'
  }
  return map[props.event.status] || props.event.status
})

const formatDate = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}
</script>

<style scoped>
.event-list-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.3s;
  position: relative;
}

.event-list-item:hover {
  background: #f8f9fa;
}

.item-cover {
  width: 120px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.cover-fallback {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.item-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.item-title {
  margin: 0;
  font-size: 15px;
  font-weight: 500;
  color: #333;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: #666;
}

.item-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.item-footer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.participant-count {
  font-size: 13px;
  color: #999;
}

.item-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 2px 8px;
  background: #e6f2ff;
  color: #409eff;
  font-size: 12px;
  border-radius: 4px;
}
</style>
