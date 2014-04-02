from distutils.core import setup

setup(
    name='wiin',
    version='',
    packages=['wiin'],
    url='',
    requires=[
        'SQLAlchemy(>=0.9)', 'psycopg2', 'Flask-Restless', 'flask(==0.10)',
        'python-dateutil(>2.0)', 'mimerender(>=0.5.2)', 'Flask-SQLAlchemy'
    ],
    license='',
    author='derfenix',
    author_email='derfenix@gmail.com',
    description=''
)
