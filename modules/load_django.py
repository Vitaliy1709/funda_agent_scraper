import sys
import os
import django

sys.path.append('/home/user12/Project/work/funda_project')

os.environ['DJANGO_SETTINGS_MODULE'] = 'funda_project.settings'
django.setup()