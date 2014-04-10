#!python2
# -*- coding: utf-8 -*-
"""
.. module: init_db
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from wiin.models import *

if __name__ == "__main__":
    db.create_all(bind='db1')