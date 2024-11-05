import $ from 'jquery';

// define custom adapters
$.fn.select2.amd.define('select2/data/singleValueAjaxAdapter',[
        'select2/data/ajax',
        'select2/utils'
    ],
    function (AjaxAdapter, Utils) {
        function SingleValueAjaxAdapter ($element, options) {
            SingleValueAjaxAdapter.__super__.constructor.call(this, $element, options);
        }
        Utils.Extend(SingleValueAjaxAdapter, AjaxAdapter);

        SingleValueAjaxAdapter.prototype.current = function (callback) {
            let value = this.$element.val();
            let vocab = this.$element.data('vocabulary');
            function label(key) {
                return (!vocab || !vocab[key]) ? key : vocab[key];
            }
            callback([{ id: value, text: label(value) }]);
        };

        SingleValueAjaxAdapter.prototype.select = function(data) {
            this.$element.find('option[value="' + data.id + '"]').prop('selected', true);
            AjaxAdapter.prototype.select.call(this, data);
        };

        return SingleValueAjaxAdapter;
    });

$.fn.select2.amd.define('select2/data/multiValueAjaxAdapter',[
    'select2/data/ajax',
    'select2/utils'
],
function (AjaxAdapter, Utils) {
    function MultiValueAjaxAdapter ($element, options) {
        MultiValueAjaxAdapter.__super__.constructor.call(this, $element, options);
    }
    Utils.Extend(MultiValueAjaxAdapter, AjaxAdapter);

    MultiValueAjaxAdapter.prototype.current = function (callback) {
        let value = this.$element.val();
        let vocab = this.$element.data('vocabulary');
        function label(key) {
            return (!vocab || !vocab[key]) ? key : vocab[key];
        }
        let data = [];
        value.split(',').forEach((v) => {
            data.push({ id: v, text: label(v) });
        });
        callback(data);
    };

    MultiValueAjaxAdapter.prototype.select = function(data) {
        AjaxAdapter.prototype.select.call(this, data);
    };

    return MultiValueAjaxAdapter;
});

const singleValueAjaxAdapter = $.fn.select2.amd.require('select2/data/singleValueAjaxAdapter');
const multiValueAjaxAdapter = $.fn.select2.amd.require('select2/data/multiValueAjaxAdapter');

export class Select2Widget {

    /**
     * @param {jQuery} context - DOM context for initialization.
     */
    static initialize(context) {
        $('.select2', context).each(function (event) {
            let elem = $(this);
            if (window.yafowil_array !== undefined &&
                window.yafowil_array.inside_template(elem)) {
                return;
            }
            let options = elem.data();
            new Select2Widget(elem, options);
        });
    }

    /**
     * @param {jQuery} elem - The widget input element.
     * @param {Object} ops - Configuration options.
     */
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

    /**
     * @param {Object} options - The original options.
     * @returns {Object} - The initialized options.
     */
    init_options(options) {
        for (let name in options) {
            options[name] = this.extract_value(options[name]);
        }
        if (options.ajaxurl) {
            options.ajax = {
                url: options.ajaxurl,
                dataType: 'json',
                data: function (params) {
                    return { q: params.term };
                },
                processResults: function (data, params) {
                    if (options.tags && !data.length) {
                        data.push({
                            id: params.term,
                            text: params.term
                        });
                    }
                    let results = data.map(item => ({ id: item.id, text: item.text || item.id }));
                    return { results: results };
                }
            };
            if (options.multiple) {
                options.dataAdapter = multiValueAjaxAdapter;
            } else {
                options.dataAdapter = singleValueAjaxAdapter;
            }
        }

        options.theme = 'bootstrap-5';
        options.selectionCssClass = "select2--medium";
        options.dropdownCssClass = "select2--medium";
        options.width = '500px';

        return options;
    }

    /**
     * Extracts and resolves values from the options.
     * @param {string|Function} value - The value to extract.
     * @returns {Function} - The resolved value.
     */
    extract_value(value) {
        if (typeof value === 'string' && !value.indexOf('javascript:')) {
            value = value.substring(11, value.length).split('.');
            // value.length is always at least 1, because split returns
            // empty string in array.
            if (!value[0].length) {
                throw "No function defined";
            }
            let ctx = window;
            for (let name of value) {
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


//////////////////////////////////////////////////////////////////////////////
// yafowil.widget.array integration
//////////////////////////////////////////////////////////////////////////////

/**
 * Re-initializes widget on array add event.
 */
function select2_on_array_add(inst, context) {
    Select2Widget.initialize(context);
}

/**
 * Registers subscribers to yafowil array events.
 */
export function register_array_subscribers() {
    if (window.yafowil_array === undefined) {
        return;
    }
    window.yafowil_array.on_array_event('on_add', select2_on_array_add);
}
