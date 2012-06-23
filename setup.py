from setuptools import setup, find_packages

setup(
    name='django4facebook',
    version='0.1.0',
    description='Replace Django Authentication with Facebook',
    long_description=open('README.md').read(),
    author='Aidan Lister',
    author_email='aidan@php.net',
    maintainer='Martey Dodoo',
    maintainer_email='django4facebook@marteydodoo.com',
    url='http://github.com/pythonforfacebook/django-facebook',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.2.7',
        'facebook-sdk>0.2.0,>=0.3.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
