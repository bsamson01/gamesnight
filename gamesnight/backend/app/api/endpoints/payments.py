from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_active_user
from app.models import User, Payment
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.paypal import paypal_service
from app.core.config import settings

router = APIRouter()


@router.post("/verify", response_model=PaymentResponse)
async def verify_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if order already processed
    result = await db.execute(
        select(Payment).where(Payment.order_id == payment_data.order_id)
    )
    existing_payment = result.scalar_one_or_none()
    
    if existing_payment:
        if existing_payment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This payment belongs to another user"
            )
        return PaymentResponse.from_orm(existing_payment)
    
    # Verify with PayPal
    verification = await paypal_service.verify_order(payment_data.order_id)
    
    if not verification['success']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=verification.get('error', 'Payment verification failed')
        )
    
    # Calculate expiry date
    expires_at = paypal_service.calculate_expiry_date(payment_data.payment_type)
    
    # Create payment record
    db_payment = Payment(
        user_id=current_user.id,
        order_id=payment_data.order_id,
        amount=verification['amount'],
        status='completed',
        payment_type=payment_data.payment_type,
        expires_at=expires_at
    )
    db.add(db_payment)
    
    # Update user's paid status
    current_user.is_paid = True
    current_user.paid_until = expires_at
    current_user.role = "paid"
    
    await db.commit()
    await db.refresh(db_payment)
    
    return PaymentResponse.from_orm(db_payment)


@router.get("/history", response_model=list[PaymentResponse])
async def get_payment_history(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Payment)
        .where(Payment.user_id == current_user.id)
        .order_by(Payment.created_at.desc())
    )
    payments = result.scalars().all()
    
    return [PaymentResponse.from_orm(p) for p in payments]


@router.get("/config")
async def get_payment_config(
    current_user: User = Depends(get_current_active_user)
):
    """Get PayPal client ID for frontend"""
    return {
        "client_id": settings.PAYPAL_CLIENT_ID,
        "currency": "USD",
        "plans": {
            "day_pass": {
                "price": 1.99,
                "duration": "24 hours"
            },
            "month_pass": {
                "price": 9.99,
                "duration": "30 days"
            }
        }
    }