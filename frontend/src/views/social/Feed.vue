<template>
  <div class="social-feed-page">
    <div class="page-header">
      <h1>校友圈</h1>
      <p>连接校友，分享生活</p>
    </div>
    <div class="container">
      <el-empty description="社交模块开发中，敬请期待...">
        <el-button type="primary" @click="$router.push('/social/circles')">浏览圈子</el-button>
      </el-empty>
    </div>
  </div>
</template>

<style scoped>
.social-feed-page { min-height: 100vh; background: #f5f7fa; }
.page-header { background: linear-gradient(135deg, #F56C6C 0%, #E6A23C 100%); color: #fff; padding: 40px 0; text-align: center; }
.container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; text-align: center; }
</style>
