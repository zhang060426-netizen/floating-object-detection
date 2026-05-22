<template>
  <el-container class="app-shell">
    <el-aside width="230px" class="app-aside">
      <div class="brand">
        <strong>漂浮物检测</strong>
        <span>Phase 2B 最小版</span>
      </div>
      <el-menu router :default-active="$route.path" background-color="#0f172a" text-color="#cbd5e1" active-text-color="#60a5fa">
        <el-menu-item index="/dashboard">Dashboard / 数据概览</el-menu-item>
        <el-menu-item index="/detect/image">图片检测</el-menu-item>
        <el-menu-item index="/records/detection">检测记录</el-menu-item>
        <el-menu-item index="/video">视频检测（暂不开放）</el-menu-item>
        <el-menu-item index="/realtime">实时检测（暂不开放）</el-menu-item>
        <el-menu-item index="/reports">Word 报告（暂不开放）</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="app-header">
        <span class="muted">水面漂浮物智能检测平台</span>
        <div class="user-actions">
          <span>{{ user.user?.username || '已登录用户' }}</span>
          <el-button type="primary" plain size="small" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const user = useUserStore()

function logout() {
  user.logout()
  router.replace('/login')
}
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.app-aside {
  background: #0f172a;
}

.brand {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 22px 20px;
  color: #fff;
}

.brand span {
  color: #94a3b8;
  font-size: 12px;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e5e7eb;
  background: #fff;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
