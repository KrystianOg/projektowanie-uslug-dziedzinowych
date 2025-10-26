import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import RiskView from '@/views/RiskView.vue'
import LogsView from '@/views/LogsView.vue'
import ConfigurationView from '@/views/ConfigurationView.vue'

import LiveView from '@/views/trading/LiveView.vue'
import HistoryView from '@/views/trading/HistoryView.vue'
import PositionsView from '@/views/trading/PositionsView.vue'

import PerformanceView from '@/views/analytics/PerformanceView.vue'
import MLInsightsView from '@/views/analytics/MLInsightsView.vue'
import SentimentView from '@/views/analytics/SentimentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home', // overview
      component: HomeView,
    },
    {
      path: '/trading/live',
      name: 'trading-live',
      component: LiveView
    },
    {
      path: '/trading/positions',
      name: 'trading-positions',
      component: PositionsView
    },
    {
      path: '/trading/history',
      name: 'trading-history',
      component: HistoryView
    },
    {
      path: '/analytics/performance',
      name: 'analytics-performance',
      component: PerformanceView
    },
    {
      path: '/analytics/ml-insights',
      name: 'analytics-ml-insights',
      component:MLInsightsView
    },
    {
      path: '/analytics/sentiment',
      name: 'analytics-sentiment',
      component: SentimentView
    },
    {
      path: "/risk",
      name: "risk",
      component: RiskView
    },
    {
      path: '/configuration',
      name: 'configuration',
      component: ConfigurationView
    },
    {
      path: '/logs',
      name: "logs",
      component: LogsView
    }
  ],
})

export default router
