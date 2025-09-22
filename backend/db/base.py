from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from ..models.user import User
from ..models.expenses import Expense
from ..models.payments import Payment
