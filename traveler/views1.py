from django.shortcuts import render, redirect
from .models import Contact, User_Signup,Flights,Cabs,Hotels,Wishlist,HotelCart,FlightCart,CabCart,HotelGallery,Transaction
from django.conf import settings 
from django.core.mail import send_mail 
import random
from datetime import datetime
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time,)
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def initiate_payment(request):
    try:
        user=User_Signup.objects.get(email=request.session['email'])
        amount = int(request.POST['amount'])
    except:
        return render(request, 'mycart.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)


def index(request):
	return render(request,'index.html')

def seller_index(request):
	return render(request,'seller_index.html')

def destination(request):
	flights=Flights.objects.all()
	cabs=Cabs.objects.all()
	return render(request,'destination.html',{'flights':flights,'cabs':cabs})

def contact(request):
	if request.method=="POST":

		try:
			contact=Contact.objects.get(email=request.POST['email'])
			msg="Email Already Exist"
			contacts=Contact.objects.all().order_by('-id')[:5]
			return render(request,'contact.html',{'msg':msg,'contacts':contacts})
		except Exception as e:
			Contact.objects.create(
					name=request.POST['name'],
					email=request.POST['email'],
					subject=request.POST['subject'],
					message=request.POST['message']
				)			
			#print(request.POST['name'])
			#print(request.POST['email'])
			#print(request.POST['subject'])
			#print(request.POST['message'])
			contacts=Contact.objects.all().order_by('-id')[:5]
			msg="Contact saved Successfully"
			return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by('-id')[:5]
		return render(request,'contact.html',{'contacts':contacts})

def pricing(request):
	return render(request,'pricing.html')
	
def signup(request):
	if request.method=="POST":
		try:
			user=User_Signup.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except Exception as e:
			print("Exception : ",e)
			if request.POST['password']==request.POST['cpassword']:
				user = User_Signup.objects.create(
					usertype=request.POST['usertype'],
					fname=request.POST['fname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					gender=request.POST['gender'],
					address=request.POST['address'],
					password=request.POST['password'],
					cpassword=request.POST['cpassword'],
					image=request.FILES['image'],
					)
				subject = 'OTP for Registration'
				otp=random.randint(1000,9999)
				message = f'Hello {user.fname}, Your OTP for Successfull Registration Is :'+str(otp)
				email_from = settings.EMAIL_HOST_USER 
				recipient_list = [request.POST['email'],] 
				send_mail( subject, message, email_from, recipient_list ) 

				return render(request,'otp.html',{'otp':otp,'email':request.POST['email']})
			else:
				msg="Password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		if request.POST['action']=="Forgot Password":
			return render(request,'enter_email.html')
		elif request.POST['action']=="Sign In":
			try:
				user=User_Signup.objects.get(
					email=request.POST['email'],
					password=request.POST['password']
					)
				if user.usertype=="User":
					wishlists=Wishlist.objects.filter(user=user)
					flightcart=FlightCart.objects.filter(user=user)
					hotelcart=HotelCart.objects.filter(user=user)
					cabcart=CabCart.objects.filter(user=user)
					request.session['fname']=user.fname
					request.session['email']=user.email
					request.session['image']=user.image.url
					request.session['wishlist_count']=len(wishlists)
					request.session['cart_count'] = len(flightcart)+len(hotelcart)+len(cabcart)
					return render(request,'index.html')
				elif user.usertype=="Seller":
					request.session['fname']=user.fname
					request.session['email']=user.email
					request.session['image']=user.image.url
					return render(request,'seller_index.html')
				else:
					pass
			except Exception as e:
				print(e)
				msg="Email Or Password Is Incorrect"
				return render(request,'login.html',{'msg':msg})
		else:
			pass
	return render(request,'login.html')

def enter_otp(request):
	otp1=request.POST['otp1']
	otp2=request.POST['otp2']
	email=request.POST['email']

	if otp1==otp2:
		user=User_Signup.objects.get(email=email)
		user.status="active"
		user.save()
		msg="User Verified Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'otp':otp1,'email':email})

def enter_email(request):
	if request.method=="POST":
		try:
			user=User_Signup.objects.get(email=request.POST['email'])
			subject = 'OTP for Forgot Password'
			otp=random.randint(1000,9999)
			message = f'Hello {user.fname}, Your OTP for Forgot Password Is :'+str(otp)
			email_from = settings.EMAIL_HOST_USER 
			recipient_list = [request.POST['email'],] 
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'forgot_enter_otp.html',{'otp':otp,'email':request.POST['email']})
		except Exception as e:
			print(e)
			msg="Email Does Not Exists In The System"
			return render(request,'enter_email.html',{'msg':msg})
		#print(request.POST['email'])
	else:
		return render(request,'enter_email.html')

def verify_forgot_otp(request):
	if request.method=="POST":
		otp1=request.POST['otp1']
		otp2=request.POST['otp2']
		email=request.POST['email']

		if otp1==otp2:
			return render(request,'new_password.html',{'email':email})
		else:
			msg="Entered OTP Is Invalid"
			return render(request,'forgot_enter_otp.html',{'otp':otp1,'email':email,'msg':msg})

def update_password(request):
	if request.method=="POST":
		user=User_Signup.objects.get(email=request.POST['email'])

		if request.POST['npassword']==request.POST['cnpassword']:
			user.password=request.POST['npassword']
			user.cpassword=request.POST['cnpassword']
			user.save()
			return render(request,'login.html')

		else:
			msg=""+user.fname+", Entered Password Does Not Matched...!"
			return render(request,'new_password.html',{'email':request.POST['email'],'msg':msg})

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del	request.session['image'] 
		return render(request,'login.html')

	except Exception as e:
		raise

def change_password(request):
	if request.method=="POST":
		user=User_Signup.objects.get(email=request.session['email'])
			
		if user.password==request.POST['old_password']:
			if request.POST['npassword']==request.POST['cnpassword']:
				user.password=request.POST['npassword']
				user.cpassword=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg=""+user.fname+", Entered Password Does Not Matched...!"
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg=""+user.fname+", Old Password Is Incorrect...!"
			return render(request,'change_password.html',{'msg':msg})

	else: return render(request,'change_password.html')

def edit_profile(request):
	user=User_Signup.objects.get(email=request.session['email'])
	if request.method == "POST":
		user.fname=request.POST['fname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.gender=request.POST['gender']
		user.address=request.POST['address']
		try:
			user.image=request.FILES['image']
			user.save()
			user=User_Signup.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			request.session['image']=user.image.url
			return render(request,'edit_profile.html',{'user':user,'msg':msg})
		except Exception as e:
			user.save()
			user=User_Signup.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			return render(request,'edit_profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'edit_profile.html',{'user':user})

def seller_change_password(request):
	if request.method=="POST":
		user=User_Signup.objects.get(email=request.session['email'])
			
		if user.password==request.POST['old_password']:
			if request.POST['npassword']==request.POST['cnpassword']:
				user.password=request.POST['npassword']
				user.cpassword=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg=""+user.fname+", Entered Password Does Not Matched...!"
				return render(request,'seller_change_password.html',{'msg':msg})
		else:
			msg=""+user.fname+", Old Password Is Incorrect...!"
			return render(request,'seller_change_password.html',{'msg':msg})

	else: return render(request,'seller_change_password.html')

def seller_edit_profile(request):
	user=User_Signup.objects.get(email=request.session['email'])
	if request.method == "POST":
		user.fname=request.POST['fname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.gender=request.POST['gender']
		user.address=request.POST['address']
		try:
			user.image=request.FILES['image']
			user.save()
			user=User_Signup.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			request.session['image']=user.image.url
			return render(request,'seller_edit_profile.html',{'user':user,'msg':msg})
		except Exception as e:
			user.save()
			user=User_Signup.objects.get(email=request.session['email'])
			msg="Profile Saved Successfully"
			return render(request,'seller_edit_profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'seller_edit_profile.html',{'user':user})

def seller_add_flight(request):
	if request.method=="POST":
		seller=User_Signup.objects.get(email=request.session['email'])
		Flights.objects.create(
			seller=seller,
			flight_name=request.POST['flight_name'],
			flight_src=request.POST['flight_src'],
			flight_dest=request.POST['flight_dest'],
			flight_fare=request.POST['flight_fare'],
			flight_deptime=request.POST['flight_deptime'],
			flight_arrtime=request.POST['flight_arrtime'],
			flight_image=request.FILES['flight_image'],
			flight_dest_image=request.FILES['flight_dest_image'],
			flight_desc=request.POST['flight_desc'],
			)
		msg="Flight Added Successfully"
		return render(request,'seller_add_flight.html',{'msg':msg})
	else:
		return render(request,'seller_add_flight.html')

def seller_view_products(request):
	seller=User_Signup.objects.get(email=request.session['email'])
	flights=Flights.objects.filter(seller=seller)
	cabs=Cabs.objects.filter(seller=seller)
	hotels=Hotels.objects.filter(seller=seller)
	return render(request,'seller_view_products.html',{'flights':flights,'cabs':cabs,'hotels':hotels})

def seller_flight_detail(request,pk):
	#print(pk)
	flights=Flights.objects.get(pk=pk)
	return render(request,'seller_flight_details.html',{'flights':flights})

def seller_edit_flight(request,pk):
	flights=Flights.objects.get(pk=pk)
	

	if request.method=="POST":
		flights.flight_fare=request.POST['flight_fare']
		flights.flight_desc=request.POST['flight_desc']
		
		try:
			flights.flight_deptime = request.POST['flight_deptime']
			flights.flight_arrtime = request.POST['flight_arrtime']
			flights.save()
			return redirect('seller_view_products')
		except Exception as e:
			flights.save()
			return redirect('seller_view_products')

		# try:
		# 	flights.flight_deptime = parse_datetime('%a %b %d %H:%M:%S %Y')
		# 	flights.flight_arrtime = parse_datetime('%a %b %d %H:%M:%S %Y')
		# 	flights.save()
		# 	return redirect('seller_view_products')
		# except ValueError as ve:
		# 	print('ValueError Raised:', ve)
		# 	flights.save()
		# 	return redirect('seller_view_products')
	else:
		return render(request,'seller_edit_flight.html',{'flights':flights})

def index_datetime(request):
	return render(request,'index_datetime.html')

def seller_delete_flight(request,pk):
	flights=Flights.objects.get(pk=pk)
	flights.delete()
	return redirect('seller_view_products')

def seller_add_cab(request):
	if request.method=="POST":
		seller=User_Signup.objects.get(email=request.session['email'])
		Cabs.objects.create(
			seller=seller,
			cab_name=request.POST['cab_name'],
			cab_src=request.POST['cab_src'],
			cab_dest=request.POST['cab_dest'],
			cab_bookfare=request.POST['cab_bookfare'],
			cab_deptime=request.POST['cab_deptime'],
			cab_arrtime=request.POST['cab_arrtime'],
			cab_image=request.FILES['cab_image'],
			cab_desc=request.POST['cab_desc'],
			)
		msg="Cab Added Successfully"
		return render(request,'seller_add_cab.html',{'msg':msg})
	else:
		return render(request,'seller_add_cab.html')

def seller_add_hotel(request):
	if request.method=="POST":
		seller=User_Signup.objects.get(email=request.session['email'])
		Hotels.objects.create(
			seller=seller,
			hotel_name=request.POST['hotel_name'],
			hotel_roomfare=request.POST['hotel_roomfare'],
			hotel_image=request.FILES['hotel_image'],
			hotel_desc=request.POST['hotel_desc'],
			)
		msg="Hotel Added Successfully"
		return render(request,'seller_add_hotel.html',{'msg':msg})
	else:
		return render(request,'seller_add_hotel.html')

def seller_add_hotelgallery(request):
	if request.method=="POST":
		seller=User_Signup.objects.get(email=request.session['email'])
		hotels=Hotels.objects.get(hotel_name=request.POST['hotel_name'])
		HotelGallery.objects.create(
			seller=seller,
			hotels=hotels,
			hotel_image=request.FILES['hotel_image'],
			)
		msg="Hotel Added in Gallery Successfully"
		return render(request,'seller_add_hotelgallery.html',{'msg':msg,'hotels':hotels})
	else:
		return render(request,'seller_add_hotelgallery.html')

def seller_hotel_detail(request,pk):
	hotels=Hotels.objects.get(pk=pk)
	if request.POST['action']=='LEARN MORE':
    		hotelgallery=HotelGallery.objects.filter(pk=pk)
	else:
		pass
	# for i in hotelgallery:
	# 	data=hotelgallery.objects.get(hotel_image=hotel_image)
	# 	print(data)
	return render(request,'seller_hotel_details.html',{'hotels':hotels,'hotelgallery':hotelgallery})

def seller_edit_hotel(request,pk):
	hotels=Hotels.objects.get(pk=pk)
	
	if request.method=="POST":
		hotels.hotel_roomfare=request.POST['hotel_roomfare']
		hotels.hotel_desc=request.POST['hotel_desc']
		
		hotels.save()
		return redirect('seller_view_products')
	else:
		return render(request,'seller_edit_hotel.html',{'hotels':hotels})

def seller_delete_hotel(request,pk):
	hotels=Hotels.objects.get(pk=pk)
	hotels.delete()
	return redirect('seller_view_products')

def seller_cab_detail(request,pk):
	cabs=Cabs.objects.get(pk=pk)
	return render(request,'seller_cab_details.html',{'cabs':cabs})

def seller_edit_cab(request,pk):
	cabs=Cabs.objects.get(pk=pk)
	
	if request.method=="POST":
		cabs.flight_fare=request.POST['cab_bookfare']
		cabs.flight_desc=request.POST['cab_desc']
		
		try:
			cabs.flight_deptime = request.POST['cab_deptime']
			cabs.flight_arrtime = request.POST['cab_arrtime']
			cabs.save()
			return redirect('seller_view_products')
		except Exception as e:
			cabs.save()
			return redirect('seller_view_products')
	else:
		return render(request,'seller_edit_cab.html',{'cabs':cabs})

def seller_delete_cab(request,pk):
	cabs=Cabs.objects.get(pk=pk)
	cabs.delete()
	return redirect('seller_view_products')

def hotel_view_products(request):
	hotels=Hotels.objects.all()
	return render(request,'hotel_view_products.html',{'hotels':hotels})

def destination_view_products(request):
	flights=Flights.objects.all()
	cabs=Cabs.objects.all()
	return render(request,'destination.html',{'flights':flights,'cabs':cabs})

def user_hotel_detail(request,pk):
	flag=False
	flag1=False
	hotels=Hotels.objects.get(pk=pk)
	try:
		user=User_Signup.objects.get(email=request.session['email'])
	except User_Signup.DoesNotExist:
		user = None
	
	try:
		Wishlist.objects.get(user=user,hotels=hotels)
		flag=True
	except Exception as e:
		print('Exception',e)
		pass
	try:
		HotelCart.objects.get(user=user,hotels=hotels)
		flag1=True
	except Exception as e:
		pass
	return render(request,'user_hotel_details.html',{'hotels':hotels,'flag':flag,'flag1':flag1})

def user_flight_detail(request,pk):
	flag1=False
	user=User_Signup.objects.get(email=request.session['email'])
	flights=Flights.objects.get(pk=pk)
	try:
		FlightCart.objects.get(user=user,flights=flights)
		flag1=True
	except Exception as e:
		pass
	return render(request,'user_flight_details.html',{'flights':flights,'flag1':flag1})

def user_cab_detail(request,pk):
	flag1=False
	user=User_Signup.objects.get(email=request.session['email'])
	cabs=Cabs.objects.get(pk=pk)
	try:
		CabCart.objects.get(user=user,cabs=cabs)
		flag1=True
	except Exception as e:
		pass
	return render(request,'user_cab_details.html',{'cabs':cabs,'flag1':flag1})

def mywishlist(request):
	u=User_Signup.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=u)
	request.session['wishlist_count']=len(wishlists)
	#print(wishlists)
	return render(request,'mywishlist.html',{'wishlists':wishlists})

def user_add_wishlist(request,pk):
	hotels=Hotels.objects.get(pk=pk)
	u=User_Signup.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=u,hotels=hotels)
	return redirect('mywishlist')

def user_remove_wishlist(request,pk):
	user=User_Signup.objects.get(email=request.session['email'])
	hotels=Hotels.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,hotels=hotels)
	wishlist.delete()
	return redirect('mywishlist')

def mycart(request):
	net_price=0
	flag=False
	user=User_Signup.objects.get(email=request.session['email'])
	flightcart=FlightCart.objects.filter(user=user)
	hotelcart=HotelCart.objects.filter(user=user)
	cabcart=CabCart.objects.filter(user=user)

	for i in (flightcart):
		for j in hotelcart:
			for k in cabcart:
				net_price=net_price+int(i.f_total_price)+int(j.h_total_price)+int(k.c_total_price)

	request.session['cart_count'] = len(flightcart)+len(hotelcart)+len(cabcart)
	print(request.session['cart_count'])

	try:
		FlightCart.objects.filter(user=user)
		flag=True
	except Exception as e:
		raise

	try:
		HotelCart.objects.filter(user=user)
		flag=True
	except Exception as e:
		raise

	try:
		CabCart.objects.filter(user=user)
		flag=True
	except Exception as e:
		raise
	return render(request,'mycart.html',{'flightcart':flightcart,'hotelcart':hotelcart,'cabcart':cabcart,'flag':flag, 'net_price':net_price})

def flight_add_cart(request,pk):
	flights=Flights.objects.get(pk=pk)
	user=User_Signup.objects.get(email=request.session['email'])
	FlightCart.objects.create(
		user=user,
		flights=flights,
		flight_fare=flights.flight_fare,
		f_total_price=flights.flight_fare
		)
	return redirect('mycart')

def hotel_add_cart(request,pk):
	hotels=Hotels.objects.get(pk=pk)
	user=User_Signup.objects.get(email=request.session['email'])
	HotelCart.objects.create(
		user=user,
		hotels=hotels,
		hotel_fare=hotels.hotel_roomfare,
		h_total_price=hotels.hotel_roomfare
		)
	return redirect('mycart')

def cab_add_cart(request,pk):
	cabs=Cabs.objects.get(pk=pk)
	user=User_Signup.objects.get(email=request.session['email'])
	CabCart.objects.create(
		user=user,
		cabs=cabs,
		cab_fare=cabs.cab_bookfare,
		c_total_price=cabs.cab_bookfare
		)
	return redirect('mycart')

def hotel_remove_cart(request,pk):
	user=User_Signup.objects.get(email=request.session['email'])
	hotels=Hotels.objects.get(pk=pk)
	hotelcart=HotelCart.objects.get(user=user,hotels=hotels)
	hotelcart.delete()
	return redirect('mycart')

def flight_remove_cart(request,pk):
	user=User_Signup.objects.get(email=request.session['email'])
	flights=Flights.objects.get(pk=pk)
	flightcart=FlightCart.objects.get(user=user,flights=flights)
	flightcart.delete()
	return redirect('mycart')

def cab_remove_cart(request,pk):
	user=User_Signup.objects.get(email=request.session['email'])
	cabs=Cabs.objects.get(pk=pk)
	cabcart=CabCart.objects.get(user=user,cabs=cabs)
	cabcart.delete()
	return redirect('mycart')

def hotel_change_qty(request):
	hotelcart=HotelCart.objects.get(pk=request.POST['pk'])
	qty=request.POST['qty']
	hotelcart.qty=qty
	hotelcart.h_total_price=int(qty)*int(hotelcart.hotel_fare)
	hotelcart.save()
	return redirect('mycart')

def flight_change_qty(request):
	flightcart=FlightCart.objects.get(pk=request.POST['pk'])
	qty=request.POST['qty']
	flightcart.qty=qty
	flightcart.f_total_price=int(qty)*int(flightcart.flight_fare)
	flightcart.save()
	return redirect('mycart')

def cab_change_qty(request):
	cabcart=CabCart.objects.get(pk=request.POST['pk'])
	qty=request.POST['qty']
	cabcart.qty=qty
	cabcart.c_total_price=int(qty)*int(cabcart.cab_fare)
	cabcart.save()
	return redirect('mycart')