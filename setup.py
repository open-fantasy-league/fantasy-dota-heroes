import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',  # dont think this is actually necessary
    'pyramid_debugtoolbar',
    'pyramid_mako',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction==1.4.4',  # had some funny issues with some version combinations transaction and zope
    'waitress',
    'docutils',
    'mysql-python',
    'zope.deprecation==4.2.0',
    'zope.interface==4.1.3',
    'zope.sqlalchemy==0.7.6',
    'bcrypt',
    'passlib'
    ]

setup(name='fantasydota',
      version='1.0',
      description='fantasydota',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='fantasydota',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = fantasydota:main
      [console_scripts]
      initialize_fantasydota_db = fantasydota.scripts.initializedb:main
      """,
      )
