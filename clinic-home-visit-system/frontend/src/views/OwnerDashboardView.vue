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
        <router-link to="/owner/dashboard" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/owner/dashboard' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:bg-emerald-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          Dashboard
        </router-link>

        <router-link to="/owner/clinics" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/owner/clinics' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:bg-emerald-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          Phòng khám của tôi
        </router-link>

        <router-link to="/owner/doctors" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/owner/doctors' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:bg-emerald-800 hover:text-white'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          Bác sĩ
        </router-link>

        <router-link to="/owner/revenue" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-emerald-200 hover:bg-emerald-800 hover:text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Doanh thu
        </router-link>

        <!-- Nav: Hồ sơ bệnh án -->
        <button @click="activeSection = 'records'; fetchAllRecords()"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="activeSection === 'records' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:bg-emerald-800 hover:text-white'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          Hồ sơ bệnh án
        </button>
      </nav>

      <div class="px-4 py-4 border-t border-emerald-800">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center text-xs font-bold">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ user?.full_name || 'Chủ phòng khám' }}</p>
            <p class="text-xs text-emerald-300 truncate">{{ user?.email }}</p>
          </div>
          <button @click="handleLogout" class="p-1.5 rounded-lg hover:bg-emerald-800 text-emerald-300 hover:text-red-400 transition-colors" title="Đăng xuất">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-64 min-h-screen">
      <!-- Top Bar -->
      <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div class="px-8 py-4 flex items-center justify-between">
          <div>
            <h1 class="text-xl font-semibold text-gray-900">Dashboard</h1>
            <p class="text-sm text-gray-500">Quản lý phòng khám của bạn</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5"></span>
              Chủ phòng khám
            </span>
          </div>
        </div>
      </header>

      <div class="px-8 py-6">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-20">
          <div class="inline-block w-10 h-10 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
          <p class="ml-4 text-gray-500">Đang tải dữ liệu...</p>
        </div>

        <template v-else>
          <!-- ========= REVENUE SECTION ========= -->
          <template v-if="activeSection === 'revenue'">
            <div class="mb-6">
              <h2 class="text-xl font-bold text-gray-900 mb-1">Báo cáo Doanh thu</h2>
              <p class="text-sm text-gray-500">Tính dựa trên các đơn khám có trạng thái <strong>Hoàn thành</strong></p>
            </div>

            <!-- Tab switcher -->
            <div class="flex gap-2 mb-6">
              <button v-for="tab in revenueTabs" :key="tab.key" @click="revenueTab = tab.key"
                class="px-4 py-2 rounded-xl text-sm font-semibold transition-all"
                :class="revenueTab === tab.key
                  ? 'bg-emerald-600 text-white shadow-md'
                  : 'bg-white text-gray-600 border border-gray-200 hover:border-emerald-300 hover:text-emerald-700'"
              >
                {{ tab.label }}
              </button>
            </div>

            <!-- ---- Tab: Khoảng ngày ---- -->
            <div v-if="revenueTab === 'range'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
              <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                Theo khoảng ngày
              </h3>
              <div class="flex flex-wrap items-end gap-4 mb-6">
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Từ ngày</label>
                  <input type="date" v-model="rangeFrom" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Đến ngày</label>
                  <input type="date" v-model="rangeTo" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
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
              <div v-if="rangeRevenue.bookings.length > 0">
                <h4 class="text-sm font-semibold text-gray-700 mb-3">Chi tiết đơn hoàn thành</h4>
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
                      <tr v-for="b in rangeRevenue.bookings" :key="b.id" class="hover:bg-gray-50">
                        <td class="py-2.5 pr-4 text-gray-700">{{ formatDate(b.scheduled_at) }}</td>
                        <td class="py-2.5 pr-4">
                          <span :class="b.booking_type === 'home_visit' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'" class="px-2 py-0.5 rounded-full text-xs font-medium">
                            {{ b.booking_type === 'home_visit' ? 'Tại nhà' : 'Phòng khám' }}
                          </span>
                        </td>
                        <td class="py-2.5 pr-4 text-gray-600">{{ b.package_name || '—' }}</td>
                        <td class="py-2.5 text-right font-semibold text-emerald-700">{{ formatPrice(b.total_price || b.package_price) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div v-else class="text-center py-8 text-gray-400 text-sm">Không có đơn hoàn thành trong khoảng thời gian này.</div>
            </div>

            <!-- ---- Tab: Theo tháng ---- -->
            <div v-if="revenueTab === 'monthly'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
              <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                Theo tháng — Năm {{ monthlyYear }}
              </h3>
              <div class="flex items-center gap-3 mb-6">
                <label class="text-xs font-medium text-gray-500">Năm</label>
                <select v-model="monthlyYear" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400">
                  <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
                <div v-for="m in monthlyRevenue" :key="m.month"
                  class="rounded-xl border p-4 transition-all"
                  :class="m.total > 0 ? 'border-blue-200 bg-blue-50' : 'border-gray-100 bg-gray-50'"
                >
                  <p class="text-xs font-semibold uppercase tracking-wide mb-2" :class="m.total > 0 ? 'text-blue-500' : 'text-gray-400'">Tháng {{ m.month }}</p>
                  <p class="text-lg font-extrabold" :class="m.total > 0 ? 'text-blue-700' : 'text-gray-400'">{{ formatPrice(m.total) }}</p>
                  <p class="text-xs mt-1" :class="m.total > 0 ? 'text-blue-400' : 'text-gray-300'">{{ m.count }} đơn</p>
                </div>
              </div>
              <div class="mt-6 flex items-center justify-between bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl px-6 py-4">
                <div>
                  <p class="text-sm font-medium text-blue-100">Tổng doanh thu năm {{ monthlyYear }}</p>
                  <p class="text-3xl font-extrabold mt-0.5">{{ formatPrice(monthlyRevenue.reduce((s,m)=>s+m.total,0)) }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm text-blue-100">Tổng đơn</p>
                  <p class="text-2xl font-bold">{{ monthlyRevenue.reduce((s,m)=>s+m.count,0) }}</p>
                </div>
              </div>
            </div>

            <!-- ---- Tab: Theo quý ---- -->
            <div v-if="revenueTab === 'quarterly'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
              <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"/></svg>
                Theo quý — Năm {{ quarterlyYear }}
              </h3>
              <div class="flex items-center gap-3 mb-6">
                <label class="text-xs font-medium text-gray-500">Năm</label>
                <select v-model="quarterlyYear" class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400">
                  <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div v-for="q in quarterlyRevenue" :key="q.quarter"
                  class="rounded-2xl border p-5 transition-all"
                  :class="q.total > 0 ? 'border-purple-200 bg-gradient-to-br from-purple-50 to-indigo-50' : 'border-gray-100 bg-gray-50'"
                >
                  <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-bold" :class="q.total > 0 ? 'text-purple-700' : 'text-gray-400'">Quý {{ q.quarter }}</span>
                    <span class="text-xs px-2 py-0.5 rounded-full font-medium" :class="q.total > 0 ? 'bg-purple-100 text-purple-600' : 'bg-gray-100 text-gray-400'">
                      {{ q.months }}
                    </span>
                  </div>
                  <p class="text-2xl font-extrabold" :class="q.total > 0 ? 'text-purple-800' : 'text-gray-300'">{{ formatPrice(q.total) }}</p>
                  <p class="text-xs mt-2" :class="q.total > 0 ? 'text-purple-400' : 'text-gray-300'">{{ q.count }} đơn hoàn thành</p>
                  <div v-if="q.total > 0" class="mt-3 pt-3 border-t border-purple-100">
                    <p class="text-xs text-purple-400">Trung bình / đơn</p>
                    <p class="text-sm font-bold text-purple-600">{{ formatPrice(Math.round(q.total / q.count)) }}</p>
                  </div>
                </div>
              </div>
              <div class="mt-6 flex items-center justify-between bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl px-6 py-4">
                <div>
                  <p class="text-sm font-medium text-purple-100">Tổng doanh thu năm {{ quarterlyYear }}</p>
                  <p class="text-3xl font-extrabold mt-0.5">{{ formatPrice(quarterlyRevenue.reduce((s,q)=>s+q.total,0)) }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm text-purple-100">Tổng đơn</p>
                  <p class="text-2xl font-bold">{{ quarterlyRevenue.reduce((s,q)=>s+q.count,0) }}</p>
                </div>
              </div>
            </div>
          </template>

          <!-- ========= MEDICAL RECORDS SECTION ========= -->
          <template v-if="activeSection === 'records'">
            <div class="mb-6 flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-gray-900 mb-1 flex items-center gap-2">
                  <svg class="w-6 h-6 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  Quản lý Hồ sơ bệnh án
                </h2>
                <p class="text-sm text-gray-500">Tất cả ca khám đã hoàn thành — xem chi tiết hồ sơ từng bệnh nhân</p>
              </div>
              <span class="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-semibold bg-violet-100 text-violet-700">
                {{ allRecords.length }} hồ sơ
              </span>
            </div>

            <!-- Search + Filter bar -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4 flex flex-wrap gap-3 items-center">
              <!-- Search by patient ID -->
              <div class="flex items-center gap-2 flex-1 min-w-56 border border-gray-200 rounded-xl px-3 py-2 focus-within:border-violet-400 transition-colors">
                <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                <input v-model="ownerRecordSearch" type="text" placeholder="Tìm theo ID bệnh nhân..."
                  class="flex-1 text-sm outline-none text-gray-700 bg-transparent"/>
                <button v-if="ownerRecordSearch" @click="ownerRecordSearch = ''" class="text-gray-300 hover:text-gray-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
              <!-- Filter: only with diagnosis -->
              <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer select-none">
                <input type="checkbox" v-model="ownerRecordOnlyDiagnosed" class="rounded text-violet-600"/>
                Chỉ hiện đã ghi hồ sơ
              </label>
              <span v-if="ownerRecordSearch || ownerRecordOnlyDiagnosed"
                class="text-xs font-bold bg-violet-50 text-violet-700 px-2.5 py-1 rounded-full">
                {{ ownerFilteredRecords.length }} kết quả
              </span>
            </div>

            <!-- Loading -->
            <div v-if="recordsLoading" class="bg-white rounded-xl shadow-sm border border-gray-100 p-16 text-center text-gray-400">
              <div class="w-10 h-10 border-4 border-violet-200 border-t-violet-600 rounded-full animate-spin mx-auto mb-3"></div>
              <p class="text-sm">Đang tải hồ sơ...</p>
            </div>

            <!-- Empty -->
            <div v-else-if="ownerFilteredRecords.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-100 p-16 text-center text-gray-400">
              <svg class="w-14 h-14 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p class="font-medium text-gray-500">{{ ownerRecordSearch ? 'Không tìm thấy hồ sơ khớp' : 'Chưa có ca khám hoàn thành nào' }}</p>
            </div>

            <!-- Table -->
            <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <table class="w-full text-sm">
                <thead class="bg-gray-50 border-b border-gray-100">
                  <tr>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">ID bệnh nhân</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Phòng khám</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Thời gian</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Hình thức</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Chẩn đoán</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Chi tiết</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                  <tr v-for="b in ownerFilteredRecords" :key="b.id" class="hover:bg-gray-50 transition-colors">
                    <td class="px-5 py-3">
                      <div class="flex flex-col gap-0.5">
                        <span class="font-mono text-xs bg-indigo-50 border border-indigo-200 text-indigo-700 px-2 py-0.5 rounded-md w-fit">
                          {{ b.user_id?.slice(0, 14) }}...
                        </span>
                        <span class="text-xs text-gray-400">LH: {{ b.id?.slice(0,8) }}</span>
                      </div>
                    </td>
                    <td class="px-5 py-3 text-gray-700 text-xs">{{ ownerClinicName(b.clinic_id) }}</td>
                    <td class="px-5 py-3">
                      <p class="font-medium text-gray-800 text-xs">{{ formatDate(b.scheduled_at) }}</p>
                      <p class="text-gray-400 text-xs">{{ formatTime(b.scheduled_at) }}</p>
                    </td>
                    <td class="px-5 py-3">
                      <span :class="b.booking_type === 'home_visit' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'"
                        class="px-2 py-0.5 rounded-full text-xs font-medium">
                        {{ b.booking_type === 'home_visit' ? '🏠 Tại nhà' : '🏥 Phòng khám' }}
                      </span>
                    </td>
                    <td class="px-5 py-3">
                      <span v-if="b.diagnosis"
                        class="inline-flex items-center gap-1 text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-0.5 rounded-md max-w-40 truncate">
                        ✅ {{ b.diagnosis.slice(0,25) }}{{ b.diagnosis.length > 25 ? '...' : '' }}
                      </span>
                      <span v-else class="text-xs bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded-md">
                        ⏳ Chưa ghi
                      </span>
                    </td>
                    <td class="px-5 py-3">
                      <button @click="openOwnerRecord(b)"
                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-violet-600 text-white hover:bg-violet-700 transition-colors">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                        </svg>
                        Xem hồ sơ
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>

          <!-- ========= MAIN DASHBOARD ========= -->
          <template v-else>
          <!-- No Clinics Warning -->
          <div v-if="clinics.length === 0" class="bg-amber-50 border border-amber-200 rounded-xl p-6 mb-6">
            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-amber-900">Bạn chưa có phòng khám nào</h3>
                <p class="mt-1 text-sm text-amber-700">Liên hệ admin để được tạo phòng khám hoặc tạo mới tại đây.</p>
                <router-link to="/owner/clinics" class="inline-flex items-center mt-3 px-4 py-2 bg-amber-600 text-white rounded-lg text-sm font-medium hover:bg-amber-700 transition-colors">
                  Tạo phòng khám mới
                </router-link>
              </div>
            </div>
          </div>

          <template v-else>
            <!-- Stats Cards -->
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Phòng khám</p>
                <p class="text-2xl font-bold text-emerald-600 mt-1">{{ clinics.length }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Bác sĩ</p>
                <p class="text-2xl font-bold text-blue-600 mt-1">{{ stats.total_doctors }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center gap-2 mb-1">
                  <div class="w-2 h-2 rounded-full bg-yellow-400"></div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đang chờ</p>
                </div>
                <p class="text-2xl font-bold text-yellow-600">{{ stats.by_status?.pending || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center gap-2 mb-1">
                  <div class="w-2 h-2 rounded-full bg-blue-400"></div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Đã xác nhận</p>
                </div>
                <p class="text-2xl font-bold text-blue-600">{{ stats.by_status?.confirmed || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center gap-2 mb-1">
                  <div class="w-2 h-2 rounded-full bg-green-400"></div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider font-medium">Hoàn thành</p>
                </div>
                <p class="text-2xl font-bold text-green-600">{{ stats.by_status?.completed || 0 }}</p>
              </div>
            </div>

            <!-- Clinics List -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-semibold text-gray-900">Phòng khám của bạn</h2>
                <router-link to="/owner/clinics" class="text-sm text-emerald-600 hover:text-emerald-700 font-medium">
                  Quản lý phòng khám
                </router-link>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="clinic in clinics.slice(0, 3)" :key="clinic.id" class="border border-gray-100 rounded-lg p-4 hover:border-emerald-200 transition-colors">
                  <div class="flex items-start justify-between">
                    <div>
                      <h3 class="font-medium text-gray-900">{{ clinic.name }}</h3>
                      <p class="text-sm text-gray-500 mt-1">{{ clinic.address }}</p>
                    </div>
                    <span :class="clinic.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium">
                      {{ clinic.is_active ? 'Hoạt động' : 'Không hoạt động' }}
                    </span>
                  </div>
                  <div class="mt-3 flex items-center gap-4 text-sm text-gray-500">
                    <span class="flex items-center gap-1">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                      </svg>
                      {{ clinic.doctor_count || 0 }} bác sĩ
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pending Bookings -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
                <h2 class="text-lg font-semibold text-gray-900">Lịch hẹn đang chờ xác nhận</h2>
                <span class="text-sm text-gray-500">{{ bookings.length }} lịch hẹn</span>
              </div>

              <div v-if="bookings.length === 0" class="text-center py-12">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                </div>
                <p class="text-gray-500">Không có lịch hẹn nào đang chờ</p>
              </div>

              <div v-else class="divide-y divide-gray-50">
                <div v-for="booking in bookings" :key="booking.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
                  <div class="flex-1">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center">
                        <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                      </div>
                      <div>
                        <p class="font-medium text-gray-900">{{ formatDate(booking.scheduled_at) }} - {{ formatTime(booking.scheduled_at) }}</p>
                        <p class="text-sm text-gray-500">
                          {{ booking.clinic_name || 'Phòng khám' }} - 
                          <span :class="booking.booking_type === 'home_visit' ? 'text-purple-600' : 'text-blue-600'">
                            {{ booking.booking_type === 'home_visit' ? 'Khám tại nhà' : 'Khám tại phòng khám' }}
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span :class="statusClass(booking.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ statusLabel(booking.status) }}
                    </span>
                    <button v-if="booking.status === 'pending'" @click="approveBooking(booking)"
                      class="px-3 py-1.5 bg-green-50 text-green-600 rounded-lg text-xs font-medium hover:bg-green-100 transition-colors">
                      Duyệt
                    </button>
                    <button v-if="booking.status === 'pending'" @click="showRejectModal(booking)"
                      class="px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100 transition-colors">
                      Từ chối
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template> <!-- end v-else dashboard -->

          </template> <!-- end v-else activeSection -->
        </template>
      </div>
    </main>

    <!-- Reject Modal -->
    <div v-if="rejectModal.show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="rejectModal.show = false">
      <div class="bg-white rounded-xl shadow-xl max-w-md w-full mx-4 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Từ chối lịch hẹn</h3>
          <button @click="rejectModal.show = false" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <p class="text-sm text-gray-600 mb-3">
            Bạn đang từ chối lịch hẹn. Hành động này sẽ đặt trạng thái thành <strong class="text-red-600">cancelled</strong>.
          </p>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Lý do từ chối (tùy chọn)</label>
          <textarea v-model="rejectModal.reason" rows="3" placeholder="Nhập lý do từ chối..."
            class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"></textarea>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex gap-2 justify-end">
          <button @click="rejectModal.show = false"
            class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            Hủy
          </button>
          <button @click="confirmReject" :disabled="rejectModal.loading"
            class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-60">
            {{ rejectModal.loading ? 'Đang xử lý...' : 'Xác nhận từ chối' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Owner Record Detail Modal -->
    <div v-if="ownerSelectedRecord" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="ownerSelectedRecord = null">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
        <!-- Header -->
        <div style="background:linear-gradient(135deg,#059669,#0d9488);" class="px-6 py-4 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 bg-white/20 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-white font-bold text-base">Chi tiết Hồ sơ bệnh án</h3>
              <p class="text-green-100 text-xs">{{ ownerClinicName(ownerSelectedRecord.clinic_id) }}</p>
            </div>
          </div>
          <button @click="ownerSelectedRecord = null" class="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center hover:bg-white/30 transition-colors">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Info strip -->
        <div class="bg-green-50 border-b border-green-100 px-6 py-3 flex flex-wrap gap-4 text-xs">
          <div>
            <p class="text-green-600 font-bold uppercase">ID bệnh nhân</p>
            <p class="font-mono text-gray-700 mt-0.5">{{ ownerSelectedRecord.user_id?.slice(0,24) }}...</p>
          </div>
          <div>
            <p class="text-green-600 font-bold uppercase">Ngày khám</p>
            <p class="text-gray-700 font-semibold mt-0.5">{{ formatDate(ownerSelectedRecord.scheduled_at) }} {{ formatTime(ownerSelectedRecord.scheduled_at) }}</p>
          </div>
          <div v-if="ownerSelectedRecord.package_name">
            <p class="text-green-600 font-bold uppercase">Gói khám</p>
            <p class="text-gray-700 font-semibold mt-0.5">{{ ownerSelectedRecord.package_name }}</p>
          </div>
        </div>

        <!-- Body -->
        <div class="px-6 py-4 space-y-3 max-h-96 overflow-y-auto">
          <!-- Patient booking notes (read-only) - always shown -->
          <div class="bg-sky-50 border border-sky-200 rounded-xl p-3">
            <p class="text-xs font-bold text-sky-700 uppercase mb-1.5 flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
              Mô tả của bệnh nhân khi đặt lịch
            </p>
            <p v-if="ownerSelectedRecord.notes" class="text-sm text-sky-800">{{ ownerSelectedRecord.notes }}</p>
            <p v-else class="text-sm text-sky-300 italic">Bệnh nhân không để lại mô tả</p>
          </div>

          <div v-if="!ownerSelectedRecord.diagnosis" class="text-center py-8 text-gray-400">
            <p class="font-medium">Chưa có hồ sơ bệnh án</p>
            <p class="text-sm mt-1">Bác sĩ chưa ghi kết quả khám</p>
          </div>
          <template v-else>
            <!-- Diagnosis -->
            <div class="bg-purple-50 border border-purple-200 rounded-xl p-3">
              <p class="text-xs font-bold text-purple-700 uppercase mb-1.5 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                Chẩn đoán
              </p>
              <p class="text-sm text-gray-800">{{ ownerSelectedRecord.diagnosis }}</p>
            </div>
            <!-- Prescription -->
            <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-3">
              <p class="text-xs font-bold text-emerald-700 uppercase mb-1.5">Đơn thuốc</p>
              <pre v-if="ownerSelectedRecord.prescription" class="text-sm text-gray-700 whitespace-pre-wrap font-sans">{{ ownerSelectedRecord.prescription }}</pre>
              <p v-else class="text-sm text-emerald-400 italic">Chưa có đơn thuốc</p>
            </div>
            <!-- Doctor notes -->
            <div class="bg-amber-50 border border-amber-200 rounded-xl p-3">
              <p class="text-xs font-bold text-amber-700 uppercase mb-1.5">Lời dặn bác sĩ</p>
              <p v-if="ownerSelectedRecord.record_notes" class="text-sm text-gray-700">{{ ownerSelectedRecord.record_notes }}</p>
              <p v-else class="text-sm text-amber-400 italic">Chưa có lời dặn</p>
            </div>
            <!-- Follow-up -->
            <div v-if="ownerSelectedRecord.follow_up_date" class="bg-blue-50 border border-blue-200 rounded-xl p-3 flex items-center gap-3">
              <svg class="w-8 h-8 text-blue-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <div>
                <p class="text-xs font-bold text-blue-700 uppercase">Lịch tái khám</p>
                <p class="text-sm font-bold text-blue-900 mt-0.5">{{ formatDate(ownerSelectedRecord.follow_up_date) }}</p>
              </div>
            </div>
          </template>
        </div>

        <div class="px-6 py-3 bg-gray-50 border-t border-gray-100 flex justify-end">
          <button @click="ownerSelectedRecord = null"
            class="px-5 py-2 bg-emerald-600 text-white rounded-lg text-sm font-semibold hover:bg-emerald-700 transition-colors">
            Đóng
          </button>
        </div>
      </div>
    </div>
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

const clinics = ref([])
const bookings = ref([])
const stats = ref({ by_status: {}, total_doctors: 0 })
const loading = ref(false)

// ===== Section navigation =====
const activeSection = ref('dashboard') // 'dashboard' | 'revenue' | 'records'

// ===== Medical Records State (Owner) =====
const allRecords = ref([])
const recordsLoading = ref(false)
const ownerRecordSearch = ref('')
const ownerRecordOnlyDiagnosed = ref(false)
const ownerSelectedRecord = ref(null)

const ownerFilteredRecords = computed(() => {
  let list = allRecords.value
  if (ownerRecordOnlyDiagnosed.value) list = list.filter(b => b.diagnosis)
  if (ownerRecordSearch.value.trim()) {
    const q = ownerRecordSearch.value.trim().toLowerCase()
    list = list.filter(b => b.user_id?.toLowerCase().includes(q))
  }
  return list
})

const ownerClinicName = (clinicId) => {
  const c = clinics.value.find(cl => cl.id === clinicId)
  return c?.name || clinicId?.slice(0, 8)
}

const openOwnerRecord = (b) => { ownerSelectedRecord.value = b }

const fetchAllRecords = async () => {
  recordsLoading.value = true
  try {
    const res = await api.get('/bookings/clinic/owner/all', {
      params: { status: 'completed', page_size: 100 }
    })
    allRecords.value = res.data.bookings || []
  } catch (e) {
    console.error('fetchAllRecords error:', e?.response?.status, e?.response?.data)
    allRecords.value = []
  } finally {
    recordsLoading.value = false
  }
}

// ===== Revenue state =====
const revenueTabs = [
  { key: 'range',     label: 'Khoảng ngày' },
  { key: 'monthly',   label: 'Theo tháng' },
  { key: 'quarterly', label: 'Theo quý' },
]
const revenueTab = ref('range')

// Date range
const today = new Date()
const rangeFrom = ref(new Date(today.getFullYear(), today.getMonth(), 1).toISOString().slice(0, 10))
const rangeTo   = ref(today.toISOString().slice(0, 10))

// Monthly / quarterly year selectors
const monthlyYear    = ref(today.getFullYear())
const quarterlyYear  = ref(today.getFullYear())

// Helpers
const completedBookings = computed(() => bookings.value.filter(b => b.status === 'completed'))

const availableYears = computed(() => {
  const years = new Set(completedBookings.value.map(b => new Date(b.scheduled_at).getFullYear()))
  years.add(today.getFullYear())
  return [...years].sort((a, b) => b - a)
})

const bookingRevenue = (b) => +(b.total_price || b.package_price || 0)

// Range revenue
const rangeRevenue = computed(() => {
  const from = new Date(rangeFrom.value + 'T00:00:00')
  const to   = new Date(rangeTo.value   + 'T23:59:59')
  const filtered = completedBookings.value.filter(b => {
    const d = new Date(b.scheduled_at)
    return d >= from && d <= to
  })
  const total = filtered.reduce((s, b) => s + bookingRevenue(b), 0)
  return {
    bookings: filtered,
    count: filtered.length,
    total,
    avg: filtered.length ? Math.round(total / filtered.length) : 0,
  }
})

// Monthly revenue
const monthlyRevenue = computed(() => {
  return Array.from({ length: 12 }, (_, i) => {
    const month = i + 1
    const filtered = completedBookings.value.filter(b => {
      const d = new Date(b.scheduled_at)
      return d.getFullYear() === monthlyYear.value && d.getMonth() + 1 === month
    })
    return {
      month,
      count: filtered.length,
      total: filtered.reduce((s, b) => s + bookingRevenue(b), 0),
    }
  })
})

// Quarterly revenue
const quarterlyRevenue = computed(() => {
  const quarters = [
    { quarter: 1, months: 'Th1–3',  monthRange: [1, 3] },
    { quarter: 2, months: 'Th4–6',  monthRange: [4, 6] },
    { quarter: 3, months: 'Th7–9',  monthRange: [7, 9] },
    { quarter: 4, months: 'Th10–12', monthRange: [10, 12] },
  ]
  return quarters.map(q => {
    const filtered = completedBookings.value.filter(b => {
      const d = new Date(b.scheduled_at)
      const m = d.getMonth() + 1
      return d.getFullYear() === quarterlyYear.value && m >= q.monthRange[0] && m <= q.monthRange[1]
    })
    return {
      ...q,
      count: filtered.length,
      total: filtered.reduce((s, b) => s + bookingRevenue(b), 0),
    }
  })
})

// Format
const formatPrice = (v) => {
  if (!v && v !== 0) return '—'
  return new Intl.NumberFormat('vi-VN').format(v) + 'đ'
}

const rejectModal = ref({ show: false, booking: null, reason: '', loading: false })

const statusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    in_progress: 'bg-purple-100 text-purple-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700',
    expired: 'bg-gray-100 text-gray-500',
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

const statusLabel = (status) => {
  const labels = {
    pending: 'Đang chờ',
    confirmed: 'Đã xác nhận',
    in_progress: 'Đang khám',
    completed: 'Hoàn thành',
    cancelled: 'Đã hủy',
    expired: 'Hết hạn',
  }
  return labels[status] || status
}

const formatDate = (dt) => {
  if (!dt) return ''
  const d = new Date(dt)
  return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const formatTime = (dt) => {
  if (!dt) return ''
  const d = new Date(dt)
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

const fetchClinics = async () => {
  try {
    const response = await api.get('/clinics/owner/my-clinics')
    clinics.value = response.data.clinics || response.data || []
    
    // Calculate total doctors
    stats.value.total_doctors = clinics.value.reduce((sum, c) => sum + (c.doctor_count || 0), 0)
  } catch (error) {
    console.error('Error fetching clinics:', error)
  }
}

const fetchBookings = async () => {
  try {
    const response = await api.get('/bookings/clinic/owner/all')
    bookings.value = response.data.bookings || []

    // Calculate stats from bookings
    const byStatus = {}
    bookings.value.forEach(b => {
      byStatus[b.status] = (byStatus[b.status] || 0) + 1
    })
    stats.value.by_status = byStatus
  } catch (error) {
    console.error('Error fetching bookings:', error)
  }
}

const showRejectModal = (booking) => {
  rejectModal.value = { show: true, booking, reason: '', loading: false }
}

const approveBooking = async (booking) => {
  try {
    await api.put(`/bookings/clinic/${booking.clinic_id}/owner/update-status/${booking.id}`, { status: 'confirmed' })
    await fetchBookings()
  } catch (error) {
    console.error('Error approving booking:', error)
    alert('Lỗi khi duyệt lịch hẹn: ' + (error.response?.data?.detail || error.message))
  }
}

const confirmReject = async () => {
  rejectModal.value.loading = true
  try {
    await api.put(`/bookings/clinic/${rejectModal.value.booking.clinic_id}/owner/update-status/${rejectModal.value.booking.id}`, {
      status: 'cancelled',
      cancellation_reason: rejectModal.value.reason
    })
    rejectModal.value.show = false
    await fetchBookings()
  } catch (error) {
    console.error('Error rejecting booking:', error)
    alert('Lỗi khi từ chối lịch hẹn: ' + (error.response?.data?.detail || error.message))
  } finally {
    rejectModal.value.loading = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  loading.value = true
  await Promise.all([fetchClinics(), fetchBookings()])
  loading.value = false
})
</script>
