from setuptools import setup, find_packages

setup(
    name='django-facebook',
    version='0.1',
    description='Replace Django Authentication with Facebook',
    long_description=open('README').read(),
    author='Aidan Lister',
    author_email='aidan@php.net',
    url='http://github.com/aidanlister/django-facebook',
    license='MPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
