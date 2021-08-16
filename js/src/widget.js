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
                    if (options.ajaxurl) {
                        options.ajax = {
                            url: options.ajaxurl,
                            dataType: 'json',
                            data: function (term, page) {
                                return {
                                    q: term, // search term
                                };
                            },
                            results: function (data, page, query) {
                                if (options.tags && data.length == 0) {
                                    data.push({
                                        id: query.term,
                                        text: query.term
                                    });
                                }
                                return {results: data};
                            }
                        };
                        options.initSelection = function(element, callback) {
                            var value = element.val();
                            if (!value) {
                                return;
                            }
                            var vocabulary = element.data('vocabulary');
                            var label = function(key) {
                                if (!vocabulary) {
                                    return key;
                                }
                                var term = vocabulary[key];
                                if (!term) {
                                    return key;
                                }
                                return term
                            }
                            if (!options.multiple) {
                                callback({id: value, text: label(value)});
                                return;
                            }
                            var data = [];
                            $(element.val().split(",")).each(function() {
                                data.push({id: this, text: label(this)});
                            });
                            callback(data);
                        }
                    }
                    try {
                        elem.select2(options);
                    } catch(error) {
                        console.log('Failed to initialize select2: ' + error);
                    }
                });
            }
        }
    });

})(jQuery);
