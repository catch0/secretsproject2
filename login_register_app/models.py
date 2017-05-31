from __future__ import unicode_literals
from django.db import models
import bcrypt
class UserManager(models.Manager):
    def validate(self, form_data):
        print "Inside User.objects.validate method."
        result = {'pass': True}
        errors = []
        if len(form_data['first_name']) == 0:
            errors.append({
                'field': 'first_name', 
                'message': "First name is required."
            })
            result['pass'] = False
        if len(form_data['last_name']) == 0:
            errors.append({
                'field': 'last_name',
                 'message': "Last name is required."
            })
            result['pass'] = False
        if len(form_data['email']) == 0:
            errors.append({
                'field': 'email', 
                'message': "Email is required."
            })
            result['pass'] = False
        if len(form_data['password']) == 0:
            errors.append({
                'field': 'password', 
                'message': "Password is required."
            })
            result['pass'] = False
        if len(form_data['password_confirmation']) == 0:
            errors.append({
                'field': 'password_confirmation',
                'message': "Password confirmation is required."
            })
            result['pass'] = False
        if form_data['password'] != form_data['password_confirmation']:
            errors.append({
                'field': 'password_confirmation',
                'message': "Password confirmation must match password."
            })
            result['pass'] = False
        if errors:
            result['errors'] = errors
        return result
    def createUser(self, form_data):
        password = form_data['password'].encode()
        #Encrypt user's password
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create(
            first_name = form_data['first_name'],
            last_name = form_data['last_name'],
            email = form_data['email'],
            password = encryptedpw
        )
        return user
    def findUser(self, data):
        user= User.objects.filter(id=data['user_id']).first()
        return user
    def login(self, form_data):
        result = {'pass': True}
        errors = []
        user = User.objects.filter(email=form_data['email']).first()
        if user:
            password = form_data['password'].encode()
            user_pass = user.password.encode()
            if bcrypt.hashpw(password, user_pass) == user_pass:
                result['user'] = user
                return result
            errors.append({
            'field': 'password',
            'message': 'Invalid password.'
            })
        else :
            errors.append({
                'field': 'email',
                'message': 'Could not find email. Please register first.'
            }) 
        result['pass'] = False
        result['errors'] = errors
        return result
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Secret(models.Model):
    content=models.CharField(max_length=255)
    user=models.ForeignKey(User, related_name="secrets")
    liked_by=models.ManyToManyField(User, related_name="liked_by")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Secret contents: {}".format(self.content)
