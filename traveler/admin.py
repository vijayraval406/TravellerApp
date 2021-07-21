from django.contrib import admin
from . models import Contact,User_Signup,Flights,Hotels,Cabs,Wishlist,HotelCart,FlightCart,CabCart,HotelGallery,Transaction
# Register your models here.
admin.site.site_header = "TRAVELER."

class AdminContact(admin.ModelAdmin):
	"""docstring for AdmicContact"""
	list_display=('name','email','subject','message')
	list_filter=('name',)

class AdminUser_Signup(admin.ModelAdmin):
	"""docstring for AdminUser_Signup"""
	list_display=('usertype','fname','email','mobile','gender','address','password','cpassword','status')
		
		
admin.site.register(Contact,AdminContact)
admin.site.register(User_Signup,AdminUser_Signup)
admin.site.register(Flights)
admin.site.register(Hotels)
admin.site.register(Cabs)
admin.site.register(Wishlist)
admin.site.register(HotelCart)
admin.site.register(FlightCart)
admin.site.register(CabCart)
admin.site.register(HotelGallery)
admin.site.register(Transaction)