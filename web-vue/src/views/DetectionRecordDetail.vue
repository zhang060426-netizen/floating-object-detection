<template>
  <div>
    <el-page-header title="返回记录列表" content="检测记录详情" @back="$router.push('/records/detection')" />
    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" class="detail-alert" />
    <el-skeleton v-if="loading" :rows="8" animated class="detail-alert" />
    <template v-else-if="record">
      <el-row :gutter="18" class="detail-grid">
        <el-col :xs="24" :lg="12">
          <el-card class="page-card">
            <template #header><strong>记录概览</strong></template>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="记录 ID">{{ record.id }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ recordTime(record) }}</el-descriptions-item>
              <el-descriptions-item label="模型">{{ modelName }}</el-descriptions-item>
              <el-descriptions-item label="置信度阈值">{{ percent(confidenceThreshold) }}</el-descriptions-item>
              <el-descriptions-item label="目标数量">{{ detectionCount }}</el-descriptions-item>
              <el-descriptions-item label="最高置信度">{{ percent(detectionResult?.summary?.max_confidence) }}</el-descriptions-item>
              <el-descriptions-item label="平均置信度">{{ percent(detectionResult?.summary?.avg_confidence) }}</el-descriptions-item>
              <el-descriptions-item label="推理耗时">{{ inferenceMs }}</el-descriptions-item>
            </el-descriptions>

            <h4>原图</h4>
            <AuthImage :source="originalImageRef" label="原图" image-class="detail-image" />

            <h4>结果图</h4>
            <AuthImage :source="resultImageRef" label="结果图" image-class="detail-image" />
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card class="page-card">
            <template #header><strong>检测目标</strong></template>
            <el-alert
              v-if="detections.length === 0"
              title="该记录无检测目标"
              type="info"
              show-icon
              :closable="false"
              class="detail-section"
            />
            <el-table v-else :data="detections" empty-text="无目标" size="small">
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

            <el-collapse class="json-collapse">
              <el-collapse-item title="detection_result JSON">
                <pre>{{ JSON.stringify(detectionResult, null, 2) }}</pre>
              </el-collapse-item>
              <el-collapse-item title="record JSON">
                <pre>{{ JSON.stringify(record, null, 2) }}</pre>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import AuthImage from '../components/AuthImage.vue'
import { fetchDetectionRecord } from '../api/detection'
import type { DetectionArtifacts, DetectionRecord, FileRef } from '../types/detection'
import { bboxText, percent, recordTime, targetCount } from '../utils/format'

const props = defineProps<{ id: string }>()
const loading = ref(false)
const error = ref('')
const record = ref<DetectionRecord | null>(null)

const detectionResult = computed(() => record.value?.detection_result)
const artifacts = computed(() => detectionResult.value?.artifacts)
const originalImageRef = computed(() =>
  record.value?.original_image ||
  artifacts.value?.original_image ||
  artifactKeyRef(artifacts.value, 'original_image_key', 'uploads'),
)
const resultImageRef = computed(() =>
  record.value?.result_image ||
  artifacts.value?.result_image ||
  artifacts.value?.result_image_url ||
  artifactKeyRef(artifacts.value, 'result_image_key', 'results') ||
  artifactKeyRef(artifacts.value, 'annotated_image_key', 'results'),
)
const detections = computed(() => detectionResult.value?.detections ?? [])
const detectionCount = computed(() => (record.value ? targetCount(record.value) : 0))
const modelName = computed(() => record.value?.model_name || record.value?.model?.name || detectionResult.value?.model?.model_name || detectionResult.value?.model?.model_id || '-')
const confidenceThreshold = computed(() => record.value?.confidence_threshold ?? detectionResult.value?.summary?.confidence_threshold ?? detectionResult.value?.model?.confidence_threshold)
const inferenceMs = computed(() => {
  const value = detectionResult.value?.timing?.inference_ms ?? detectionResult.value?.timing_ms?.inference_ms
  return value === undefined ? '-' : `${value} ms`
})

onMounted(loadRecord)

async function loadRecord() {
  loading.value = true
  error.value = ''
  try {
    record.value = await fetchDetectionRecord(props.id)
  } catch (err) {
    error.value = err instanceof Error ? err.message : '检测记录详情加载失败'
  } finally {
    loading.value = false
  }
}

function artifactKeyRef(artifact: DetectionArtifacts | undefined, key: string, bucket: string): FileRef | null {
  const value = artifact?.[key]
  return typeof value === 'string' && value ? { bucket, object_key: value } : null
}
</script>

<style scoped>
.detail-alert,
.detail-grid {
  margin-top: 18px;
}

.detail-section {
  margin-bottom: 14px;
}

.detail-image {
  width: 100%;
  max-height: 360px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
}

.json-collapse {
  margin-top: 18px;
}

pre {
  max-height: 420px;
  overflow: auto;
  margin: 0;
  padding: 12px;
  border-radius: 8px;
  background: #0f172a;
  color: #e2e8f0;
}
</style>
