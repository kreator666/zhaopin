<template>
  <Navbar />
  <div class="chat-page">
    <div class="container">
      <h2>私信聊天</h2>
      <el-empty description="聊天功能开发中..." />
      <el-button @click="$router.push('/messages')">返回消息列表</el-button>
    </div>
  </div>
</template>

<style scoped>
.chat-page { min-height: 100vh; background: #f5f7fa; padding: 100px 0 40px; }
.container { max-width: 800px; margin: 0 auto; padding: 0 20px; text-align: center; }
</style>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>
