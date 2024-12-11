from django.db import models

class Login(models.Model):
    f_sno = models.AutoField(primary_key=True)
    f_userName = models.CharField(max_length=150, unique=True)
    f_Pwd = models.CharField(max_length=100)

    def __str__(self):
        return self.f_userName

class Employee(models.Model):
    f_Id = models.AutoField(primary_key=True)
    f_Image = models.ImageField(upload_to='employee_images/')
    f_Name = models.CharField(max_length=100)
    f_Email = models.EmailField(unique=True)
    f_Mobile = models.CharField(max_length=10)
    f_Designation = models.CharField(max_length=100)
    f_Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    f_Course = models.CharField(max_length=100)
    f_Createdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.f_Name
