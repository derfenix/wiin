from distutils.core import setup

setup(
    name='wiin',
    version='0.1.0',
    packages=['wiin'],
    url='',
    requires=[
        'SQLAlchemy(>=0.9)', 'psycopg2', 'Flask_Restless', 'flask(==0.10)',
        'python_dateutil(>2.0)', 'mimerender(>=0.5.2)', 'Flask_SQLAlchemy'
    ],
    license='',
    author='derfenix',
    author_email='derfenix@gmail.com',
    description=''
)
