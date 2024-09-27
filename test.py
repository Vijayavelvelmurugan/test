from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import time

# 1st question answer -->By default are django signals executed synchronously or asynchronously? Please
# support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant
# and production ready, we just need to understand your logic.


class Rectangle(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()

# Signal handler
@receiver(post_save, sender=Rectangle)
def rectangle_signal_handler(sender, instance, **kwargs):
    print(f"Signal received! Rectangle length: {instance.length}")
    time.sleep(5)  # Simulate synchronous long-running task
    print(f"Signal received! Rectangle width: {instance.width}")

# Simulate rectangle creation
rect = Rectangle.objects.create(length=10, width=5)
print("Rectangle created!")


#2nd question -->Do django signals run in the same thread as the caller? Please
# support your answer with a code snippet that conclusively proves your stance. The code
# does not need to be elegant and production ready, we just need to understand your logic.

import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


# Define Rectangle model
class Rectangle(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()

# Signal handler
@receiver(post_save, sender=Rectangle)
def rectangle_signal_handler(sender, instance, **kwargs):
    print(f"Signal handler thread: {threading.current_thread().name}")
    print(f"Rectangle length: {instance.length}, width: {instance.width}")

# Simulate rectangle creation
print(f"Caller thread: {threading.current_thread().name}")
rect = Rectangle.objects.create(length=20, width=10)




#3rd Question --> By default do django signals run in the same database transaction 
# as the caller? Please support your answer with a code snippet that conclusively proves
# your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define Rectangle model
class Rectangle(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()

# Signal handler with exception
@receiver(post_save, sender=Rectangle)
def rectangle_signal_handler(sender, instance, **kwargs):
    print(f"Signal received for Rectangle length: {instance.length}")
    raise Exception("Signal handler error!")  # Intentional error

# Simulate rectangle creation in a transaction
try:
    with transaction.atomic():
        rect = Rectangle.objects.create(length=15, width=8)
        print("Rectangle created!")
except Exception as e:
    print(f"Transaction rolled back: {e}")

# Check if the rectangle was created
print(f"Rectangle exists: {Rectangle.objects.filter(length=15).exists()}")











