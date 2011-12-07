from django.conf import settings
from django.template.loader import render_to_string

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField
from inplaceeditform.fields import AdaptorForeingKeyField, AdaptorCommaSeparatedManyToManyField


class AdaptorAutoCompleteProvider(object):

    def get_field(self):
        field = super(AdaptorAutoCompleteProvider, self).get_field()
        lookup = self.config.get('lookup', None)
        if lookup:
            field.field = self.auto_complete_field(lookup, required=field.field.required)
        return field

    def render_media_field(self, template_name="inplaceeditform_extra_fields/autocomplete/render_media_field.html", extra_context=None):
        return super(AdaptorAutoCompleteProvider, self).render_media_field(template_name, extra_context)


    def render_value_edit(self):
        value = super(AdaptorAutoCompleteProvider, self).render_value_edit()
        return render_to_string('inplaceeditform_extra_fields/autocomplete/render_value.html', {'value': value,
                                                                                                'MEDIA_URL': settings.MEDIA_URL,
                                                                                                'is_ajax': self.request.is_ajax()})


class AdaptorAutoCompleteForeingKeyField(AdaptorAutoCompleteProvider, AdaptorForeingKeyField):

    auto_complete_field = AutoCompleteSelectField

    @property
    def name(self):
        return 'auto_fk'


class AdaptorAutoCompleteManyToManyField(AdaptorAutoCompleteProvider, AdaptorCommaSeparatedManyToManyField):

    auto_complete_field = AutoCompleteSelectMultipleField

    @property
    def name(self):
        return 'auto_m2m'

    def get_value_editor(self, value):
        return [pk for pk in value.split("|") if pk]
