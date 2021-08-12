from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save(self)

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False


# for save in database we have to register method