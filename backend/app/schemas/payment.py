from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaymentCreate(BaseModel):
    order_id: str
    payment_type: str  # day_pass or month_pass


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    order_id: str
    amount: float
    status: str
    payment_type: str
    expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaymentVerify(BaseModel):
    order_id: str