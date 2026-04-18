<template>
  <div class="doctor-dashboard">
    <!-- Page Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <div class="doctor-avatar">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <div>
            <h1 class="header-title">Lịch làm việc</h1>
            <p class="header-subtitle">Xin chào, <span class="doctor-name">{{ authStore.user?.full_name || 'Bác sĩ' }}</span> 👋</p>
          </div>
        </div>
        <div class="header-right">
          <div class="today-badge">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{{ formatDate(new Date()) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-body">
      <!-- Stats Row -->
      <div class="stats-row">
        <div class="stat-card stat-total">
          <div class="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-number">{{ weekStats.total }}</span>
            <span class="stat-label">Tổng lịch hẹn tuần này</span>
          </div>
        </div>
        <div class="stat-card stat-confirmed">
          <div class="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-number">{{ weekStats.confirmed }}</span>
            <span class="stat-label">Đã xác nhận</span>
          </div>
        </div>
        <div class="stat-card stat-pending">
          <div class="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-number">{{ weekStats.pending }}</span>
            <span class="stat-label">Chờ xác nhận</span>
          </div>
        </div>
        <div class="stat-card stat-completed">
          <div class="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-number">{{ weekStats.completed }}</span>
            <span class="stat-label">Đã hoàn thành</span>
          </div>
        </div>
      </div>

      <!-- Week Navigation + Calendar -->
      <div class="calendar-card">
        <!-- Week Nav -->
        <div class="week-nav">
          <button class="week-btn" @click="prevWeek">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Tuần trước
          </button>
          <div class="week-label">
            <span class="week-range">{{ weekRangeLabel }}</span>
            <button v-if="!isCurrentWeek" class="today-btn" @click="goToCurrentWeek">
              Tuần này
            </button>
          </div>
          <button class="week-btn" @click="nextWeek">
            Tuần sau
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <span>Đang tải lịch làm việc...</span>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="error-state">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <p>{{ error }}</p>
          <button @click="fetchWeeklySchedule" class="retry-btn">Thử lại</button>
        </div>

        <!-- Weekly Grid -->
        <div v-else class="weekly-grid">
          <div
            v-for="day in weekDays"
            :key="day.date"
            class="day-column"
            :class="{
              'day-today': isToday(day.date),
              'day-weekend': day.weekday >= 5,
            }"
          >
            <!-- Day Header -->
            <div class="day-header" :class="{ 'day-header-today': isToday(day.date) }">
              <span class="day-name">{{ getDayName(day.weekday) }}</span>
              <span class="day-date" :class="{ 'day-date-today': isToday(day.date) }">
                {{ formatDayDate(day.date) }}
              </span>
              <span v-if="day.bookings.length" class="booking-count-badge">{{ day.bookings.length }}</span>
            </div>

            <!-- Bookings or Empty -->
            <div class="day-slots">
              <div v-if="day.bookings.length === 0" class="empty-day">
                <div class="empty-dot"></div>
                <span>Không có lịch</span>
              </div>

              <div
                v-for="booking in day.bookings"
                :key="booking.id"
                class="booking-slot"
                :class="getStatusClass(booking.status)"
                @click="openBookingDetail(booking)"
              >
                <div class="booking-time">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ formatTime(booking.scheduled_at) }}
                </div>
                <div class="booking-duration">{{ booking.duration_minutes }} phút</div>
                <div class="booking-type-badge" :class="booking.booking_type === 'home_visit' ? 'type-home' : 'type-clinic'">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="booking.booking_type === 'home_visit'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  {{ booking.booking_type === 'home_visit' ? 'Tại nhà' : 'Tại phòng khám' }}
                </div>
                <div class="booking-status-pill" :class="getStatusClass(booking.status)">
                  {{ getStatusLabel(booking.status) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Legend -->
        <div class="legend">
          <span class="legend-title">Chú thích trạng thái:</span>
          <div class="legend-items">
            <div class="legend-item">
              <div class="legend-dot status-pending"></div>
              <span>Chờ xác nhận</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot status-confirmed"></div>
              <span>Đã xác nhận</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot status-in_progress"></div>
              <span>Đang khám</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot status-completed"></div>
              <span>Hoàn thành</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot status-cancelled"></div>
              <span>Huỷ</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Detail Modal -->
    <div v-if="selectedBooking" class="modal-overlay" @click.self="selectedBooking = null">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Chi tiết lịch hẹn</h3>
          <button class="modal-close" @click="selectedBooking = null">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">Mã lịch hẹn</span>
            <span class="detail-value mono">{{ selectedBooking.id?.slice(0, 8) }}...</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Thời gian</span>
            <span class="detail-value">{{ formatFullDatetime(selectedBooking.scheduled_at) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Thời lượng</span>
            <span class="detail-value">{{ selectedBooking.duration_minutes }} phút</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Loại khám</span>
            <span class="detail-value">
              <span class="booking-type-badge" :class="selectedBooking.booking_type === 'home_visit' ? 'type-home' : 'type-clinic'">
                {{ selectedBooking.booking_type === 'home_visit' ? '🏠 Tại nhà' : '🏥 Tại phòng khám' }}
              </span>
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Trạng thái</span>
            <span class="booking-status-pill" :class="getStatusClass(selectedBooking.status)">
              {{ getStatusLabel(selectedBooking.status) }}
            </span>
          </div>
          <div v-if="selectedBooking.home_address" class="detail-row">
            <span class="detail-label">Địa chỉ</span>
            <span class="detail-value">{{ selectedBooking.home_address }}</span>
          </div>
          <div v-if="selectedBooking.notes" class="detail-row">
            <span class="detail-label">Ghi chú</span>
            <span class="detail-value">{{ selectedBooking.notes }}</span>
          </div>
          <div v-if="selectedBooking.payment_method" class="detail-row">
            <span class="detail-label">Thanh toán</span>
            <span class="detail-value">{{ selectedBooking.payment_method === 'cash' ? 'Tiền mặt' : 'Chuyển khoản' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()

// State
const loading = ref(false)
const error = ref(null)
const weekDays = ref([])
const selectedBooking = ref(null)

// Current week Monday
const currentWeekStart = ref(getThisMonday())

function getThisMonday() {
  const today = new Date()
  const day = today.getDay() // 0=Sun, 1=Mon ...
  const diff = (day === 0) ? -6 : 1 - day
  const monday = new Date(today)
  monday.setDate(today.getDate() + diff)
  monday.setHours(0, 0, 0, 0)
  return monday
}

function toISODate(d) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

// Week range label
const weekRangeLabel = computed(() => {
  const end = new Date(currentWeekStart.value)
  end.setDate(end.getDate() + 6)
  return `${formatDate(currentWeekStart.value)} – ${formatDate(end)}`
})

const isCurrentWeek = computed(() => {
  const thisMonday = getThisMonday()
  return toISODate(currentWeekStart.value) === toISODate(thisMonday)
})

// Stats
const weekStats = computed(() => {
  const all = weekDays.value.flatMap(d => d.bookings || [])
  return {
    total: all.length,
    confirmed: all.filter(b => b.status === 'confirmed').length,
    pending: all.filter(b => b.status === 'pending').length,
    completed: all.filter(b => b.status === 'completed').length,
  }
})

// Navigation
function prevWeek() {
  const d = new Date(currentWeekStart.value)
  d.setDate(d.getDate() - 7)
  currentWeekStart.value = d
}

function nextWeek() {
  const d = new Date(currentWeekStart.value)
  d.setDate(d.getDate() + 7)
  currentWeekStart.value = d
}

function goToCurrentWeek() {
  currentWeekStart.value = getThisMonday()
}

// Fetch
async function fetchWeeklySchedule() {
  loading.value = true
  error.value = null
  try {
    const params = { week_start: toISODate(currentWeekStart.value) }
    const res = await api.get('/bookings/doctor/me/weekly', { params })
    weekDays.value = res.data.days || []
  } catch (e) {
    // Fallback: build empty 7-day grid when API fails (e.g. doctor_id not linked yet)
    error.value = e.response?.data?.detail || 'Không thể tải lịch làm việc. Vui lòng thử lại.'
    weekDays.value = buildEmptyWeek()
  } finally {
    loading.value = false
  }
}

function buildEmptyWeek() {
  const days = []
  for (let i = 0; i < 7; i++) {
    const d = new Date(currentWeekStart.value)
    d.setDate(d.getDate() + i)
    days.push({ date: toISODate(d), weekday: d.getDay() === 0 ? 6 : d.getDay() - 1, bookings: [] })
  }
  return days
}

// Helpers
function isToday(dateStr) {
  return dateStr === toISODate(new Date())
}

function getDayName(weekday) {
  const names = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
  return names[weekday] || ''
}

function formatDayDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00')
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`
}

function formatDate(d) {
  if (typeof d === 'string') d = new Date(d + 'T00:00:00')
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`
}

function formatTime(dateStr) {
  const d = new Date(dateStr)
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function formatFullDatetime(dateStr) {
  const d = new Date(dateStr)
  return `${formatTime(dateStr)} - ${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`
}

function getStatusClass(status) {
  const map = {
    pending: 'status-pending',
    confirmed: 'status-confirmed',
    in_progress: 'status-in_progress',
    completed: 'status-completed',
    cancelled: 'status-cancelled',
    expired: 'status-expired',
  }
  return map[status] || 'status-pending'
}

function getStatusLabel(status) {
  const map = {
    pending: 'Chờ xác nhận',
    confirmed: 'Đã xác nhận',
    in_progress: 'Đang khám',
    completed: 'Hoàn thành',
    cancelled: 'Đã huỷ',
    expired: 'Hết hạn',
  }
  return map[status] || status
}

function openBookingDetail(booking) {
  selectedBooking.value = booking
}

// Watch week changes
watch(currentWeekStart, () => fetchWeeklySchedule())

onMounted(() => fetchWeeklySchedule())
</script>

<style scoped>
/* ========== Layout ========== */
.doctor-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0fdf4 100%);
}

/* ========== Header ========== */
.dashboard-header {
  background: linear-gradient(135deg, #1e40af 0%, #4338ca 50%, #7c3aed 100%);
  padding: 32px 0 24px;
  box-shadow: 0 8px 32px rgba(67, 56, 202, 0.3);
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.doctor-avatar {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(8px);
}

.doctor-avatar svg {
  width: 28px;
  height: 28px;
  color: white;
}

.header-title {
  font-size: 24px;
  font-weight: 800;
  color: white;
  margin: 0;
  letter-spacing: -0.5px;
}

.header-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin: 4px 0 0;
}

.doctor-name {
  font-weight: 600;
  color: #a5f3fc;
}

.today-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  padding: 8px 16px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  backdrop-filter: blur(8px);
}

.today-badge svg {
  width: 16px;
  height: 16px;
}

/* ========== Body ========== */
.dashboard-body {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========== Stats ========== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

@media (max-width: 900px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
  .stats-row { grid-template-columns: 1fr; }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg { width: 24px; height: 24px; }

.stat-total .stat-icon { background: #eff6ff; color: #3b82f6; }
.stat-confirmed .stat-icon { background: #ecfdf5; color: #10b981; }
.stat-pending .stat-icon { background: #fffbeb; color: #f59e0b; }
.stat-completed .stat-icon { background: #f0fdf4; color: #22c55e; }

.stat-info { display: flex; flex-direction: column; gap: 2px; }
.stat-number { font-size: 28px; font-weight: 800; color: #111827; line-height: 1; }
.stat-label { font-size: 12px; color: #6b7280; font-weight: 500; }

/* ========== Calendar Card ========== */
.calendar-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  overflow: hidden;
}

/* Week Nav */
.week-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
  background: linear-gradient(to right, #fafafa, #ffffff);
}

.week-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #f3f4f6;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.week-btn:hover { background: #e5e7eb; transform: translateX(-2px); }
.week-btn:last-child:hover { transform: translateX(2px); }

.week-btn svg { width: 16px; height: 16px; }

.week-label {
  display: flex;
  align-items: center;
  gap: 12px;
}

.week-range {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.today-btn {
  padding: 4px 12px;
  background: linear-gradient(135deg, #4338ca, #7c3aed);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.today-btn:hover { opacity: 0.85; }

/* Loading / Error */
.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  gap: 12px;
  color: #6b7280;
}

.error-state svg { width: 40px; height: 40px; color: #f59e0b; }
.error-state p { font-size: 14px; }

.retry-btn {
  padding: 8px 20px;
  background: #4338ca;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e5e7eb;
  border-top-color: #4338ca;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Weekly Grid */
.weekly-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  min-height: 400px;
}

@media (max-width: 900px) {
  .weekly-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 560px) {
  .weekly-grid { grid-template-columns: repeat(2, 1fr); }
}

.day-column {
  border-right: 1px solid #f3f4f6;
  display: flex;
  flex-direction: column;
  transition: background 0.2s;
}

.day-column:last-child { border-right: none; }
.day-weekend { background: #fafafa; }
.day-today { background: linear-gradient(to bottom, #eff6ff, #fafbff); }

/* Day Header */
.day-header {
  padding: 14px 10px 10px;
  text-align: center;
  border-bottom: 2px solid #f3f4f6;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.day-header-today {
  border-bottom-color: #4338ca;
  background: linear-gradient(to bottom, #eff6ff, rgba(239, 246, 255, 0));
}

.day-name {
  font-size: 11px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.day-date {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
}

.day-date-today {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #4338ca, #7c3aed);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.booking-count-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 18px;
  height: 18px;
  background: #4338ca;
  color: white;
  border-radius: 50%;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Day Slots */
.day-slots {
  flex: 1;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.empty-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 20px 8px;
  color: #d1d5db;
  font-size: 11px;
  font-weight: 500;
}

.empty-dot {
  width: 8px;
  height: 8px;
  background: #e5e7eb;
  border-radius: 50%;
}

/* Booking Slot */
.booking-slot {
  border-radius: 10px;
  padding: 8px 10px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 5px;
  border-left: 3px solid transparent;
  transition: transform 0.15s, box-shadow 0.15s;
}

.booking-slot:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.booking-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 700;
}

.booking-time svg { width: 12px; height: 12px; flex-shrink: 0; }

.booking-duration {
  font-size: 10px;
  opacity: 0.7;
  font-weight: 500;
}

.booking-type-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 6px;
  width: fit-content;
}

.booking-type-badge svg { width: 10px; height: 10px; }

.type-home { background: #fef3c7; color: #92400e; }
.type-clinic { background: #dbeafe; color: #1e40af; }

.booking-status-pill {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 20px;
  width: fit-content;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

/* Status Colors */
.status-pending {
  background: #fffbeb;
  color: #92400e;
  border-left-color: #f59e0b;
}

.status-confirmed {
  background: #ecfdf5;
  color: #065f46;
  border-left-color: #10b981;
}

.status-in_progress {
  background: #eff6ff;
  color: #1e40af;
  border-left-color: #3b82f6;
}

.status-completed {
  background: #f0fdf4;
  color: #14532d;
  border-left-color: #22c55e;
}

.status-cancelled {
  background: #fef2f2;
  color: #991b1b;
  border-left-color: #ef4444;
  opacity: 0.7;
}

.status-expired {
  background: #f9fafb;
  color: #6b7280;
  border-left-color: #9ca3af;
  opacity: 0.6;
}

/* Legend */
.legend {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  border-top: 1px solid #f3f4f6;
  background: #fafafa;
  flex-wrap: wrap;
}

.legend-title {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
}

.legend-items {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #374151;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-dot.status-pending { background: #f59e0b; }
.legend-dot.status-confirmed { background: #10b981; }
.legend-dot.status-in_progress { background: #3b82f6; }
.legend-dot.status-completed { background: #22c55e; }
.legend-dot.status-cancelled { background: #ef4444; }

/* ========== Modal ========== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 24px;
}

.modal-card {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  animation: modal-in 0.2s ease-out;
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #4338ca, #7c3aed);
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: white;
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.modal-close:hover { background: rgba(255, 255, 255, 0.3); }
.modal-close svg { width: 16px; height: 16px; }

.modal-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid #f3f4f6;
}

.detail-row:last-child { border-bottom: none; padding-bottom: 0; }

.detail-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  flex-shrink: 0;
}

.detail-value {
  font-size: 13px;
  color: #111827;
  font-weight: 600;
  text-align: right;
}

.mono { font-family: monospace; font-size: 12px; }
</style>
