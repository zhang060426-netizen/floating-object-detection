<template>
  <el-card class="page-card">
    <template #header>
      <div class="panel-header">
        <strong>检测结果</strong>
        <div class="panel-tags">
          <el-tag :type="statusTagType">{{ statusText }}</el-tag>
          <el-tag v-if="result?.record_id" type="success">记录 {{ result.record_id }}</el-tag>
        </div>
      </div>
    </template>

    <el-empty v-if="!result" description="请上传图片并开始检测，结果将在此处展示" />
    <template v-else>
      <el-alert
        v-if="isDevPlaceholderResult"
        title="当前为开发占位模型或占位结果：仅用于 Stage2 smoke，不代表生产精度。"
        type="warning"
        show-icon
        :closable="false"
        class="result-alert"
      />

      <el-alert
        v-if="reasonText"
        :title="`后端提示：${reasonText}`"
        type="warning"
        show-icon
        :closable="false"
        class="result-alert"
      />

      <el-row :gutter="18">
        <el-col :xs="24" :md="12">
          <h4>结果图</h4>
          <AuthImage :source="imageRef" label="结果图" image-class="result-image" />
        </el-col>
        <el-col :xs="24" :md="12">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="模型">{{ displayModelName }}</el-descriptions-item>
            <el-descriptions-item label="检测状态">{{ statusText }}</el-descriptions-item>
            <el-descriptions-item label="检测数量">{{ count }}</el-descriptions-item>
            <el-descriptions-item label="最高置信度">{{ percent(detectionResult.summary?.max_confidence) }}</el-descriptions-item>
            <el-descriptions-item label="平均置信度">{{ percent(detectionResult.summary?.avg_confidence ?? detectionResult.summary?.mean_confidence) }}</el-descriptions-item>
            <el-descriptions-item label="置信度阈值">{{ percent(threshold) }}</el-descriptions-item>
            <el-descriptions-item label="推理耗时">{{ inferenceMs }}</el-descriptions-item>
          </el-descriptions>

          <el-alert
            v-if="count === 0"
            class="result-alert"
            title="未检测到目标"
            description="后端返回成功，但 detections 为空。可调整阈值或更换图片后重试。"
            type="info"
            :closable="false"
            show-icon
          />

          <el-table v-else :data="detections" size="small" class="result-table">
            <el-table-column label="#" width="56">
              <template #default="{ $index }">{{ $index + 1 }}</template>
            </el-table-column>
            <el-table-column label="类别">
              <template #default="{ row }">{{ row.chinese_name || row.class_name }}</template>
            </el-table-column>
            <el-table-column label="置信度" width="110">
              <template #default="{ row }">{{ percent(row.confidence) }}</template>
            </el-table-column>
            <el-table-column label="bbox">
              <template #default="{ row }">{{ bboxText(row) }}</template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AuthImage from './AuthImage.vue'
import type { ImageDetectionResponse } from '../types/detection'
import { bboxText, percent } from '../utils/format'
import { backendReason, confidenceThreshold, detectionCount, detectionStatus, isDevPlaceholder, modelDisplayName, resultImageRef } from '../utils/detectionDisplay'

const props = defineProps<{ result?: ImageDetectionResponse | null }>()

const detectionResult = computed(() => props.result?.detection_result ?? { detections: [] })
const detections = computed(() => detectionResult.value.detections ?? [])
const count = computed(() => detectionCount(detectionResult.value))
const imageRef = computed(() => resultImageRef(props.result, null, detectionResult.value))
const displayModelName = computed(() => modelDisplayName(null, detectionResult.value))
const threshold = computed(() => confidenceThreshold(null, detectionResult.value))
const status = computed(() => detectionStatus(detectionResult.value, props.result))
const statusText = computed(() => (status.value === 'detected' ? 'detected' : status.value === 'no_detection' ? 'no_detection' : status.value))
const statusTagType = computed(() => (status.value === 'detected' ? 'success' : status.value === 'no_detection' ? 'info' : 'warning'))
const inferenceMs = computed(() => {
  const value = detectionResult.value.timing?.inference_ms ?? detectionResult.value.timing_ms?.inference_ms
  return value === undefined ? '-' : `${value} ms`
})
const isDevPlaceholderResult = computed(() => isDevPlaceholder(detectionResult.value))
const reasonText = computed(() => backendReason(detectionResult.value, detectionResult.value.artifacts))
</script>

<style scoped>
.panel-header,
.panel-tags {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-header {
  justify-content: space-between;
}

.result-image {
  width: 100%;
  max-height: 460px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
}

.result-alert,
.result-table {
  margin-top: 16px;
}
</style>
