<template>
  <div>
    <el-image
      v-if="displayUrl"
      :src="displayUrl"
      :preview-src-list="[displayUrl]"
      fit="contain"
      :class="imageClass"
    />
    <el-alert v-else-if="loading" :title="`${label}加载中...`" type="info" :closable="false" />
    <el-alert v-else :title="errorMessage" type="warning" :closable="false" />
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { getToken } from '../stores/user'
import { fileRefError, resolveFileUrl } from '../utils/fileUrl'
import type { FileRef } from '../types/detection'

const props = withDefaults(
  defineProps<{
    source?: FileRef | string | null
    label?: string
    imageClass?: string
  }>(),
  {
    label: '图片',
    imageClass: 'image-preview',
  },
)

const loading = ref(false)
const error = ref('')
const displayUrl = ref('')
let objectUrl = ''
let requestSeq = 0

const sourceUrl = computed(() => resolveFileUrl(props.source))
const sourceError = computed(() => fileRefError(props.source))
const errorMessage = computed(() => sourceError.value || error.value || `${props.label}加载失败。`)

watch(sourceUrl, loadImage, { immediate: true })
onBeforeUnmount(revokeObjectUrl)

async function loadImage(url: string) {
  const seq = ++requestSeq
  revokeObjectUrl()
  displayUrl.value = ''
  error.value = ''

  if (!url) {
    loading.value = false
    return
  }

  if (url.startsWith('blob:') || url.startsWith('data:')) {
    displayUrl.value = url
    loading.value = false
    return
  }

  loading.value = true
  try {
    const headers = new Headers()
    const token = getToken()
    if (token) headers.set('Authorization', `Bearer ${token}`)
    const response = await fetch(url, { headers })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const blob = await response.blob()
    if (seq !== requestSeq) return
    objectUrl = URL.createObjectURL(blob)
    displayUrl.value = objectUrl
  } catch (err) {
    if (seq !== requestSeq) return
    error.value = `${props.label}加载失败：${err instanceof Error ? err.message : '未知错误'}。URL：${url}`
  } finally {
    if (seq === requestSeq) loading.value = false
  }
}

function revokeObjectUrl() {
  if (objectUrl) {
    URL.revokeObjectURL(objectUrl)
    objectUrl = ''
  }
}
</script>
