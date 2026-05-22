<template>
  <div>
    <div class="detail-header">
      <el-page-header title="返回记录列表" content="检测记录详情" @back="$router.push('/records/detection')" />
      <el-button
        v-if="record"
        type="primary"
        :loading="exportLoading"
        @click="handleExportWordReport"
      >
        导出 Word 报告
      </el-button>
    </div>
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
              <el-descriptions-item label="文件名">{{ displayFilename }}</el-descriptions-item>
              <el-descriptions-item label="模型">{{ displayModelName }}</el-descriptions-item>
              <el-descriptions-item label="检测状态">
                <el-tag :type="statusTagType">{{ status }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="置信度阈值">{{ percent(threshold) }}</el-descriptions-item>
              <el-descriptions-item label="目标数量">{{ count }}</el-descriptions-item>
              <el-descriptions-item label="最高置信度">{{ percent(detectionResult?.summary?.max_confidence) }}</el-descriptions-item>
              <el-descriptions-item label="平均置信度">{{ percent(detectionResult?.summary?.avg_confidence ?? detectionResult?.summary?.mean_confidence) }}</el-descriptions-item>
            </el-descriptions>

            <el-alert
              v-if="!detectionResult"
              title="该记录缺少 detection_result，已按旧记录兼容展示基础信息。"
              type="warning"
              show-icon
              :closable="false"
              class="detail-section"
            />

            <el-alert
              v-if="reasonText"
              :title="`后端提示：${reasonText}`"
              type="warning"
              show-icon
              :closable="false"
              class="detail-section"
            />

            <div class="detail-section">
              <h4>耗时信息</h4>
              <el-descriptions v-if="timingItems.length > 0" :column="1" border size="small">
                <el-descriptions-item v-for="item in timingItems" :key="item.key" :label="item.label">
                  {{ item.value }}
                </el-descriptions-item>
              </el-descriptions>
              <el-alert
                v-else
                title="该记录暂无耗时信息"
                type="info"
                show-icon
                :closable="false"
              />
            </div>

            <h4>原图</h4>
            <AuthImage :source="originalRef" label="原图" image-class="detail-image" />

            <h4>结果图</h4>
            <AuthImage :source="resultRef" label="结果图" image-class="detail-image" />
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card class="page-card">
            <template #header><strong>检测目标</strong></template>
            <el-alert
              v-if="detections.length === 0"
              :title="emptyDetectionMessage"
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
import { ElMessage } from 'element-plus'
import AuthImage from '../components/AuthImage.vue'
import { ApiClientError } from '../api/request'
import { exportDetectionRecordWordReport, fetchDetectionRecord } from '../api/detection'
import type { DetectionRecord } from '../types/detection'
import { saveBlob } from '../utils/download'
import { bboxText, percent, recordTime } from '../utils/format'
import {
  backendReason,
  confidenceThreshold,
  detectionCount,
  detectionStatus,
  modelDisplayName,
  originalImageRef,
  resultImageRef,
  timingDisplayItems,
} from '../utils/detectionDisplay'

type TagType = 'success' | 'info' | 'warning' | 'danger'

const props = defineProps<{ id: string }>()
const loading = ref(false)
const exportLoading = ref(false)
const error = ref('')
const record = ref<DetectionRecord | null>(null)

const detectionResult = computed(() => record.value?.detection_result)
const detections = computed(() => detectionResult.value?.detections ?? [])
const count = computed(() => detectionCount(detectionResult.value, record.value))
const displayModelName = computed(() => modelDisplayName(record.value, detectionResult.value))
const displayFilename = computed(() => record.value?.filename || detectionResult.value?.image?.filename || record.value?.title || '-')
const threshold = computed(() => confidenceThreshold(record.value, detectionResult.value))
const status = computed(() => detectionStatus(detectionResult.value))
const statusTagType = computed<TagType>(() => {
  if (status.value === 'failed') return 'danger'
  if (status.value === 'detected') return 'success'
  if (status.value === 'processing' || status.value === 'pending') return 'warning'
  return 'info'
})
const emptyDetectionMessage = computed(() => (
  detectionResult.value ? '该记录无检测目标' : '该记录缺少 detection_result，无法读取检测目标。'
))
const originalRef = computed(() => originalImageRef(record.value, detectionResult.value))
const resultRef = computed(() => resultImageRef(null, record.value, detectionResult.value))
const reasonText = computed(() => backendReason(detectionResult.value, detectionResult.value?.artifacts))
const timingItems = computed(() => timingDisplayItems(detectionResult.value))

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

async function handleExportWordReport() {
  if (!record.value) return

  exportLoading.value = true
  try {
    const response = await exportDetectionRecordWordReport(record.value.id)
    saveBlob(response.blob, response.filename || defaultReportFilename(record.value))
    ElMessage.success('Word 报告下载已开始')
  } catch (err) {
    ElMessage.error(exportErrorMessage(err))
  } finally {
    exportLoading.value = false
  }
}

function defaultReportFilename(value: DetectionRecord): string {
  return `detection-record-${value.id}-report.docx`
}

function exportErrorMessage(err: unknown): string {
  if (err instanceof ApiClientError && err.status === 404) {
    return '报告导出接口暂不可用或记录不存在'
  }
  return err instanceof Error ? err.message : 'Word 报告下载失败'
}
</script>

<style scoped>
.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.detail-alert,
.detail-grid {
  margin-top: 18px;
}

.detail-section {
  margin: 14px 0;
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
