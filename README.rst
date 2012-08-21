.. contents::

==============================
Inplace Edit Form Extra Fields
==============================

Information
===========

Inplace Edit Form Extra Field is a Django application that adds other useful fields.

It is distributed under the terms of the GNU Lesser General Public
License <http://www.gnu.org/licenses/lgpl.html>

Requeriments
============

 * `Django Inplace Edit <http://pypi.python.org/pypi/django-inplaceedit/>`_

And other eggs, but it is important: If you want to use one of the fields, you do not have to install its requirements


Demo
====

Video Demo, of django-inplaceedit and `Django-inlinetrans <http://pypi.python.org/pypi/django-inlinetrans>`_ (Set full screen mode to view it correctly)


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

If you want overwrite the adaptors for any case in your project:

::

    ADAPTOR_INPLACEEDIT = {'textarea': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',
                           'image': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
                           'fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
                           'm2mcomma': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField'}

If you want, you can register these fields in your settings, with other keys:

::

    ADAPTOR_INPLACEEDIT = {'auto_fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
                           'auto_m2m': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField',
                           'image_thumb': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
                           'tiny': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',}

And after when you want use this specific adaptor you indicate it, e.g.:

::

   {% inplace_edit "content.field_name" adaptor="tiny" %}


Because these fields are not in django-inplaceedit
==================================================

 * They have dependece of the other eggs
 * They are a particular solution
 * Theese do not work immediately, you have to code them


AdaptorAutoCompleteForeingKeyField and AdaptorAutoCompleteManyToManyField
=========================================================================

These fields are dependent of `Django Ajax Select <http://pypi.python.org/pypi/django-ajax-selects/>`_. You have to create a channel (lookup)

::

    {% inplace_edit "content.field_name" adaptor="auto_fk", lookup="my_lookup" %}

For more info, visit the `doc of ajax select <https://github.com/twidi/django-ajax-select/blob/master/ajax_select/docs.txt#L40>`_

It is recomended overwrite the next templates:

 * `inc.css_library.html <http://github.com/goinnn/django-inplaceedit-extra-fields/blob/master/inplaceeditform_extra_fields/templates/inplaceeditform_extra_fields/adaptor_autocomplete/inc.css_library.html>`_
 * `inc.js_library.html <http://github.com/goinnn/django-inplaceedit-extra-fields/blob/master/inplaceeditform_extra_fields/templates/inplaceeditform_extra_fields/adaptor_autocomplete/inc.js_library.html>`_

AdaptorImageThumbnailField
==========================

This field is dependent of `Sorl thumbnail <http://pypi.python.org/pypi/sorl-thumbnail/>`_. You only should indicate the size.

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


It's very recommended that in your base.html you include the CSS to normalize the first element of the iframe


::

    <link rel="stylesheet" href="{{ STATIC_URL }}adaptor_tiny/css/block_normalize.css"> 



Development
===========

You can get the leading edge version of inplaceedit-extra-fields by doing a checkout
of its repository:

  https://github.com/goinnn/django-inplaceedit-extra-fields

