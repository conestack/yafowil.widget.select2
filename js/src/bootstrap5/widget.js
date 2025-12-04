import $ from 'jquery';
import {
    singleValueAjaxAdapter,
    multiValueAjaxAdapter
} from '../adapters/adapters.js';

export class Select2Widget {

    /**
     * Initializes each widget in the given DOM context.
     * 
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
