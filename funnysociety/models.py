# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#This model is common for everyone- DO NOT Edit without notifying others!
class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    telephoneNumber = models.CharField(max_length=10)
    birthDay = models.TimeField()


#Profile models by Chathura: Only Chathura will edit
#This is a sample table structure, modify as per your requirements
class Friend(models.Model):
        id = models.AutoField(primary_key=True)
        party1 = models.IntegerField()
        party2 = models.IntegerField()
        timestamp = models.TimeField(default=datetime.now, blank=True)
        isPending = models.BooleanField()
        isReceived = models.BooleanField()
        
class Status(models.Model):
        id = models.AutoField(primary_key=True)
        user = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
        text = models.CharField(max_length=999)
        timestamp = models.TimeField(default=datetime.now, blank=True)

class StatusComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    text = models.CharField(max_length=999)
    timestamp = models.TimeField(default=datetime.now, blank=True)
    statusId = models.ForeignKey(Status,on_delete=models.CASCADE)


#Discussion models by Le:  Only Le will edit
#This is a sample table structure, modify as per your requirements
class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    timestamp = models.TimeField(default=datetime.now, blank=True)
    

#Events models by Chris:   Only Chris will edit
#This is a sample table structure, modify as per your requirements
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    startDate = models.TimeField()
    endDate = models.TimeField()
    venue = models.CharField(max_length=500)
    timestamp = models.TimeField(default=datetime.now, blank=True)
    admin = models.ForeignKey(SiteUser,on_delete=models.CASCADE)

class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    category=models.IntegerField()
    timestamp = models.TimeField(default=datetime.now, blank=True)
    
