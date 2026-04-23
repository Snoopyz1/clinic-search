"""
Review Service - Reviews Router
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from review_service.models.models import Review, ReviewReport
from review_service.schemas.schemas import ReviewCreate, ReviewReply, ReviewReport as ReviewReportSchema, ReviewResponse
from review_service.utils.dependencies import get_db, get_current_user
from datetime import datetime
import httpx

router = APIRouter()


async def _get_booking(booking_id: str, user_id: str) -> dict:
    """Call booking-service to get booking info and validate ownership + completion."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"http://booking-service:8002/api/v1/bookings/{booking_id}",
                headers={"X-User-Id": user_id, "X-User-Role": "patient"},
            )
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    return None


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_review(
    request: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a review for a completed booking"""
    user_id = current_user["user_id"]

    # Check duplicate: one review per booking
    existing = await db.execute(
        select(Review).where(
            Review.booking_id == request.booking_id,
            Review.user_id == user_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Bạn đã đánh giá lịch hẹn này rồi")

    # Validate booking via booking-service
    booking = await _get_booking(request.booking_id, user_id)

    if booking is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn")

    if booking.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền đánh giá lịch hẹn này")

    if booking.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Chỉ có thể đánh giá sau khi hoàn thành khám")

    clinic_id = booking.get("clinic_id", "")
    doctor_id = booking.get("doctor_id", "")

    review = Review(
        booking_id=request.booking_id,
        user_id=user_id,
        clinic_id=clinic_id,
        doctor_id=doctor_id,
        rating=request.rating,
        comment=request.comment,
        pros=request.pros,
        cons=request.cons,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)

    return ReviewResponse(
        id=str(review.id),
        booking_id=str(review.booking_id),
        user_id=str(review.user_id),
        clinic_id=str(review.clinic_id),
        doctor_id=str(review.doctor_id),
        rating=review.rating,
        comment=review.comment,
        pros=review.pros,
        cons=review.cons,
        is_hidden=review.is_hidden,
        is_reported=review.is_reported,
        report_count=review.report_count or 0,
        created_at=review.created_at,
        updated_at=review.updated_at,
    )


@router.get("/clinic/{clinic_id}")
async def get_clinic_reviews(
    clinic_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get reviews for a clinic"""
    # Total count
    count_result = await db.execute(
        select(func.count(Review.id))
        .where(Review.clinic_id == clinic_id)
        .where(Review.is_hidden == False)
    )
    total = count_result.scalar() or 0

    # Average rating
    avg_result = await db.execute(
        select(func.avg(Review.rating))
        .where(Review.clinic_id == clinic_id)
        .where(Review.is_hidden == False)
    )
    avg_rating = avg_result.scalar()

    # Reviews list
    result = await db.execute(
        select(Review)
        .where(Review.clinic_id == clinic_id)
        .where(Review.is_hidden == False)
        .order_by(Review.created_at.desc())
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    reviews = result.scalars().all()

    return {
        "reviews": [
            ReviewResponse(
                id=str(r.id),
                booking_id=str(r.booking_id),
                user_id=str(r.user_id),
                clinic_id=str(r.clinic_id),
                doctor_id=str(r.doctor_id),
                rating=r.rating,
                comment=r.comment,
                pros=r.pros,
                cons=r.cons,
                is_hidden=r.is_hidden,
                reply=r.reply,
                replied_at=r.replied_at,
                is_reported=r.is_reported,
                report_count=r.report_count or 0,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in reviews
        ],
        "total": total,
        "average_rating": round(float(avg_rating), 1) if avg_rating else None,
        "page": page,
        "page_size": page_size,
    }


@router.get("/doctor/{doctor_id}")
async def get_doctor_reviews(
    doctor_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get reviews for a doctor"""
    count_result = await db.execute(
        select(func.count(Review.id))
        .where(Review.doctor_id == doctor_id)
        .where(Review.is_hidden == False)
    )
    total = count_result.scalar() or 0

    avg_result = await db.execute(
        select(func.avg(Review.rating))
        .where(Review.doctor_id == doctor_id)
        .where(Review.is_hidden == False)
    )
    avg_rating = avg_result.scalar()

    result = await db.execute(
        select(Review)
        .where(Review.doctor_id == doctor_id)
        .where(Review.is_hidden == False)
        .order_by(Review.created_at.desc())
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    reviews = result.scalars().all()

    return {
        "reviews": [
            ReviewResponse(
                id=str(r.id),
                booking_id=str(r.booking_id),
                user_id=str(r.user_id),
                clinic_id=str(r.clinic_id),
                doctor_id=str(r.doctor_id),
                rating=r.rating,
                comment=r.comment,
                pros=r.pros,
                cons=r.cons,
                is_hidden=r.is_hidden,
                reply=r.reply,
                replied_at=r.replied_at,
                is_reported=r.is_reported,
                report_count=r.report_count or 0,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in reviews
        ],
        "total": total,
        "average_rating": round(float(avg_rating), 1) if avg_rating else None,
        "page": page,
        "page_size": page_size,
    }


@router.get("/booking/{booking_id}/check")
async def check_booking_reviewed(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Check if current user already reviewed this booking"""
    result = await db.execute(
        select(Review).where(
            Review.booking_id == booking_id,
            Review.user_id == current_user["user_id"],
        )
    )
    review = result.scalar_one_or_none()
    return {
        "reviewed": review is not None,
        "review_id": str(review.id) if review else None,
        "rating": review.rating if review else None,
    }


@router.post("/{review_id}/reply")
async def reply_review(
    review_id: str,
    request: ReviewReply,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reply to a review (clinic owner or doctor)"""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.reply:
        raise HTTPException(status_code=400, detail="Already replied")

    review.reply = request.reply
    review.replied_by = current_user["user_id"]
    review.replied_at = datetime.utcnow()

    await db.commit()
    await db.refresh(review)

    return {"message": "Reply added"}


@router.post("/{review_id}/report")
async def report_review(
    review_id: str,
    request: ReviewReportSchema,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Report a review"""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Create report
    report = ReviewReport(
        review_id=review.id,
        reporter_id=current_user["user_id"],
        reason=request.reason,
        description=request.description,
    )
    db.add(report)

    # Update review
    review.report_count = (review.report_count or 0) + 1
    if review.report_count >= 3:
        review.is_reported = True

    await db.commit()

    return {"message": "Report submitted"}
