<template>
  <div class="dashboard-page">
    <div class="dashboard-header">
      <div>
        <h2>数据概览</h2>
        <p class="muted">Dashboard Visualization MVP：展示检测记录、目标数量、置信度与最近检测记录。</p>
      </div>
      <el-button type="primary" plain :loading="loading" @click="loadSummary">刷新</el-button>
    </div>

    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      :closable="false"
      class="dashboard-section"
    />

    <el-skeleton v-if="loading && !summary" :rows="8" animated class="dashboard-section" />

    <template v-else>
      <el-row :gutter="16" class="metric-grid">
        <el-col v-for="metric in metrics" :key="metric.label" :xs="24" :sm="12" :lg="6">
          <el-card class="metric-card" shadow="never">
            <span class="metric-label">{{ metric.label }}</span>
            <strong class="metric-value">{{ metric.value }}</strong>
            <span class="metric-help">{{ metric.help }}</span>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="16" class="dashboard-section">
        <el-col :xs="24" :lg="8">
          <el-card class="page-card" shadow="never">
            <template #header><strong>状态统计</strong></template>
            <div v-if="hasStatusStats" class="status-list">
              <div v-for="item in statusItems" :key="item.status" class="status-item">
                <span>
                  <el-tag :type="statusTagType(item.status)">{{ item.label }}</el-tag>
                </span>
                <strong>{{ item.count }}</strong>
              </div>
            </div>
            <el-empty v-else description="暂无状态统计" :image-size="80" />
          </el-card>
        </el-col>

        <el-col :xs="24" :lg="16">
          <el-card class="page-card" shadow="never">
            <template #header>
              <div class="card-header">
                <strong>最近检测记录</strong>
                <span class="muted">兼容缺少 detection_result 的旧记录</span>
              </div>
            </template>

            <el-alert
              v-if="hasLegacyRecords"
              title="部分记录缺少 detection_result，页面已按旧记录字段降级展示。"
              type="warning"
              show-icon
              :closable="false"
              class="record-warning"
            />

            <el-table
              v-loading="loading"
              :data="recentRecords"
              empty-text="暂无最近检测记录"
            >
              <el-table-column label="时间" min-width="170">
                <template #default="{ row }">{{ recordTime(row) }}</template>
              </el-table-column>
              <el-table-column label="文件名" min-width="180">
                <template #default="{ row }">{{ recordFilename(row) }}</template>
              </el-table-column>
              <el-table-column label="模型" min-width="160">
                <template #default="{ row }">{{ modelDisplayName(row, row.detection_result) }}</template>
              </el-table-column>
              <el-table-column label="目标数" width="90">
                <template #default="{ row }">{{ detectionCount(row.detection_result, row) }}</template>
              </el-table-column>
              <el-table-column label="状态" width="130">
                <template #default="{ row }">
                  <el-tag :type="recordStatusTagType(row)">{{ recordStatus(row) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="详情入口" width="120" fixed="right">
                <template #default="{ row }">
                  <el-button
                    type="primary"
                    link
                    :disabled="!row.id"
                    @click="$router.push(`/records/detection/${row.id}`)"
                  >
                    详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>

      <el-empty
        v-if="!loading && !error && isEmptyDashboard"
        description="暂无 Dashboard 数据，请先完成图片检测并保存记录。"
        class="dashboard-section empty-state"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchDashboardSummary } from '../api/detection'
import type { DashboardRecentRecord, DashboardStatusStats, DashboardSummary } from '../types/detection'
import { detectionCount, detectionStatus, modelDisplayName } from '../utils/detectionDisplay'
import { formatDate, percent, recordTime } from '../utils/format'

type TagType = 'success' | 'info' | 'warning' | 'danger'

const loading = ref(false)
const error = ref('')
const summary = ref<DashboardSummary | null>(null)

const recentRecords = computed(() => summary.value?.recent_records ?? [])
const statusStats = computed(() => summary.value?.status_stats ?? summary.value?.status_counts ?? {})
const hasStatusStats = computed(() => statusItems.value.some((item) => item.count > 0))
const hasLegacyRecords = computed(() => recentRecords.value.some((record) => !record.detection_result))
const isEmptyDashboard = computed(() => (
  totalRecords.value === 0 &&
  totalDetections.value === 0 &&
  !hasStatusStats.value &&
  recentRecords.value.length === 0
))

const totalRecords = computed(() => safeNumber(summary.value?.total_records))
const totalDetections = computed(() => safeNumber(summary.value?.total_detections ?? summary.value?.total_targets))
const averageConfidence = computed(() => summary.value?.avg_confidence ?? summary.value?.average_confidence)
const latestDetectionTime = computed(() => summary.value?.latest_detection_time ?? summary.value?.recent_detection_time)

const metrics = computed(() => [
  { label: '总检测记录数', value: formatInteger(totalRecords.value), help: '已保存的检测记录' },
  { label: '检测目标总数', value: formatInteger(totalDetections.value), help: '所有记录中的目标数量' },
  { label: '平均置信度', value: percent(averageConfidence.value), help: '后端汇总平均值' },
  { label: '最近检测时间', value: formatDate(latestDetectionTime.value || undefined), help: '最新一条检测记录时间' },
])

const statusItems = computed(() => {
  const stats = statusStats.value
  const preferred = ['detected', 'no_detection', 'unknown']
  const extra = Object.keys(stats).filter((status) => !preferred.includes(status)).sort()
  return [...preferred, ...extra].map((status) => ({
    status,
    label: statusLabel(status),
    count: safeNumber(stats[status]),
  }))
})

onMounted(loadSummary)

async function loadSummary() {
  loading.value = true
  error.value = ''
  try {
    summary.value = normalizeSummary(await fetchDashboardSummary())
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Dashboard 数据加载失败'
    summary.value = null
  } finally {
    loading.value = false
  }
}

function normalizeSummary(value: DashboardSummary): DashboardSummary {
  return {
    ...value,
    status_stats: normalizeStatusStats(value.status_stats ?? value.status_counts),
    recent_records: Array.isArray(value.recent_records) ? value.recent_records : [],
  }
}

function normalizeStatusStats(value?: DashboardStatusStats): DashboardStatusStats {
  const stats = value ?? {}
  return {
    ...stats,
    detected: safeNumber(stats.detected),
    no_detection: safeNumber(stats.no_detection),
    unknown: safeNumber(stats.unknown),
  }
}

function recordFilename(record: DashboardRecentRecord): string {
  return record.filename || record.detection_result?.image?.filename || record.title || '-'
}

function recordStatus(record: DashboardRecentRecord): string {
  return record.status || detectionStatus(record.detection_result)
}

function recordStatusTagType(record: DashboardRecentRecord): TagType {
  return statusTagType(recordStatus(record))
}

function statusTagType(status: string): TagType {
  if (status === 'failed') return 'danger'
  if (status === 'detected') return 'success'
  if (status === 'processing' || status === 'pending') return 'warning'
  return 'info'
}

function statusLabel(status: string): string {
  const labels: Record<string, string> = {
    detected: 'detected / 有目标',
    no_detection: 'no_detection / 无目标',
    unknown: 'unknown / 未知',
  }
  return labels[status] || status
}

function safeNumber(value: unknown): number {
  return typeof value === 'number' && Number.isFinite(value) ? value : 0
}

function formatInteger(value: number): string {
  return Math.max(0, Math.trunc(value)).toLocaleString()
}
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.dashboard-header,
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.dashboard-header {
  flex-wrap: wrap;
}

.dashboard-header h2 {
  margin: 0 0 6px;
}

.dashboard-header p {
  margin: 0;
}

.dashboard-section,
.metric-grid {
  margin-top: 18px;
}

.metric-card {
  min-height: 132px;
}

.metric-label,
.metric-help {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.metric-value {
  display: block;
  margin: 14px 0 10px;
  color: var(--el-text-color-primary);
  font-size: 28px;
  line-height: 1.1;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.status-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.status-item:last-child {
  padding-bottom: 0;
  border-bottom: 0;
}

.record-warning {
  margin-bottom: 12px;
}

.empty-state {
  border: 1px dashed var(--el-border-color);
  border-radius: 10px;
  background: #fff;
}
</style>
