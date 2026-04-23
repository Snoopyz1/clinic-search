-- Migration: Thêm cột gói khám và cập nhật status constraint cho bảng bookings
-- Chạy script này khi DB đang hoạt động (không cần reset data)

-- 1. Thêm các cột mới vào bảng bookings (IF NOT EXISTS để idempotent)
ALTER TABLE booking_schema.bookings
    ADD COLUMN IF NOT EXISTS package_id     VARCHAR(50),
    ADD COLUMN IF NOT EXISTS package_name   VARCHAR(200),
    ADD COLUMN IF NOT EXISTS package_price  DECIMAL(10, 2),
    ADD COLUMN IF NOT EXISTS deposit_amount DECIMAL(10, 2);

-- 2. Cập nhật constraint status để cho phép 'awaiting_payment'
ALTER TABLE booking_schema.bookings
    DROP CONSTRAINT IF EXISTS valid_status;

ALTER TABLE booking_schema.bookings
    ADD CONSTRAINT valid_status CHECK (
        status IN ('awaiting_payment', 'pending', 'confirmed', 'in_progress', 'completed', 'cancelled', 'expired')
    );

-- 3. Xác nhận
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'booking_schema'
  AND table_name   = 'bookings'
  AND column_name  IN ('package_id', 'package_name', 'package_price', 'deposit_amount');
