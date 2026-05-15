<template>
  <div>
    <el-page-header title="返回记录列表" content="检测记录详情" @back="$router.push('/records/detection')" />
    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" class="detail-alert" />
    <el-skeleton v-if="loading" :rows="8" animated />
    <template v-else-if="record">
      <el-row :gutter="18" class="detail-grid">
        <el-col :xs="24" :lg="12">
          <el-card class="page-card">
            <template #header><strong>图片产物</strong></template>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="记录 ID">{{ record.id }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ recordTime(record) }}</el-descriptions-item>
              <el-descriptions-item label="模型">{{ record.model_name || record.detection_result?.model?.model_name || '-' }}</el-descriptions-item>
              <el-descriptions-item label="目标数量">{{ targetCount(record) }}</el-descriptions-item>
            </el-descriptions>
            <h4>原图</h4>
            <el-image v-if="originalUrl" :src="originalUrl" :preview-src-list="[originalUrl]" fit="contain" class="detail-image" />
            <el-alert v-else title="原图 URL 缺失或不可访问" type="warning" :closable="false" />
            <h4>结果图</h4>
            <el-image v-if="resultUrl" :src="resultUrl" :preview-src-list="[resultUrl]" fit="contain" class="detail-image" />
            <el-alert v-else title="结果图 URL 缺失或不可访问" type="warning" :closable="false" />
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card class="page-card">
            <template #header><strong>目标列表</strong></template>
            <el-table :data="detections" empty-text="无目标">
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
              <el-collapse-item title="原始 JSON">
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
import { fetchDetectionRecord } from '../api/detection'
import { fileUrl } from '../api/file'
import type { DetectionRecord } from '../types/detection'
import { bboxText, percent, recordTime, targetCount } from '../utils/format'

const props = defineProps<{ id: string }>()
const loading = ref(false)
const error = ref('')
const record = ref<DetectionRecord | null>(null)

const originalUrl = computed(() => fileUrl(record.value?.original_image))
const resultUrl = computed(() => fileUrl(record.value?.result_image))
const detections = computed(() => record.value?.detection_result?.detections ?? [])

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
</script>

<style scoped>
.detail-alert,
.detail-grid {
  margin-top: 18px;
}

.detail-image {
  width: 100%;
  max-height: 360px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
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
