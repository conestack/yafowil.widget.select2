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

export const singleValueAjaxAdapter = $.fn.select2.amd.require('select2/data/singleValueAjaxAdapter');
export const multiValueAjaxAdapter = $.fn.select2.amd.require('select2/data/multiValueAjaxAdapter');
