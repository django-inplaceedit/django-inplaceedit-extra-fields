function (editor) {
    var self = $.inplaceeditform;
    setTimeout(function () {
       $('#' + editor.id).parents(self.formSelector).find('.apply').data('editor', editor);
       $('#' + editor.id).parents(self.formSelector).find('.cancel').data('editor', editor);
    }, 300);
    var value = $('#' + editor.id).html();
    var form = $('#' + editor.id).parents(self.formSelector);
    {% ifequal autosave '1' %}
        editor.on('blur', function () {
            if (editor.isDirty()) {
                self.methods.bind(self.methods.autoSaveCallBack, {'oldValue': value,
                                                                  'tag': $('#' + editor.id)})();
            } else {
                form.find('.cancel').click();
            }
        });
    {% else %}
        editor.on('blur', function () {
            return false;
        });
    {% endifequal %}
    {% ifequal add_buttons '1' %}
        editor.addMenuItem('apply', {
            text: 'Apply',
            context: '{{ menubar_item }}',
            onclick: function() {
                if (form.data('ajaxTime')) {
                    return
                }
                form.find('.apply').click();
            }
        });
        editor.addMenuItem('cancel', {
            text: 'Cancel',
            context: '{{ menubar_item }}',
            onclick: function() {
                if (form.data('ajaxTime')) {
                    return
                }
                form.find('.cancel').click();
            }
        });
    {% endifequal %}
}