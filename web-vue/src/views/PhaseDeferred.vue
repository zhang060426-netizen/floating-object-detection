<template>
  <el-card class="page-card">
    <el-empty :description="`${title}：Phase 2B 暂不开放`">
      <p class="muted">本批次只实现登录、图片检测、检测记录与基础鉴权。</p>
    </el-empty>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const title = computed(() => String(route.meta.title || '该功能'))
</script>
