<template>
  <div class="flea-market-page">
    <Navbar />
    <div class="page-header">
      <h1>跳蚤市场</h1>
      <p>校园二手交易，让闲置流动起来</p>
      <el-button v-if="userStore.isLoggedIn" type="primary" size="large" @click="$router.push('/flea/publish')">
        发布闲置
      </el-button>
    </div>
    <div class="container">
      <el-empty description="跳蚤市场开发中，敬请期待..." />
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import Navbar from '@/components/Navbar.vue'
const userStore = useUserStore()
</script>

<style scoped>
.flea-market-page { min-height: 100vh; background: #f5f7fa; padding-top: 60px; }
.page-header { background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%); color: #fff; padding: 40px 0; text-align: center; }
.page-header h1 { margin-bottom: 16px; }
.container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
</style>
