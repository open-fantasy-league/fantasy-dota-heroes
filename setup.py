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
    'SQLAlchemy==1.0',
    'transaction',#==1.4.4',  # had some funny issues with some version combinations transaction and zope
    'waitress',
    'docutils',
    'mysql-python',
    'zope.deprecation',#==4.2.0',
    'zope.interface',#==4.1.3',
    'zope.sqlalchemy',#==0.7.6',
    'bcrypt',
    'passlib',
    'social-auth-app-pyramid',
    'repoze.sendmail',
    'pyramid_tm',
    'pyramid_mailer'
    # the sendmail.repoze thingy needs to be 4.1 not 4.2
    ]

setup(name='fantasyesport',
      version='1.0',
      description='fantasyesport',
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
      test_suite='fantasyesport',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = fantasyesport:main
      [console_scripts]
      initialize_fantasyesport_db = fantasyesport.scripts.initializedb:main
      """,
      )
