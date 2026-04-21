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
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow duration-200 overflow-hidden relative"
        >
          <!-- Left accent line based on status -->
          <div class="absolute left-0 top-0 bottom-0 w-1" :class="getStatusAccent(booking.status)"></div>

          <div class="flex flex-col sm:flex-row justify-between gap-4">
            <!-- Left Info -->
            <div class="flex items-start gap-4 cursor-pointer" @click="openDetail(booking)">
              <div class="hidden sm:flex w-12 h-12 bg-indigo-50 rounded-lg items-center justify-center flex-shrink-0 text-indigo-600">
                <svg v-if="booking.booking_type === 'home_visit'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
                <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
              </div>
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <h3 class="text-lg font-bold text-gray-900">
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

            <!-- Right: Status + Review button -->
            <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2 border-t sm:border-t-0 border-gray-100 pt-3 sm:pt-0 mt-3 sm:mt-0">
              <span :class="statusClass(booking.status)" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm border">
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="statusDot(booking.status)"></span>
                {{ statusLabel(booking.status) }}
              </span>
              <p class="text-xs text-gray-400 hidden sm:block">Mã LH: {{ booking.id.slice(0, 8).toUpperCase() }}</p>

              <!-- Nút đánh giá: chỉ hiện khi hoàn thành và chưa đánh giá -->
              <button
                v-if="booking.status === 'completed'"
                @click.stop="openReviewModal(booking)"
                :disabled="reviewedBookings.has(booking.id)"
                class="mt-1 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-150"
                :class="reviewedBookings.has(booking.id)
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-amber-50 text-amber-700 border border-amber-200 hover:bg-amber-100 hover:border-amber-300'"
              >
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                {{ reviewedBookings.has(booking.id) ? 'Đã đánh giá' : 'Đánh giá' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- ===== Review Modal ===== -->
    <Transition name="fade">
      <div v-if="showReviewModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeReviewModal"></div>

        <!-- Modal card -->
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 z-10">
          <!-- Header -->
          <div class="flex items-center justify-between mb-5">
            <div>
              <h2 class="text-lg font-bold text-gray-900">Đánh giá lịch khám</h2>
              <p class="text-sm text-gray-500 mt-0.5">{{ clinicNames[reviewingBooking?.clinic_id] || 'Phòng khám' }}</p>
            </div>
            <button @click="closeReviewModal" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <form @submit.prevent="submitReview" class="space-y-4">
            <!-- Star Rating -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Đánh giá của bạn <span class="text-red-500">*</span></label>
              <div class="flex items-center gap-1">
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  @click="reviewForm.rating = star"
                  @mouseover="hoverRating = star"
                  @mouseleave="hoverRating = 0"
                  class="w-10 h-10 transition-transform hover:scale-110 focus:outline-none"
                >
                  <svg class="w-10 h-10 transition-colors"
                    :class="star <= (hoverRating || reviewForm.rating) ? 'text-amber-400' : 'text-gray-200'"
                    fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </button>
                <span class="ml-2 text-sm font-medium text-gray-600">
                  {{ ratingLabel(reviewForm.rating) }}
                </span>
              </div>
            </div>

            <!-- Comment -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Nhận xét</label>
              <textarea
                v-model="reviewForm.comment"
                rows="3"
                placeholder="Chia sẻ trải nghiệm của bạn về buổi khám..."
                class="w-full px-3 py-2.5 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none placeholder-gray-400"
              ></textarea>
            </div>

            <!-- Pros & Cons -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-sm font-medium text-emerald-700 mb-1.5 flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                  Ưu điểm
                </label>
                <input
                  v-model="reviewForm.pros"
                  type="text"
                  placeholder="Vd: Bác sĩ thân thiện"
                  class="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent placeholder-gray-400"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-red-500 mb-1.5 flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                  Nhược điểm
                </label>
                <input
                  v-model="reviewForm.cons"
                  type="text"
                  placeholder="Vd: Chờ lâu"
                  class="w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent placeholder-gray-400"
                />
              </div>
            </div>

            <!-- Error -->
            <div v-if="reviewError" class="bg-red-50 border border-red-100 text-red-600 px-4 py-3 rounded-xl text-sm flex items-center gap-2">
              <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              {{ reviewError }}
            </div>

            <!-- Success -->
            <div v-if="reviewSuccess" class="bg-emerald-50 border border-emerald-100 text-emerald-700 px-4 py-3 rounded-xl text-sm flex items-center gap-2">
              <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
              {{ reviewSuccess }}
            </div>

            <!-- Buttons -->
            <div class="flex gap-3 pt-1">
              <button
                type="button"
                @click="closeReviewModal"
                class="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors"
              >
                Hủy
              </button>
              <button
                type="submit"
                :disabled="reviewLoading || !reviewForm.rating"
                class="flex-1 px-4 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                <span v-if="reviewLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                {{ reviewLoading ? 'Đang gửi...' : 'Gửi đánh giá' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const bookings = ref([])
const clinicNames = ref({})
const loading = ref(false)
const reviewedBookings = ref(new Set())

// Review modal state
const showReviewModal = ref(false)
const reviewingBooking = ref(null)
const hoverRating = ref(0)
const reviewForm = ref({ rating: 0, comment: '', pros: '', cons: '' })
const reviewError = ref('')
const reviewSuccess = ref('')
const reviewLoading = ref(false)

const ratingLabel = (r) => {
  const labels = { 1: 'Rất tệ', 2: 'Chưa tốt', 3: 'Bình thường', 4: 'Tốt', 5: 'Xuất sắc' }
  return labels[r] || 'Chọn số sao'
}

const formatDate = (isoString) => {
  const d = new Date(isoString)
  return d.toLocaleDateString('vi-VN', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' })
}

const formatTime = (isoString) => {
  const d = new Date(isoString)
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
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

    // Fetch clinic names
    const cIds = [...new Set(bookings.value.map(b => b.clinic_id))]
    for (const cid of cIds) {
      if (!clinicNames.value[cid]) fetchClinicName(cid)
    }

    // Check which completed bookings are already reviewed
    const completedBookings = bookings.value.filter(b => b.status === 'completed')
    for (const b of completedBookings) {
      checkReviewed(b.id)
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

const checkReviewed = async (bookingId) => {
  try {
    const res = await api.get(`/reviews/booking/${bookingId}/check`)
    if (res.data.reviewed) {
      reviewedBookings.value = new Set([...reviewedBookings.value, bookingId])
    }
  } catch (e) {
    // ignore - review service may not have this booking
  }
}

const openReviewModal = (booking) => {
  reviewingBooking.value = booking
  reviewForm.value = { rating: 0, comment: '', pros: '', cons: '' }
  reviewError.value = ''
  reviewSuccess.value = ''
  hoverRating.value = 0
  showReviewModal.value = true
}

const closeReviewModal = () => {
  if (reviewLoading.value) return
  showReviewModal.value = false
  reviewingBooking.value = null
}

const submitReview = async () => {
  if (!reviewForm.value.rating) {
    reviewError.value = 'Vui lòng chọn số sao đánh giá'
    return
  }
  reviewError.value = ''
  reviewSuccess.value = ''
  reviewLoading.value = true

  try {
    await api.post('/reviews', {
      booking_id: reviewingBooking.value.id,
      rating: reviewForm.value.rating,
      comment: reviewForm.value.comment || undefined,
      pros: reviewForm.value.pros || undefined,
      cons: reviewForm.value.cons || undefined,
    })

    reviewSuccess.value = 'Cảm ơn bạn đã đánh giá! Ý kiến của bạn rất có giá trị.'
    reviewedBookings.value = new Set([...reviewedBookings.value, reviewingBooking.value.id])

    setTimeout(() => closeReviewModal(), 1800)
  } catch (err) {
    reviewError.value = err.response?.data?.detail || 'Gửi đánh giá thất bại, vui lòng thử lại.'
  } finally {
    reviewLoading.value = false
  }
}

const openDetail = (booking) => {
  // placeholder for future detail modal
}

onMounted(() => {
  fetchBookings()
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
