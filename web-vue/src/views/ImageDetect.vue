<template>
  <div>
    <el-page-header title="图片检测" content="上传单张图片并展示检测结果" @back="$router.push('/records/detection')" />

    <el-alert
      title="Phase 2B Batch2 Stage2：仅稳定图片检测最小闭环、错误分支与 smoke 复现；视频、实时、Word、大屏仍未开放。"
      type="info"
      show-icon
      :closable="false"
      class="content-row"
    />

    <el-alert
      v-if="detectError"
      :title="detectError"
      type="error"
      show-icon
      :closable="false"
      class="content-row"
    />

    <el-row :gutter="18" class="content-row">
      <el-col :xs="24" :lg="10">
        <el-card class="page-card">
          <template #header><strong>检测配置</strong></template>
          <el-form label-position="top">
            <el-form-item label="检测模型">
              <el-select v-model="modelId" filterable placeholder="请选择已发布模型" :loading="modelsLoading" style="width: 100%">
                <el-option v-for="model in models" :key="model.id" :label="model.name" :value="model.id">
                  <span>{{ model.name }}</span>
                  <span class="muted option-meta">{{ model.base_model || model.id }}</span>
                </el-option>
              </el-select>
              <div v-if="selectedModel" class="form-tip muted">
                当前模型：{{ selectedModel.name }}
                <span v-if="selectedModel.base_model">({{ selectedModel.base_model }})</span>
                <el-tag v-if="selectedModel.is_dev_placeholder" size="small" type="warning" class="model-tag">dev placeholder</el-tag>
              </div>
              <div v-if="modelError" class="form-tip error">{{ modelError }}</div>
            </el-form-item>
            <el-form-item label="置信度阈值">
              <el-slider v-model="confidenceThreshold" :min="0.1" :max="0.95" :step="0.05" show-input />
            </el-form-item>
            <el-form-item label="待检测图片">
              <ImageUploader @selected="onFileSelected" />
            </el-form-item>
            <el-button type="primary" :loading="detecting" :disabled="!selectedFile || !modelId" @click="startDetect">
              开始检测
            </el-button>
          </el-form>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="14">
        <DetectionResultPanel :result="result" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import DetectionResultPanel from '../components/DetectionResultPanel.vue'
import ImageUploader from '../components/ImageUploader.vue'
import { detectImage } from '../api/detection'
import { fetchPublishedModels } from '../api/model'
import type { ImageDetectionResponse } from '../types/detection'
import type { PublishedModel } from '../types/model'
import { detectionCount, detectionStatus } from '../utils/detectionDisplay'

const models = ref<PublishedModel[]>([])
const modelId = ref('')
const modelError = ref('')
const detectError = ref('')
const modelsLoading = ref(false)
const confidenceThreshold = ref(0.5)
const selectedFile = ref<File | null>(null)
const detecting = ref(false)
const result = ref<ImageDetectionResponse | null>(null)

const selectedModel = computed(() => models.value.find((model) => model.id === modelId.value))

onMounted(loadModels)

function onFileSelected(file: File | null) {
  selectedFile.value = file
  detectError.value = ''
  result.value = null
}

async function loadModels() {
  modelsLoading.value = true
  modelError.value = ''
  try {
    models.value = await fetchPublishedModels()
    modelId.value = models.value[0]?.id || ''
    if (!models.value.length) modelError.value = '暂无可用模型，请先在后端发布模型。'
  } catch (error) {
    modelError.value = error instanceof Error ? error.message : '模型列表加载失败'
  } finally {
    modelsLoading.value = false
  }
}

async function startDetect() {
  if (!selectedFile.value || !modelId.value) return
  detecting.value = true
  detectError.value = ''
  try {
    result.value = await detectImage({
      image: selectedFile.value,
      modelId: modelId.value,
      confidenceThreshold: confidenceThreshold.value,
      saveRecord: true,
    })
    const status = detectionStatus(result.value.detection_result, result.value)
    const count = detectionCount(result.value.detection_result)
    ElMessage.success(`图片检测完成：${status}，目标数量：${count}`)
  } catch (error) {
    detectError.value = error instanceof Error ? error.message : '图片检测失败'
    ElMessage.error(detectError.value)
  } finally {
    detecting.value = false
  }
}
</script>

<style scoped>
.content-row {
  margin-top: 18px;
}

.option-meta {
  float: right;
  margin-left: 18px;
  font-size: 12px;
}

.form-tip {
  margin-top: 6px;
  font-size: 12px;
}

.model-tag {
  margin-left: 8px;
}

.error {
  color: #dc2626;
}
</style>
