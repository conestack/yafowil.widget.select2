// Import mock first to set up $.fn.select2.amd before widget module loads.
// A side effect import is never reordered by import sorting.
import './select2_mock.js';
import { multiValueAjaxAdapter, singleValueAjaxAdapter } from '../src/adapters/adapters.js';
import * as bs5_widget from '../src/bootstrap5/widget.js';
import * as default_widget from '../src/default/widget.js';
import { $ } from './select2_mock.js';

const widget_variants = [
    ['default', default_widget, undefined],
    ['bootstrap5', bs5_widget, 'bootstrap-5'],
];

for (const [variant, widget_module, theme] of widget_variants) {
    QUnit.module(`select2 ${variant}`, (hooks) => {
        const { register_array_subscribers, Select2Widget } = widget_module;
        let wid;
        const el = $('<input class="select2" value=""/>');
        const vocab = ['One', 'Two', 'Four'];
        let _array_subscribers = {
            on_add: [],
        };

        hooks.beforeEach(() => {
            el.appendTo('body');
            el.data('vocabulary', vocab);
        });
        hooks.afterEach(() => {
            // Reset select2 but preserve AMD mock for subsequent tests
            const savedAmd = $.fn.select2.amd;
            $.fn.select2 = function () {
                return this;
            };
            $.fn.select2.amd = savedAmd;
            el.remove();
            wid = null;
        });

        QUnit.test('initialize', (assert) => {
            $.fn.extend({
                select2: function () {
                    assert.step('select2 called');
                    return this;
                },
            });
            Select2Widget.initialize();
            wid = el.data('yafowil-select2');
            assert.ok(wid);

            assert.verifySteps(['select2 called']);
        });

        QUnit.test('register_array_subscribers', (assert) => {
            $.fn.extend({
                select2: function () {
                    assert.step('select2 called');
                    return this;
                },
            });

            // return if window.yafowil === undefined
            register_array_subscribers();
            assert.deepEqual(_array_subscribers.on_add, []);

            // patch yafowil_array
            window.yafowil_array = {
                on_array_event: (evt_name, evt_function) => {
                    _array_subscribers[evt_name] = evt_function;
                },
                inside_template(elem) {
                    return elem.parents('.arraytemplate').length > 0;
                },
            };
            register_array_subscribers();

            // create table DOM
            const table = $('<table />').append($('<tr />')).append($('<td />')).appendTo('body');

            $('td', table).addClass('arraytemplate');
            el.detach().appendTo($('td', table));

            // invoke array on_add - returns
            _array_subscribers.on_add.apply(null, $('tr', table));
            wid = el.data('yafowil-select2');
            assert.notOk(wid);
            $('td', table).removeClass('arraytemplate');
            assert.verifySteps([]);

            // invoke array on_add
            $('td', table).removeClass('arraytemplate');
            _array_subscribers.on_add.apply(null, $('tr', table));
            wid = el.data('yafowil-select2');
            assert.ok(wid);
            assert.verifySteps(['select2 called']);

            table.remove();
            window.yafowil_array = undefined;
            _array_subscribers = undefined;
        });

        QUnit.test('fail initialize', (assert) => {
            // fails because of faulty elem
            assert.throws(() => {
                new Select2Widget(el[0], { ajaxurl: 'test' });
            }, /Failed to initialize select2: TypeError: this.elem.select2 is not a function/);
        });

        QUnit.test('ajax', (assert) => {
            $.fn.extend({
                select2: function (opts) {
                    return this.each((_i, el) => {
                        $(el).on('change', () => {
                            const term = $(el).val();
                            // Select2 4.x passes params object with term property
                            assert.step(`term: ${opts.ajax.data({ term: term }).q}`);

                            for (const word of vocab) {
                                if (term && term[0].toUpperCase() === word[0].toUpperCase()) {
                                    assert.step(`match: ${word}`);
                                }
                            }
                        });
                    });
                },
            });

            const wid = new Select2Widget(el, {
                ajaxurl: 'test-ajax-url',
                tags: ['Six', 'Eight'],
            });
            assert.strictEqual(wid.options.ajax.url, 'test-ajax-url');
            el.val('O');
            el.trigger('change');
            assert.verifySteps(['term: O', 'match: One']);

            el.val('Z');
            el.trigger('change');
            assert.verifySteps(['term: Z']);
        });

        QUnit.test('Ajax & no data', (assert) => {
            el.data('vocabulary', '');

            $.fn.extend({
                select2: function (opts) {
                    return this.each((_i, el) => {
                        $(el).on('change', () => {
                            const term = $(el).val();
                            // Select2 4.x uses processResults instead of results
                            // When tags is enabled and data is empty, adds term as option
                            const result = opts.ajax.processResults([], { term: term });
                            if (term) {
                                assert.deepEqual(result.results, [{ id: term, text: term }]);
                            } else {
                                assert.deepEqual(result.results, [{ id: '', text: '' }]);
                            }
                        });
                    });
                },
            });

            const wid = new Select2Widget(el, {
                ajaxurl: 'test-ajax-url',
                multiple: false,
                tags: ['Six', 'Eight'],
            });
            assert.strictEqual(wid.options.ajax.url, 'test-ajax-url');

            // empty value - with tags enabled, adds empty term as option
            el.val('');
            el.trigger('change');

            // term no match - with tags enabled, adds term as new option
            el.val('Z');
            el.trigger('change');
        });

        QUnit.test('Ajax & multiple', (assert) => {
            $.fn.extend({
                select2: function (opts) {
                    return this.each((_i, el) => {
                        $(el).on('change', () => {
                            const term = $(el).val();
                            // Select2 4.x passes params object with term property
                            assert.step(`term: ${opts.ajax.data({ term: term }).q}`);

                            for (const word of vocab) {
                                if (term && term[0].toUpperCase() === word[0].toUpperCase()) {
                                    // Select2 4.x uses processResults with array of {id, text} objects
                                    const data = [{ id: word, text: word }];
                                    const result = opts.ajax.processResults(data, { term: term });
                                    assert.deepEqual(result.results, [{ id: word, text: word }]);
                                    assert.step(`match: ${word}`);
                                }
                            }
                        });
                    });
                },
            });

            const wid = new Select2Widget(el, {
                ajaxurl: 'test-ajax-url',
                multiple: true,
                tags: ['Six', 'Eight'],
            });
            assert.strictEqual(wid.options.ajax.url, 'test-ajax-url');
            // Select2 4.x uses dataAdapter instead of initSelection
            assert.ok(wid.options.dataAdapter);

            el.val('O');
            el.trigger('change');
            assert.verifySteps(['term: O', 'match: One']);

            el.val('Z');
            el.trigger('change');
            assert.verifySteps(['term: Z']);

            el.val('');
            el.trigger('change');
            assert.strictEqual(el.val(), '');
            assert.verifySteps(['term: ']);
        });

        QUnit.test('function call', (assert) => {
            $.fn.extend({
                select2: function (opts) {
                    return this.each((_i, el) => {
                        $(el).on('change', () => {
                            opts.findResult(el);
                        });
                    });
                },
            });
            // save function on window
            window.some = {
                findWord: (el) => {
                    for (const word of vocab) {
                        const value = $(el).val();
                        if (value && value[0].toUpperCase() === word[0].toUpperCase()) {
                            $(el).val(word);
                            assert.step(`find word: ${word}`);
                        }
                    }
                },
            };
            wid = new Select2Widget(el, {
                findResult: 'javascript:some.findWord',
            });

            // change event triggers custom function
            el.val('o');
            el.trigger('change');
            assert.verifySteps(['find word: One']);

            el.val('T');
            el.trigger('change');
            assert.strictEqual(el.val(), 'Two');
            assert.verifySteps(['find word: Two']);

            // no val that fits words
            el.val('z');
            el.trigger('change');
        });

        QUnit.test('function call - no function defined', (assert) => {
            assert.throws(() => {
                new Select2Widget(el, {
                    findResult: 'javascript:',
                });
            }, /No function defined/);
        });

        QUnit.test('function call - function not found', (assert) => {
            assert.throws(() => {
                new Select2Widget(el, {
                    findResult: 'javascript:willFail',
                });
            }, /willFail not found/);
        });

        QUnit.test('static options', (assert) => {
            wid = new Select2Widget(el, {});
            assert.strictEqual(wid.options.theme, theme);
            assert.strictEqual(wid.options.selectionCssClass, 'select2--medium');
            assert.strictEqual(wid.options.dropdownCssClass, 'select2--medium');
            assert.strictEqual(wid.options.width, '500px');
            assert.strictEqual(wid.options.ajax, undefined);
            assert.strictEqual(wid.options.dataAdapter, undefined);
        });

        QUnit.test('ajax data adapter', (assert) => {
            wid = new Select2Widget(el, { ajaxurl: 'test-ajax-url' });
            assert.strictEqual(wid.options.dataAdapter, singleValueAjaxAdapter);

            wid = new Select2Widget(el, { ajaxurl: 'test-ajax-url', multiple: true });
            assert.strictEqual(wid.options.dataAdapter, multiValueAjaxAdapter);
        });
    });
}

QUnit.module('adapters', (hooks) => {
    let el;

    hooks.beforeEach(() => {
        el = $('<input class="select2" value=""/>');
        el.appendTo('body');
    });

    hooks.afterEach(() => {
        el.remove();
    });

    QUnit.test('SingleValueAjaxAdapter - current without vocabulary', (assert) => {
        const done = assert.async();
        el.val('test-value');

        const adapter = new singleValueAjaxAdapter(el, {});
        adapter.current((data) => {
            assert.deepEqual(data, [{ id: 'test-value', text: 'test-value' }]);
            done();
        });
    });

    QUnit.test('SingleValueAjaxAdapter - current with vocabulary', (assert) => {
        const done = assert.async();
        el.val('key1');
        el.data('vocabulary', { key1: 'Label One', key2: 'Label Two' });

        const adapter = new singleValueAjaxAdapter(el, {});
        adapter.current((data) => {
            assert.deepEqual(data, [{ id: 'key1', text: 'Label One' }]);
            done();
        });
    });

    QUnit.test('SingleValueAjaxAdapter - current with vocabulary missing key', (assert) => {
        const done = assert.async();
        el.val('unknown');
        el.data('vocabulary', { key1: 'Label One' });

        const adapter = new singleValueAjaxAdapter(el, {});
        adapter.current((data) => {
            // Falls back to key when not in vocabulary
            assert.deepEqual(data, [{ id: 'unknown', text: 'unknown' }]);
            done();
        });
    });

    QUnit.test('SingleValueAjaxAdapter - select', (assert) => {
        // Add an option element to select
        const selectEl = $(
            '<select class="select2"><option value="opt1">Option 1</option></select>',
        );
        selectEl.appendTo('body');

        const adapter = new singleValueAjaxAdapter(selectEl, {});
        adapter.select({ id: 'opt1', text: 'Option 1' });

        assert.ok(selectEl.find('option[value="opt1"]').prop('selected'));
        selectEl.remove();
    });

    QUnit.test('MultiValueAjaxAdapter - current without vocabulary', (assert) => {
        const done = assert.async();
        el.val('val1,val2,val3');

        const adapter = new multiValueAjaxAdapter(el, {});
        adapter.current((data) => {
            assert.deepEqual(data, [
                { id: 'val1', text: 'val1' },
                { id: 'val2', text: 'val2' },
                { id: 'val3', text: 'val3' },
            ]);
            done();
        });
    });

    QUnit.test('MultiValueAjaxAdapter - current with vocabulary', (assert) => {
        const done = assert.async();
        el.val('a,b');
        el.data('vocabulary', { a: 'Alpha', b: 'Beta', c: 'Gamma' });

        const adapter = new multiValueAjaxAdapter(el, {});
        adapter.current((data) => {
            assert.deepEqual(data, [
                { id: 'a', text: 'Alpha' },
                { id: 'b', text: 'Beta' },
            ]);
            done();
        });
    });

    QUnit.test('MultiValueAjaxAdapter - current with partial vocabulary', (assert) => {
        const done = assert.async();
        el.val('known,unknown');
        el.data('vocabulary', { known: 'Known Label' });

        const adapter = new multiValueAjaxAdapter(el, {});
        adapter.current((data) => {
            assert.deepEqual(data, [
                { id: 'known', text: 'Known Label' },
                { id: 'unknown', text: 'unknown' },
            ]);
            done();
        });
    });

    QUnit.test('MultiValueAjaxAdapter - select', (assert) => {
        const adapter = new multiValueAjaxAdapter(el, {});
        // select() just calls parent's select, which is mocked
        // Verify it doesn't throw
        adapter.select({ id: 'test', text: 'Test' });
        assert.ok(true, 'select() executed without error');
    });
});
