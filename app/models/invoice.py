from app import db

class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    service_invoice = db.relationship("ServiceInvoice", back_populates='service')

class PaymentStatus(db.Enum):
    PENDING = "pending"
    PARTIALY_PAYED = "partialy_payed"
    PAYED = "payed"

class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))
    
    issuance_date = db.Column(db.Date, nullable=False)
    status_payment = db.Column(db.Enum("PaymentStatus", name="payment_status"), nullable=False, default=PaymentStatus.PENDING)

    reservation = db.relationship("Reservation", backref='invoice')
    service_invoice = db.relationship("ServiceInvoice", back_populates="invoice", cascade="all, delete-orphan")
    
class ServiceInvoice(db.Model):
    __tablename__ = "service_invoice"
    id = db.Column(db.Integer, primary_key=True)

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    quantity = db.Column(db.Integer, nullable=False, default=1)
    unitary_price = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)

    service = db.relationship("Service", back_populates='service_invoice')
    invoice = db.relationship("Invoice", back_populates='service_invoice')

    @property
    def total_price(self):
        return self.unitary_price * self.quantity