<template>
  <div class="my-events-page">
    <div class="container">
      <h2>我的活动</h2>
      <el-empty description="您还没有参加任何活动" />
      <el-button type="primary" @click="$router.push('/social/events')">去发现活动</el-button>
    </div>
  </div>
</template>

<style scoped>
.my-events-page { min-height: 100vh; background: #f5f7fa; padding: 40px 0; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; text-align: center; }
h2 { margin-bottom: 40px; }
</style>
