from django.core.management import setup_environ
import settings
setup_environ(settings)
from app.models import *
import sys
import os


def save_countries():
    path = os.path.abspath(os.path.dirname(__file__))
    f = open(path + "/resources/countries", "r")
    for country in f.readlines():
        c, created = Country.objects.get_or_create(
            name=country.replace("\n", ""))
        c.save()


def setup():
    save_countries()


def main():
    if len(sys.argv) < 2:
        sys.exit("Must provide an option")
    else:
        if sys.argv[1] == 'setup':
            setup()

if __name__ == '__main__':
    main()
