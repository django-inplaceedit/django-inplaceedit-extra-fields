from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from inplaceeditform.commons import get_static_url
from inplaceeditform.fields import (AdaptorForeingKeyField,
                                    AdaptorCommaSeparatedManyToManyField,
                                    AdaptorImageField,
                                    AdaptorTextAreaField)


class AdaptorAutoCompleteProvider(object):

    def __init__(self, *args, **kwargs):
        super(AdaptorAutoCompleteProvider, self).__init__(*args, **kwargs)
        self.config['can_auto_save'] = 0

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
            return render_to_string('inplaceeditform_extra_fields/adaptor_autocomplete/render_value_edit.html',
                                    {'value': value,
                                    'STATIC_URL': get_static_url(),
                                    'STATIC_URL_AJAX_SELECTS': get_static_url('ajax_selects'),
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
        return 'tiny'

    @property
    def classes(self):
        return super(AdaptorTinyMCEField, self).classes + " textareainplaceedit"

    def __init__(self, *args, **kwargs):
        super(AdaptorTinyMCEField, self).__init__(*args, **kwargs)
        self.widget_options = self.config and self.config.get('widget_options', {})
        self.config['can_auto_save'] = 0

    @property
    def TinyMCE(self):
        from inplaceeditform_extra_fields.widgets import TinyMCE
        return TinyMCE

    def treatment_height(self, height, width=None):
        height = super(AdaptorTinyMCEField, self).treatment_height(height, width=width)
        if isinstance(height, basestring) and height.endswith('px'):
            height = height[:-2]
        return height

    def treatment_width(self, width, height=None):
        height = super(AdaptorTinyMCEField, self).treatment_width(width, height=width)
        if isinstance(height, basestring) and height.endswith('px'):
            width = height[:-2]
        return width

    def get_field(self):
        field = super(AdaptorTinyMCEField, self).get_field()
        inplace_edit_auto_save = getattr(settings, 'INPLACEEDIT_AUTO_SAVE', False)
        tiny_mce_buttons = {
            '0': ['apply_inplace_edit', 'cancel_inplace_edit'],
            '1': ['undo', 'redo'],
            '2': ['bold', 'italic', 'underline', 'justifyleft',
                'justifycenter', 'justifyright', 'justifyfull'],
            '3': ['bullist', 'numlist', 'outdent', 'indent'],
        }
        if not inplace_edit_auto_save:
            tiny_mce_buttons['4'] = ['cut', 'copy', 'paste', 'pasteword']
            tiny_mce_buttons['5'] = ['forecolor', 'link', 'code', 'internal_links']
            tiny_mce_buttons['6'] = ['iframes', 'file', 'removeformat']
            tiny_mce_selectors = {'0': ['fontsizeselect'],
                                  '1': ['formatselect', 'fontselect'],
                                  '2': ['styleselect']}
        else:
            tiny_mce_selectors = {}
        extra_mce_settings = {}
        extra_mce_settings.update(self._order_tinymce_buttons(tiny_mce_buttons, tiny_mce_selectors))
        tiny_extra_media = getattr(settings, 'TINYMCE_EXTRA_MEDIA', {})
        content_css = [i for i in tiny_extra_media.get('css', [])]
        css_page = self.config.get('__css', '').split(',')
        content_css = ["%s%s" % (get_static_url(), css) for css in content_css]
        content_css += css_page
        content_css = ','.join(content_css)
        include_content_css = getattr(settings, 'TINYMCE_INCLUDE_CONTENT_CSS', False)
        if content_css:
            js_css = ["ed.dom.loadCSS('%s')" % css for css in content_css.split(',')]
            load_css = """function loadMyCSS(ed) {
                %s
            }""" % ';'.join(js_css)
            extra_mce_settings['init_instance_callback'] = "loadMyCSS"
            extra_mce_settings['functions'] = load_css
        if not content_css or include_content_css:
            content_css = False
        content_js = [i for i in tiny_extra_media.get('css', [])]
        extra_mce_settings.update({'inplace_edit': True,
                                   'inplace_edit_auto_save': getattr(settings, 'INPLACEEDIT_AUTO_SAVE', False),
                                   'theme_advanced_blockformats': 'h1,h2,h4,blockquote',
                                   'theme_advanced_statusbar_location': "none",
                                   'theme_advanced_toolbar_location': "external",
                                   'theme_advanced_resizing': False,
                                   'theme_advanced_resize_horizontal': False,
                                   'content_css': False,
                                   'content_js': content_js})
        if 'height' in self.widget_options:
            extra_mce_settings['height'] = self.treatment_height(self.widget_options['height'], self.widget_options.get('width', None))
            extra_mce_settings['min_height'] = extra_mce_settings['height']
        if 'width' in self.widget_options:
            extra_mce_settings['width'] = self.treatment_width(self.widget_options['width'], self.widget_options.get('height', None))
        extra_mce_settings.update(getattr(settings, 'INPLACE_EXTRA_MCE', {}))
        field.field.widget = self.TinyMCE(extra_mce_settings=extra_mce_settings)
        return field

    def _render_value(self, field_name=None):
        return mark_safe(super(AdaptorTinyMCEField, self).render_value(field_name=field_name))

    def render_value(self, field_name=None):
        value = self._render_value(field_name)
        classes = ' '.join(self.classes.split(' ')[1:])
        return render_to_string('inplaceeditform_extra_fields/adaptor_tiny/render_value.html',
                                {'value': value,
                                 'classes': classes,
                                 'adaptor': self})

    def render_value_edit(self):
        value = self._render_value()
        return render_to_string('inplaceeditform_extra_fields/adaptor_tiny/render_value_edit.html',
                                {'value': value,
                                 'adaptor': self,
                                 'field': self.get_field(),
                                 'is_ajax': self.request.is_ajax()})

    def render_field(self, template_name="inplaceeditform_extra_fields/adaptor_tiny/render_field.html", extra_context=None):
        return super(AdaptorTinyMCEField, self).render_field(template_name=template_name,
                                                             extra_context=extra_context)

    def render_media_field(self,
                          template_name="inplaceeditform_extra_fields/adaptor_tiny/render_media_field.html",
                          extra_context=None):
        return super(AdaptorTinyMCEField, self).render_media_field(template_name=template_name,
                                                                    extra_context=extra_context)

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
            buttons_selectors = buttons + selectors
            theme_advanced_buttons1 = ','.join(buttons_selectors)
            result['theme_advanced_buttons1'] = theme_advanced_buttons1
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
        buttons_keys = buttons.keys()
        buttons_keys.sort()
        for key in buttons_keys:
            if (used_width + button_width * len(buttons[key])) < total_width:
                buttons_list += buttons[key]
                used_width += button_width * len(buttons[key])
            if key in selectors:
                if (used_width + selector_width * len(selectors[key])) < total_width:
                    selectors_list += selectors[key]
                    used_width += selector_width * len(selectors[key])

        return buttons_list, selectors_list
