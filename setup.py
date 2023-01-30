from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
long_description = None
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
print(find_packages())
setup(
    name='omniunibot',
    version='0.0.1',
    description='A universal multiplatform message bot',
    long_description=long_description,  # shown in pypi homepage
    long_description_content_type='text/markdown',
    author='yttty',
    author_email='yttty@noreply.com',
    url='https://github.com/yttty/omniunibot',
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.26.0',
        'loguru>=0.6.0'
    ],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    license='MIT',
    keywords='bots'
)
