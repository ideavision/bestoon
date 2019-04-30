# -*- coding: utf-8 -*-

from json import JSONEncoder
from datetime import datetime

from django.core import serializers
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST

from .models import User, Token, Expense, Income, Passwordresetcodes

# Create your views here.


random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# REGISTER
def register(request):
    if request.POST.has_key('requestcode'): #form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        #is this spam? check reCaptcha
        if not grecaptcha_verify(request): # captcha was not correct
            context = {'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'} #TODO: forgot password
            return render(request, 'register.html', context)

        if User.objects.filter(email = request.POST['email']).exists(): # duplicate email
            context = {'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)

        if not User.objects.filter(username = request.POST['username']).exists(): #if user does not exists
                code = random_str(28)
                now = datetime.now()
                email = request.POST['email']
                password = make_password(request.POST['password'])
                username = request.POST['username']
                temporarycode = Passwordresetcodes (email = email, time = now, code = code, username=username, password=password)
                temporarycode.save()
                message = PMMail(api_key = settings.POSTMARK_API_TOKEN,
                                 subject = "Account Activation",
                                 sender = "info@galexit.com",
                                 to = email,
                                 text_body = "برای فعال سازی ایمیلی تودویر خود روی لینک روبرو کلیک کنید: http://\/accounts/register/?email={}&code={}".format(email, code),
                                 tag = "Create account")
                message.send()
                context = {'message': 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'}
                return render(request, 'login.html', context)
        else:
            context = {'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)
    elif request.GET.has_key('code'): # user clicked on code
        email = request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(code=code).exists(): #if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            # Create token
            this_token= random_str(48)
            token=Token.objects.create(user=newuser,token=this_token)
            
            Passwordresetcodes.objects.filter(code=code).delete() #delete the temporary activation code from db
            context = {'message': 'اکانت شما فعال شد. لاگین کنید - البته اگر دوست داشتی'}
            return render(request, 'login.html', context)
        else:
            context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'login.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)




# Create your views here.
@csrf_exempt
def submit_expense(request):
    """ User submits an expense """

    #TODO:validate data, user might be fake, amount might be fake , token might be fake
    this_token = request.POST['token']
    this_user  = User.objects.filter(token__token=this_token).get()
    #TODO: user might want to submit the date herself
    if 'date' not in request.POST:
        date=datetime.now()
    
    Expense.objects.create(user=this_user, amount=request.POST['amount'],
    text=request.POST['text'],date=date )

    # print('I am in submit expense')
    # print (request.POST)

    return JsonResponse({
        'status':'ok',
    },encoder=JSONEncoder)

@csrf_exempt
def submit_income(request):
    """ User Submits an income"""
    #TODO: validate date, user might be fake,token might be fake , amount might be fake
    this_token=request.POSST['token']
    this_user= User.objects.filter(token__token=this_token).get()
    #TODO: user might want to submit the date herself
    if 'date' not in request.POST:
        date=datetime.now()

    Income.objects.create(user=this_user, amount=request.POST['amount'],text=request.POST['text'],date=date)

    return JsonResponse({
        'status':'ok'
    },encoder=JSONEncoder)


