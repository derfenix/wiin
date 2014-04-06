=======
INSTALL
=======
-------------------
System dependencies
-------------------
::

   2.7 < python < 3.0

   python-pip

   python-setuptools

   libpq-dev

---------------
Install package
---------------
>>> pip install /path/to/wiin-x.y.z.tar.gz

=============
API ACCESSING
=============
---------
Endpoints
---------
``GET /api/v1/users           get all users``

``GET /api/v1/users/1         get user with id=1``

``PUT/PATCH /api/v1/users/1   change user with id=1``

``POST /api/v1/users          add new user``

``DELETE /api/v1/users        delete user``

--------------------
Queryies and filters
--------------------
    For queries and filters see
    `online documentation
    <https://flaskrestless.readthedocs.org/en/latest/searchformat.html>`_ 
    for Flask Restless

-----------------
Models and fields
-----------------
*Available fields see in models.py*

-------------
Authorization
-------------
``GET /api/v1/login`` 

Response::

{"auth_url": "https://graph.facebook.com/oauth/authorize?redirect_uri=http%3A%2F%2Ftest.fx%3A5000%2Fapi%2Fv1%2Flogin&client_id=304948042989420"}

Open url specified in "auth_url", allow access. Will be redirected to ::

/api/v1/login?code=AQCf0BfOnkex0SVyLDE2ylc3tPlyWYfTJ0Yrfnz69xYvjTL2kh4F0tYYOxJNMOWTxxW7azg-LhGEiQT-YdrmEpDOwWB-rRgvCwXa062taEqwjm1htUhEzbzmAS2rNwVJ3YMuxYEPwCql6h5kw_TbVeiP0n57nOde47n8ulCQm-mJH58pTiEz_X29co9DdVmhLfVcvRZEjJ0bjYOX7kdC2dYf4_r7JmAsKTzHznwO0Xoxz57pqFSXsxEeE_wwGo_SdymJEp-709X7fmncP9wmpc1-fSm55wD3f-bsl5wIj-CTnBbANViFM7yASe-gwuBEcRw#_=_

Response::

{"status": true, "access_token": "CAAEVWTZCGZC2wBAAmijvdzLNwlV4D0O03R0woz7IZBl9zFxZBXe67ajXI7wYXmWBGHJDNk1RabYMdny0ADr57SMuotpEVHvfkCudychFJumlsys5F6J2O35aVyynfJdsHDVHIYhhq5DbEHllYGYyEpZAUX5tBJ9SwRKtjK0lQ7qKDszKuPJQV", "uid": 1}

Store **access_token** (and **uid** if will used more secure version of authentication).
**access_token** (and **uid**) should be appended to each request in GET params ::

/api/v1/posts?access_token=CAAEVWTZCGZC2wBAAmijvdzLNwlV4D0O03R0woz7IZBl9zFxZBXe67ajXI7wYXmWBGHJDNk1RabYMdny0ADr57SMuotpEVHvfkCudychFJumlsys5F6J2O35aVyynfJdsHDVHIYhhq5DbEHllYGYyEpZAUX5tBJ9SwRKtjK0lQ7qKDszKuPJQV
