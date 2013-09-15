function (editor) {
    var self = $.inplaceeditform;
    setTimeout(function () {
       $('#' + editor.id).parents(self.formSelector).find('.apply').data('editor', editor);
       $('#' + editor.id).parents(self.formSelector).find('.cancel').data('editor', editor);
    }, 300);
    var value = $('#' + editor.id).html();
    {% ifequal autosavetiny '1' %}
        editor.on('blur', function () {
            self.methods.bind(self.methods.autoSaveCallBack, {'oldValue': value,
                                                              'tag': $('#' + editor.id)})();
        });
    {% else %}
        editor.on('blur', function () {
            return false;
        });
    {% endifequal %}
    var form = $('#' + editor.id).parents('form');
    editor.addMenuItem('apply', {
        text: 'Apply',
        context: 'edit',
        onclick: function() {
            if (form.data('ajaxTime')) {
                return
            }
            form.find('.apply').click();
        }
    });
    editor.addMenuItem('cancel', {
        text: 'Cancel',
        context: 'edit',
        onclick: function() {
            if (form.data('ajaxTime')) {
                return
            }
            form.find('.cancel').click();
        }
    });
}