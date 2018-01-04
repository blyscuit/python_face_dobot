import datetime as dt

class Order:

    orderCount = 0
    customerCount = 0

    def __init__(self, customer=Order.customerCount,order=Order.orderCount, faceId="", burger="hamburger", status="ordered"):
        self.customer = customer
        self.faceId = faceId
        self.burger = burger
        self.status = status
        self.startTime = dt.datetime.now()
        Order.orderCount += 1
        Order.customerCount += 1