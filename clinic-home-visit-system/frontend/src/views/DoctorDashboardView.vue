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

    <!-- Tab Navigation -->
    <div class="tab-nav-bar">
      <div class="tab-nav-inner">
        <button
          id="tab-schedule"
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'schedule' }"
          @click="activeTab = 'schedule'"
        >
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Lịch làm việc
        </button>
        <button
          id="tab-patients"
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'patients' }"
          @click="activeTab = 'patients'; fetchPatients()"
        >
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Quản lý Bệnh nhân
          <span v-if="patientStats.pending > 0" class="tab-badge">{{ patientStats.pending }}</span>
        </button>
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

      <!-- ===== TAB: SCHEDULE ===== -->
      <template v-if="activeTab === 'schedule'">
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
              <div class="legend-item"><div class="legend-dot status-pending"></div><span>Chờ xác nhận</span></div>
              <div class="legend-item"><div class="legend-dot status-confirmed"></div><span>Đã xác nhận</span></div>
              <div class="legend-item"><div class="legend-dot status-in_progress"></div><span>Đang khám</span></div>
              <div class="legend-item"><div class="legend-dot status-completed"></div><span>Hoàn thành</span></div>
              <div class="legend-item"><div class="legend-dot status-cancelled"></div><span>Huỷ</span></div>
            </div>
          </div>
        </div>
      </template>

      <!-- ===== TAB: PATIENTS ===== -->
      <template v-if="activeTab === 'patients'">
        <div class="patients-card">
          <!-- Patients Header -->
          <div class="patients-header">
            <div class="patients-title-row">
              <h2 class="patients-title">Danh sách Bệnh nhân</h2>
              <div class="patients-meta">Tổng: {{ patientTotal }} lịch hẹn</div>
            </div>
            <!-- Filters -->
            <div class="patients-filters">
              <button
                v-for="f in patientFilters"
                :key="f.value"
                class="filter-pill"
                :class="{ 'filter-active': patientStatusFilter === f.value }"
                @click="patientStatusFilter = f.value; fetchPatients()"
              >
                {{ f.label }}
                <span v-if="f.value === 'pending' && patientStats.pending > 0" class="filter-count">{{ patientStats.pending }}</span>
              </button>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="patientsLoading" class="loading-state">
            <div class="spinner"></div>
            <span>Đang tải danh sách bệnh nhân...</span>
          </div>

          <!-- Empty -->
          <div v-else-if="patients.length === 0" class="patients-empty">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <p>Không có bệnh nhân nào trong danh mục này</p>
          </div>

          <!-- Patient Table -->
          <div v-else class="patients-table-wrapper">
            <table class="patients-table">
              <thead>
                <tr>
                  <th>Mã lịch hẹn</th>
                  <th>Thời gian</th>
                  <th>Hình thức</th>
                  <th>Ghi chú / Địa chỉ</th>
                  <th>Thanh toán</th>
                  <th>Trạng thái</th>
                  <th>Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in patients" :key="b.id" class="patient-row">
                  <td>
                    <span class="booking-id-chip">{{ b.id.slice(0, 8) }}…</span>
                  </td>
                  <td>
                    <div class="patient-datetime">
                      <span class="patient-date">{{ formatFullDatetime(b.scheduled_at).split(' - ')[1] }}</span>
                      <span class="patient-time">{{ formatTime(b.scheduled_at) }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="booking-type-badge" :class="b.booking_type === 'home_visit' ? 'type-home' : 'type-clinic'">
                      {{ b.booking_type === 'home_visit' ? '🏠 Tại nhà' : '🏥 Phòng khám' }}
                    </span>
                  </td>
                  <td class="patient-notes">
                    <span v-if="b.home_address" class="note-text">📍 {{ b.home_address }}</span>
                    <span v-else-if="b.notes" class="note-text">💬 {{ b.notes }}</span>
                    <span v-else class="note-none">—</span>
                  </td>
                  <td>
                    <span class="payment-chip">
                      {{ b.payment_method === 'cash' ? '💵 Tiền mặt' : '🏦 Chuyển khoản' }}
                    </span>
                  </td>
                  <td>
                    <span class="booking-status-pill" :class="getStatusClass(b.status)">
                      {{ getStatusLabel(b.status) }}
                    </span>
                  </td>
                  <td>
                    <div class="action-btns">
                      <button
                        v-if="b.status === 'pending'"
                        class="action-btn btn-confirm"
                        :disabled="updatingId === b.id"
                        @click="updatePatientStatus(b, 'confirmed')"
                        title="Xác nhận"
                      >
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                        Xác nhận
                      </button>
                      <button
                        v-if="b.status === 'confirmed'"
                        class="action-btn btn-start"
                        :disabled="updatingId === b.id"
                        @click="updatePatientStatus(b, 'in_progress')"
                        title="Bắt đầu khám"
                      >
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        Bắt đầu
                      </button>
                      <button
                        v-if="b.status === 'in_progress'"
                        class="action-btn btn-complete"
                        :disabled="updatingId === b.id"
                        @click="updatePatientStatus(b, 'completed')"
                        title="Hoàn thành"
                      >
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        Hoàn thành
                      </button>
                      <span v-if="updatingId === b.id" class="updating-spinner"></span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="patientTotalPages > 1" class="patients-pagination">
            <button class="page-btn" :disabled="patientPage === 1" @click="patientPage--; fetchPatients()">← Trước</button>
            <span class="page-info">Trang {{ patientPage }} / {{ patientTotalPages }}</span>
            <button class="page-btn" :disabled="patientPage === patientTotalPages" @click="patientPage++; fetchPatients()">Sau →</button>
          </div>
        </div>
      </template>
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

// Active Tab
const activeTab = ref('schedule')

// State
const loading = ref(false)
const error = ref(null)
const weekDays = ref([])
const selectedBooking = ref(null)

// ===== Patient Management State =====
const patients = ref([])
const patientsLoading = ref(false)
const patientTotal = ref(0)
const patientPage = ref(1)
const patientPageSize = 10
const patientStatusFilter = ref('')
const updatingId = ref(null)

const patientTotalPages = computed(() => Math.ceil(patientTotal.value / patientPageSize))

const patientFilters = [
  { label: 'Tất cả', value: '' },
  { label: 'Chờ xác nhận', value: 'pending' },
  { label: 'Đã xác nhận', value: 'confirmed' },
  { label: 'Đang khám', value: 'in_progress' },
  { label: 'Hoàn thành', value: 'completed' },
  { label: 'Đã huỷ', value: 'cancelled' },
]

const patientStats = computed(() => ({
  pending: patients.value.filter(b => b.status === 'pending').length,
}))

async function fetchPatients() {
  patientsLoading.value = true
  try {
    const doctorId = authStore.user?.doctor_id || authStore.user?.id
    const params = { page: patientPage.value, page_size: patientPageSize }
    if (patientStatusFilter.value) params.status = patientStatusFilter.value
    const res = await api.get(`/bookings/doctor/${doctorId}/all`, { params })
    patients.value = res.data.bookings || []
    patientTotal.value = res.data.total || 0
  } catch (e) {
    patients.value = []
    patientTotal.value = 0
  } finally {
    patientsLoading.value = false
  }
}

async function updatePatientStatus(booking, newStatus) {
  updatingId.value = booking.id
  try {
    await api.put(`/bookings/${booking.id}/status`, { status: newStatus })
    booking.status = newStatus
    if (newStatus === 'completed') booking.completed_at = new Date().toISOString()
    if (newStatus === 'confirmed') booking.confirmed_at = new Date().toISOString()
  } catch (e) {
    alert(e.response?.data?.detail || 'Cập nhật trạng thái thất bại')
  } finally {
    updatingId.value = null
  }
}

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

/* ========== Tab Nav ========== */
.tab-nav-bar {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 10;
}

.tab-nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  gap: 4px;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
  position: relative;
}

.tab-btn svg { width: 18px; height: 18px; }

.tab-btn:hover { color: #4338ca; background: #f5f3ff; border-radius: 8px 8px 0 0; }

.tab-active {
  color: #4338ca;
  border-bottom-color: #4338ca;
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #ef4444;
  color: white;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  animation: pulse-badge 1.5s infinite;
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* ========== Patients Card ========== */
.patients-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  border: 1px solid rgba(255,255,255,0.8);
  overflow: hidden;
}

.patients-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.patients-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.patients-title {
  font-size: 18px;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.patients-meta {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.patients-filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-pill:hover { border-color: #4338ca; color: #4338ca; }

.filter-active {
  background: linear-gradient(135deg, #4338ca, #7c3aed);
  border-color: transparent;
  color: white;
}

.filter-count {
  background: rgba(255,255,255,0.3);
  border-radius: 10px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: 700;
}

.filter-active .filter-count { background: rgba(255,255,255,0.3); }

/* Table */
.patients-table-wrapper {
  overflow-x: auto;
}

.patients-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.patients-table thead tr {
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

.patients-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.patient-row {
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.15s;
}

.patient-row:hover { background: #f9fafb; }
.patient-row:last-child { border-bottom: none; }

.patients-table td {
  padding: 14px 16px;
  vertical-align: middle;
}

.booking-id-chip {
  font-family: monospace;
  font-size: 12px;
  background: #f3f4f6;
  padding: 3px 8px;
  border-radius: 6px;
  color: #374151;
}

.patient-datetime {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.patient-date {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.patient-time {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
}

.patient-notes { max-width: 200px; }

.note-text {
  font-size: 12px;
  color: #374151;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  max-width: 180px;
}

.note-none { color: #d1d5db; font-size: 12px; }

.payment-chip {
  font-size: 12px;
  font-weight: 500;
  color: #374151;
}

/* Action Buttons */
.action-btns {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: none;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.action-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.action-btn svg { width: 14px; height: 14px; }

.btn-confirm { background: #ecfdf5; color: #065f46; }
.btn-confirm:hover:not(:disabled) { background: #6ee7b7; }

.btn-start { background: #eff6ff; color: #1e40af; }
.btn-start:hover:not(:disabled) { background: #93c5fd; }

.btn-complete { background: #f0fdf4; color: #14532d; }
.btn-complete:hover:not(:disabled) { background: #86efac; }

.updating-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top-color: #4338ca;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

/* Empty State */
.patients-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  gap: 12px;
  color: #9ca3af;
}

.patients-empty svg { width: 56px; height: 56px; }
.patients-empty p { font-size: 14px; font-weight: 500; }

/* Pagination */
.patients-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 16px 24px;
  border-top: 1px solid #f3f4f6;
}

.page-btn {
  padding: 8px 18px;
  background: #f3f4f6;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) { background: #4338ca; color: white; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.page-info {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
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
