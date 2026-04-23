"""
Booking Service - Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class BookingCreate(BaseModel):
    clinic_id: str
    doctor_id: Optional[str] = Field(None)
    booking_type: str = Field(..., pattern="^(at_clinic|home_visit)$")
    scheduled_at: datetime
    duration_minutes: int = Field(default=30, ge=30, le=120)
    home_address: Optional[str] = None
    home_lat: Optional[float] = Field(None, ge=-90, le=90)
    home_lng: Optional[float] = Field(None, ge=-180, le=180)
    notes: Optional[str] = None
    payment_method: str = Field(default="qr_deposit", pattern="^(cash|transfer|qr_deposit)$")
    # Gói khám
    package_id: Optional[str] = Field(None)           # 'package_1' | 'package_2'
    package_name: Optional[str] = Field(None)         # Tên gói
    package_price: Optional[float] = Field(None, ge=0) # Giá gói

    @field_validator("scheduled_at", mode="before")
    @classmethod
    def parse_scheduled_at(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
                if dt.tzinfo is not None:
                    return dt.replace(tzinfo=None)
                return dt
            except Exception:
                pass
        return v


class BookingUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=30, le=120)
    notes: Optional[str] = None


class BookingStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(confirmed|in_progress|completed)$")


class AdminBookingStatusUpdate(BaseModel):
    """Admin or clinic owner can set any status"""
    status: str = Field(
        ...,
        pattern="^(pending|confirmed|in_progress|completed|cancelled|expired)$",
    )
    cancellation_reason: Optional[str] = None


class BookingCancel(BaseModel):
    reason: Optional[str] = None


class MedicalRecordUpdate(BaseModel):
    """Bác sĩ ghi hồ sơ bệnh án sau khi khám xong"""
    diagnosis: str = Field(..., min_length=1, description="Chẩn đoán bệnh")
    prescription: Optional[str] = Field(None, description="Đơn thuốc")
    record_notes: Optional[str] = Field(None, description="Ghi chú của bác sĩ")
    follow_up_date: Optional[datetime] = Field(None, description="Ngày tái khám")


class BookingResponse(BaseModel):
    id: str
    user_id: str
    clinic_id: str
    doctor_id: str
    booking_type: str
    scheduled_at: datetime
    duration_minutes: int
    status: str
    home_address: Optional[str] = None
    home_lat: Optional[float] = None
    home_lng: Optional[float] = None
    notes: Optional[str] = None
    total_price: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    cancellation_reason: Optional[str] = None
    cancelled_by: Optional[str] = None
    cancelled_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    # Gói khám
    package_id: Optional[str] = None
    package_name: Optional[str] = None
    package_price: Optional[float] = None
    deposit_amount: Optional[float] = None  # 50% của package_price
    # Hồ sơ bệnh án
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    record_notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class BookingListResponse(BaseModel):
    bookings: list[BookingResponse]
    total: int
    page: int
    page_size: int


class ConfirmPaymentRequest(BaseModel):
    """Người dùng xác nhận đã chuyển khoản đặt cọc"""
    transaction_ref: Optional[str] = Field(None, description="Mã giao dịch tham chiếu (nếu có)")


class SlotResponse(BaseModel):
    id: str
    doctor_id: str
    slot_start: datetime
    slot_end: datetime
    is_available: bool

    class Config:
        from_attributes = True
