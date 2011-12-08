from django.conf import settings
from django.template.loader import render_to_string

from inplaceeditform.fields import (AdaptorForeingKeyField,
                                    AdaptorCommaSeparatedManyToManyField,
                                    AdaptorImageField,
                                    AdaptorTextAreaField)

from cmsutils.forms.widgets import TinyMCE
class AdaptorAutoCompleteProvider(object):

    def install_ajax_select(self):
        if 'ajax_select' in settings.INSTALLED_APPS:
            lookup = self.config.get('lookup', None)
            auto_field = self.auto_complete_field
            if lookup and auto_field:
                return True
        return False

    def get_field(self):
        field = super(AdaptorAutoCompleteProvider, self).get_field()
        if self.install_ajax_select():
            lookup = self.config.get('lookup', None)
            auto_field = self.auto_complete_field
            field.field = auto_field(lookup, required=field.field.required)
        return field

    def render_media_field(self,
            template_name="inplaceeditform_extra_fields/adaptor_autocomplete/render_media_field.html",
            extra_context=None):
        if self.install_ajax_select():
            return super(AdaptorAutoCompleteProvider, self).render_media_field(template_name, extra_context)
        return super(AdaptorAutoCompleteProvider, self).render_media_field()


    def render_value_edit(self):
        value = super(AdaptorAutoCompleteProvider, self).render_value_edit()
        if self.install_ajax_select():
            return render_to_string('inplaceeditform_extra_fields/adaptor_autocomplete/render_value.html',
                                    {'value': value,
                                    'MEDIA_URL': settings.MEDIA_URL,
                                    'is_ajax': self.request.is_ajax()})
        return super(AdaptorAutoCompleteProvider, self).render_value_edit()


class AdaptorAutoCompleteForeingKeyField(AdaptorAutoCompleteProvider, AdaptorForeingKeyField):

    @property
    def auto_complete_field(self):
        try:
            from ajax_select.fields import AutoCompleteSelectField
            return AutoCompleteSelectField
        except ImportError:
            return None

    @property
    def name(self):
        return 'auto_fk'


class AdaptorAutoCompleteManyToManyField(AdaptorAutoCompleteProvider, AdaptorCommaSeparatedManyToManyField):

    @property
    def auto_complete_field(self):
        try:
            from ajax_select.fields import AutoCompleteSelectMultipleField
            return AutoCompleteSelectMultipleField
        except ImportError:
            return None

    @property
    def name(self):
        return 'auto_m2m'

    def get_value_editor(self, value):
        return [pk for pk in value.split("|") if pk]


class AdaptorImageThumbnailField(AdaptorImageField):

    # code of: http://dev.merengueproject.org/browser/trunk/merengueproj/merengue/uitools/fields.py?rev=5352#L59

    @property
    def name(self):
        return 'image_thumb'

    def install_sorl_thumbnail(self):
        if 'sorl.thumbnail' in settings.INSTALLED_APPS:
            try:
                from sorl import thumbnail
                return True 
            except ImportError:
                pass
        return False

    def render_value(self,
                    field_name=None,
                    template_name='inplaceeditform_extra_fields/adaptor_image_thumb/render_value.html'):
        if self.install_sorl_thumbnail():
            return super(AdaptorImageThumbnailField, self).render_value(field_name=field_name, template_name=template_name)
        return super(AdaptorImageThumbnailField, self).render_value(field_name=field_name)


class AdaptorTinyMCEField(AdaptorTextAreaField):

    #code of: http://dev.merengueproject.org/browser/trunk/merengueproj/merengue/uitools/fields.py?rev=5352#L65

    @property
    def name(self):
        return 'textarea'

    def __init__(self, *args, **kwargs):
        super(AdaptorTinyMCEField, self).__init__(*args, **kwargs)
        self.widget_options = self.config and self.config.get('widget_options', {})

    def install_cmsutils(self):
        if 'cmsutils' in settings.INSTALLED_APPS:
            try:
                from cmsutils.forms.widgets import TinyMCE
                return True 
            except ImportError:
                pass
        return False

    def get_field(self):
        field = super(AdaptorTinyMCEField, self).get_field()
        if not self.install_cmsutils():
            return field
        tiny_mce_buttons = {
            '0': ['bold', 'italic', 'underline', 'justifyleft',
                  'justifycenter', 'justifyright', 'justifyfull'],
            '1': ['bullist', 'numlist', 'outdent', 'indent'],
            '2': ['undo', 'redo'],
            '3': ['cut', 'copy', 'paste', 'pasteword'],
            '4': ['forecolor', 'link', 'code', 'internal_links'],
            '5': ['iframes', 'image', 'file', 'removeformat'],
            }
        tiny_mce_selectors = {'0': ['fontsizeselect'],
                              '1': ['formatselect', 'fontselect'],
                              '2': ['styleselect']}

        extra_mce_settings = getattr(settings, 'EXTRA_MCE', {})
        extra_mce_settings.update(self._order_tinymce_buttons(tiny_mce_buttons, tiny_mce_selectors))

        tiny_extra_media = getattr(settings, 'TINYMCE_EXTRA_MEDIA', {})
        content_css = [i for i in tiny_extra_media.get('css', [])]
        content_css = ','.join(["%s%s" % (settings.MEDIA_URL, css) for css in content_css])
        content_js = [i for i in tiny_extra_media.get('css', [])]
        extra_mce_settings.update({'inplace_edit': True,
                                   'theme_advanced_blockformats': 'h1,h2,h4,blockquote',
                                   'file_browser_callback': 'CustomFileBrowser',
                                   'theme_advanced_statusbar_location': "bottom",
                                   'theme_advanced_resizing': True,
                                   'theme_advanced_resize_horizontal': True,
                                   'convert_on_click': True,
                                   'content_css': content_css,
                                   'content_js': content_js})
        extra_mce_settings.update(self.widget_options)
        from cmsutils.forms.widgets import TinyMCE
        field.field.widget = TinyMCE(extra_mce_settings=extra_mce_settings,
                                             print_head=False)
        return field

    def render_value_edit(self):
        value = super(AdaptorTinyMCEField, self).render_value_edit()
        if self.install_cmsutils():
            return render_to_string('inplaceeditform_extra_fields/adaptor_tiny/render_value.html',
                                    {'value': value,
                                    'MEDIA_URL': settings.MEDIA_URL,
                                    'adaptor': self,
                                    'is_ajax': self.request.is_ajax()})
        return value

    def render_media_field(self, template_name="inplaceeditform_extra_fields/adaptor_tiny/render_media_field.html"):
        if self.install_cmsutils():
            return super(AdaptorTinyMCEField, self).render_media_field(template_name)
        return super(AdaptorTinyMCEField, self).render_media_field()

    def _order_tinymce_buttons(self, buttons_priorized, selectors_priorized,
                               button_width=20, selector_width=80):

        result = {
            'theme_advanced_buttons1': '',
            'theme_advanced_buttons2': '',
            'theme_advanced_buttons3': '',
            }
        if not 'width' in self.widget_options or not self.widget_options['width']:
            return result

        total_width = int(self.widget_options['width'].replace('px', ''))
        buttons, selectors = self._priorize_tinymce_buttons(buttons_priorized,
                                                            selectors_priorized,
                                                            button_width,
                                                            selector_width)
        buttons_width = len(buttons) * button_width
        selectors_width = len(selectors) * selector_width

        if total_width >= buttons_width + selectors_width:  # one row
            if total_width >= selectors_width:
                result['theme_advanced_buttons1'] = ','.join(buttons)
                result['theme_advanced_buttons2'] = ','.join(selectors)
            else:
                num_selectors = (total_width - buttons_width) / selector_width
                result['theme_advanced_buttons1'] = ','.join(selectors[:num_selectors] + buttons)

        elif total_width * 2 >= buttons_width + selectors_width:  # two rows
            aux_index = total_width / button_width
            if total_width >= buttons_width:
                result['theme_advanced_buttons1'] = ','.join(buttons)
                result['theme_advanced_buttons2'] = ','.join(selectors)
            else:
                result['theme_advanced_buttons1'] = ','.join(buttons[:aux_index])
                result['theme_advanced_buttons2'] = ','.join(selectors + buttons[aux_index:])

        else:
            aux_index = total_width / button_width
            result['theme_advanced_buttons1'] = ','.join(buttons[:aux_index])
            result['theme_advanced_buttons2'] = ','.join(buttons[aux_index:])
            num_selectors = total_width / selector_width
            result['theme_advanced_buttons3'] = ','.join(selectors[:num_selectors])

        return result

    def _priorize_tinymce_buttons(self, buttons, selectors, button_width=20, selector_width=80):
        row_width = int(self.widget_options['width'].replace('px', ''))
        total_width = row_width * 3
        used_width = 0

        buttons_list = []
        selectors_list = []
        # we assume that we have more priority levels on buttons

        for key in buttons:
            if (used_width + button_width * len(buttons[key])) < total_width:
                buttons_list += buttons[key]
                used_width += button_width * len(buttons[key])
            if key in selectors:
                if (used_width + selector_width * len(selectors[key])) < total_width:
                    selectors_list += selectors[key]
                    used_width += selector_width * len(selectors[key])

        return buttons_list, selectors_list
