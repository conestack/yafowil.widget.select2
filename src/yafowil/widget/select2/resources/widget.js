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
                $('.select2', context).each(function(event) {
                    var elem = $(this);
                    var options = elem.data();
                    elem.select2(options);
                });
            }
        }
    });

})(jQuery);
