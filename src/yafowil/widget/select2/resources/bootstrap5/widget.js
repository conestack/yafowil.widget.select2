var yafowil_select2 = (function (exports, $) {
    'use strict';

    $.fn.select2.amd.define(
        'select2/data/singleValueAjaxAdapter',
        ['select2/data/ajax', 'select2/utils'],
        (AjaxAdapter, Utils) => {
            function SingleValueAjaxAdapter($element, options) {
                SingleValueAjaxAdapter.__super__.constructor.call(this, $element, options);
            }
            Utils.Extend(SingleValueAjaxAdapter, AjaxAdapter);
            SingleValueAjaxAdapter.prototype.current = function (callback) {
                const value = this.$element.val();
                const vocab = this.$element.data('vocabulary');
                function label(key) {
                    return !vocab?.[key] ? key : vocab[key];
                }
                callback([{ id: value, text: label(value) }]);
            };
            SingleValueAjaxAdapter.prototype.select = function (data) {
                this.$element.find(`option[value="${data.id}"]`).prop('selected', true);
                AjaxAdapter.prototype.select.call(this, data);
            };
            return SingleValueAjaxAdapter;
        },
    );
    $.fn.select2.amd.define(
        'select2/data/multiValueAjaxAdapter',
        ['select2/data/ajax', 'select2/utils'],
        (AjaxAdapter, Utils) => {
            function MultiValueAjaxAdapter($element, options) {
                MultiValueAjaxAdapter.__super__.constructor.call(this, $element, options);
            }
            Utils.Extend(MultiValueAjaxAdapter, AjaxAdapter);
            MultiValueAjaxAdapter.prototype.current = function (callback) {
                const value = this.$element.val();
                const vocab = this.$element.data('vocabulary');
                function label(key) {
                    return !vocab?.[key] ? key : vocab[key];
                }
                const data = [];
                value.split(',').forEach((v) => {
                    data.push({ id: v, text: label(v) });
                });
                callback(data);
            };
            MultiValueAjaxAdapter.prototype.select = function (data) {
                AjaxAdapter.prototype.select.call(this, data);
            };
            return MultiValueAjaxAdapter;
        },
    );
    const singleValueAjaxAdapter = $.fn.select2.amd.require(
        'select2/data/singleValueAjaxAdapter',
    );
    const multiValueAjaxAdapter = $.fn.select2.amd.require('select2/data/multiValueAjaxAdapter');

    class Select2Widget {
        static initialize(context) {
            $('.select2', context).each(function () {
                const elem = $(this);
                if (window.yafowil_array?.inside_template(elem)) {
                    return;
                }
                const options = elem.data();
                new Select2Widget(elem, options);
            });
        }
        constructor(elem, ops) {
            this.elem = elem;
            this.options = this.init_options(ops);
            try {
                this.elem.select2(this.options);
            } catch (error) {
                throw `Failed to initialize select2: ${error}`;
            }
            elem.data('yafowil-select2', this);
        }
        init_options(options) {
            for (const name in options) {
                options[name] = this.extract_value(options[name]);
            }
            if (options.ajaxurl) {
                options.ajax = {
                    url: options.ajaxurl,
                    dataType: 'json',
                    data: (params) => ({ q: params.term }),
                    processResults: (data, params) => {
                        if (options.tags && !data.length) {
                            data.push({
                                id: params.term,
                                text: params.term,
                            });
                        }
                        const results = data.map((item) => ({
                            id: item.id,
                            text: item.text || item.id,
                        }));
                        return { results: results };
                    },
                };
                if (options.multiple) {
                    options.dataAdapter = multiValueAjaxAdapter;
                } else {
                    options.dataAdapter = singleValueAjaxAdapter;
                }
            }
            options.theme = 'bootstrap-5';
            options.selectionCssClass = 'select2--medium';
            options.dropdownCssClass = 'select2--medium';
            options.width = '500px';
            return options;
        }
        extract_value(value) {
            if (typeof value === 'string' && !value.indexOf('javascript:')) {
                value = value.substring(11, value.length).split('.');
                if (!value[0].length) {
                    throw 'No function defined';
                }
                let ctx = window;
                for (const name of value) {
                    if (ctx[name] === undefined) {
                        throw `${name} not found`;
                    }
                    ctx = ctx[name];
                }
                value = ctx;
            }
            return value;
        }
    }
    function select2_on_array_add(_inst, context) {
        Select2Widget.initialize(context);
    }
    function register_array_subscribers() {
        if (window.yafowil_array === undefined) {
            return;
        }
        window.yafowil_array.on_array_event('on_add', select2_on_array_add);
    }

    $(() => {
        if (window.ts !== undefined) {
            ts.ajax.register(Select2Widget.initialize, true);
        } else if (window.bdajax !== undefined) {
            bdajax.register(Select2Widget.initialize, true);
        } else {
            Select2Widget.initialize();
        }
        register_array_subscribers();
    });

    exports.Select2Widget = Select2Widget;
    exports.register_array_subscribers = register_array_subscribers;

    Object.defineProperty(exports, '__esModule', { value: true });


    window.yafowil = window.yafowil || {};
    window.yafowil.select2 = exports;


    return exports;

})({}, jQuery);
