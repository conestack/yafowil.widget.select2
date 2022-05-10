import { Select2Widget } from "../src/widget";

QUnit.module('select2', hooks => {
    let wid;
    let el = $('<input class="select2" value="20"/>');

    hooks.before(()=> {
        // mock select2 - legacy code
        $.fn.extend({
            select2: function () {
                return this.each(function () {});
            }
        });
    });
    hooks.beforeEach(()=> {
        el.appendTo('body');
    });
    hooks.afterEach(()=> {
        el.remove();
        wid = null;
    });
    hooks.after(()=> {
        // remove select2 from jQuery namespace
        delete $.fn.select2;
    });

    QUnit.test('initialize', assert => {
        Select2Widget.initialize();
        wid = el.data('select2');
        assert.ok(wid);
    });

    QUnit.test('ajax', assert => {
        let vocab = ['One','Two','Three'];
        el.data('vocabulary', vocab);

        wid = new Select2Widget(el, {
            1: 'ajaxurl',
            ajaxurl: 'test-ajax-url'
        });
        assert.ok(wid);
        assert.strictEqual(wid.options.ajax.url, 'test-ajax-url');

        wid.options.initSelection(el, function(data){ console.log(data); });
    });

    QUnit.test.only('multiple', assert => {
        let vocab = ['One','Two','Three'];
        el.data('vocabulary', vocab);

        wid = new Select2Widget(el, {
            1: 'ajaxurl',
            ajaxurl: 'test-ajax-url',
            2: 'multiple',
            multiple: true
        });
        assert.ok(wid);
        wid.options.initSelection(el, function(data){ console.log(data); });
    });

    QUnit.test('vocab', assert => {
        let vocab = ['One','Two','Three'];
        el.data('vocabulary', vocab);

        wid = new Select2Widget(el, {multiple: false});
        assert.ok(wid);
    });

    QUnit.test('extract_value', assert => {
        let vocab = ['One','Two','Three'];
        el.data('vocabulary', vocab);

        wid = new Select2Widget(el, {
        });
        assert.ok(wid);
    });
});
