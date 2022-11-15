import profile
from django.db.models.signals import post_save , post_delete
from django.db import models
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    if created:
        user= instance
        profile =Profile.objects.create(
            user=user,
            username = user.username,
            email=user.email,
            name = user.first_name
        )
        
        subject = 'Welcome to DevSearch'
        message = 'We glad to have you on our platform!'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently= False
        )
        
def updateProfile(sender, instance, created, **kwargs):
    
    profile = instance
    user = profile.user
    if created == False :
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender,instance,**kwargs):
    try :
        user = instance.user
        user.delete()
    except:
        pass

# registering receiver function....this functon will execute once signal is sent.
post_save.connect(createProfile, sender =User) # createProfile is receiver function ...User model is sender.
post_save.connect(updateProfile, sender =Profile)
post_delete.connect(deleteUser, sender =Profile)
#can be implemented using receiver decorator