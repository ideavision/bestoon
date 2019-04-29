from django.urls import include, path
from . import views
from django.conf.urls import url

urlpatterns=[
    url(r'^submit/expense/$',views.submit_expense, name='submit_expense'),

]
