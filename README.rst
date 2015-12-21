Email Verif
===========

A `Python <https://www.python.org/>`_ email validator.

Verify if an email address is valid and really exists.

Install
-------

.. code:: bash

    $ pip install git+https://github.com/scls19fr/email-verif

Usage
-----

see `samples <samples>`_ directory

A Command Line Interface is also given

.. code:: bash

    $ email_verif --filename email_to_check.xls --provider YOURPROVIDER --username YOURUSERNAME --password YOURUSERNAME

:code:`YOURPROVIDER` can be :code:`verify-email.org`, :code:`emailhippo.com`, :code:`email-validator.net`
but if you are a developer it shouldn't be hard to add some others.

You can provide an Excel or CSV file using `--filename`.

Development
-----------

You can help to develop this library.



Requirements
^^^^^^^^^^^^

- python-requests http://docs.python-requests.org/

  Requests is an Apache2 Licensed HTTP library, written in Python, for human beings.

- six https://pythonhosted.org/six/

  Six is a Python 2 and 3 Compatibility Library

Optional dependencies
^^^^^^^^^^^^^^^^^^^^^

- https://github.com/reclosedev/requests-cache

  requests-cache is a transparent persistent cache for http://python-requests.org/ library


Issues
^^^^^^

You can submit issues using https://github.com/scls19fr/email-verif/issues

Clone
^^^^^

You can clone repository to try to fix issues yourself using:

::

    $ git clone https://github.com/scls19fr/email-verif.git


Install development version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ python setup.py install

or

::

    $ sudo pip install git+https://github.com/scls19fr/email-verif.git

Collaborating
^^^^^^^^^^^^^

-  Fork repository
-  Create a branch which fix a given issue
-  Submit pull requests

https://help.github.com/categories/collaborating/
