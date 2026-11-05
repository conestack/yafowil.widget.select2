import $ from 'jquery';
import { multiValueAjaxAdapter, singleValueAjaxAdapter } from '../adapters/adapters.js';
import { extract_value } from '../callbacks.js';

export class Select2Widget {
    /**
     * Initializes each widget in the given DOM context.
     *
     * @param {jQuery} context - DOM context for initialization.
     */
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

    /**
     * @param {jQuery} elem - The widget input element.
     * @param {Object} ops - Configuration options.
     */
    constructor(elem, ops) {
        this.elem = elem;
        this.options = this.init_options(ops);

        try {
            // Never from markup: select2 reads the data attributes itself as well.
            this.elem.removeAttr('data-escape-markup').removeData('escapeMarkup');
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
        delete options.escapeMarkup;
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

    /**
     * Extracts and resolves values from the options.
     * @param {string|Function} value - The value to extract.
     * @returns {Function} - The resolved value.
     */
    extract_value(value) {
        return extract_value(value);
    }
}

//////////////////////////////////////////////////////////////////////////////
// yafowil.widget.array integration
//////////////////////////////////////////////////////////////////////////////

/**
 * Re-initializes widget on array add event.
 */
function select2_on_array_add(_inst, context) {
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
