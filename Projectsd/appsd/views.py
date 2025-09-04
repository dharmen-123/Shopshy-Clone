from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User ,Product,ProductImages,Query,Payment , Address
from django.http import JsonResponse, HttpResponse
import re # Regular Expresssion
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.core.mail import send_mail
import random

# Create your views here.

def home(request):
    userid =request.session.get('user_id')
    cart=request.session.get('cart',{})
    products = Product.objects.all()
    product_items=[]
    for product in products:
        images=product.product_data.all()
        image_url=[]
        for img in images:
            image_url.append(img.images.url)
        percent=int((product.offprice*product.mrp)/100)
        sellingprice=int(product.mrp-percent)
        data_item={
            'id':product.id,
            'name':product.name,
            'description':product.description,
            'mrp':product.mrp,
            'price':sellingprice,
            'offprice':product.offprice,
            'rating':product.rating,
            'color':product.color,
            'thumbnail':image_url[0],
            'images':image_url
        }
        product_items.append(data_item)
    if userid:
        if cart and cart['userid']==userid:
            count=len(cart['item'])
            return render(request,'home.html',{'userid':userid,'products': product_items ,'count':count})
        else:
            return render(request,'home.html',{'userid':userid,'products': product_items})
    else :
        return render(request,'home.html',{'products': product_items})
    
def login_user(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=User.objects.filter(email=email)
        if email == "chilhateadmin101@gmail.com" and password == "dontenter101" :
                request.session['admin_id']=10001
                return redirect('admin_panel')
        elif password=="":
            messages.error(request,"I Password")
            return redirect('login_user')
            pass
        elif user:
            userdata=User.objects.get(email=email)
            pass1=userdata.password
            if pass1==password:
            #    messages.success(request,"Login Successful")
               user_id=userdata.id
               request.session['user_id']=user_id
               return redirect('home')
            else:
                messages.error(request,"Incorrect Password")
                return redirect('login_user')
        else:
            messages.error(request,"Email is not registered")
            return redirect('login_user')
    else:
        return render(request,'login.html')

def generate_otp():
    return str(random.randint(100000, 999999))

def register_user(request):
    context={}
    if request.method=='POST':
        name=request.POST.get('name','').strip()
        email=request.POST.get('email','').strip()
        number=request.POST.get('number','').strip()
        password=request.POST.get('password','')
        cpassword=request.POST.get('cpassword','')
        
        context.update({
            'name':name,
            'email':email,
            'number':number,
            'password':password,
        })
        if not name:
            messages.error(request,'Enter your name')
            return render(request,'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request,'Email Already exist')
            return render(request,'register.html')
           
        if not number:
            messages.error(request,'Please enter the number')
            return render(request,'register.html')

        if not number.isdigit():
            messages.error(request, 'Contact number must contain only digits.')
            return render(request,'register.html')

        if len(number) != 10:
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return render(request,'register.html')

        if not re.match(r'^[6-9]\d{9}$', number):
            messages.error(request, 'Enter a valid mobile number.')
            return render(request,'register.html')
        
        if not password:
            messages.error(request, 'Enter the password')
            return render(request,'register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request,'register.html')
         
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Password must contain at least one special character.')
            return render(request,'register.html')

        elif password != cpassword:
            messages.error(request,'Password do not match')
            return render(request,'register.html',context)

        User.objects.create(name=name,email=email,number=number,password=password)
        messages.success(request,'Registration successful ! Please login')
        context={}
        return redirect('login_user')
    else:
       return render(request,'register.html',context)

def logout_user(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        return redirect('home')
    messages.error(request,"You are not login")
    return redirect('login_user') 

def change_password_page(request):
    userid =request.session.get('user_id')
    cart=request.session.get('cart')
    if userid:   
        if cart:
            count=len(cart['item'])
            return render(request,'userdetail.html',{'userid':userid,'count':count})
        return render(request,'userdetail.html',{'userid':userid})
    else:
        return redirect('login_user') 

def changepassword_user(request):
    userid =request.session.get('user_id')
    cart=request.session.get('cart')
    if userid:
        if request.method=='POST':
            print("hello.....................")
            oldpassword=request.POST.get('oldpassword')
            newpassword=request.POST.get('newpassword')
            password=User.objects.get(id=userid)
            print(password.password)
            if password.password == oldpassword:
                password.password=newpassword
                password.save()
                messages.success(request,"Password Update Successfully",extra_tags='update' )
                return redirect('change_password_page')    
            else:
                messages.error(request,"Old password is not correct",extra_tags='update')
                return redirect('change_password_page')    
        return redirect('change_password_page')    
    return redirect('login_user')        

def my_account(request):
    userid =request.session.get('user_id')
    cart=request.session.get('cart')
    if userid:
        name=User.objects.get(id=userid).name
        if cart:
            count=len(cart['item'])
            return render(request,'useraccount.html',{'userid':userid,'count':count,'name':name})
        return render(request,'useraccount.html',{'userid':userid,'name':name})  
    else :
        return redirect('login_user')

def login_cart(request):
    return render(request,'cart.html')
    
def cart_user(request):
    userid= request.session.get('user_id')
    cart=request.session.get('cart',{})
    print(cart)
    if userid:
        if cart and cart['userid']==userid:
            count=len(cart['item'])
            print(cart)
            l=[]
            totalprice=0
            totalmrp=0
            for i,j in zip(cart['item'],cart['quantity']):
               products=Product.objects.get(id=i)
               images=products.product_data.all()
               image_url=[]
               for img in images:
                   image_url.append(img.images.url)
               percent=int((products.offprice*products.mrp)/100)
               sellingprice=int(products.mrp-percent)    
               product_detail={
                   'id':products.id,
                   'name':products.name,
                   'description':products.description,
                   'mrp':products.mrp*j,
                   'offprice':products.offprice,
                   'price':sellingprice*j,
                   'rating':products.rating,
                   'quantity':j,
                   'thumbnail':image_url[0],
                   'color':products.color,
                   'category':products.category,
                   'itemtype':products.itemtype,
                   'images':image_url
               }
               totalmrp+=products.mrp*j
               totalprice+=sellingprice*j
               l.append(product_detail)
            savings=totalmrp-totalprice   
            return render(request,'cart.html',{'userid':userid,'count':count,'cartitems':l,'totalmrp':totalmrp,'totalprice':totalprice+3,'savings':savings})
        else:
            return render(request,'cart.html',{'userid':userid})
    else:
        return redirect('login_cart')
    

def show_item(request,ds,pk):
    products=Product.objects.get(id=pk)
    images=products.product_data.all()
    image_url=[]
    for img in images:
        image_url.append(img.images.url)
    percent=int((products.offprice*products.mrp)/100)
    sellingprice=int(products.mrp-percent)    
    product_detail={
        'id':products.id,
        'name':products.name,
        'description':products.description,
        'mrp':products.mrp,
        'offprice':products.offprice,
        'price':sellingprice,
        'rating':products.rating,
        'thumbnail':image_url[0],
        'color':products.color,
        'category':products.category,
        'itemtype':products.itemtype,
        'images':image_url
    }
    userid= request.session.get('user_id')
    cart=request.session.get('cart',{})
    # print("Count of cart",count)
    if userid:
        if cart:
            count=len(cart['item'])
            return render(request,'showitem.html',{'products':product_detail,'userid':1,'count':count})
        else:
            return render(request,'showitem.html',{'products':product_detail,'userid':1})
    return render(request,'showitem.html',{'products':product_detail})
   
from django.db.models import Q
   
def categoryproducts(request,name):
    userid =request.session.get('user_id')
    cart=request.session.get('cart',{})
    products = Product.objects.filter(Q(itemtype__icontains=name) & Q(category__icontains=name) & Q(description__icontains=name))
    product_items=[]
    for product in products:
        images=product.product_data.all()
        image_url=[]
        for img in images:
            image_url.append(img.images.url)
        percent=int((product.offprice*product.mrp)/100)
        sellingprice=int(product.mrp-percent)
        data_item={
            'id':product.id,
            'name':product.name,
            'description':product.description,
            'mrp':product.mrp,
            'price':sellingprice,
            'offprice':product.offprice,
            'rating':product.rating,
            'color':product.color,
            'thumbnail':image_url[0],
            'images':image_url
        }
        product_items.append(data_item)
    if userid:
        if cart and cart['userid']==userid:
            count=len(cart['item'])
            return render(request,'allproducts.html',{'userid':userid,'products': product_items ,'count':count})
        else:
            return render(request,'allproducts.html',{'userid':userid,'products': product_items})
    else :
        return render(request,'allproducts.html',{'products': product_items})

def searchvalue(request):
    userid =request.session.get('user_id')
    cart=request.session.get('cart',{})
    if request.method=='POST':
        searchvalue=request.POST.get('search')
        products = Product.objects.filter(Q(itemtype__icontains=searchvalue) & Q(category__icontains=searchvalue) & Q(description__icontains=searchvalue) & Q(name__icontains=searchvalue))
        product_items=[]
        for product in products:
            images=product.product_data.all()
            image_url=[]
            for img in images:
                image_url.append(img.images.url)
            percent=int((product.offprice*product.mrp)/100)
            sellingprice=int(product.mrp-percent)
            data_item={
                'id':product.id,
                'name':product.name,
                'description':product.description,
                'mrp':product.mrp,
                'price':sellingprice,
                'offprice':product.offprice,
                'rating':product.rating,
                'color':product.color,
                'thumbnail':image_url[0],
                'images':image_url
            }
            product_items.append(data_item)
        if userid:
            if cart and cart['userid']==userid:
                count=len(cart['item'])
                return render(request,'allproducts.html',{'userid':userid,'products': product_items ,'count':count})
            else:
                return render(request,'allproducts.html',{'userid':userid,'products': product_items})
        else :
            return render(request,'allproducts.html',{'products': product_items})

def add_to_cart(request,ds,pk):
    userid=request.session.get('user_id')
    if userid:
        if request.method=='POST':
            cart=request.session.get('cart',{})
            print(cart)
            if 'userid' not in cart:
                cart['userid']=userid
            if 'item' not in cart:
                cart['item']=[]
            if 'quantity' not in cart:
                cart['quantity']=[]
            if cart['userid']==userid:
                if pk not in cart['item']:
                    cart['item'].append(pk)
                    cart['quantity'].append(1)
            request.session['cart']=cart
            print(cart)
            return redirect('show_item',ds=ds,pk=pk)    
    else:
       return redirect('login_user')

def remove_item(request,pk):
    cart=request.session.get('cart',{})
    if cart:
       print(cart)
       index_item=cart['item'].index(pk)
       cart['item'].remove(pk)
       item_qua=cart['quantity'][index_item]
       cart['quantity'].remove(item_qua)
       request.session.modified=True
       return redirect('cart_user')
    else:
       return redirect('cart_user')

def increase_quantity(request,pk):
    cart=request.session.get('cart',{})
    if cart:
        item_index=cart['item'].index(pk)
        item_qua=cart['quantity'][item_index]
        if item_qua<5:
            cart['quantity'][item_index]+=1
            request.session.modified=True
            return redirect('cart_user')
        else :
            messages.success(request,"Quantity not more then 5 of item",extra_tags='increase-msg')
            return redirect('cart_user')
    else:
        return redirect('cart_user')

def decrease_quantity(request,pk):
    cart=request.session.get('cart',{})
    if cart:
        item_index=cart['item'].index(pk)
        item_qua=cart['quantity'][item_index]
        if item_qua>1:
            cart['quantity'][item_index]-=1
            request.session.modified=True
            return redirect('cart_user')
        else :
            messages.error(request,"Quantity not less than 1 of item",extra_tags='decrease-msg')
            return redirect('cart_user')
    else:
        return redirect('cart_user')

# # -------------------- Admin Panel Views Code ------------------# #

def admin_panel(request):
    if not request.session['admin_id']:
        return redirect('login_user')
    else:
        dashboard="Admin dashboard"
        if request.method=='POST':
           return render(request,'admindashboard.html',{'dashboard':dashboard})
        return render(request,'admindashboard.html',{'dashboard':dashboard})
        
def admin_logout(request):
    if request.session.get('admin_id'):
        if request.method=='POST':
            if request.session['admin_id']:
                del request.session['admin_id']
                return redirect('home')
            else:
                return redirect('home')   
    else:
        return redirect('Login_user')     
    return redirect('home')


def add_product_btn(request):
    product="products"
    if request.method=='POST':
       return render(request,'admindashboard.html',{'product':product})
    return render(request,'admindashboard.html',{'product':product})

def customers(request):
    customers="customers"
    if request.method=='POST':
       customers=User.objects.all() 
       return render(request,'admindashboard.html',{'customers':customers})
    return render(request,'admindashboard.html',{'customers':customers})

def submit_product(request):
    if request.method=='POST':
        data=request.POST
        name=data.get('name',None)
        description=data.get('description',None)
        category=data.get('category',None)
        mrp=int(data.get('mrp',None))
        offprice=int(data.get('offprice',None))
        rating=float(data.get('rating',None))
        itemtype=data.get('itemtype',None)
        color=data.get('color',None)
        images=request.FILES.getlist('images',None)

        product=Product.objects.create(
            name=name,description=description,category=category,
           mrp=mrp,offprice=offprice,rating=rating,itemtype=itemtype,color=color)
        for img in images:
            ProductImages.objects.create(product=product,images=img)
        return redirect('add_product')   
    else:
        return redirect('add_product')   

def admin_all_product(request):
    if request.session.get('admin_id'):
        if request.method=='POST':
            products = Product.objects.all()
            product_items=[]
            for product in products:
               images=product.product_data.all()
               image_url=[]
               for img in images:
                   image_url.append(img.images.url)
               percent=int((product.offprice*product.mrp)/100)
               sellingprice=int(product.mrp-percent)
               data_item={
                   'id':product.id,
                   'name':product.name,
                   'description':product.description,
                   'mrp':product.mrp,
                   'price':sellingprice,
                   'offprice':product.offprice,
                   'rating':product.rating,
                   'category':product.category,
                   'itemtype':product.itemtype,
                   'color':product.color,
                   'thumbnail':image_url[0],
                   'images':image_url
               }
               product_items.append(data_item)
            return render(request,'admindashboard.html',{'allproduct':product_items})
        dashboard="dashboard"
        return render(request,'admindashboard.html',{'dashboard':dashboard})


def checkout(request):
    userid= request.session.get('user_id')
    cart=request.session.get('cart',{})
    if userid:
        userdata=User.objects.get(id=userid)
        if cart and cart['userid']==userid:
            count=len(cart['item'])
            print(cart)
            l=[]
            totalprice=0
            totalmrp=0
            for i,j in zip(cart['item'],cart['quantity']):
               products=Product.objects.get(id=i)
               percent=int((products.offprice*products.mrp)/100)
               sellingprice=int(products.mrp-percent)    
               product_detail={
                        'id':products.id,
                        'mrp':products.mrp*j,
                        'offprice':products.offprice,
                        'price':sellingprice*j,
                        'quantity':j
                }
               totalmrp+=products.mrp*j
               totalprice+=sellingprice*j
               l.append(product_detail)
            savings=totalmrp-totalprice   
            addressall=Address.objects.filter(userid=userid) 
            return render(request,'addresspage.html',{'userid':userid,'count':count,'cartitems':l,'totalmrp':totalmrp,'totalprice':totalprice+3,
            'savings':savings,'userdata':userdata,'address':addressall})
        else:
            return render(request,'addresspage.html',{'userid':userid,'userdata':userdata})
    else:
        return redirect('login_cart')

def user_address(request):
    userid= request.session.get('user_id')
    cart=request.session.get('cart',{})
    if userid:  
        userdata=User.objects.get(id=userid)
        if request.method=='POST':
            data=request.POST
            alternateno=data.get('alternateno')
            address1=data.get('address1')
            address2=data.get('address2')
            country=data.get('country')
            zipcode=data.get('zipcode')
            city=data.get('city')
            state=data.get('state')
            Address.objects.create(userid=userid,alternateno=alternateno,
            address1=address1,address2=address2,country=country,zipcode=zipcode,
            city=city,state=state)  
            if cart and cart['userid']==userid:
               count=len(cart['item'])
               print(cart)
               l=[]
               totalprice=0
               totalmrp=0
               for i,j in zip(cart['item'],cart['quantity']):
                  products=Product.objects.get(id=i)
                  percent=int((products.offprice*products.mrp)/100)
                  sellingprice=int(products.mrp-percent)    
                  product_detail={
                        'id':products.id,
                        'mrp':products.mrp*j,
                        'offprice':products.offprice,
                        'price':sellingprice*j,
                        'quantity':j 
                  }
                  totalmrp+=products.mrp*j
                  totalprice+=sellingprice*j
                  l.append(product_detail)
               savings=totalmrp-totalprice  
               addressall=Address.objects.filter(userid=userid) 
               return render(request,'addresspage.html',{'userid':userid,'count':count,'cartitems':l,'totalmrp':totalmrp,
               'totalprice':totalprice+3,'savings':savings,'userdata':userdata,
               'address':addressall,'paybtn':101})
            else:
               return render(request,'addresspage.html',{'userid':userid,'userdata':userdata})
    else:
        return redirect('login_cart')

def selectaddress(request):
    userid= request.session.get('user_id')
    cart=request.session.get('cart',{})
    if userid:
        if request.method=='POST':
            addressid=request.POST.get('alladdress')
            saddress=Address.objects.get(id=addressid)
            userdata=User.objects.get(id=userid)
            if cart and cart['userid']==userid:
                 count=len(cart['item'])
                 print(cart)
                 l=[]
                 totalprice=0
                 totalmrp=0
                 for i,j in zip(cart['item'],cart['quantity']):
                    products=Product.objects.get(id=i)
                    percent=int((products.offprice*products.mrp)/100)
                    sellingprice=int(products.mrp-percent)    
                    product_detail={
                        'id':products.id,
                        'mrp':products.mrp*j,
                        'offprice':products.offprice,
                        'price':sellingprice*j,
                        'quantity':j,
                    }
                    totalmrp+=products.mrp*j
                    totalprice+=sellingprice*j
                    l.append(product_detail)
                 savings=totalmrp-totalprice   
                 return render(request,'addresspage.html',{'userid':userid,'count':count,'cartitems':l,'totalmrp':totalmrp,'totalprice':totalprice+3,
                 'savings':savings,'userdata':userdata,'paybtn':101})
            else:
                return render(request,'addresspage.html',{'userid':userid,'userdata':userdata})
    else:
        return redirect('login_cart')  

 
csrf_exempt
def payment(request):
     if request.method == "POST":
        print("hello")
        userid= request.session.get('user_id')
        amount = int(request.POST.get('amount')) * 100  # Convert to paise
        client = razorpay.Client(auth=("rzp_test_8MpcoTaUXnGlMQ", "wz2Q1xWs4LueA8LZwxIBMuPR"))
        order_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_rcptid_11",
            "payment_capture": 1
        }
        order = client.order.create(data=order_data)
        Payment.objects.create(
        order_id=order["id"],
        amount=amount,
        status="Created",
        user_id=userid
        )
        payment = {
            "order_id": order["id"],
            "amount": amount,
            "razorpay_key": "rzp_test_8MpcoTaUXnGlMQ",
            "currency": "INR",
            "callback_url": "/paymenthandle/"
        }
        cart=request.session.get('cart',{})
        if userid:
            if cart and cart['userid']==userid:  
                count=len(cart['item'])
                l=[]
                totalprice=0
                totalmrp=0
                for i,j in zip(cart['item'],cart['quantity']):
                   products=Product.objects.get(id=i)
                   percent=int((products.offprice*products.mrp)/100)
                   sellingprice=int(products.mrp-percent)    
                   product_detail={
                       'id':products.id,
                       'name':products.name,
                       'description':products.description,
                       'mrp':products.mrp*j,
                       'offprice':products.offprice,
                       'price':sellingprice*j,
                       'rating':products.rating,
                       'quantity':j,
                       'color':products.color,
                       'category':products.category,
                       'itemtype':products.itemtype,
                   }
                   totalmrp+=products.mrp*j
                   totalprice+=sellingprice*j
                   l.append(product_detail)
                savings=totalmrp-totalprice   
                return render(request,'addresspage.html',{'userid':userid,'count':count,'cartitems':l,'totalmrp':totalmrp,'totalprice':totalprice+3,'savings':savings,'payment':payment})
            else:
                return render(request,'addresspage.html',{'userid':userid})
        else:
            return redirect('login_cart')
     return render(request,'addresspage.html',{'userid':userid,'count':count,'cartitems':l,'totalmrp':totalmrp,'totalprice':totalprice+3,'savings':savings})

@csrf_exempt  
def paymenthandle(request):
    userid=request.session.get('user_id')
    if request.method=='POST':
        client = razorpay.Client(auth=("rzp_test_8MpcoTaUXnGlMQ", "wz2Q1xWs4LueA8LZwxIBMuPR"))
        params_dict = {
            'razorpay_order_id': request.POST.get('razorpay_order_id'),
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_signature': request.POST.get('razorpay_signature')
        }
        # Verify the payment signature
        client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=request.POST.get('razorpay_order_id'))
        payment.payment_id = request.POST.get('razorpay_payment_id')
        payment.signature = request.POST.get('razorpay_signature')
        payment.status = "Paid"
        payment.save()
        send_mail(
                "Payment done", 
                "A successful payment is a transaction where a customer's payment method is successfully processed, resulting in the completion of a purchase or service. This means the customer's funds have been transferred to the recipient, and the transaction is finalized without any errors or issues. It's a critical indicator of a smooth checkout experience and directly impacts customer satisfaction and business revenue. ",
                "dharmendrachilhate11@gmail.com",
                [],
                fail_silently=False,
         )
        cart=request.session.get('cart',{})
        if userid:
            if cart and cart['userid']==userid: 
                cart['item'].clear() 
                cart['quantity'].clear() 
                request.session.modified=True   
                print(cart)
        return redirect('home')