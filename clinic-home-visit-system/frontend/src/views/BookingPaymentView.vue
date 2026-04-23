<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center p-4">
    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center gap-4 py-20">
      <div class="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      <p class="text-gray-500 font-medium">Đang tải thông tin đặt lịch...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center max-w-md bg-white rounded-2xl shadow-lg p-8 border border-red-100">
      <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
      </div>
      <h2 class="text-lg font-bold text-gray-900 mb-2">Không tìm thấy đơn đặt</h2>
      <p class="text-gray-500 text-sm mb-6">{{ error }}</p>
      <router-link to="/bookings" class="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-medium hover:bg-indigo-700 transition-colors">
        Quay lại lịch hẹn
      </router-link>
    </div>

    <!-- Paid already -->
    <div v-else-if="booking && booking.status !== 'awaiting_payment'" class="text-center max-w-md bg-white rounded-2xl shadow-lg p-8 border border-emerald-100">
      <div class="w-16 h-16 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-9 h-9 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <h2 class="text-lg font-bold text-gray-900 mb-1">Đặt cọc đã được xác nhận!</h2>
      <p class="text-gray-500 text-sm mb-6">Lịch khám của bạn đang ở trạng thái <span class="font-semibold text-indigo-600">{{ statusLabel(booking.status) }}</span>.</p>
      <router-link to="/bookings" class="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-medium hover:bg-indigo-700 transition-colors">
        Xem lịch hẹn
      </router-link>
    </div>

    <!-- Main Booking Ticket -->
    <div v-else-if="booking" class="w-full max-w-lg">
      <!-- Header -->
      <div class="text-center mb-6">
        <div class="inline-flex items-center gap-2 bg-indigo-100 text-indigo-700 px-4 py-1.5 rounded-full text-sm font-semibold mb-3">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
          Xác nhận đặt lịch & Thanh toán
        </div>
        <h1 class="text-2xl font-extrabold text-gray-900">Đặt cọc 50%</h1>
        <p class="text-gray-500 text-sm mt-1">Vui lòng chuyển khoản đặt cọc để xác nhận lịch khám</p>
      </div>

      <!-- Ticket Card -->
      <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
        <!-- Top gradient bar -->
        <div class="h-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>

        <!-- Booking Info -->
        <div class="p-6 space-y-4">
          <!-- Clinic & Doctor -->
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-indigo-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <div>
              <p class="text-xs text-gray-400 font-medium uppercase tracking-wider">Phòng khám</p>
              <h3 class="text-base font-bold text-gray-900 mt-0.5">{{ clinicName || 'Đang tải...' }}</h3>
              <p class="text-sm text-gray-500 mt-0.5">BS. {{ doctorName || 'Đang tải...' }}</p>
            </div>
          </div>

          <!-- Divider with dots -->
          <div class="relative flex items-center">
            <div class="flex-1 border-t border-dashed border-gray-200"></div>
            <div class="mx-3 flex gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
              <span class="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
              <span class="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
            </div>
            <div class="flex-1 border-t border-dashed border-gray-200"></div>
          </div>

          <!-- Grid Info -->
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-gray-50 rounded-xl p-3">
              <p class="text-xs text-gray-400 mb-1 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                Ngày khám
              </p>
              <p class="text-sm font-semibold text-gray-900">{{ formatDate(booking.scheduled_at) }}</p>
            </div>
            <div class="bg-gray-50 rounded-xl p-3">
              <p class="text-xs text-gray-400 mb-1 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Giờ khám
              </p>
              <p class="text-sm font-semibold text-gray-900">{{ formatTime(booking.scheduled_at) }}</p>
            </div>
            <div class="bg-gray-50 rounded-xl p-3">
              <p class="text-xs text-gray-400 mb-1 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                </svg>
                Hình thức
              </p>
              <p class="text-sm font-semibold text-gray-900">
                {{ booking.booking_type === 'home_visit' ? 'Khám tại nhà' : 'Tại phòng khám' }}
              </p>
            </div>
            <div class="bg-indigo-50 rounded-xl p-3 border border-indigo-100">
              <p class="text-xs text-indigo-400 mb-1 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                Gói khám
              </p>
              <p class="text-sm font-semibold text-indigo-800">{{ booking.package_name || '—' }}</p>
            </div>
          </div>

          <!-- Divider with tear effect -->
          <div class="relative -mx-6 flex items-center">
            <div class="absolute -left-3 w-6 h-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-full border border-gray-100"></div>
            <div class="flex-1 border-t border-dashed border-gray-200 mx-3"></div>
            <div class="absolute -right-3 w-6 h-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-full border border-gray-100"></div>
          </div>

          <!-- Price Summary -->
          <div class="space-y-2 pt-1">
            <div class="flex justify-between items-center text-sm">
              <span class="text-gray-500">Giá gói khám</span>
              <span class="font-semibold text-gray-800">{{ formatPrice(booking.package_price) }}</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="text-gray-500">Số tiền đặt cọc (50%)</span>
              <span class="font-bold text-lg text-indigo-700">{{ formatPrice(booking.deposit_amount) }}</span>
            </div>
            <div class="flex justify-between items-center text-xs text-gray-400">
              <span>Thanh toán phần còn lại khi khám</span>
              <span>{{ formatPrice((booking.package_price || 0) - (booking.deposit_amount || 0)) }}</span>
            </div>
          </div>
        </div>

        <!-- QR Section -->
        <div class="bg-gradient-to-br from-indigo-600 to-purple-700 p-6 text-white">
          <div class="flex items-center gap-2 mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/>
            </svg>
            <span class="font-bold text-base">Quét mã QR để đặt cọc</span>
          </div>

          <div class="flex gap-5 items-center">
            <!-- QR Code (generated from QR API) -->
            <div class="bg-white p-2 rounded-2xl shadow-lg flex-shrink-0">
              <img
                :src="qrCodeUrl"
                alt="QR Code thanh toán"
                class="w-32 h-32 rounded-lg"
              />
            </div>

            <!-- Bank Info -->
            <div class="flex-1 space-y-2.5">
              <div>
                <p class="text-white/60 text-xs uppercase tracking-wide">Ngân hàng</p>
                <p class="font-bold text-sm">MB Bank (MBBank)</p>
              </div>
              <div>
                <p class="text-white/60 text-xs uppercase tracking-wide">Số tài khoản</p>
                <p class="font-bold text-sm font-mono">0123456789</p>
              </div>
              <div>
                <p class="text-white/60 text-xs uppercase tracking-wide">Chủ tài khoản</p>
                <p class="font-bold text-sm">CLINIC HOME VISIT</p>
              </div>
              <div>
                <p class="text-white/60 text-xs uppercase tracking-wide">Số tiền</p>
                <p class="font-extrabold text-lg text-yellow-300">{{ formatPrice(booking.deposit_amount) }}</p>
              </div>
              <div>
                <p class="text-white/60 text-xs uppercase tracking-wide">Nội dung</p>
                <p class="font-bold text-xs font-mono bg-white/10 rounded-lg px-2 py-1 mt-0.5">DAT COC {{ booking.id.slice(0, 8).toUpperCase() }}</p>
              </div>
            </div>
          </div>

          <!-- Refund policy -->
          <div class="mt-4 bg-white/10 rounded-xl p-3 text-xs text-white/80 flex items-start gap-2">
            <svg class="w-4 h-4 text-yellow-300 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>Hoàn trả <strong class="text-white">100%</strong> tiền cọc nếu bạn hủy lịch trước <strong class="text-white">3 ngày</strong> so với giờ hẹn.</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="p-5 bg-white space-y-3">
          <!-- Error -->
          <div v-if="confirmError" class="bg-red-50 border border-red-100 text-red-600 px-4 py-3 rounded-xl text-sm flex items-center gap-2">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            {{ confirmError }}
          </div>

          <!-- Success -->
          <div v-if="confirmSuccess" class="bg-emerald-50 border border-emerald-100 text-emerald-700 px-4 py-3 rounded-xl text-sm flex items-center gap-2">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            {{ confirmSuccess }}
          </div>

          <button
            id="confirm-payment-btn"
            @click="confirmPayment"
            :disabled="confirmLoading || !!confirmSuccess"
            class="w-full py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-2xl font-bold text-sm hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-indigo-200"
          >
            <span v-if="confirmLoading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ confirmLoading ? 'Đang xác nhận...' : (confirmSuccess ? 'Đã xác nhận ✓' : 'Tôi đã chuyển khoản xong') }}
          </button>

          <router-link
            to="/bookings"
            class="block text-center w-full py-3 border border-gray-200 text-gray-600 rounded-2xl font-medium text-sm hover:bg-gray-50 transition-colors"
          >
            Quay lại lịch hẹn
          </router-link>

          <p class="text-center text-xs text-gray-400">
            Mã đặt lịch: <span class="font-mono font-semibold text-gray-600">{{ booking.id.slice(0, 8).toUpperCase() }}</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const booking = ref(null)
const clinicName = ref('')
const doctorName = ref('')
const loading = ref(true)
const error = ref('')

const confirmLoading = ref(false)
const confirmError = ref('')
const confirmSuccess = ref('')

// Tạo nội dung QR chuyển khoản (VietQR API)
const qrCodeUrl = computed(() => {
  if (!booking.value) return ''
  const bank = 'MB' // MBBank
  const accountNo = '0123456789'
  const amount = booking.value.deposit_amount || 0
  const content = encodeURIComponent(`DAT COC ${booking.value.id.slice(0, 8).toUpperCase()}`)
  // Dùng VietQR public API
  return `https://img.vietqr.io/image/${bank}-${accountNo}-compact2.png?amount=${amount}&addInfo=${content}&accountName=CLINIC%20HOME%20VISIT`
})

function formatPrice(value) {
  if (!value && value !== 0) return '—'
  return new Intl.NumberFormat('vi-VN').format(value) + 'đ'
}

function formatDate(isoString) {
  if (!isoString) return '—'
  const d = new Date(isoString)
  return d.toLocaleDateString('vi-VN', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' })
}

function formatTime(isoString) {
  if (!isoString) return '—'
  const d = new Date(isoString)
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

function statusLabel(status) {
  const labels = {
    awaiting_payment: 'Chờ thanh toán',
    pending: 'Chờ xác nhận',
    confirmed: 'Đã xác nhận',
    in_progress: 'Đang khám',
    completed: 'Hoàn thành',
    cancelled: 'Đã huỷ',
    expired: 'Hết hạn',
  }
  return labels[status] || status
}

async function fetchBooking() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.get(`/bookings/${route.params.id}`)
    booking.value = res.data

    // Lấy tên phòng khám
    try {
      const clinicRes = await api.get(`/clinics/${booking.value.clinic_id}`)
      clinicName.value = clinicRes.data.name || ''
    } catch { clinicName.value = 'Phòng khám' }

    // Lấy tên bác sĩ
    try {
      const docRes = await api.get(`/doctors/${booking.value.doctor_id}`)
      doctorName.value = docRes.data.name || ''
    } catch { doctorName.value = 'Bác sĩ' }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Không thể tải thông tin đặt lịch'
  } finally {
    loading.value = false
  }
}

async function confirmPayment() {
  confirmError.value = ''
  confirmLoading.value = true
  try {
    const res = await api.post(`/bookings/${booking.value.id}/confirm-payment`, {
      transaction_ref: null
    })
    booking.value = res.data
    confirmSuccess.value = 'Xác nhận đặt cọc thành công! Lịch khám đang chờ phòng khám phê duyệt.'
    setTimeout(() => router.push('/bookings'), 2500)
  } catch (err) {
    confirmError.value = err.response?.data?.detail || 'Xác nhận thất bại, vui lòng thử lại.'
  } finally {
    confirmLoading.value = false
  }
}

onMounted(() => {
  fetchBooking()
})
</script>

<style scoped>
/* Ticket tear effect */
</style>
