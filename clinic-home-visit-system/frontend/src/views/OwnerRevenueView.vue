<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-emerald-900 text-white flex flex-col min-h-screen fixed left-0 top-0">
      <div class="px-6 py-5 border-b border-emerald-800">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-emerald-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <div>
            <span class="text-lg font-bold">Chủ phòng khám</span>
            <p class="text-xs text-emerald-300">ClinicSearch</p>
          </div>
        </div>
      </div>
      <nav class="flex-1 px-3 py-4 space-y-1">
        <router-link to="/owner/dashboard" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-emerald-200 hover:bg-emerald-800 hover:text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
          Dashboard
        </router-link>
        <router-link to="/owner/clinics" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-emerald-200 hover:bg-emerald-800 hover:text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          Phòng khám của tôi
        </router-link>
        <router-link to="/owner/doctors" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-emerald-200 hover:bg-emerald-800 hover:text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          Bác sĩ
        </router-link>
        <router-link to="/owner/revenue" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors bg-emerald-600 text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Doanh thu
        </router-link>
      </nav>
      <div class="px-4 py-4 border-t border-emerald-800">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center text-xs font-bold">{{ userInitials }}</div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ user?.full_name || 'Chủ phòng khám' }}</p>
            <p class="text-xs text-emerald-300 truncate">{{ user?.email }}</p>
          </div>
          <button @click="handleLogout" class="p-1.5 rounded-lg hover:bg-emerald-800 text-emerald-300 hover:text-red-400 transition-colors" title="Đăng xuất">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 ml-64 min-h-screen">
      <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div class="px-8 py-4 flex items-center justify-between">
          <div>
            <h1 class="text-xl font-semibold text-gray-900">Báo cáo Doanh thu</h1>
          </div>
          <button @click="refresh" :disabled="loading" class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 transition-colors">
            <svg class="w-4 h-4" :class="loading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            {{ loading ? 'Đang tải...' : 'Làm mới' }}
          </button>
        </div>
      </header>

      <div class="px-8 py-6">
        <!-- Loading -->
        <div v-if="loading" class="flex items-center justify-center py-20">
          <div class="w-10 h-10 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
          <p class="ml-4 text-gray-500">Đang tải dữ liệu...</p>
        </div>

        <template v-else>
          <!-- Clinic Filter -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
            <div class="flex flex-wrap gap-3 items-center">
              <label class="text-sm font-medium text-gray-700">Phòng khám:</label>
              <select v-model="selectedClinic" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 min-w-[250px]">
                <option value="">Tất cả phòng khám</option>
                <option v-for="c in clinics" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
          </div>

          <!-- Tab switcher -->
          <div class="flex flex-wrap gap-2 mb-6">
            <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
              class="px-5 py-2.5 rounded-xl text-sm font-semibold transition-all"
              :class="activeTab === tab.key ? 'bg-emerald-600 text-white shadow-md' : 'bg-white text-gray-600 border border-gray-200 hover:border-emerald-300'"
            >{{ tab.label }}</button>
          </div>

          <!-- ===== KHOẢNG NGÀY ===== -->
          <div v-if="activeTab === 'range'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
            <h3 class="font-semibold text-gray-800 mb-5 flex items-center gap-2">
              <svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              Theo khoảng ngày
            </h3>
            <div class="flex flex-wrap items-end gap-4 mb-6">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Từ ngày</label>
                <input type="date" v-model="rangeFrom" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"/>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Đến ngày</label>
                <input type="date" v-model="rangeTo" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"/>
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
              <div class="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
                <p class="text-xs text-emerald-600 font-medium uppercase tracking-wide mb-1">Tổng doanh thu</p>
                <p class="text-2xl font-extrabold text-emerald-700">{{ formatPrice(rangeRevenue.total) }}</p>
              </div>
              <div class="bg-blue-50 rounded-xl p-4 border border-blue-100">
                <p class="text-xs text-blue-600 font-medium uppercase tracking-wide mb-1">Số đơn hoàn thành</p>
                <p class="text-2xl font-extrabold text-blue-700">{{ rangeRevenue.count }}</p>
              </div>
              <div class="bg-purple-50 rounded-xl p-4 border border-purple-100">
                <p class="text-xs text-purple-600 font-medium uppercase tracking-wide mb-1">Trung bình / đơn</p>
                <p class="text-2xl font-extrabold text-purple-700">{{ formatPrice(rangeRevenue.avg) }}</p>
              </div>
            </div>
            <div v-if="rangeRevenue.items.length > 0">
              <h4 class="text-sm font-semibold text-gray-700 mb-3">Chi tiết</h4>
              <div class="overflow-x-auto">
                <table class="w-full text-sm">
                  <thead>
                    <tr class="border-b border-gray-100">
                      <th class="text-left py-2 pr-4 text-xs font-semibold text-gray-400 uppercase">Ngày khám</th>
                      <th class="text-left py-2 pr-4 text-xs font-semibold text-gray-400 uppercase">Hình thức</th>
                      <th class="text-left py-2 pr-4 text-xs font-semibold text-gray-400 uppercase">Gói khám</th>
                      <th class="text-right py-2 text-xs font-semibold text-gray-400 uppercase">Doanh thu</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-50">
                    <tr v-for="b in rangeRevenue.items" :key="b.id" class="hover:bg-gray-50">
                      <td class="py-2.5 pr-4 text-gray-700">{{ formatDate(b.scheduled_at) }}</td>
                      <td class="py-2.5 pr-4">
                        <span :class="b.booking_type === 'home_visit' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'" class="px-2 py-0.5 rounded-full text-xs font-medium">
                          {{ b.booking_type === 'home_visit' ? 'Tại nhà' : 'Phòng khám' }}
                        </span>
                      </td>
                      <td class="py-2.5 pr-4 text-gray-600">{{ b.package_name || '—' }}</td>
                      <td class="py-2.5 text-right font-semibold text-emerald-700">{{ formatPrice(bRevenue(b)) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-400 text-sm">Không có đơn hoàn thành trong khoảng thời gian này.</div>
          </div>

          <!-- ===== THEO THÁNG ===== -->
          <div v-if="activeTab === 'monthly'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
            <h3 class="font-semibold text-gray-800 mb-5 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              Theo tháng
            </h3>
            <div class="flex items-center gap-3 mb-6">
              <label class="text-xs font-medium text-gray-500">Năm</label>
              <select v-model="monthlyYear" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400">
                <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
              </select>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mb-6">
              <div v-for="m in monthlyData" :key="m.month" class="rounded-xl border p-4"
                :class="m.total > 0 ? 'border-blue-200 bg-blue-50' : 'border-gray-100 bg-gray-50'">
                <p class="text-xs font-semibold uppercase tracking-wide mb-2" :class="m.total > 0 ? 'text-blue-500' : 'text-gray-400'">Tháng {{ m.month }}</p>
                <p class="text-lg font-extrabold" :class="m.total > 0 ? 'text-blue-700' : 'text-gray-400'">{{ formatPrice(m.total) }}</p>
                <p class="text-xs mt-1" :class="m.total > 0 ? 'text-blue-400' : 'text-gray-300'">{{ m.count }} đơn</p>
              </div>
            </div>
            <div class="flex items-center justify-between bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl px-6 py-4">
              <div>
                <p class="text-sm text-blue-100">Tổng doanh thu năm {{ monthlyYear }}</p>
                <p class="text-3xl font-extrabold mt-0.5">{{ formatPrice(monthlyData.reduce((s,m)=>s+m.total,0)) }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-blue-100">Tổng đơn</p>
                <p class="text-2xl font-bold">{{ monthlyData.reduce((s,m)=>s+m.count,0) }}</p>
              </div>
            </div>
          </div>

          <!-- ===== THEO QUÝ ===== -->
          <div v-if="activeTab === 'quarterly'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
            <h3 class="font-semibold text-gray-800 mb-5 flex items-center gap-2">
              <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"/></svg>
              Theo quý
            </h3>
            <div class="flex items-center gap-3 mb-6">
              <label class="text-xs font-medium text-gray-500">Năm</label>
              <select v-model="quarterlyYear" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400">
                <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
              </select>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <div v-for="q in quarterlyData" :key="q.quarter" class="rounded-2xl border p-5"
                :class="q.total > 0 ? 'border-purple-200 bg-gradient-to-br from-purple-50 to-indigo-50' : 'border-gray-100 bg-gray-50'">
                <div class="flex items-center justify-between mb-3">
                  <span class="text-sm font-bold" :class="q.total > 0 ? 'text-purple-700' : 'text-gray-400'">Quý {{ q.quarter }}</span>
                  <span class="text-xs px-2 py-0.5 rounded-full font-medium" :class="q.total > 0 ? 'bg-purple-100 text-purple-600' : 'bg-gray-100 text-gray-400'">{{ q.label }}</span>
                </div>
                <p class="text-2xl font-extrabold" :class="q.total > 0 ? 'text-purple-800' : 'text-gray-300'">{{ formatPrice(q.total) }}</p>
                <p class="text-xs mt-2" :class="q.total > 0 ? 'text-purple-400' : 'text-gray-300'">{{ q.count }} đơn hoàn thành</p>
                <div v-if="q.total > 0" class="mt-3 pt-3 border-t border-purple-100">
                  <p class="text-xs text-purple-400">Trung bình / đơn</p>
                  <p class="text-sm font-bold text-purple-600">{{ formatPrice(Math.round(q.total / q.count)) }}</p>
                </div>
              </div>
            </div>
            <div class="flex items-center justify-between bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl px-6 py-4">
              <div>
                <p class="text-sm text-purple-100">Tổng doanh thu năm {{ quarterlyYear }}</p>
                <p class="text-3xl font-extrabold mt-0.5">{{ formatPrice(quarterlyData.reduce((s,q)=>s+q.total,0)) }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-purple-100">Tổng đơn</p>
                <p class="text-2xl font-bold">{{ quarterlyData.reduce((s,q)=>s+q.count,0) }}</p>
              </div>
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const user = computed(() => authStore.user)
const userInitials = computed(() => {
  const name = user.value?.full_name || 'C'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

const loading = ref(false)
const allBookings = ref([])
const clinics = ref([])
const selectedClinic = ref('')

const tabs = [
  { key: 'range',     label: 'Khoảng ngày' },
  { key: 'monthly',   label: 'Theo tháng' },
  { key: 'quarterly', label: 'Theo quý' },
]
const activeTab = ref('range')

// Date range — mặc định tháng hiện tại
const now = new Date()
const firstOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
const rangeFrom = ref(firstOfMonth.toISOString().slice(0, 10))
const rangeTo   = ref(now.toISOString().slice(0, 10))

const monthlyYear   = ref(now.getFullYear())
const quarterlyYear = ref(now.getFullYear())

// Chỉ đơn hoàn thành và lọc theo phòng khám (nếu có)
const completed = computed(() => {
  let filtered = allBookings.value.filter(b => b.status === 'completed')
  if (selectedClinic.value) {
    filtered = filtered.filter(b => b.clinic_id === selectedClinic.value)
  }
  return filtered
})

const availableYears = computed(() => {
  const yrs = new Set(completed.value.map(b => new Date(b.scheduled_at).getFullYear()))
  yrs.add(now.getFullYear())
  return [...yrs].sort((a, b) => b - a)
})

const bRevenue = (b) => +(b.total_price || b.package_price || 0)

// Khoảng ngày
const rangeRevenue = computed(() => {
  const from = new Date(rangeFrom.value + 'T00:00:00')
  const to   = new Date(rangeTo.value   + 'T23:59:59')
  const items = completed.value.filter(b => {
    const d = new Date(b.scheduled_at)
    return d >= from && d <= to
  })
  const total = items.reduce((s, b) => s + bRevenue(b), 0)
  return { items, count: items.length, total, avg: items.length ? Math.round(total / items.length) : 0 }
})

// Theo tháng
const monthlyData = computed(() =>
  Array.from({ length: 12 }, (_, i) => {
    const month = i + 1
    const items = completed.value.filter(b => {
      const d = new Date(b.scheduled_at)
      return d.getFullYear() === monthlyYear.value && d.getMonth() + 1 === month
    })
    return { month, count: items.length, total: items.reduce((s, b) => s + bRevenue(b), 0) }
  })
)

// Theo quý
const quarterlyData = computed(() =>
  [
    { quarter: 1, label: 'Th1–3',  range: [1, 3]   },
    { quarter: 2, label: 'Th4–6',  range: [4, 6]   },
    { quarter: 3, label: 'Th7–9',  range: [7, 9]   },
    { quarter: 4, label: 'Th10–12',range: [10, 12] },
  ].map(q => {
    const items = completed.value.filter(b => {
      const d = new Date(b.scheduled_at)
      const m = d.getMonth() + 1
      return d.getFullYear() === quarterlyYear.value && m >= q.range[0] && m <= q.range[1]
    })
    return { ...q, count: items.length, total: items.reduce((s, b) => s + bRevenue(b), 0) }
  })
)

// Helpers
const formatPrice = (v) => {
  if (!v && v !== 0) return '—'
  return new Intl.NumberFormat('vi-VN').format(v) + 'đ'
}
const formatDate = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const refresh = async () => {
  loading.value = true
  try {
    const [bookingsRes, clinicsRes] = await Promise.all([
      api.get('/bookings/clinic/owner/all'),
      api.get('/clinics/owner/my-clinics'),
    ])
    allBookings.value = bookingsRes.data.bookings || []
    clinics.value = clinicsRes.data.clinics || clinicsRes.data || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(refresh)
</script>
