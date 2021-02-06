from django.db import models

import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        email_check = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password = postData['password']
        conf_password = postData['conf_password']
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Your first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "You last name should be at least 3 characters"
        if not email_check.match(postData['email']):
            errors["email"] = "Your email should be a valid email"
        email_exist = self.filter(email=postData['email'])
        if email_exist:
            errors['email'] = "Email already in use"
        if len(postData['password']) < 8:
            errors["password_len"] = "Your password should be at least 8 characters"
        if not password == conf_password:
            errors["password"] = "Your passwords do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
