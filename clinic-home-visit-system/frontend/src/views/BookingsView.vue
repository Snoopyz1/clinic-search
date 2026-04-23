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
                  <!-- Gói khám -->
                  <div v-if="booking.package_name" class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                    <span class="text-indigo-600 font-medium">{{ booking.package_name }}</span>
                    <span class="text-gray-400">&bull; {{ formatPrice(booking.package_price) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right: Status + Action buttons -->
            <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2 border-t sm:border-t-0 border-gray-100 pt-3 sm:pt-0 mt-3 sm:mt-0">
              <span :class="statusClass(booking.status)" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm border">
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="statusDot(booking.status)"></span>
                {{ statusLabel(booking.status) }}
              </span>
              <p class="text-xs text-gray-400 hidden sm:block">Mã LH: {{ booking.id.slice(0, 8).toUpperCase() }}</p>

              <!-- Nút thanh toán cọc: hiện khi đang chờ thanh toán -->
              <router-link
                v-if="booking.status === 'awaiting_payment'"
                :to="`/bookings/${booking.id}/payment`"
                @click.stop
                class="mt-1 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-500 text-white hover:bg-orange-600 transition-all duration-150 shadow-sm"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/>
                </svg>
                Thanh toán cọc
              </router-link>

              <!-- Nút huỷ: hiện với awaiting_payment/pending/confirmed và còn > 3 ngày -->
              <button
                v-if="canCancel(booking)"
                @click.stop="openCancelModal(booking)"
                class="mt-1 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-red-600 border border-red-200 bg-red-50 hover:bg-red-100 hover:border-red-300 transition-all duration-150"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
                Huỷ lịch
              </button>

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

              <!-- Nút xem hồ sơ bệnh án: hiện khi hoàn thành -->
              <button
                v-if="booking.status === 'completed'"
                @click.stop="openMedicalRecord(booking)"
                class="mt-1 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-violet-50 text-violet-700 border border-violet-200 hover:bg-violet-100 hover:border-violet-300 transition-all duration-150"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Hồ sơ bệnh án
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- ===== Cancel Modal ===== -->
    <Transition name="fade">
      <div v-if="showCancelModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeCancelModal"></div>

        <!-- Modal card -->
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 z-10">
          <!-- Header -->
          <div class="flex items-center gap-3 mb-5">
            <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
            </div>
            <div class="flex-1">
              <h2 class="text-lg font-bold text-gray-900">Huỷ lịch khám</h2>
              <p class="text-sm text-gray-500 mt-0.5">{{ clinicNames[cancellingBooking?.clinic_id] || 'Phòng khám' }}</p>
            </div>
            <button @click="closeCancelModal" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <!-- Booking info summary -->
          <div class="bg-gray-50 rounded-xl p-4 mb-4 text-sm space-y-1.5">
            <div class="flex justify-between">
              <span class="text-gray-500">Ngày khám</span>
              <span class="font-semibold text-gray-900">{{ cancellingBooking ? formatDate(cancellingBooking.scheduled_at) : '' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Giờ khám</span>
              <span class="font-semibold text-gray-900">{{ cancellingBooking ? formatTime(cancellingBooking.scheduled_at) : '' }}</span>
            </div>
            <div v-if="cancellingBooking?.package_name" class="flex justify-between">
              <span class="text-gray-500">Gói khám</span>
              <span class="font-semibold text-indigo-700">{{ cancellingBooking.package_name }}</span>
            </div>
            <div v-if="cancellingBooking?.deposit_amount" class="flex justify-between border-t border-gray-200 pt-1.5 mt-1.5">
              <span class="text-gray-500">Tiền cọc đã trả</span>
              <span class="font-semibold text-emerald-700">{{ formatPrice(cancellingBooking.deposit_amount) }} <span class="text-xs font-normal text-gray-400">(hoàn trả 100%)</span></span>
            </div>
          </div>

          <!-- Reason input -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Lý do huỷ <span class="text-gray-400 font-normal">(tuỳ chọn)</span></label>
            <textarea
              v-model="cancelReason"
              rows="3"
              placeholder="Vd: Bận việc đột xuất, muốn đổi lịch..."
              class="w-full px-3 py-2.5 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent resize-none placeholder-gray-400"
            ></textarea>
          </div>

          <!-- Warning -->
          <div class="bg-amber-50 border border-amber-100 text-amber-700 px-4 py-3 rounded-xl text-xs flex items-start gap-2 mb-4">
            <svg class="w-4 h-4 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>Sau khi huỷ, lịch hẹn này sẽ không thể khôi phục. Bạn có thể đặt lịch mới bất kỳ lúc nào.</span>
          </div>

          <!-- Error -->
          <div v-if="cancelError" class="bg-red-50 border border-red-100 text-red-600 px-4 py-3 rounded-xl text-sm flex items-center gap-2 mb-4">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            {{ cancelError }}
          </div>

          <!-- Buttons -->
          <div class="flex gap-3">
            <button
              type="button"
              @click="closeCancelModal"
              :disabled="cancelLoading"
              class="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 rounded-xl text-sm font-medium hover:bg-gray-50 disabled:opacity-50 transition-colors"
            >
              Giữ lịch
            </button>
            <button
              type="button"
              @click="submitCancel"
              :disabled="cancelLoading"
              class="flex-1 px-4 py-2.5 bg-red-600 text-white rounded-xl text-sm font-semibold hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              <span v-if="cancelLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              {{ cancelLoading ? 'Đang huỷ...' : 'Xác nhận huỷ' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

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

    <!-- ===== Medical Record Modal ===== -->
    <Transition name="fade">
      <div v-if="showMedicalRecord" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showMedicalRecord = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg z-10 overflow-hidden">
          <!-- Header gradient -->
          <div style="background:linear-gradient(135deg,#4338ca,#7c3aed);padding:20px 24px;" class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div style="width:36px;height:36px;background:rgba(255,255,255,0.2);border-radius:50%;display:flex;align-items:center;justify-content:center;">
                <svg style="width:18px;height:18px;color:white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <div>
                <h2 style="color:white;font-size:16px;font-weight:800;margin:0;">Hồ sơ bệnh án</h2>
                <p style="color:rgba(255,255,255,0.75);font-size:12px;margin:0;">{{ clinicNames[viewingRecord?.clinic_id] || 'Phòng khám' }}</p>
              </div>
            </div>
            <button @click="showMedicalRecord = false" style="width:32px;height:32px;background:rgba(255,255,255,0.2);border:none;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;">
              <svg style="width:16px;height:16px;color:white;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <!-- Visit info strip -->
          <div style="background:#f8f7ff;border-bottom:1px solid #e9d5ff;padding:12px 24px;display:flex;gap:20px;flex-wrap:wrap;">
            <div>
              <p style="font-size:10px;color:#7c3aed;font-weight:700;text-transform:uppercase;margin:0 0 2px;">Ngày khám</p>
              <p style="font-size:13px;font-weight:600;color:#1e1b4b;margin:0;">{{ viewingRecord ? formatDate(viewingRecord.scheduled_at) : '' }}</p>
            </div>
            <div>
              <p style="font-size:10px;color:#7c3aed;font-weight:700;text-transform:uppercase;margin:0 0 2px;">Giờ khám</p>
              <p style="font-size:13px;font-weight:600;color:#1e1b4b;margin:0;">{{ viewingRecord ? formatTime(viewingRecord.scheduled_at) : '' }}</p>
            </div>
            <div v-if="viewingRecord?.package_name">
              <p style="font-size:10px;color:#7c3aed;font-weight:700;text-transform:uppercase;margin:0 0 2px;">Gói khám</p>
              <p style="font-size:13px;font-weight:600;color:#1e1b4b;margin:0;">{{ viewingRecord.package_name }}</p>
            </div>
          </div>

          <!-- Content -->
          <div style="padding:20px 24px;display:flex;flex-direction:column;gap:16px;max-height:60vh;overflow-y:auto;">

            <!-- No record yet -->
            <div v-if="!viewingRecord?.diagnosis" style="text-align:center;padding:32px 16px;color:#9ca3af;">
              <!-- Still show patient notes if available -->
              <div v-if="viewingRecord?.notes" style="text-align:left;margin-bottom:16px;background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:14px 16px;">
                <p style="font-size:11px;font-weight:700;color:#0284c7;text-transform:uppercase;letter-spacing:0.5px;margin:0 0 8px;display:flex;align-items:center;gap:6px;">
                  <svg style="width:14px;height:14px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
                  Mô tả của bạn khi đặt lịch
                </p>
                <p style="font-size:13px;color:#0369a1;margin:0;line-height:1.6;">{{ viewingRecord.notes }}</p>
              </div>
              <svg style="width:48px;height:48px;margin:0 auto 12px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p style="font-size:14px;font-weight:600;color:#6b7280;margin:0 0 6px;">Chưa có hồ sơ bệnh án</p>
              <p style="font-size:12px;color:#9ca3af;margin:0;">Bác sĩ chưa cập nhật kết quả khám cho lịch hẹn này</p>
            </div>

            <template v-else>
              <!-- Patient notes (booking description) - always shown -->
              <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:14px 16px;">
                <p style="font-size:11px;font-weight:700;color:#0284c7;text-transform:uppercase;letter-spacing:0.5px;margin:0 0 8px;display:flex;align-items:center;gap:6px;">
                  <svg style="width:14px;height:14px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
                  Mô tả của bạn khi đặt lịch
                </p>
                <p v-if="viewingRecord.notes" style="font-size:13px;color:#0369a1;margin:0;line-height:1.6;">{{ viewingRecord.notes }}</p>
                <p v-else style="font-size:13px;color:#7dd3fc;margin:0;font-style:italic;">Bạn không để lại mô tả khi đặt lịch</p>
              </div>

              <!-- Diagnosis -->
              <div style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:12px;padding:14px 16px;">
                <p style="font-size:11px;font-weight:700;color:#7c3aed;text-transform:uppercase;letter-spacing:0.5px;margin:0 0 8px;display:flex;align-items:center;gap:6px;">
                  <svg style="width:14px;height:14px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                  Chẩn đoán
                </p>
                <p style="font-size:14px;color:#1e1b4b;margin:0;line-height:1.6;">{{ viewingRecord.diagnosis }}</p>
              </div>

              <!-- Prescription -->
              <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px 16px;">
                <p style="font-size:11px;font-weight:700;color:#15803d;text-transform:uppercase;letter-spacing:0.5px;margin:0 0 8px;display:flex;align-items:center;gap:6px;">
                  <svg style="width:14px;height:14px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
                  Đơn thuốc
                </p>
                <pre v-if="viewingRecord.prescription" style="font-size:13px;color:#166534;margin:0;white-space:pre-wrap;font-family:inherit;line-height:1.7;">{{ viewingRecord.prescription }}</pre>
                <p v-else style="font-size:13px;color:#86efac;margin:0;font-style:italic;">Chưa có đơn thuốc</p>
              </div>

              <!-- Doctor notes -->
              <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:12px;padding:14px 16px;">
                <p style="font-size:11px;font-weight:700;color:#b45309;text-transform:uppercase;letter-spacing:0.5px;margin:0 0 8px;display:flex;align-items:center;gap:6px;">
                  <svg style="width:14px;height:14px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  Lời dặn của bác sĩ
                </p>
                <p v-if="viewingRecord.record_notes" style="font-size:13px;color:#92400e;margin:0;line-height:1.6;">{{ viewingRecord.record_notes }}</p>
                <p v-else style="font-size:13px;color:#fbbf24;margin:0;font-style:italic;">Chưa có lời dặn</p>
              </div>

              <!-- Follow-up date -->
              <div v-if="viewingRecord.follow_up_date" style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:14px 16px;display:flex;align-items:center;gap:12px;">
                <div style="width:40px;height:40px;background:#dbeafe;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg style="width:20px;height:20px;color:#2563eb;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                </div>
                <div>
                  <p style="font-size:11px;font-weight:700;color:#1d4ed8;text-transform:uppercase;margin:0 0 2px;">Lịch tái khám</p>
                  <p style="font-size:14px;font-weight:700;color:#1e40af;margin:0;">{{ formatDate(viewingRecord.follow_up_date) }}</p>
                </div>
              </div>
            </template>
          </div>

          <!-- Footer -->
          <div style="padding:14px 24px;border-top:1px solid #f3f4f6;display:flex;justify-content:flex-end;">
            <button
              @click="showMedicalRecord = false"
              style="background:linear-gradient(135deg,#4338ca,#7c3aed);color:white;padding:8px 24px;border:none;border-radius:10px;font-weight:700;font-size:13px;cursor:pointer;"
            >
              Đóng
            </button>
          </div>
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

// Cancel modal state
const showCancelModal = ref(false)
const cancellingBooking = ref(null)
const cancelReason = ref('')
const cancelError = ref('')
const cancelLoading = ref(false)

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

const formatPrice = (value) => {
  if (!value && value !== 0) return '—'
  return new Intl.NumberFormat('vi-VN').format(value) + 'đ'
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
    awaiting_payment: 'bg-orange-50 text-orange-700 border-orange-200',
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
    awaiting_payment: 'bg-orange-500',
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
    awaiting_payment: 'bg-orange-400',
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

// Medical record state
const showMedicalRecord = ref(false)
const viewingRecord = ref(null)

const openMedicalRecord = (booking) => {
  viewingRecord.value = booking
  showMedicalRecord.value = true
}

// Kiểm tra có thể huỷ không: trạng thái hợp lệ VÀ còn > 3 ngày
const canCancel = (booking) => {
  const cancellableStatuses = ['awaiting_payment', 'pending', 'confirmed']
  if (!cancellableStatuses.includes(booking.status)) return false
  const scheduledAt = new Date(booking.scheduled_at)
  const now = new Date()
  const diffDays = (scheduledAt - now) / (1000 * 60 * 60 * 24)
  return diffDays > 3
}

const openCancelModal = (booking) => {
  cancellingBooking.value = booking
  cancelReason.value = ''
  cancelError.value = ''
  showCancelModal.value = true
}

const closeCancelModal = () => {
  if (cancelLoading.value) return
  showCancelModal.value = false
  cancellingBooking.value = null
}

const submitCancel = async () => {
  if (!cancellingBooking.value) return
  cancelError.value = ''
  cancelLoading.value = true
  try {
    await api.post(`/bookings/${cancellingBooking.value.id}/cancel`, {
      reason: cancelReason.value || 'Người dùng tự huỷ'
    })
    // Cập nhật trạng thái local ngay lập tức
    const idx = bookings.value.findIndex(b => b.id === cancellingBooking.value.id)
    if (idx !== -1) {
      bookings.value[idx] = { ...bookings.value[idx], status: 'cancelled' }
    }
    closeCancelModal()
  } catch (err) {
    cancelError.value = err.response?.data?.detail || 'Huỷ lịch thất bại, vui lòng thử lại.'
  } finally {
    cancelLoading.value = false
  }
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
