.. contents::

==============================
Inplace Edit Form Extra Fields
==============================

Information
===========

Inplace Edit Form Extra Field is a Django application that adds other useful fields to `Inplace Edit <https://github.com/Yaco-Sistemas/django-inplaceedit>`_.

It is distributed under the terms of the `GNU Lesser General Public
License <http://www.gnu.org/licenses/lgpl.html>`_.

Requirements
============

 * `Django Inplace Edit <http://pypi.python.org/pypi/django-inplaceedit/>`_

And other packages, depending on which fields you want to use (see below).


Demo
====

Video Demo of django-inplaceedit and `Django-inlinetrans <http://pypi.python.org/pypi/django-inlinetrans>`_ (Set full screen mode to view it correctly)


.. image:: https://github.com/Yaco-Sistemas/django-inplaceedit/raw/master/video-frame.png
   :target: http://www.youtube.com/watch?v=_EjisXtMy_Y



Installation
============

After installing `django inplace edit egg`_


.. _`django inplace edit egg`: http://pypi.python.org/pypi/django-inplaceedit/#installation


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
                           'image': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
                           'fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
                           'm2mcomma': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField'}

If you want, you can register these fields in your settings with different keys:

::

    ADAPTOR_INPLACEEDIT = {'auto_fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
                           'auto_m2m': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField',
                           'image_thumb': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
                           'tiny': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',}

And after that, to want use a specific adaptor you can pass it to the templatetag, e.g.:

::

   {% inplace_edit "content.field_name" adaptor="tiny" %}


Why these fields are not in django-inplaceedit
==============================================

 * They depends on the other eggs
 * They are a specific solution
 * These do not work immediately, you have to code them


AdaptorAutoCompleteForeingKeyField and AdaptorAutoCompleteManyToManyField
=========================================================================

These fields depend on `Django Ajax Select <http://pypi.python.org/pypi/django-ajax-selects/>`_. You have to create a channel (lookup)

::

    {% inplace_edit "content.field_name" adaptor="auto_fk", lookup="my_lookup" %}

For more info, visit the `doc of ajax select <https://github.com/twidi/django-ajax-select/blob/master/ajax_select/docs.txt#L40>`_

It is recomended you overwrite the following templates:

 * `inc.css_library.html <http://github.com/goinnn/django-inplaceedit-extra-fields/blob/master/inplaceeditform_extra_fields/templates/inplaceeditform_extra_fields/adaptor_autocomplete/inc.css_library.html>`_
 * `inc.js_library.html <http://github.com/goinnn/django-inplaceedit-extra-fields/blob/master/inplaceeditform_extra_fields/templates/inplaceeditform_extra_fields/adaptor_autocomplete/inc.js_library.html>`_

AdaptorImageThumbnailField
==========================

This field depends on `Sorl thumbnail <http://pypi.python.org/pypi/sorl-thumbnail/>`_. You just need to specify the thumb size.

::

    {% inplace_edit "content.field_name" adaptor="image_thumb", size="16x16" %}

It can help you, configure in your settings:

::

    THUMBNAIL_DEBUG = True


For more info, visit the `doc of thumbnail <http://thumbnail.sorl.net/>`_


AdaptorTinyMCEField
===================

::

    {% inplace_edit "content.field_name" adaptor="tiny" %}


It's highly recommended that in your base.html you include the following CSS, to normalize the first element of the iframe


::

    <link rel="stylesheet" href="{{ STATIC_URL }}adaptor_tiny/css/block_normalize.css"> 

.. note:: 

    We use tinyMCE (version 3.5.6) without changes, except we have added a `inplaceedit plugin <https://github.com/goinnn/django-inplaceedit-extra-fields/tree/master/inplaceeditform_extra_fields/static/adaptor_tiny/js/tiny_mce_3.5.6/plugins/inplaceedit>`_


Development
===========

You can get the leading edge version of inplaceedit-extra-fields by doing a checkout
of its repository:

  https://github.com/goinnn/django-inplaceedit-extra-fields

