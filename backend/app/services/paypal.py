from datetime import datetime, timedelta
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class PayPalService:
    def __init__(self):
        if settings.PAYPAL_MODE == "sandbox":
            environment = SandboxEnvironment(
                client_id=settings.PAYPAL_CLIENT_ID,
                client_secret=settings.PAYPAL_CLIENT_SECRET
            )
        else:
            environment = LiveEnvironment(
                client_id=settings.PAYPAL_CLIENT_ID,
                client_secret=settings.PAYPAL_CLIENT_SECRET
            )
        
        self.client = PayPalHttpClient(environment)
    
    async def verify_order(self, order_id: str) -> dict:
        """Verify a PayPal order and return its details"""
        try:
            request = OrdersGetRequest(order_id)
            response = self.client.execute(request)
            
            order = response.result
            
            # Check if order is completed
            if order.status != 'COMPLETED':
                return {
                    'success': False,
                    'error': 'Order not completed'
                }
            
            # Extract payment info
            amount = float(order.purchase_units[0].amount.value)
            currency = order.purchase_units[0].amount.currency_code
            
            return {
                'success': True,
                'order_id': order.id,
                'status': order.status,
                'amount': amount,
                'currency': currency,
                'payer_email': order.payer.email_address if hasattr(order.payer, 'email_address') else None
            }
            
        except Exception as e:
            logger.error(f"PayPal order verification failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def calculate_expiry_date(self, payment_type: str) -> datetime:
        """Calculate the expiry date based on payment type"""
        now = datetime.utcnow()
        
        if payment_type == "day_pass":
            return now + timedelta(days=1)
        elif payment_type == "month_pass":
            return now + timedelta(days=30)
        else:
            raise ValueError(f"Invalid payment type: {payment_type}")


paypal_service = PayPalService()