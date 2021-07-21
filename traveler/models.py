from django.db import models
import datetime
from django.utils import timezone
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time,)

# Create your models here.
class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	subject=models.CharField(max_length=100)
	message=models.TextField()

	def __str__(self):
		return self.name+" - "+self.email

class User_Signup(models.Model):
	"""docstring for User_Signup"""
	"""def __init__(self, arg):
		super(User_Signup, self).__init__()
		self.arg = arg"""
	fname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	gender=models.CharField(max_length=100)
	address=models.TextField()
	password=models.CharField(max_length=100)
	cpassword=models.CharField(max_length=100)
	status=models.CharField(max_length=100,default="inactive")
	image=models.ImageField(upload_to="images/",blank=True,null=True)
	usertype=models.CharField(max_length=100,default="User")

	def __str__(self):
		return self.fname+" - "+self.email
		
class Flights(models.Model):
	"""docstring for Flights"""
	NAMES=(
			('IndiGo','IndiGo'),
			('Air India','Air India'),
			('SpiceJet','SpiceJet'),
			('GoAir','GoAir'),
			('AirAsia','AirAsia'),
			('TruJet','TruJet'),
			('Alliance Air','Alliance Air'),
		)
	seller=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	flight_name=models.CharField(max_length=100,choices=NAMES)
	flight_image=models.ImageField(upload_to="flight_images/",blank=True,null=True)
	flight_src=models.CharField(max_length=100)
	flight_dest=models.CharField(max_length=100)
	flight_fare=models.CharField(max_length=100)
	flight_deptime=models.DateTimeField(blank=True, null=True,default=datetime.date.today)
	flight_arrtime=models.DateTimeField(blank=True, null=True,default=datetime.date.today)
	flight_desc=models.TextField(blank=True,null=True)
	flight_dest_image=models.ImageField(upload_to="flight_images/",blank=True,null=True)

	def __str__(self):
		return self.seller.fname+" - "+self.flight_name+" - "+self.flight_src+" to "+self.flight_dest+" ₹ "+self.flight_fare
	
class Cabs(models.Model):
	"""docstring for Cabs"""
	NAMES=(
			('Fareies','Fareies'),
			('Fair Fares','Fair Fares'),
			('Cabme','Cabme'),
			('Cool Cab','Cool Cab'),
			('Quick Cab','Quick Cab'),
		)
	seller=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	cab_name=models.CharField(max_length=100,choices=NAMES)
	cab_image=models.ImageField(upload_to="cab_images/",blank=True,null=True)
	cab_src=models.CharField(max_length=100)
	cab_dest=models.CharField(max_length=100)
	cab_bookfare=models.CharField(max_length=100)
	cab_deptime=models.DateTimeField(blank=True, null=True,default=datetime.date.today)
	cab_arrtime=models.DateTimeField(blank=True, null=True,default=datetime.date.today)
	cab_desc=models.TextField(blank=True,null=True)
	cab_dest_image=models.ImageField(upload_to="cab_images/",blank=True,null=True)

	def __str__(self):
		return self.seller.fname+" - "+self.cab_name+" - "+self.cab_src+" to "+self.cab_dest+" ₹ "+self.cab_bookfare

class Hotels(models.Model):
	"""docstring for Hotels"""
	NAMES=(
			('The Paradise Inn','The Paradise Inn'),
			('Hotel deLuxe','Hotel deLuxe'),
			('Four Seasons','Four Seasons'),
			('Hi-Way Inn','Hi-Way Inn'),
			('Candlewood Suites','Candlewood Suites'),
			('Cute Mountains','Cute Mountains.'),
			('Hotel Bliss','Hotel Bliss'),
		)

	seller=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	hotel_name=models.CharField(max_length=100,choices=NAMES)
	hotel_image=models.ImageField(upload_to="hotel_images/",blank=True,null=True)
	hotel_roomfare=models.CharField(max_length=100)
	hotel_desc=models.TextField(blank=True,null=True)

	def __str__(self):
		return self.seller.fname+" - "+self.hotel_name+" - "+" ₹ "+self.hotel_roomfare

class HotelGallery(models.Model):
	"""docstring for HotelsGallery"""
	seller=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	hotels=models.ForeignKey(Hotels,on_delete=models.CASCADE)
	hotel_image=models.ImageField(upload_to="hotel_gallery/",blank=True,null=True)

	def __str__(self):
		return self.seller.fname+" - "+self.hotels.hotel_name+" - " +str(self.hotel_image)


class Wishlist(models.Model):
	"""docstring for Wishlist"""
	user=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	hotels=models.ForeignKey(Hotels,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.fname+" - "+self.hotels.hotel_name

class HotelCart(models.Model):
	"""docstring for HotelCart"""
	user=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	hotels=models.ForeignKey(Hotels,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	qty=models.IntegerField(default=1)
	hotel_fare=models.FloatField(blank=False, null=False, default=0.0)
	h_total_price=models.FloatField(blank=False, null=False, default=0.0)

	def __str__(self):
		return self.user.fname+" - "+self.hotels.hotel_name

class FlightCart(models.Model):
	"""docstring for FlightCart"""
	user=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	flights=models.ForeignKey(Flights,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	qty=models.IntegerField(default=1)
	flight_fare=models.FloatField(blank=False, null=False, default=0.0)
	f_total_price=models.FloatField(blank=False, null=False, default=0.0)

	def __str__(self):
		return self.user.fname+" - "+self.flights.flight_name

class CabCart(models.Model):
	"""docstring for CabCart"""
	user=models.ForeignKey(User_Signup,on_delete=models.CASCADE)
	cabs=models.ForeignKey(Cabs,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	qty=models.IntegerField(default=1)
	cab_fare=models.FloatField(blank=False, null=False, default=0.0)
	c_total_price=models.FloatField(blank=False, null=False, default=0.0)

	def __str__(self):
		return self.user.fname+" - "+self.cabs.cab_name

class Transaction(models.Model):
    made_by = models.ForeignKey(User_Signup, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

# class Trains(models.Model):
# 	"""docstring for Trains"""
# 	NAMES=(
# 			('Ajanta Express','Ajanta Express'),
# 			('Ahilyanagari Express','Ahilyanagari Express'),
# 			('Amaravati Express','Amaravati Express'),
# 			('Andhra Pradesh Express','Andhra Pradesh Express'),
# 			('Arunachal Express','Arunachal Express'),
# 			('Bagmati Express','Bagmati Express'),
# 			('Chennai Mail','Chennai Mail'),
# 			('Chhattisgarh Express','Chhattisgarh Express'),
# 			('Darjeeling Mail','Darjeeling Mail'),
# 			('Deccan Queen Express','Deccan Queen Express'),
# 			('East Coast Express','East Coast Express'),
# 			('Gomti Express','Gomti Express'),
# 			('Goa Express','Goa Express'),
# 			('Gujarat Express','Gujarat Express'),
# 			('Himsagar Express','Himsagar Express'),
# 			('Island Express','Island Express'),
# 			('Jhelum Express','Jhelum Express'),
# 			('Janshatabdi Express','Janshatabdi Express'),
# 		)


# class Bus(models.Model):
# 	"""docstring for Food"""
# 	TYPES=(
# 			('Minibus','Minibus'),
# 			('Single deck','Single deck'),
# 			('Double deck','Double deck'),
# 			('Midibus','Midibus'),
# 			('Chassis','Chassis'),
# 			('Shuttle bus','Shuttle bus'),
# 			('AC bus','AC bus'),
# 		)
	
	
# class Food(models.Model):
# 	"""docstring for Food"""
# 	CATEGORIES=(
# 			('Dairy Items','Dairy Items'),
# 			('Beverages','Beverages'),
# 			('Packaged Food','Packaged Food'),
# 			('Frozen Food','Frozen Food'),
# 			('Pet Care','Pet Care'),
# 		)

# 		