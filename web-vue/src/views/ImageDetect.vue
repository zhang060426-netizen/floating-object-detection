<template>
  <div>
    <el-page-header title="返回" content="图片检测" @back="$router.push('/records/detection')" />
    <el-row :gutter="18" class="content-row">
      <el-col :xs="24" :lg="10">
        <el-card class="page-card">
          <template #header><strong>上传与参数</strong></template>
          <el-form label-position="top">
            <el-form-item label="检测模型">
              <el-select v-model="modelId" filterable placeholder="请选择模型" :loading="modelsLoading" style="width: 100%">
                <el-option v-for="model in models" :key="model.id" :label="model.name" :value="model.id">
                  <span>{{ model.name }}</span>
                  <span class="muted option-meta">{{ model.base_model }}</span>
                </el-option>
              </el-select>
              <div v-if="modelError" class="form-tip error">{{ modelError }}</div>
            </el-form-item>
            <el-form-item label="置信度阈值">
              <el-slider v-model="confidenceThreshold" :min="0.1" :max="0.95" :step="0.05" show-input />
            </el-form-item>
            <el-form-item label="待检测图片">
              <ImageUploader @selected="selectedFile = $event" />
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
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import DetectionResultPanel from '../components/DetectionResultPanel.vue'
import ImageUploader from '../components/ImageUploader.vue'
import { detectImage } from '../api/detection'
import { fetchPublishedModels } from '../api/model'
import type { ImageDetectionResponse } from '../types/detection'
import type { PublishedModel } from '../types/model'

const models = ref<PublishedModel[]>([])
const modelId = ref('')
const modelError = ref('')
const modelsLoading = ref(false)
const confidenceThreshold = ref(0.5)
const selectedFile = ref<File | null>(null)
const detecting = ref(false)
const result = ref<ImageDetectionResponse | null>(null)

onMounted(loadModels)

async function loadModels() {
  modelsLoading.value = true
  modelError.value = ''
  try {
    models.value = await fetchPublishedModels()
    modelId.value = models.value[0]?.id || ''
    if (!models.value.length) modelError.value = '后端未返回可用模型，请先发布模型或检查 /api/models/published。'
  } catch (error) {
    modelError.value = error instanceof Error ? error.message : '模型列表加载失败'
  } finally {
    modelsLoading.value = false
  }
}

async function startDetect() {
  if (!selectedFile.value || !modelId.value) return
  detecting.value = true
  try {
    result.value = await detectImage({
      image: selectedFile.value,
      modelId: modelId.value,
      confidenceThreshold: confidenceThreshold.value,
      saveRecord: true,
    })
    ElMessage.success('检测完成')
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '图片检测失败')
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

.error {
  color: #dc2626;
}
</style>
