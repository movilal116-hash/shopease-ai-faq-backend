 # Script to create tables & dummy data
from api.database import engine, SessionLocal, Base
import api.models as models


Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()


# Checks if there is already at least one customer in the database.
        # If there is, it stops the function. This prevents you from adding duplicate dummy data every time you run the script.
    if db.query(models.Customer).first():
        print("database already has data")
        return 

    customer = models.Customer(name="MObilal", email="movilal893@gmail.com", hashed_password="dummy_password")
    # create a new python object representing a customer
    # in phase -2 I will replace dummy_password with a secure hash instead of dummy

    db.add(customer)
    # stages the new customer in the session. It is not saved in the database yet

    db.commit()
    # saves(commits) permanently customer to mysql

    db.refresh(customer)
    # refreshes the python object with the data from the database
    #  this is how the customer_id becomes available in python

    order1 = models.Order(customer_id=customer.id, product_name="sony headphones", status="delivered", amount=199.00)

    order2 = models.Order(customer_id=customer.id, product_name="Blutooth", status="shipped", amount=799.00)

    db.add(order1)
    db.add(order2)

    db.commit()
# Saves both orders to the MySQL database permanently.

    print("database table is created and dummy data added")

if __name__ == "__main__":
    seed_data()
