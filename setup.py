from setuptools import setup, find_packages


version = '1.0.0'


setup(
    name='djpwrentch',
    version=version,
    description="Common Django functionality library",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Programming Language :: Python",
    ],
    keywords='pwrentch library Python Django',
    author='Paul Rentschler',
    author_email='paul@rentschler.ws',
    url='https://bitbucket.org/paulrentschler/django-pwrentch',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)

