/*
 * yafowil select2 widget
 *
 * Optional: bdajax
 */

if (typeof(window.yafowil) == "undefined") yafowil = {};

(function($) {

    $(document).ready(function() {
        // initial binding
        yafowil.select2.binder();

        // add after ajax binding if bdajax present
        if (typeof(window.bdajax) != "undefined") {
            $.extend(bdajax.binders, {
                select2_binder: yafowil.select2.binder
            });
        }
    });

    $.extend(yafowil, {

        select2: {

            extract_value: function(value) {
                if (typeof value == 'string'
                 && value.indexOf('javascript:') == 0) {
                    value = value.substring(11, value.length);
                    value = value.split('.');
                    if (!value.length) {
                        throw "No function defined";
                    }
                    var ctx = window;
                    var name;
                    for (var idx in value) {
                        name = value[idx];
                        if (typeof(ctx[name]) == "undefined") {
                            throw "'" + name + "' not found";
                        }
                        ctx = ctx[name];
                    }
                    value = ctx;
                }
                return value;
            },

            update_options: function(options) {
                var name, value;
                for (var idx in options) {
                    name = options[idx];
                    value = yafowil.select2.extract_value(options[name]);
                    options[name] = value;
                }
                return options;
            },

            binder: function(context) {
                $('.select2', context).each(function(event) {
                    var elem = $(this);
                    var options = yafowil.select2.update_options(elem.data());
                    elem.select2(options);
                });
            }
        }
    });

})(jQuery);
