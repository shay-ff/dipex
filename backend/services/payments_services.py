from sqlalchemy.orm import Session
from datetime import date
from ..models.payments import Payment
from ..schemas.payments import Payment as PaymentSchema


def create_payment(
    db: Session,
    *,
    user_id: int,
    amount: float,
    payment_date: date,
    payment_method: str,
    payment_status: str,
    raw_text: str,
) -> Payment:
    payment = Payment(
        user_id=user_id,
        amount=amount,
        payment_date=payment_date,
        payment_method=payment_method,
        payment_status=payment_status,
        raw_text=raw_text,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def to_schema(payment: Payment) -> PaymentSchema:
    return PaymentSchema(
        id=payment.id,
        user_id=payment.user_id,
        amount=float(payment.amount),
        payment_date=payment.payment_date,
        payment_method=payment.payment_method,
        payment_status=payment.payment_status,
        raw_text=payment.raw_text,
    )


