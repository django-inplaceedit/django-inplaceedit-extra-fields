.. contents::

===============================
django-inplaceedit-extra-fields
===============================

Information
===========

.. image:: https://badge.fury.io/py/django-inplaceedit-extra-fields.png
    :target: https://badge.fury.io/py/django-inplaceedit-extra-fields

.. image:: https://pypip.in/d/django-inplaceedit-extra-fields/badge.png
    :target: https://pypi.python.org/pypi/django-inplaceedit-extra-fields

django-inplaceedit-extra-fields is a Django application that adds other useful fields to `django-inplaceedit <http://pypi.python.org/pypi/django-inplaceedit/>`_ .

It is distributed under the terms of the `GNU Lesser General Public
License <http://www.gnu.org/licenses/lgpl.html>`_.

Requirements
============

 * `django-inplaceedit <http://pypi.python.org/pypi/django-inplaceedit/>`_ (>= 1.2.2)

And other packages, depending on which fields you want to use (see below).


Demo (this video use a very old version of django-inplaceedit and django-inplaceedit-extra-fields)
==================================================================================================

Video Demo, of `django-inplaceedit <http://pypi.python.org/pypi/django-inplaceedit/>`_, django-inplaceedit-extra-fields and `django-inlinetrans <http://pypi.python.org/pypi/django-inlinetrans>`_ (Set full screen mode to view it correctly)


.. image:: https://github.com/Yaco-Sistemas/django-inplaceedit/raw/master/video-frame.png
   :target: http://www.youtube.com/watch?v=_EjisXtMy_Y?t=34s



Installation
============

After installing `django-inplaceedit egg`_


.. _`django-inplaceedit egg`: https://django-inplaceedit.readthedocs.org/en/latest/install.html


In your settings.py
-------------------

::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',
        #.....................#
        'inplaceeditform',
        'inplaceeditform_extra_fields',
    )

If you want to overwrite the adaptors for all cases in your project:

::

    ADAPTOR_INPLACEEDIT = {'textarea': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',
                           #'textarea': 'inplaceeditform_extra_fields.fields.AdaptorSimpleTinyMCEField',
                           'image': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
                           'fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
                           'm2mcomma': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField'}

If you want, you can register these fields in your settings with different keys:

::

    ADAPTOR_INPLACEEDIT = {'auto_fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
                           'auto_m2m': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField',
                           'image_thumb': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
                           'tiny': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',
                           'tiny_simple': 'inplaceeditform_extra_fields.fields.AdaptorSimpleTinyMCEField'}

And after that, to want use a specific adaptor you can pass it to the templatetag, e.g.:

::

   {% inplace_edit "content.field_name" adaptor="tiny" %}


Why these fields are not in django-inplaceedit?
===============================================

 * They depend on the other eggs
 * They are a specific solution
 * These do not work immediately, you have to code them


AdaptorAutoCompleteForeingKeyField and AdaptorAutoCompleteManyToManyField
=========================================================================

These fields depend on `django-ajax-selects (1.2.5) <http://pypi.python.org/pypi/django-ajax-selects/1.2.5>`_. You have to create a channel (lookup)

::

    {% inplace_edit "content.field_name" adaptor="auto_fk", lookup="my_lookup" %}

For more info, visit the `doc of django-ajax-selects <https://github.com/twidi/django-ajax-select/blob/master/ajax_select/docs.txt#L40>`_

It is recomended you overwrite the following templates:

 * `inc.css_library.html <http://github.com/goinnn/django-inplaceedit-extra-fields/blob/master/inplaceeditform_extra_fields/templates/inplaceeditform_extra_fields/adaptor_autocomplete/inc.css_library.html>`_
 * `inc.js_library.html <http://github.com/goinnn/django-inplaceedit-extra-fields/blob/master/inplaceeditform_extra_fields/templates/inplaceeditform_extra_fields/adaptor_autocomplete/inc.js_library.html>`_

AdaptorImageThumbnailField
==========================

This field depends on `sorl-thumbnail (11.12) <http://pypi.python.org/pypi/sorl-thumbnail/11.12>`_. You just need to specify the thumb size.

::

    {% inplace_edit "content.field_name" adaptor="image_thumb", size="16x16" %}

It can help you, configure in your settings:

::

    THUMBNAIL_DEBUG = True


For more info, visit the `doc of sorl-thumbnail <http://thumbnail.sorl.net/>`_


AdaptorTinyMCEField and AdaptorSimpleTinyMCEField
=================================================

::

    {% inplace_edit "content.field_name" adaptor="tiny" %}
    or 
    {% inplace_edit "content.field_name" adaptor="tiny_simple" %}


.. note:: 

    We use tinyMCE 4.0 without changes (from django-inplaceedit-extra-fields==0.3.0), if you want to use another version (4.X) of tinyMCE set INPLACE_TINYMCE_JS in your settings.


::

    INPLACE_TINYMCE_JS = '/my/path/of/tinyMCE'


If you want to use a tinyMCE 3.X, please use `django-inplaceedit-extra-fields==0.2.3 <http://pypi.python.org/pypi/django-inplaceedit-extra-fields/0.2.3>`_


Testing
=======

You can test it with the `testing project of django-inplaceedit <https://github.com/Yaco-Sistemas/django-inplaceedit/tree/master/testing>`_ or with the `testing project of django-inplaceedit-bootstrap <https://github.com/goinnn/django-inplaceedit-bootstrap/tree/master/testing>`_ 


Development
===========

You can get the leading edge version of django-inplaceedit-extra-fields by doing a clone
of its repository::

  git clone git@github.com:goinnn/django-inplaceedit-extra-fields.git

