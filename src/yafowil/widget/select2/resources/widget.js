(function (exports, $) {
    'use strict';

    class Select2Widget {
        static initialize(context) {
            $('.select2', context).each(function (event) {
                let elem = $(this);
                let options = elem.data();
                new Select2Widget(elem, options);
            });
        }
        constructor(elem, ops) {
            this.elem = elem;
            let options = this.update_options(ops);
            options = this.init_options(options);
            try {
                this.elem.select2(options);
            } catch (error) {
                console.log('Failed to initialize select2: ' + error);
            }
        }
        init_options(options) {
            if (options.ajaxurl) {
                options.ajax = {
                    url: options.ajaxurl,
                    dataType: 'json',
                    data: function (term, page) {
                        return { q: term };
                    },
                    results: function (data, page, query) {
                        if (options.tags && !data.length) {
                            data.push({
                                id: query.term,
                                text: query.term
                            });
                        }
                        return { results: data };
                    }
                };
                options.initSelection = function (element, callback) {
                    let value = element.val();
                    if (!value) { return; }
                    let vocab = element.data('vocabulary');
                    function label(key) {
                        return (!vocab || !vocab[key]) ? key : vocab[key];
                    }
                    if (options.multiple) {
                        let data = [];
                        $(element.val().split(",")).each(function() {
                            data.push({ id: this, text: label(this) });
                        });
                        callback(data);
                    } else {
                        callback({ id: value, text: label(value) });
                    }
                };
            }
            return options;
        }
        extract_value(value) {
            if (typeof value === 'string' && !value.indexOf('javascript:')) {
               value = value.substring(11, value.length).split('.');
               if (!value.length) {
                   throw "No function defined";
               }
               let ctx = window;
               for (let idx in value) {
                   let name = value[idx];
                   if (typeof(ctx[name]) === "undefined") {
                       throw "'" + name + "' not found";
                   }
                   ctx = ctx[name];
               }
               value = ctx;
           }
           return value;
        }
        update_options(options) {
            for (let idx in options) {
                let name = options[idx];
                let value = this.extract_value(options[name]);
                options[name] = value;
            }
            return options;
        }
    }

    $(function() {
        if (window.ts !== undefined) {
            ts.ajax.register(Select2Widget.initialize, true);
        } else {
            Select2Widget.initialize();
        }
    });

    exports.Select2Widget = Select2Widget;

    Object.defineProperty(exports, '__esModule', { value: true });


    if (window.yafowil === undefined) {
        window.yafowil = {};
    }

    window.yafowil.select2 = exports;


    return exports;

})({}, jQuery);
//# sourceMappingURL=widget.js.map
