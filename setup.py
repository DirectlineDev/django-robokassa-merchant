from setuptools import setup, find_packages
from os import path
import codecs


def readfile(file_path):
    return codecs.open(file_path, 'r', 'utf-8').read()


setup(
    name='django-robokassa-merchant',
    version='0.3',

    author='Anton Kuzmichev',
    author_email='assargin@gmail.com',
    license='MIT License',

    packages=find_packages(exclude=("tests",)),

    description='Django Application for Robokassa.ru',
    long_description=readfile(path.join(path.dirname(__file__), 'README.rst')),

    url='https://github.com/DirectlineDev/django-robokassa-merchant',
    download_url='https://github.com/DirectlineDev/django-robokassa-merchant/archive/master.zip',

    keywords=['django', 'robokassa', 'merchant', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable', - coming soon
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
