from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import RegistrationForm
from .models import Registration, FeeStructure, FeePaymentDetail, SemesterFees
from django.http import JsonResponse
from instamojo_wrapper import Instamojo
from cms.settings import INSTA_MOJO_API_KEY,INSTA_MOJO_AUTH_TOKEN,INSTA_MOJO_SALT
import datetime
# Create your views here.

class StudentRegistrationView(CreateView):
    form_class = RegistrationForm
    model = Registration
    template_name = "student/student_registration.html"
    success_url = "/"

def fetch_fee_detail(request):
    if request.method=='GET':

        student = Registration.objects.get(roll_no = request.GET['rollno'])
        if student != None:
            if student.selected_course.split(' ')[0].lower() == request.GET['course'].lower():             
                fees_data = FeeStructure.objects.get(program_name = request.GET['course'])
                if student.fees == None:
                    data ={
                        '1stsem' : str(fees_data.semester1) + ','+ 'FirstSemester',
                        '2stsem' : str(fees_data.semester2)+ ',' + 'SecondSemester',
                        '3stsem' : str(fees_data.semester3)+ ',' + 'ThirdSemester',
                        '4thsem' : str(fees_data.semester4)+ ',' + 'FourthSemester',
                    }
                elif student.fees.second_semester_fee == None:
                    data ={
                        '2stsem' : str(fees_data.semester2)+ ',' + 'SecondSemester',
                        '3stsem' : str(fees_data.semester3)+ ',' + 'ThirdSemester',
                        '4thsem' : str(fees_data.semester4)+ ',' + 'FourthSemester',
                    }
                elif student.fees.third_semester_fee == None:
                    data ={
                        '3stsem' : str(fees_data.semester3)+ ',' + 'ThirdSemester',
                        '4thsem' : str(fees_data.semester4)+ ',' + 'FourthSemester',
                    } 
                elif student.fees.fourth_semester_fee == None:
                    data ={
                        '4thsem' : str(fees_data.semester4)+ ',' + 'FourthSemester',
                    }
                else:
                    data = {
                        "NA":"No Fees Pending"
                    }                              
                print(data)
                return JsonResponse(data)
            else:
                return JsonResponse({"error" : "invalid course"})
        else:
            return JsonResponse({"error" : "invalid Roll number"})

def payment_success(request):
    return render(request,"student/payment_success.html")        

def fee_payment(request):
    if request.method == "POST":
       rollno = request.POST.get("rollno")
       email = request.POST.get("email")
       fees_data = request.POST.get("semester")
       fees = fees_data.split(',')[0]
       purpose = fees_data.split(',')[1]
       purpose+=','+rollno
       print(fees)
       api = Instamojo(api_key = INSTA_MOJO_API_KEY, auth_token = INSTA_MOJO_AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
       response = api.payment_request_create(
           amount=fees,
           purpose=purpose,
           send_email = True,
           email = email,
           redirect_url = "http://127.0.0.1:8000/register/paymentsuccess/"
       )
        
       print(response.get('payment_request').get('id'))
       return render(request,"student/payment_link_generated.html",{
           'url' :response.get('payment_request').get('longurl'),
           'id' : response.get('payment_request').get('id') 
       })
    else:
        return render(request,'student/fee_payment.html')
# http://127.0.0.1:8000/register/paymentsuccess/?payment_id=MOJO3707O05A81406740&payment_status=Credit&payment_request_id=032be4b50c294f5e86cba6bdb96bf347

def save_fee_details(student,response,semester):
    if response.get('success') == True and response.get('payment_request').get('status') == 'Completed':
        if semester == "FirstSemester" and student.fees == None:
            sem_one = SemesterFees(program_name=student.selected_course,
                    first_semester_fee = response.get('payment_request').get('amount'),
                    first_semester_fee_paid_date =datetime.date.today()   
                    )
            sem_one.save()
            student.fees = sem_one
            student.save()
        elif semester == "SecondSemester" and student.fees.second_semester_fee == None:
            sem_two = SemesterFees.objects.get(id=student.fees.id)
            sem_two.second_semester_fee = response.get('payment_request').get('amount')
            sem_two.second_semester_fee_paid_date =datetime.date.today()   
            sem_two.save()
        elif semester == "ThirdSemester" and student.fees.third_semester_fee == None:
            sem_three = SemesterFees.objects.get(id=student.fees.id)
            sem_three.third_semester_fee = response.get('payment_request').get('amount')
            sem_three.third_semester_fee_paid_date =datetime.date.today()  
            sem_three.save()
        elif semester == "FourthSemester" and student.fees.fourth_semester_fee == None:
            sem_four = SemesterFees.objects.get(id=student.fees.id)
            sem_four.fourth_semester_fee = response.get('payment_request').get('amount')
            sem_four.fourth_semester_fee_paid_date =datetime.date.today()   
            sem_four.save()


def is_fee_paid(request):
    if request.method == "GET":
        payment_id = request.GET['payment_id']
        payment_request_id = request.GET['payment_request_id']
        api = Instamojo(api_key=INSTA_MOJO_API_KEY, auth_token=INSTA_MOJO_AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
        response = api.payment_request_payment_status(payment_request_id,payment_id)
        roll_no = response.get('payment_request').get('purpose').split(',')[1]
        print(response)
        print(response.get('success') == True)
        semester = response.get('payment_request').get('purpose').split(',')[0]
        student = Registration.objects.get(roll_no=roll_no)
        if student != None and student.selected_course != None:
            save_fee_details(student=student, response=response,semester=semester)
            new_payment = FeePaymentDetail(
            rollno=roll_no,
            transaction_id = response.get('payment_request').get('payment').get('payment_id'),
                date = datetime.datetime.now()
            )
            new_payment.save()
        return JsonResponse(response)
    