(function ($) {
    "use strict";
    tinymce.create("tinymce.plugins.InplaceEdit", {
        getIframe: function (ed) {
            return $("#" + ed.id + "_ifr");
        },
        init : function (ed, url) {
            var t = this;
            if (ed.settings.inplace_edit) {
                ed.onLoadContent.add(function (ed, ev, ob) {
                    ed.settings.auto_focus = ed.id;
                    setTimeout(function() {ed.onMouseUp.dispatch(ed, ev);}, 500);
                    if (ed.settings.inplace_edit_auto_save) {
                        t.getIframe(ed).contents().find("#tinymce").blur(function () {
                            t.saveInServer(ed);
                        });
                    }
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
            var self = $.inplaceeditform;
            var configTag = this.getIframe(ed).parents(self.formSelector).prev().find(self.configSelector);
            var isDirty = ed.isDirty();
            if (configTag.length === 1) {
                var config = configTag.attr();
                var autoSave = self.methods.getOptBool(config, self.opts, "autoSave") && parseInt(config.can_auto_save);
                isDirty = isDirty || !autoSave;
            }
            if (isDirty) {
                ed.save();
            }
            return isDirty;
        },
        saveInServer: function (ed) {
            var self = $.inplaceeditform;
            if (!ed) {
                ed = this;
            }
            var isDirty = this.save(ed);
            if (isDirty) {
                this.getIframe(ed).parents(self.formSelector).find(".apply").click();
            } else {
                this.cancel(ed);
            }
        },
        cancel: function (ed) {
            var self = $.inplaceeditform;
            var that = this;
            setTimeout(function () {
                that.getIframe(ed).parents(self.formSelector).find(".cancel").click();
            }, 0);
        },
        getInfo: function () {
            return {
                longname : "Inplace Edit plugin",
                author : "Pablo Martin",
                authorurl : "http://github.com/goinnn",
                infourl : "https://github.com/goinnn",
                version : tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });

    tinymce.PluginManager.add("inplaceedit", tinymce.plugins.InplaceEdit);
})(jQuery);