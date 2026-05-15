<template>
  <el-card class="page-card">
    <template #header>
      <div class="panel-header">
        <strong>检测结果</strong>
        <el-tag v-if="result?.record_id" type="success">记录：{{ result.record_id }}</el-tag>
      </div>
    </template>

    <el-empty v-if="!result" description="上传图片并开始检测后展示结果" />
    <template v-else>
      <el-row :gutter="18">
        <el-col :xs="24" :md="12">
          <h4>结果图</h4>
          <el-image
            v-if="resultImageUrl"
            :src="resultImageUrl"
            :preview-src-list="[resultImageUrl]"
            fit="contain"
            class="result-image"
          />
          <el-alert v-else title="后端未返回结果图 URL，仅展示结构化检测列表。" type="warning" :closable="false" />
        </el-col>
        <el-col :xs="24" :md="12">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="模型">{{ modelName }}</el-descriptions-item>
            <el-descriptions-item label="目标数量">{{ detections.length }}</el-descriptions-item>
            <el-descriptions-item label="最高置信度">{{ percent(detectionResult.summary?.max_confidence) }}</el-descriptions-item>
            <el-descriptions-item label="推理耗时">{{ inferenceMs }}</el-descriptions-item>
          </el-descriptions>

          <el-alert
            v-if="detections.length === 0"
            class="result-alert"
            title="未检测到漂浮物目标"
            type="info"
            :closable="false"
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
import type { ImageDetectionResponse } from '../types/detection'
import { fileUrl } from '../api/file'
import { bboxText, percent } from '../utils/format'

const props = defineProps<{ result?: ImageDetectionResponse | null }>()

const detectionResult = computed(() => props.result?.detection_result ?? { detections: [] })
const detections = computed(() => detectionResult.value.detections ?? [])
const resultImageUrl = computed(() => fileUrl(props.result?.result_image))
const modelName = computed(() => detectionResult.value.model?.model_name || detectionResult.value.model?.model_id || '-')
const inferenceMs = computed(() => {
  const value = detectionResult.value.timing?.inference_ms ?? detectionResult.value.timing_ms?.inference_ms
  return value === undefined ? '-' : `${value} ms`
})

</script>

<style scoped>
.panel-header {
  display: flex;
  align-items: center;
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
