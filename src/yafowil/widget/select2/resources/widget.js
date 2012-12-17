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

            binder: function(context) {

                $('select.select2', context).each(function(event) {

                    var extra_keys = [];
                    var elem = $(this);
                    var options = elem.data();

                    function make_options_extra(options, extra_keys) {
                        // cleanup api options object and move out extra options
                        var options_extra = {};
                        for (i=0;i<extra_keys.length;i++) {
                            key = extra_keys[i];
                            options_extra[key] = options[key];
                            delete options[key];
                        }
                        return options_extra;
                    }
                    options_extra = make_options_extra(options, extra_keys);

                    elem.select2(options);

                });

            }
        }
    });


})(jQuery);
