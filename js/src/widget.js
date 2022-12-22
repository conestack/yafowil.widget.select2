
import $ from 'jquery';

export class Select2Widget {
    static initialize(context) {
        $('.select2', context).each(function (event) {
            let elem = $(this);
            if (elem.parents('.arraytemplate').length) {
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
                data: function (term, page) {
                    return { q: term }; // search term
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
            }
        }
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