from django.test import TestCase

# Create your tests here.
import sys
import datetime

time = datetime.datetime.now()

output = "Hai %s current time is %s " % (sys.argv[1],time)

print(output)