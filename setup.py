from setuptools import setup, find_packages


requires = [
    'clld',
]

setup(
    name='lotw_dev',
    version='0.0',
    description='lotw_dev',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=['mock==1.0'],
    test_suite="lotw_dev",
    entry_points="""\
    [paste.app_factory]
    main = lotw_dev:main
    """)
