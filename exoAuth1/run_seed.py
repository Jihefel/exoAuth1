import django
django.setup()

from blog.seed import run

if __name__== '__main__':
    run()
