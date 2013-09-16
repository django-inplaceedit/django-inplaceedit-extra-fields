0.3.0  (2013-09-16)
===================

* AdaptorTinyMCEField now use **tinyMCE 4.X**
* Not the AdaptorTinyMCEField, AdaptorAutoCompleteForeingKeyField and AdaptorAutoCompleteManyToManyField use the static file recolector, new in django-inplaceedit==1.2.1

0.2.1  (2013-09-15)
===================

* Fix an error in AdaptorTinyMCEField when the inplace edit item was very little (its width was very little)
* Update the tinyMCE to last version (3.X)

0.2.0  (2013-09-10)
===================

* Improvements in AdaptorTinyMCEField, and adapt the code to the new features of django-inplaceedit==1.2
* Improvements in the README file

0.1.1  (2013-09-06)
===================

* Update the metainfo

0.1.0  (2013-09-05)
===================

* Fix an error in IE browser with the AdaptorTinyMCEField

0.0.9  (2013-09-05)
===================

* Python 3 compatible (Only AdaptorTinyMCEField, django-ajax-fields and sorl.thumbnail are not python3 compatibles)
* django-inplaceedit (1.0.0) compatible
* django 1.2 support
* Improvements in the README
* Fix some details
* Fix some grammar in README: Thanks to `Flavio Curella <https://github.com/fcurella/>`_

0.0.8  (2012-11-12)
===================

* Fix a little error of the tinyMCE adaptor: Thanks to `Yuego <https://github.com/Yuego/>`_

0.0.7  (2012-08-21)
===================

* Improve the tinyMCE field, modify the settings of the tinyMCE for can do a real inplaceedit, the layout must be the same with the tinyMCE and with a piece of HTML:
    * Now The tinyMCE automatically load the css of the view
    * Create a normalize css, there is a problem with the first element of the documents of the iframe
    * Now you can overwrite the extra_mce_settings from settings
    * Now I can load some css and not load the content.css of the tinyMCE
    * Remove the csmutils dependence
    * Adapt the code to the new option in django-inplaceedit (autosave)
    * Improve the inplace_edit plugin of the tinyMCE editor 
    * Update tinyMCE to last release

0.0.6  (2012-05-22)
===================

* Uncouple cmsutils of the tinyMCE widget overwriting two methods


0.0.5  (2012-05-22)
===================

* Now django-inplaceedit-extra-fields managing `static files <https://docs.djangoproject.com/en/dev/howto/static-files/>`_ (backward compatible)

0.0.4  (2011-12-13)
===================

* Fixes a error in tinyMCE adaptor when the user has not edit permission
* Add MANIFEST.in. Until now, the egg is impossible that work

0.0.3  (2011-12-09)
===================

* More easy overwrite the jquery-ui
* More clean the code of tiny field

0.0.2  (2011-12-08)
===================

* Complete the README


0.0.1  (2011-12-08)
===================

* First version to AdaptorAutoCompleteForeingKeyField and AdaptorAutoCompleteManyToManyField
* First version to AdaptorImageThumbnailField
* First version to AdaptorTinyMCEField
