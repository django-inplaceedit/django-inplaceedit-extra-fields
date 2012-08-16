(function ($) {
    tinymce.create('tinymce.plugins.InplaceEdit', {
        getIframe: function (ed) {
            return $("#" + ed.id + "_ifr");
        },
        init : function (ed, url) {
            var t = this;
            t.id = ed.id + '-inplace-edit';
            if (ed.settings.inplace_edit) {
                ed.onLoadContent.add(function (ed, ev, ob) {
                    t.getIframe(ed).contents().find('#tinymce').blur(function () {
                        t.save(ed, true);
                    });
                });
                ed.onChange.add(function (ed, ev, ob) {
                    t.save(ed, false);
                });
            }
        },
        save: function (ed, saveInServer) {
            if (ed.isDirty()) {
                ed.save();
            }
            if (saveInServer) {
                this.getIframe(ed).parents(".inplaceeditform").find(".apply").click();
            }
        },
        getInfo: function () {
            return {
                longname : 'Inplace Edit plugin',
                author : 'Yaco',
                authorurl : 'http://www.yaco.es',
                infourl : 'http://www.yaco.es',
                version : tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });

    tinymce.PluginManager.add('inplaceedit', tinymce.plugins.InplaceEdit);
})(jQuery);
