from django.urls import path
from . import views

urlpatterns = [
    path("",views.StudentRegistrationView.as_view(), name="register"),
    path("payfees/", views.fee_payment, name="feepayment"),
    path("payfees/fetch-fees/",views.fetch_fee_detail, name="fee_details"),
    path("paymentsuccess/",views.payment_success),
    path("is-payment-succes",views.is_fee_paid, name="isfeepaid" ),
]
