<template>
  <div class="my-courses-page">
    <div class="container">
      <h2>我的课程</h2>
      <el-empty description="您还没有报名任何课程" />
      <el-button type="primary" @click="$router.push('/training/courses')">去发现课程</el-button>
    </div>
  </div>
</template>

<style scoped>
.my-courses-page { min-height: 100vh; background: #f5f7fa; padding: 40px 0; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; text-align: center; }
h2 { margin-bottom: 40px; }
</style>
