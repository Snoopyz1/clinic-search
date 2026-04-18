<template>
  <div class="px-4 py-8 bg-gray-50 min-h-[calc(100vh-64px)]">
    <main class="max-w-4xl mx-auto">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-2xl font-extrabold text-gray-900 tracking-tight">Lịch hẹn của tôi</h1>
        <router-link to="/clinics" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors duration-150 flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          Đặt lịch mới
        </router-link>
      </div>

      <div v-if="loading" class="flex flex-col items-center justify-center py-16 space-y-4">
        <div class="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
        <p class="text-gray-500 font-medium">Đang tải lịch hẹn...</p>
      </div>

      <div v-else-if="bookings.length === 0" class="text-center py-20 bg-white rounded-2xl shadow-sm border border-gray-100">
        <div class="w-20 h-20 mx-auto bg-gray-50 rounded-full flex items-center justify-center mb-4">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-1">Chưa có lịch hẹn nào</h3>
        <p class="text-gray-500 mb-6 max-w-sm mx-auto">Bạn chưa đặt lịch hẹn nào. Hãy tìm phòng khám phù hợp và đặt lịch khám ngay.</p>
        <router-link to="/clinics" class="inline-flex items-center justify-center px-6 py-2.5 bg-indigo-50 text-indigo-700 font-medium rounded-lg hover:bg-indigo-100 transition-colors">
          Bắt đầu tìm kiếm
        </router-link>
      </div>

      <div v-else class="space-y-4">
        <div v-for="booking in bookings" :key="booking.id" 
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow duration-200 cursor-pointer overflow-hidden relative"
          @click="openDetail(booking)"
        >
          <!-- Left accent line based on status -->
          <div class="absolute left-0 top-0 bottom-0 w-1" :class="getStatusAccent(booking.status)"></div>
          
          <div class="flex flex-col sm:flex-row justify-between gap-4">
            <!-- Left Info -->
            <div class="flex items-start gap-4">
              <div class="hidden sm:flex w-12 h-12 bg-indigo-50 rounded-lg items-center justify-center flex-shrink-0 text-indigo-600">
                <svg v-if="booking.booking_type === 'home_visit'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
                <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
              </div>
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <h3 class="text-lg font-bold text-gray-900 group-hover:text-indigo-600 transition-colors">
                    {{ clinicNames[booking.clinic_id] || 'Phòng khám ' + booking.clinic_id.slice(0, 8) }}
                  </h3>
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" :class="booking.booking_type === 'home_visit' ? 'bg-amber-50 text-amber-700 border border-amber-200' : 'bg-blue-50 text-blue-700 border border-blue-200'">
                    {{ booking.booking_type === 'home_visit' ? 'Khám tại nhà' : 'Tại phòng khám' }}
                  </span>
                </div>
                
                <div class="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                  <div class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                    <span class="font-medium text-gray-900">{{ formatDate(booking.scheduled_at) }}</span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    <span class="font-medium text-gray-900">{{ formatTime(booking.scheduled_at) }}</span> <span class="text-gray-400">({{ booking.duration_minutes }} phút)</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Status -->
            <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center border-t sm:border-t-0 border-gray-100 pt-3 sm:pt-0 mt-3 sm:mt-0">
              <span :class="statusClass(booking.status)" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm border">
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="statusDot(booking.status)"></span>
                {{ statusLabel(booking.status) }}
              </span>
              <p class="text-xs text-gray-400 mt-2 hidden sm:block">Mã LH: {{ booking.id.slice(0, 8).toUpperCase() }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Optional: Add a simple detail modal here if you want in the future -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const bookings = ref([])
const clinicNames = ref({})
const loading = ref(false)

const formatDateTime = (isoString) => {
  const d = new Date(isoString);
  return d.toLocaleString('vi-VN', {
    hour: '2-digit', minute:'2-digit',
    day: '2-digit', month: '2-digit', year: 'numeric'
  });
}

const formatDate = (isoString) => {
  const d = new Date(isoString);
  return d.toLocaleDateString('vi-VN', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' });
}

const formatTime = (isoString) => {
  const d = new Date(isoString);
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute:'2-digit' });
}

const statusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    confirmed: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    in_progress: 'bg-sky-50 text-sky-700 border-sky-200',
    completed: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    cancelled: 'bg-red-50 text-red-700 border-red-200',
    expired: 'bg-gray-50 text-gray-600 border-gray-200',
  }
  return classes[status] || 'bg-gray-50 text-gray-700 border-gray-200'
}

const statusDot = (status) => {
  const classes = {
    pending: 'bg-yellow-500',
    confirmed: 'bg-emerald-500',
    in_progress: 'bg-sky-500',
    completed: 'bg-indigo-500',
    cancelled: 'bg-red-500',
    expired: 'bg-gray-400',
  }
  return classes[status] || 'bg-gray-400'
}

const getStatusAccent = (status) => {
  const classes = {
    pending: 'bg-yellow-400',
    confirmed: 'bg-emerald-500',
    in_progress: 'bg-sky-500',
    completed: 'bg-indigo-500',
    cancelled: 'bg-red-500',
    expired: 'bg-gray-300',
  }
  return classes[status] || 'bg-transparent'
}

const statusLabel = (status) => {
  const labels = {
    pending: 'Chờ xác nhận',
    confirmed: 'Đã xác nhận',
    in_progress: 'Đang khám',
    completed: 'Hoàn thành',
    cancelled: 'Đã huỷ',
    expired: 'Hết hạn',
  }
  return labels[status] || status
}

const fetchBookings = async () => {
  loading.value = true
  try {
    const response = await api.get('/bookings')
    bookings.value = response.data.bookings || []
    
    // Fetch distinct clinic names
    const cIds = [...new Set(bookings.value.map(b => b.clinic_id))]
    for(const cid of cIds) {
      if(!clinicNames.value[cid]) {
        fetchClinicName(cid)
      }
    }
  } catch (error) {
    console.error('Error fetching bookings:', error)
  } finally {
    loading.value = false
  }
}

const fetchClinicName = async (id) => {
  try {
    const res = await api.get(`/clinics/${id}`)
    clinicNames.value[id] = res.data.name
  } catch (e) {
    clinicNames.value[id] = 'Phòng khám ẩn danh'
  }
}

const openDetail = (booking) => {
  // Can be expanded to show full modal
  console.log("View booking detail", booking)
}

onMounted(() => {
  fetchBookings()
})
</script>
