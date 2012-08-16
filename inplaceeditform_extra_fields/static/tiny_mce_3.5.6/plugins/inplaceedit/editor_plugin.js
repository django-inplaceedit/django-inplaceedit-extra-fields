(function ($) {
    tinymce.create("tinymce.plugins.InplaceEdit", {
        getIframe: function (ed) {
            return $("#" + ed.id + "_ifr");
        },
        init : function (ed, url) {
            var t = this;
            if (ed.settings.inplace_edit) {
                ed.onLoadContent.add(function (ed, ev, ob) {
                    ed.execCommand('mceFocus', false, 'mce_editor_0');
                    t.getIframe(ed).contents().find("#tinymce").blur(function () {
                        t.saveInServer(ed);
                    });
                });
                ed.onChange.add(function (ed, ev, ob) {
                    t.save(ed);
                });
                ed.addButton("apply_inplace_edit", {
                    title : "Apply",
                    cmd : "mceApplyInplaceEdit",
                    image : url + "/img/apply.gif"
                });
                ed.addButton("cancel_inplace_edit", {
                    title : "Cancel",
                    cmd : "mceCancelInplaceEdit",
                    image : url + "/img/cancel.gif"
                });
                this.ed = ed;
                ed.addCommand("mceApplyInplaceEdit", t.saveInServerBind);
                ed.addCommand("mceCancelInplaceEdit", t.cancelBind);
            }
        },
        saveInServerBind: function () {
            this.plugins.inplaceedit.saveInServer(this);
        },
        cancelBind: function () {
            this.plugins.inplaceedit.cancel(this);
        },
        save: function (ed) {
            if (ed.isDirty()) {
                ed.save();
            }
        },
        saveInServer: function (ed) {
            if (!ed) {
                ed = this;
            }
            this.save(ed);
            this.getIframe(ed).parents(".inplaceeditform").find(".apply").click();
        },
        cancel: function (ed) {
            this.getIframe(ed).parents(".inplaceeditform").find(".cancel").click();
        },
        getInfo: function () {
            return {
                longname : "Inplace Edit plugin",
                author : "Yaco",
                authorurl : "http://www.yaco.es",
                infourl : "http://www.yaco.es",
                version : tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });

    tinymce.PluginManager.add("inplaceedit", tinymce.plugins.InplaceEdit);
})(jQuery);
