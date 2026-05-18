<template>
  <div class="uploader">
    <el-upload drag :auto-upload="false" :show-file-list="false" accept="image/*" :on-change="onChange">
      <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
      <div class="el-upload__text">拖拽图片到此处，或 <em>点击选择</em></div>
      <template #tip>
        <div class="el-upload__tip">支持常见图片格式；本批次仅处理单张图片。</div>
      </template>
    </el-upload>
    <img v-if="previewUrl" :src="previewUrl" class="image-preview" alt="待检测图片预览" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import type { UploadFile } from 'element-plus'

const emit = defineEmits<{ selected: [file: File] }>()
const previewUrl = ref('')

function onChange(uploadFile: UploadFile) {
  const raw = uploadFile.raw
  if (!raw) return
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = URL.createObjectURL(raw)
  emit('selected', raw)
}
</script>

<style scoped>
.uploader {
  display: grid;
  gap: 16px;
}
</style>
