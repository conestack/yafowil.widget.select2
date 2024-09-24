
import $ from 'jquery';

export class Select2Widget {

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
        for (let name in options) {
            options[name] = this.extract_value(options[name]);
        }
        if (options.ajaxurl) {
            options.ajax = {
                url: options.ajaxurl,
                dataType: 'json',
                data: function (params) {  // `params` replaces `term` in Select2 v4.x
                    return { q: params.term };
                },
                processResults: function (data) {  // `processResults` replaces `results`
                    if (options.tags && !data.length) {
                        data.push({
                            id: params.term,
                            text: params.term
                        });
                    }
                    return { results: data };
                }
            };
            $.fn.select2.amd.require(["select2/data/select"], function(Select) {
                let CustomDataAdapter = Select;

                CustomDataAdapter.prototype.current = function (callback) {
                    console.log('current')
                    let value = this.$element.val();
                    console.log(value)

                    let vocab = this.$element.data('vocabulary');
                    function label(key) {
                        return (!vocab || !vocab[key]) ? key : vocab[key];
                    }

                    if (options.multiple) {
                        console.log('multi')
                        let data = [];
                        $(this.$element.val().split(",")).each(function() {
                            data.push({ id: this, text: label(this) });
                        });
                        callback(data);
                    } else {
                        console.log('single')
                        callback([{ id: 'foo', text: value }]);
                    }
                };
            
                let originalSelect = CustomDataAdapter.prototype.select;
                CustomDataAdapter.prototype.select = function (data) {
                    console.log(data)
                    // Your own code
                    // Call the original function while keeping 'this' context
                    originalSelect.bind(this)(data);
                };

                // Finally, use the custom data adapter
                options.dataAdapter = CustomDataAdapter;
            });
        }

        options.theme = 'bootstrap-5';
        options.selectionCssClass = "select2--medium";
        options.dropdownCssClass = "select2--medium";
        options.width = '500px';

        return options;
    }

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

function select2_on_array_add(inst, context) {
    Select2Widget.initialize(context);
}

export function register_array_subscribers() {
    if (window.yafowil_array === undefined) {
        return;
    }
    window.yafowil_array.on_array_event('on_add', select2_on_array_add);
}
