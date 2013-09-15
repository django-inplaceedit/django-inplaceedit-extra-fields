# -*- coding: utf-8 -*-
# Copyright (c) 2011-2013 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
import sys

from django.conf import settings
from django.forms import widgets
from django.forms.util import flatatt
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.simplejson import JSONEncoder

from inplaceeditform.commons import get_static_url


def get_tinyMCE_js():
    if hasattr(settings, 'INPLACE_TINYMCE_JS'):
        return settings.INPLACE_TINYMCE_JS
    return get_static_url(subfix='inplaceeditform_extra_fields') + "adaptor_tiny/js/tiny_mce_3.5.8/tiny_mce.js"


class TinyMCE(widgets.Textarea):
    """
    TinyMCE widget.

    You can customize the mce_settings by overwriting instance mce_settings,
    or add extra options using update_settings
    """
    mce_settings = dict(
        mode="exact",
        theme="advanced",
        width="100%",
        height=400,
        button_tile_map=True,
        plugins="preview,paste,inplaceedit,table",
        theme_advanced_disable="",
        theme_advanced_buttons1="undo,redo,separator,cut,copy,paste,pastetext,pasteword,separator,preview,separator,bold,italic,underline,justifyleft,justifycenter,justifyright,bullist,numlist,outdent,indent",
        theme_advanced_buttons2="fontselect,fontsizeselect,link,code",
        theme_advanced_buttons3="",
        theme_advanced_buttons4="",
        theme_advanced_toolbar_location="top",
        theme_advanced_toolbar_align="left",
        extended_valid_elements="hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]",
        file_browser_callback="mcFileManager.filebrowserCallBack",
        theme_advanced_resize_horizontal=True,
        theme_advanced_resizing=True,
        theme_advanced_statusbar_location="bottom",
        apply_source_formatting=False,
        editor_deselector="mceNoEditor",
    )

    class Media:  # this is for django admin interface
        js = (get_tinyMCE_js(),)

    def __init__(self, extra_mce_settings={}, *args, **kwargs):
        super(TinyMCE, self).__init__(*args, **kwargs)
        # copy the settings so each instance of the widget can modify them
        # without changing the other widgets (e.g. instance vs class variables)
        self.mce_settings = TinyMCE.mce_settings.copy()
        self.mce_settings['spellchecker_languages'] = getattr(settings, 'TINYMCE_LANG_SPELLCHECKER', '+English=en')
        self.mce_settings['language'] = getattr(settings, 'TINYMCE_LANG', 'en')
        self.mce_settings.update(extra_mce_settings)

    def update_settings(self, custom):
        return_dict = self.mce_settings.copy()
        return_dict.update(custom)
        return return_dict

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        if sys.version_info.major == 2:
            from django.utils.encoding import smart_unicode
            value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        self.mce_settings['elements'] = "id_%s" % name
        if 'functions' in self.mce_settings:
            functions = self.mce_settings['functions']
            del self.mce_settings['functions']
        else:
            functions = ''
        mce_json = JSONEncoder().encode(self.mce_settings)
        return mark_safe(u'''<textarea%s>%s</textarea>
                <script type="text/javascript">
                    %s
                    tinyMCE.init(%s)</script>''' % (flatatt(final_attrs),
                                                    escape(value),
                                                    functions,
                                                    mce_json))
