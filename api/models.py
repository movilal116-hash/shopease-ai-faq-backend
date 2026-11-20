# Defines the CRM Tables

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from api.database import Base

class Customer(Base):
    # Define the customer table. Each instance of this class is one row in the database
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    # the unique id for the customers
    # index=True : speedup database searches when looking a customer by ID

    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    # Stores the SECURE hashed password (never the plain text password)
    # 255 characters is standard for encrypted hashes like Bcrypt


    order = relationship("Order", back_populates="customer")  # same
    # Creates one-to-many link. A customer can have many orders
    # back_populates="customer": Links this to the 'customer' variable inside the order class they stay in sync
    
    tickets = relationship("SupportTicket", back_populates="customer")
    # Creates a "One-to-Many" link. A customer can have many support tickets.

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
        # This is the foreign key. It tells the database this order belongs to a specific customer

    product_name = Column(String(100))
    status = Column(String(50))
        # stores the order status: (Pending, Shipped, Delibered)
    tracking_number=Column(String(100), nullable=True)
        

    amount = Column(Float)

    created_at =  Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="order") # same
        # Reverse of the link if you have an order you can type order.customer to get the full customer details


class SupportTicket(Base):
    # Defines the support Ticket Table
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    # Unique id for the ticket

    customer_id = Column(Integer, ForeignKey("customers.id"))
    # links this ticket to a specific customer

    issue = Column(String(255))
    # A short description of the customer's problem

    status = Column(String(50))
    # Status of the ticket : "open" or "Resolved"

    customer = relationship('Customer', back_populates="tickets")
    # reverse link: let you type 'ticket.customer' to find out who created the ticket


