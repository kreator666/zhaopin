<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

onLaunch(() => {
  console.log('App Launch')
  
  // 初始化用户状态
  const userStore = useUserStore()
  userStore.init()
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style lang="scss">
/* 全局样式 */
page {
  background-color: #f5f7fa;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  font-size: 28rpx;
  color: #333;
  height: 100%;
}

/* 公共样式类 */
.container {
  padding: 24rpx;
}

.flex {
  display: flex;
}

.flex-col {
  display: flex;
  flex-direction: column;
}

.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text-center {
  text-align: center;
}

.text-primary {
  color: #409eff;
}

.text-success {
  color: #67c23a;
}

.text-warning {
  color: #e6a23c;
}

.text-danger {
  color: #f56c6c;
}

.text-muted {
  color: #909399;
}

/* 卡片样式 */
.card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

/* 按钮样式 */
.btn-primary {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  color: #fff;
  border: none;
  border-radius: 8rpx;
  padding: 20rpx 40rpx;
  font-size: 28rpx;
}

.btn-primary::after {
  border: none;
}

.btn-outline {
  background: transparent;
  color: #409eff;
  border: 2rpx solid #409eff;
  border-radius: 8rpx;
  padding: 18rpx 38rpx;
  font-size: 28rpx;
}

.btn-outline::after {
  border: none;
}

/* 间距 */
.mt-10 {
  margin-top: 10rpx;
}

.mt-20 {
  margin-top: 20rpx;
}

.mt-30 {
  margin-top: 30rpx;
}

.mb-10 {
  margin-bottom: 10rpx;
}

.mb-20 {
  margin-bottom: 20rpx;
}

.mb-30 {
  margin-bottom: 30rpx;
}

.pt-10 {
  padding-top: 10rpx;
}

.pt-20 {
  padding-top: 20rpx;
}

.pb-10 {
  padding-bottom: 10rpx;
}

.pb-20 {
  padding-bottom: 20rpx;
}

/* 分割线 */
.divider {
  height: 1rpx;
  background-color: #eee;
  margin: 20rpx 0;
}

/* 图片占位 */
.img-placeholder {
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c0c4cc;
}
</style>
