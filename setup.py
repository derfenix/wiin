from distutils.core import setup

setup(
    name='wiin',
    version='0.2.3',
    packages=['wiin'],
    url='https://www.odesk.com/users/~01286f3481df6273cb',
    # install_requires=open('./requirements.txt', 'r').readlines(),
    license='',
    author='Sergey Kostyuchenko',
    author_email='derfenix@gmail.com',
    description='',
    scripts=['wiin/wiin_init_db.py', 'wiin/wiin_server.py'],
    data_files=[
        ('etc/', ['wiin/wiin.cfg'])
    ],
    package_data={
        'wiin': ['frontend/templates/*', 'frontend/static/*'],
    }
)
