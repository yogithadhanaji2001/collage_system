from django.db.models.signals import post_save
from django.dispatch import receiver
from User_app.models import CustomUser , Staffs, Students,AdminHOD, Courses, SessionYearModel
from django.core.mail import send_mail


#Creating Django Signals
@receiver(post_save, sender=CustomUser)

# Now Creating a Function which will
# automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
      
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance,
                                    course_id=Courses.objects.get(id=1),
                                    session_year_id=SessionYearModel.objects.get(id=1),
                                    address="",
                                    profile_pic="",
                                    gender="")
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()



@receiver(post_save,sender = CustomUser)

def send_register_mail(sender,instance,created,**kwargs):

    if created:

        

        subject = 'hello from nmc'
        message='welcom to nmc'
        from_email='yogithadhanaji26@gmail.com'
        recipient_list=[instance.email]
        

        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)

        print('mail send')        