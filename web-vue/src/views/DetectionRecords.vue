<template>
  <el-card class="page-card">
    <template #header>
      <div class="header-row">
        <div>
          <strong>检测记录</strong>
          <span class="record-summary">共 {{ total }} 条，第 {{ currentPage }} / {{ totalPages }} 页，每页 {{ pageSize }} 条</span>
        </div>
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
    <el-table v-loading="loading" :data="pagedRecords" empty-text="暂无检测记录">
      <el-table-column label="时间" min-width="170">
        <template #default="{ row }">{{ recordTime(row) }}</template>
      </el-table-column>
      <el-table-column label="文件" min-width="180">
        <template #default="{ row }">{{ recordFilename(row) }}</template>
      </el-table-column>
      <el-table-column label="模型" min-width="180">
        <template #default="{ row }">{{ modelDisplayName(row, row.detection_result) }}</template>
      </el-table-column>
      <el-table-column label="目标" width="90">
        <template #default="{ row }">{{ detectionCount(row.detection_result, row) }}</template>
      </el-table-column>
      <el-table-column label="状态" width="130">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row)">
            {{ recordStatus(row) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="$router.push(`/records/detection/${row.id}`)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-row">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="pageSizes"
        :total="total"
        :disabled="loading"
        layout="total, sizes, prev, pager, next, jumper"
        background
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchDetectionRecords } from '../api/detection'
import type { DetectionRecord, PageResult } from '../types/detection'
import { recordTime } from '../utils/format'
import { detectionCount, detectionStatus, modelDisplayName } from '../utils/detectionDisplay'

type TagType = 'success' | 'info' | 'warning' | 'danger'

const DEFAULT_PAGE_SIZE = 10
const pageSizes = [10, 20, 50]

const loading = ref(false)
const error = ref('')
const records = ref<DetectionRecord[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(DEFAULT_PAGE_SIZE)
const serverPagination = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const pagedRecords = computed(() => {
  if (serverPagination.value) return records.value
  const start = (currentPage.value - 1) * pageSize.value
  return records.value.slice(start, start + pageSize.value)
})

onMounted(loadRecords)

async function loadRecords() {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchDetectionRecords({ page: currentPage.value, page_size: pageSize.value })
    applyRecordResponse(data)
  } catch (err) {
    await loadRecordsWithoutPaging(err)
  } finally {
    loading.value = false
  }
}

async function loadRecordsWithoutPaging(firstError: unknown) {
  try {
    const data = await fetchDetectionRecords()
    applyRecordResponse(data)
  } catch {
    error.value = firstError instanceof Error ? firstError.message : '????????'
    records.value = []
    total.value = 0
    serverPagination.value = false
  }
}

function applyRecordResponse(data: PageResult<DetectionRecord> | DetectionRecord[]) {
  if (Array.isArray(data)) {
    serverPagination.value = false
    records.value = data
    total.value = data.length
    clampCurrentPage()
    return
  }

  const pageRecords = normalizePage(data)
  const hasServerPaging = typeof data.total === 'number'
  serverPagination.value = hasServerPaging
  records.value = pageRecords
  total.value = hasServerPaging ? Math.max(0, data.total ?? 0) : pageRecords.length

  if (hasServerPaging) {
    currentPage.value = positiveInteger(data.page ?? data.current_page, currentPage.value)
    pageSize.value = positiveInteger(data.page_size ?? data.pageSize, pageSize.value)
  }
  clampCurrentPage()
}

function normalizePage(data: PageResult<DetectionRecord>): DetectionRecord[] {
  return data.items ?? data.records ?? data.list ?? data.data ?? []
}

function handleCurrentChange(page: number) {
  currentPage.value = page
  if (serverPagination.value) loadRecords()
}

function handleSizeChange(size: number) {
  pageSize.value = size
  currentPage.value = 1
  loadRecords()
}

function clampCurrentPage() {
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
  if (currentPage.value < 1) currentPage.value = 1
}

function positiveInteger(value: number | undefined, fallback: number): number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0 ? value : fallback
}

function recordFilename(record: DetectionRecord): string {
  return record.filename || record.detection_result?.image?.filename || record.title || '-'
}

function recordStatus(record: DetectionRecord): string {
  return record.status || detectionStatus(record.detection_result)
}

function statusTagType(record: DetectionRecord): TagType {
  const status = recordStatus(record)
  if (status === 'failed') return 'danger'
  if (status === 'detected') return 'success'
  if (status === 'processing' || status === 'pending') return 'warning'
  return 'info'
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

.record-summary {
  margin-left: 12px;
  color: var(--el-text-color-secondary);
  font-size: 13px;
  font-weight: normal;
}

.pagination-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
