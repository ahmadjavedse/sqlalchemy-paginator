'''
Created on Oct 20, 2015

@author: ahmadjaved.se@gmail.com
'''
from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='SQLAlchemy-Paginator',
      version='0.1',
      description='Paginator for SQLAlchemy ORM',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='sqlalchemy pagination paginator paginate sqlalchemy-orm paging slicing sqlalchemy-query',
      url='https://github.com/ahmadjavedse/sqlalchemy-paginator.git',
      author='Ahmad Javed',
      author_email='ahmadjaved.se@gmail.com',
      license='',
      packages=find_packages(exclude=['tests*']),
      include_package_data=True,
      zip_safe=False)