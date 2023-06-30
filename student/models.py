from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

SUBJECT_CHOICES = (
    ("computer science","computer science"),
    ("bio maths","bio maths"),
)
GRADUATION_SUBJECTS = (
    ("BCA","BCA"),
    ("Bsc Computer Science","Bsc Computer Science"),
    ("Bsc Physics","Bsc Physics"),
    ("Bsc Maths","Bsc Maths"),
    ("Bsc Chemistry","Bsc Chemistry"),
    ("BVoc IT","BVoc IT"),
)
COURSE_OPTIONS =(
    ("MCA","MCA"),
    ("Mvoc Software Development","Mvoc Software Development"),
)
# Create your models here.
class ExamFees(models.Model):
    course_name = models.CharField(max_length=100,null=True )
    first_semester_exam_fee = models.FloatField( null=True, default=None)
    first_semester_exam_fee_paid_date = models.DateTimeField( null=True, default=None)
    second_semester_exam_fee = models.FloatField( null=True, default=None)
    second_semester_exam_fee_paid_date = models.DateTimeField( null=True, default=None)
    third_semester_exam_fee = models.FloatField( null=True, default=None)
    third_semester_exam_fee_paid_date = models.DateTimeField( null=True, default=None)
    fourth_semester_exam_fee = models.FloatField( null=True, default=None)
    fourth_semester_exam_fee_paid_date = models.DateTimeField( null=True, default=None)
    def __str__(self):
        return f"Exam Fees Scheme {self.course_name}"

class SemesterFees(models.Model):
    program_name = models.CharField(max_length=100, null=True)
    pta_fund = models.FloatField( null=True, default=None)
    first_semester_fee = models.FloatField( null=True, default=None)
    first_semester_fee_paid_date = models.DateTimeField( null=True, default=None)
    second_semester_fee = models.FloatField( null=True, default=None)
    second_semester_fee_paid_date = models.DateTimeField( null=True, default=None)
    third_semester_fee = models.FloatField( null=True, default=None)
    third_semester_fee_paid_date = models.DateTimeField( null=True, default=None)
    fourth_semester_fee = models.FloatField( null=True, default=None)
    fourth_semester_fee_paid_date = models.DateTimeField( null=True, default=None)
    exam_fees = models.OneToOneField(
        ExamFees,
        on_delete=models.CASCADE,
        null=True
    )
    def __str__(self):
        return f"Program name : {self.program_name}"


class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(validators=[MaxValueValidator(datetime.date(2000,1,1))])
    xth_pass_year = models.IntegerField(validators = [MinValueValidator(1984),MaxValueValidator(datetime.datetime.now().year - 5)])
    xth_pass_percentage = models.FloatField(validators= [MinValueValidator(50.00), MaxValueValidator(100.00)])
    secondary_pass_year = models.IntegerField(validators = [MinValueValidator(1984),MaxValueValidator(datetime.datetime.now().year -3 )])
    secondary_pass_percentage = models.FloatField(validators= [MinValueValidator(50.00), MaxValueValidator(100.00)])
    secondary_pass_subject = models.CharField(max_length=200, choices= SUBJECT_CHOICES, default="computer science")
    degree_pass_year = models.IntegerField(validators = [MinValueValidator(1984),MaxValueValidator(datetime.datetime.now().year)])
    degree_pass_percentage = models.FloatField(validators= [MinValueValidator(50.00), MaxValueValidator(100.00)])
    degree_subject = models.CharField(max_length=200, choices= GRADUATION_SUBJECTS, default="BCA")
    course_option1 = models.CharField(max_length=200, choices= COURSE_OPTIONS, default="MCA")
    course_option2 = models.CharField(max_length=200, choices=COURSE_OPTIONS, default="Mvoc Software Development")
    selected_course = models.CharField(max_length=20, null=True)
    date_of_admission = models.DateField(null=True)
    roll_no = models.CharField(max_length=20, null=True)
    address = models.TextField(max_length=300)
    gurardian = models.CharField(max_length=100)
    guardian_contact_number = models.CharField(max_length=100)
    guardian_email = models.EmailField(null=True)
    student_email = models.EmailField()
    student_contact_number = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="student_photos", null=True)
    fees = models.OneToOneField(
        SemesterFees,
        on_delete=models.CASCADE,
        null=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.id}"
    
