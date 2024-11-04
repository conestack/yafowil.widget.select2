import {Select2Widget} from "../src/widget";
import {register_array_subscribers} from "../src/widget";
import $ from 'jquery';

QUnit.module('select2', hooks => {
    let wid;
    let el = $('<input class="select2" value=""/>');
    let vocab = ['One', 'Two', 'Four'];
    let _array_subscribers = {
        on_add: []
    };

    hooks.beforeEach(()=> {
        el.appendTo('body');
        el.data('vocabulary', vocab);
    });
    hooks.afterEach(()=> {
        // remove select2 from jQuery namespace
        delete $.fn.select2;
        el.remove();
        wid = null;
    });

    QUnit.test('initialize', assert => {
        $.fn.extend({
            select2: function () {
                assert.step('select2 called');
                return this;
            }
        });
        Select2Widget.initialize();
        wid = el.data('yafowil-select2');
        assert.ok(wid);

        assert.verifySteps(['select2 called']);
    });

    QUnit.test('register_array_subscribers', assert => {
        $.fn.extend({
            select2: function () {
                assert.step('select2 called');
                return this;
            }
        });

        // return if window.yafowil === undefined
        register_array_subscribers();
        assert.deepEqual(_array_subscribers['on_add'], []);

        // patch yafowil_array
        window.yafowil_array = {
            on_array_event: function(evt_name, evt_function) {
                _array_subscribers[evt_name] = evt_function;
            },
            inside_template(elem) {
                return elem.parents('.arraytemplate').length > 0;
            }
        };
        register_array_subscribers();

        // create table DOM
        let table = $('<table />')
            .append($('<tr />'))
            .append($('<td />'))
            .appendTo('body');

        $('td', table).addClass('arraytemplate');
        el.detach().appendTo($('td', table));

        // invoke array on_add - returns
        _array_subscribers['on_add'].apply(null, $('tr', table));
        wid = el.data('yafowil-select2');
        assert.notOk(wid);
        $('td', table).removeClass('arraytemplate');
        assert.verifySteps([]);

        // invoke array on_add
        $('td', table).removeClass('arraytemplate');
        _array_subscribers['on_add'].apply(null, $('tr', table));
        wid = el.data('yafowil-select2');
        assert.ok(wid);
        assert.verifySteps(['select2 called']);

        table.remove();
        window.yafowil_array = undefined;
        _array_subscribers = undefined;
    });

    QUnit.test('fail initialize', assert => {
        // fails because of faulty elem
        assert.throws(function() {
                new Select2Widget(el[0], {ajaxurl: 'test'});
            },
            /Failed to initialize select2: TypeError: this.elem.select2 is not a function/)
    });

    QUnit.test('ajax', assert => {
        $.fn.extend({
            select2: function (opts) {
                return this.each(function (i, el) {
                    $(el).on('change', (e) => {
                        let term = $(el).val();
                        assert.step(`term: ${opts.ajax.data(term).q}`);

                        for (let word of vocab) {
                            if (term && term[0].toUpperCase() === word[0].toUpperCase()) {
                                assert.step(`match: ${word}`);
                            }
                        }
                    });
                });
            }
        });

        let wid = new Select2Widget(el, {
            ajaxurl: 'test-ajax-url',
            tags: ['Six', 'Eight'],
        });
        assert.strictEqual(wid.options.ajax.url, 'test-ajax-url');
        el.val('O')
        el.trigger('change');
        assert.verifySteps([
            'term: O',
            'match: One'
        ]);

        el.val('Z')
        el.trigger('change');
        assert.verifySteps([
            'term: Z'
        ]);
    });

    QUnit.test('Ajax & no data', assert => {
        el.data('vocabulary', '');

        $.fn.extend({
            select2: function (opts) {
                return this.each(function (i, el) {
                    $(el).on('change', (e) => {
                        let term = $(el).val();
                        assert.deepEqual(
                            opts.ajax.results([], 0, term).results,
                            [{'id': undefined,
                                'text': undefined
                            }]);
                    });
                });
            }
        });

        let wid = new Select2Widget(el, {
            ajaxurl: 'test-ajax-url',
            multiple: false,
            tags: ['Six', 'Eight']
        });
        assert.strictEqual(wid.options.ajax.url, 'test-ajax-url');

        // empty value
        el.val('');
        el.trigger('change');

        // term no match
        el.val('Z');
        el.trigger('change');
        wid.options.initSelection(el, function(data) {
            assert.deepEqual(data, {
                "id": "Z",
                "text": "Z"
            });
        });
    });

    QUnit.test('Ajax & multiple', assert => {
        $.fn.extend({
            select2: function (opts) {
                return this.each(function (i, el) {
                    $(el).on('change', (e) => {
                        let term = $(el).val();
                        assert.step(`term: ${opts.ajax.data(term).q}`);

                        for (let word of vocab) {
                            if (term && term[0].toUpperCase() === word[0].toUpperCase()) {
                                assert.strictEqual(opts.ajax.results(word, 0, term).results, word);
                                assert.step(`match: ${word}`);
                            }
                        }
                    });
                });
            }
        });

        let wid = new Select2Widget(el, {
            ajaxurl: 'test-ajax-url',
            multiple: true,
            tags: ['Six', 'Eight']
        });
        assert.strictEqual(wid.options.ajax.url, 'test-ajax-url');

        el.val('O')
        el.trigger('change');
        assert.verifySteps([
            'term: O',
            'match: One'
        ]);
        wid.options.initSelection(el, function(data) {
            assert.deepEqual(data, [{
                "id": "O",
                "text": "O"
            }]);
        });

        el.val('Z')
        el.trigger('change');
        assert.verifySteps([
            'term: Z'
        ]);
        wid.options.initSelection(el, function(data) {
            assert.deepEqual(data, [{
                "id": "Z",
                "text": "Z"
            }]);
        });

        el.val('');
        el.trigger('change');
        assert.strictEqual(el.val(), '');
        wid.options.initSelection(el, function() {
            throw 'returns before this statement';
        });
        assert.verifySteps(['term: ']);
    });

    QUnit.test('function call', assert => {
        $.fn.extend({
            select2: function (opts) {
                return this.each(function(i, el) {
                    $(el).on('change', (e) => {
                        opts.findResult(el);
                    });
                });
            }
        });
        // save function on window
        window.some = {
            findWord: function(el) {
                for (let word of vocab) {
                    let value = $(el).val();
                    if (value && value[0].toUpperCase() === word[0].toUpperCase()) {
                        $(el).val(word);
                        assert.step(`find word: ${word}`)
                    }
                }
            }
        }
        wid = new Select2Widget(el, {
            findResult: 'javascript:some.findWord'
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

    QUnit.test('function call - no function defined', assert => {
        assert.throws(function() {
            new Select2Widget(el, {
                findResult: 'javascript:'
            })
        },
        /No function defined/)
    });

    QUnit.test('function call - function not found', assert => {
        assert.throws(function() {
            new Select2Widget(el, {
                findResult: 'javascript:willFail'
            })
        },
        /willFail not found/)
    });
});
