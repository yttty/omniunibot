from setuptools import setup, find_packages
import os

with open(
    os.path.join(os.path.dirname(__file__), "requirements/common.txt"), "r"
) as fh:
    requirements = fh.readlines()

about = {}

with open("README.md", "r") as fh:
    about["long_description"] = fh.read()

VERSION = None

root = os.path.abspath(os.path.dirname(__file__))
if not VERSION:
    with open(os.path.join(root, "omniunibot", "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

print(find_packages())

setup(
    name='omniunibot',
    version=about['__version__'],
    description='A universal multiplatform message bot',
    long_description=about['long_description'],
    long_description_content_type='text/markdown',
    author='yttty',
    author_email='yttty@noreply.com',
    url='https://github.com/yttty/omniunibot',
    zip_safe=False,
    python_requires='>=3.8',
    install_requires=[
        req for req in requirements
    ],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    license='MIT',
    keywords='bots'
)
