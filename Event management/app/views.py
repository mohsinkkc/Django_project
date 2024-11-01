from django.shortcuts import render,redirect
from .models import User,Service,Event,Rent,Cart,Transaction
from django.conf import settings
from django.core.mail import send_mail
import random
import razorpay
from django.http import JsonResponse

# Create your views here.
def home(request):
	event=Event.objects.all()
	rent=Rent.objects.all()
	return render(request,'home.html',{'event':event,'rent':rent})

def about(request):
	rent=Rent.objects.all()
	return render(request,'about.html',{'rent':rent})
def contact(request):
	return render(request,'contact.html')
def ticket(request):
	event=Event.objects.all()
	return render(request,'ticket.html',{'event':event})

def rent_venue(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		venue=Rent.objects.create(

			user=user,
			n_email=request.POST['n_email'],
			number=request.POST['number'],
			company=request.POST['company'],
			venue_name=request.POST['venue_name'],
			event_type=request.POST['event_type'],
			date_request=request.POST['date_request'],
			date_end=request.POST['date_end'],
			image=request.FILES['image'],
			desc=request.POST['desc']
			)
		return render(request,'rent_venue.html')
	else:
		return render(request,'rent_venue.html')

def signup(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			msg="Email already exist"
			return render(request,'signup.html',{'msg':msg})
		except :
			User.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				number=request.POST['number'],
				password=request.POST['password'],
				gender=request.POST['gender'],
				user_type=request.POST['user_type'],
				image=request.FILES['image']
				)
		print("===============>>>> SIGNUPPP ")
		return render(request,'home.html')
	else:
		print("------------->>>> else part")
		return render(request,'signup.html')

def login(request):
	if request.method=='POST':
		user=User.objects.get(email=request.POST['email'],password=request.POST['password'])
		request.session['email']=user.email
		request.session['name']=user.name
		
		if user.user_type=='admin':
			request.session['dashboard']=True
			return render(request,'home.html')
		else:
			return render(request,'home.html')
	else:
		msg="Please enter valid email/ password"
		return render(request,'login.html',{"msg":msg})

def logout(request):
	del request.session['email']
	del request.session['name']
	try:
		del request.session['dashboard']
	except:
		pass
	
	
	return render(request,'login.html')

def forget_pswd(request):
	if request.method=='POST':
		try:

			user=User.objects.get(email=request.POST['email'])
			subject = 'OTP for forget password'
			otp=random.randint(1000,9999)
			message = f'Hi {user.name}, Your OTP is : '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'confirm_otp.html',{'email':user.email,'otp':str(otp)})
		except:
			msg="please provide valid email"
			return render(request,'forget_pswd.html',{'msg':msg})

	else:
		return render(request,'forget_pswd.html')
def confirm_otp(request):
	if request.method=='POST':
		email=request.POST['email']
		otp=request.POST['otp']
		uotp=request.POST['uotp']

		if otp==uotp:
			return render(request,'change_pswd.html',{'email':email})
		else:
			msg='Invalid OTP'
			return render(request,'confirm_otp.html',{'msg':msg})
	else:
		return render(request,'confirm_otp.html')

def change_pswd(request):
	if request.method=='POST':
		email=request.POST['email']
		npswd=request.POST['npswd']
		cpswd=request.POST['cpswd']

		if npswd==cpswd:
			user=User.objects.get(email=email)
			user.password=npswd
			user.save()
			return redirect('login')
		else:
			msg='password doesnot match with each other'
			return render(request,'change_pswd.html',{'msg':msg})
	else:
		return render(request,'change_pswd.html')
	

#======================Admin DashBoard==================
def admin_index(request):
	user=User.objects.all()
	return render(request,'admin_index.html',{'user':user})
def add_service(request):
	if request.method=='POST':
		Service.objects.create(
			category=request.POST['category']
			)
		return render(request,'add_service.html')
	else:
		return render(request,'add_service.html')

def add_event(request):
	service=Service.objects.all()
	user=User.objects.get(email=request.session['email'])

	if request.method=='POST':
		single_category=Service.objects.get(category=request.POST['category'])
		event=Event.objects.create(
			user=user,
			service=single_category,
			sub_category=request.POST['sub_category'],
			hall_name=request.POST['hall_name'],
			location=request.POST['location'],
			price=request.POST['price'],
			desc=request.POST['desc'],
			date=request.POST['date'],
			image=request.FILES['image']
			)
		return render(request,'add_event.html',{'service':service})
	else:
		return render(request,'add_event.html',{'service':service})

def view_service(request):
	service=Service.objects.all()
	return render(request,'view_service.html',{'service':service})

def delete_service(request,pk):
	service=Service.objects.get(pk=pk)
	service.delete()
	return redirect('view_service')

def update_service(request,pk):
	service=Service.objects.get(pk=pk)
	if request.method=='POST':
		service.category=request.POST['category']
		service.save()
		return redirect('view_service')
	else:
		return render(request,'update_service.html',{'service':service})

def view_event(request):
	event=Event.objects.all()
	return render(request,'view_event.html',{'event':event})

def delete_event(request,pk):
	service=Service.objects.all()
	event=Event.objects.get(pk=pk)
	event.delete()
	return redirect('view_event')

def update_event(request,pk):
	user=User.objects.get(email=request.session['email'])
	service=Service.objects.all()
	event=Event.objects.get(pk=pk)

	if request.method=='POST':
		new_service=Service.objects.get(category=request.POST['category'])
		event.user=user
		event.service=new_service
		event.sub_category=request.POST['sub_category']
		event.hall_name=request.POST['hall_name']
		event.price=request.POST['price']
		event.location=request.POST['location']
		event.desc=request.POST['desc']
		event.image=request.FILES['image']
		event.save()
		return redirect('view_event')

	else:
		return render(request,'update_event.html',{'service':service,'event':event})

def user_detail(request):
	user=User.objects.all()
	return render(request,'user_detail.html',{'user':user})
def delete_user(request,pk):
	user=User.objects.get(pk=pk)
	user.delete()
	return redirect('user_detail')

def update_user(request,pk):
	user=User.objects.get(pk=pk)

	if request.method=='POST':
		user.name=request.POST['name']
		user.email=request.POST['email']
		user.number=request.POST['number']
		user.password=request.POST['password']
		user.gender=request.POST['gender']
		user.image=request.FILES['image']
		user.user_type=request.POST['user_type']
		user.save()
		return redirect('user_detail')

	else:
		return render(request,'update_user.html',{'user':user})



#===================================Cart===========================


def add_cart(request,pk):
	event=Event.objects.get(pk=pk)
	cart=Cart.objects.create(
		user=User.objects.get(email=request.session['email']),
		event=event,
		)
	return redirect('cart')


def cart(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user)
	
	net_price=0
	for i in cart:
		net_price+=i.event.price

	


	client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECERT))
	payment = client.order.create({"amount":net_price*100, "currency": "INR", "receipt": "order_rcptid_11"})

	global pay_id
	pay_id=payment['id']


	trans=Transaction.objects.create(
		user=user,
		amount=net_price,
		razorpay_order_id=payment['id']
		)
	

	return render(request,'cart.html',{'cart':cart,'user':user,'net_price':net_price,'trans':trans,'payment':payment})


def delete_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(pk=pk)
	cart.delete()
	return redirect('cart')


def callback(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user)
	trans=Transaction.objects.get(razorpay_order_id=pay_id)

	for i in cart:
		i.payment_status=True
		i.save()
		i.delete()


	return render(request,'callback.html',{'trans':trans,'user':user,'cart':cart})


#==================================Cart End======================

#======================AJax==============================
def validate(request):
	email=request.GET.get('email')
	print(">>>>>>>>>>>>>>>>AJAX DATA : ",email)
	data={'is_taken':User.objects.filter(email__iexact=email).exists()}

	return JsonResponse(data)