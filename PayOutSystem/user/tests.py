import time

from django.test import TestCase

# Create your tests here.
print(time.strftime('G%Y%m%d%H%M%S',time.localtime()))