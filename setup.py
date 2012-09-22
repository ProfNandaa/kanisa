from setuptools import setup, find_packages

import kanisa

setup(
    name='kanisa',
    version=kanisa.__version__,
    description="A Django app for managing Church websites.",
    long_description=open('README.md').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='http://github.com/dominicrodger/kanisa',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "BeautifulSoup==3.2.1",
        "Django==1.4",
        "PIL==1.1.7",
        "django-autoslug==1.5.0",
        "django-compressor==1.1.2",
        "django-crispy-forms==1.1.4",
        "django-haystack==1.2.7",
        "django-mptt==0.5.2",
        "factory_boy==1.2.0",
        "lxml==2.3.5",
        "markdown==2.2.0",
        "mutagen==1.20",
        "sorl-thumbnail==11.12",
        "tweepy==1.9",
        "Whoosh==2.4.1",
        "wsgiref==0.1.2",
        "git+https://github.com/dominicrodger/django-recurrence.git@dev",
    ],
)
