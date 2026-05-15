import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import AppLayout from '../components/AppLayout.vue'
import Login from '../views/Login.vue'
import ImageDetect from '../views/ImageDetect.vue'
import DetectionRecords from '../views/DetectionRecords.vue'
import DetectionRecordDetail from '../views/DetectionRecordDetail.vue'
import PhaseDeferred from '../views/PhaseDeferred.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/detect/image' },
    { path: '/login', component: Login, meta: { public: true } },
    {
      path: '/',
      component: AppLayout,
      children: [
        { path: 'detect/image', component: ImageDetect },
        { path: 'records/detection', component: DetectionRecords },
        { path: 'records/detection/:id', component: DetectionRecordDetail, props: true },
        { path: 'video', component: PhaseDeferred, meta: { title: '视频检测' } },
        { path: 'realtime', component: PhaseDeferred, meta: { title: '实时检测' } },
        { path: 'reports', component: PhaseDeferred, meta: { title: 'Word 报告' } },
      ],
    },
    { path: '/:pathMatch(.*)*', redirect: '/detect/image' },
  ],
})

router.beforeEach(async (to) => {
  const user = useUserStore()
  if (!user.token) {
    await user.hydrate()
  }
  if (!to.meta.public && !user.isAuthenticated) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.path === '/login' && user.isAuthenticated) {
    return { path: '/detect/image' }
  }
  return true
})

export default router
