from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from web.models import Income, Expense, Token, User
from datetime import datetime

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

