<template>
  <el-card class="page-card">
    <template #header>
      <div class="header-row">
        <strong>检测记录</strong>
        <el-button type="primary" plain :loading="loading" @click="loadRecords">刷新</el-button>
      </div>
    </template>
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      :closable="false"
      class="record-alert"
    />
    <el-table v-loading="loading" :data="records" empty-text="暂无检测记录">
      <el-table-column label="时间" min-width="170">
        <template #default="{ row }">{{ recordTime(row) }}</template>
      </el-table-column>
      <el-table-column label="文件" min-width="180">
        <template #default="{ row }">{{ row.filename || row.detection_result?.image?.filename || row.title || '-' }}</template>
      </el-table-column>
      <el-table-column label="模型" min-width="180">
        <template #default="{ row }">{{ modelDisplayName(row, row.detection_result) }}</template>
      </el-table-column>
      <el-table-column label="目标" width="90">
        <template #default="{ row }">{{ detectionCount(row.detection_result, row) }}</template>
      </el-table-column>
      <el-table-column label="状态" width="130">
        <template #default="{ row }">
          <el-tag :type="row.status === 'failed' ? 'danger' : detectionStatus(row.detection_result) === 'detected' ? 'success' : 'info'">
            {{ row.status || detectionStatus(row.detection_result) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="$router.push(`/records/detection/${row.id}`)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchDetectionRecords } from '../api/detection'
import type { DetectionRecord, PageResult } from '../types/detection'
import { recordTime } from '../utils/format'
import { detectionCount, detectionStatus, modelDisplayName } from '../utils/detectionDisplay'

const loading = ref(false)
const error = ref('')
const records = ref<DetectionRecord[]>([])

onMounted(loadRecords)

async function loadRecords() {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchDetectionRecords()
    records.value = Array.isArray(data) ? data : normalizePage(data)
  } catch (err) {
    error.value = err instanceof Error ? err.message : '检测记录加载失败'
  } finally {
    loading.value = false
  }
}

function normalizePage(data: PageResult<DetectionRecord>): DetectionRecord[] {
  return data.items ?? data.records ?? data.list ?? []
}
</script>

<style scoped>
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.record-alert {
  margin-bottom: 14px;
}
</style>
