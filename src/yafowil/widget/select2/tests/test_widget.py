from collections import OrderedDict
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import YafowilTestCase
import os
import unittest


if not IS_PY2:
    from importlib import reload


def np(path):
    return path.replace('/', os.path.sep)


class TestSelect2Widget(YafowilTestCase):

    def setUp(self):
        super(TestSelect2Widget, self).setUp()
        from yafowil.widget import select2
        from yafowil.widget.select2 import widget
        reload(widget)
        select2.register()

    def test_render_single(self):
        widget = factory(
            'select2',
            name='single',
            props={
                'required': True
            })
        self.assertEqual(widget(), (
            '<select class="select2" id="input-single" name="single" '
            'required="required"> </select>'
        ))

    def test_render_multiple(self):
        widget = factory(
            'select2',
            name='multi',
            props={
                'required': True,
                'multiple': True
            })
        self.assertEqual(widget(), (
            '<input id="exists-multi" name="multi-exists" type="hidden" '
            'value="exists" /><select class="select2" id="input-multi" '
            'multiple="multiple" name="multi" required="required"> </select>'
        ))

    def test_render_single_tag_mode(self):
        widget = factory(
            'select2',
            name='single',
            props={
                'inputtag': True
            })
        self.assertEqual(widget(), (
            '<input class="select2" id="input-single" name="single" '
            'value="" />'
        ))

    def test_render_multiple_tag_mode(self):
        widget = factory(
            'select2',
            name='multi',
            value=['1', '2'],
            props={
                'inputtag': True,
                'multiple': True
            })
        self.assertEqual(widget(), (
            '<input class="select2" data-multiple=\'true\' id="input-multi" '
            'name="multi" value="1,2" />'
        ))

    def test_render_with_vocabulary(self):
        # Provide a vocabulary if value terms consists of id / label pairs
        vocab = OrderedDict()
        vocab['1'] = 'Label 1'
        vocab['2'] = 'Label 2'
        widget = factory(
            'select2',
            name='multi',
            value=['1', '2'],
            props={
                'inputtag': True,
                'multiple': True,
                'vocabulary': vocab,
            })
        self.assertEqual(widget(), (
            '<input class="select2" data-multiple=\'true\' '
            'data-vocabulary=\'{"1": "Label 1", "2": "Label 2"}\' '
            'id="input-multi" name="multi" value="1,2" />'
        ))

    def test_extract_required(self):
        widget = factory(
            'select2',
            name='single',
            props={
                'required': True
            })

        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)

        request = {'single': ''}
        data = widget.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Mandatory field was empty')]
        )
        self.assertEqual(data.extracted, '')

        request = {'single': '1'}
        data = widget.extract(request)
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, '1')

    def test_extract_single_value(self):
        widget = factory(
            'select2',
            name='single',
            props={
                'inputtag': True
            })

        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)

        request = {'single': ''}
        data = widget.extract(request)
        self.assertEqual(data.extracted, '')

        request = {'single': '1'}
        data = widget.extract(request)
        self.assertEqual(data.extracted, '1')

    def test_extract_multi_value(self):
        widget = factory(
            'select2',
            name='multi',
            props={
                'multiple': True,
                'inputtag': True
            })

        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)

        request = {'multi': ''}
        data = widget.extract(request)
        self.assertEqual(data.extracted, [])

        request = {'multi': '1,2'}
        data = widget.extract(request)
        self.assertEqual(data.extracted, ['1', '2'])

    def test_extract_with_preset_value(self):
        widget = factory(
            'select2',
            name='multi',
            value=['1', '2'],
            props={
                'multiple': True,
                'inputtag': True
            })
        self.assertEqual(widget(), (
            '<input class="select2" data-multiple=\'true\' id="input-multi" '
            'name="multi" value="1,2" />'
        ))

        request = {'multi': '1,2,3'}
        data = widget.extract(request)
        self.assertEqual(widget(data=data), (
            '<input class="select2" data-multiple=\'true\' id="input-multi" '
            'name="multi" value="1,2,3" />'
        ))
        self.assertEqual(data.extracted, ['1', '2', '3'])

        request = {'multi': ''}
        data = widget.extract(request)
        self.assertEqual(widget(data=data), (
            '<input class="select2" data-multiple=\'true\' id="input-multi" '
            'name="multi" value="" />'
        ))
        self.assertEqual(data.extracted, [])

    def test_display_renderer_empty(self):
        widget = factory(
            'select2',
            name='empty',
            mode='display')
        self.assertEqual(
            widget(),
            '<div class="display-select2" id="display-empty"></div>'
        )

    def test_display_renderer_single(self):
        widget = factory(
            'select2',
            name='single',
            value='foo',
            props={
                'vocabulary': [('foo', 'Foo'), ('bar', 'Bar')]
            },
            mode='display')
        self.assertEqual(
            widget(),
            '<div class="display-select2" id="display-single">Foo</div>'
        )

    def test_display_renderer_multiple(self):
        widget = factory(
            'select2',
            name='multi',
            value=['foo', 'bar'],
            props={
                'vocabulary': [('foo', 'Foo'), ('bar', 'Bar')],
                'multiple': True,
            },
            mode='display')
        self.assertEqual(widget(), (
            '<ul class="display-select2" '
            'id="display-multi"><li>Foo</li><li>Bar</li></ul>'
        ))

    # test with display_proxy_renderer
    def test_extract_with_preset_value_and_display_proxy_renderer(self):
        widget = factory(
            'select2',
            name='multi',
            value=['1', '2'],
            mode='display',
            props={
                'multiple': True,
                'inputtag': True,
                'display_proxy': True
            })
        self.assertEqual(widget(), (
            '<ul class="display-select2" id="display-multi"><li>1</li><li>2</li></ul>'
            '<input class="select2" id="input-multi" name="multi" type="hidden" value="1" />'
            '<input class="select2" id="input-multi" name="multi" type="hidden" value="2" />'
        ))

        request = {'multi': '1,2,3'}
        data = widget.extract(request)
        self.assertEqual(widget(data=data), (
            '<ul class="display-select2" id="display-multi"><li>1</li><li>2</li><li>3</li></ul>'
            '<input class="select2" id="input-multi" name="multi" type="hidden" value="1" />'
            '<input class="select2" id="input-multi" name="multi" type="hidden" value="2" />'
            '<input class="select2" id="input-multi" name="multi" type="hidden" value="3" />'
        ))
        self.assertEqual(data.extracted, ['1', '2', '3'])

        request = {'multi': ''}
        data = widget.extract(request)
        self.assertEqual(widget(data=data), (
            '<div class="display-select2" id="display-multi"></div>'
        ))
        self.assertEqual(data.extracted, [])

    def test_display_renderer_empty_and_display_proxy_renderer(self):
        widget = factory(
            'select2',
            name='empty',
            mode='display',
            props={
                'display_proxy': True
            }
        )
        self.assertEqual(
            widget(),
            '<div class="display-select2" id="display-empty"></div>'
        )

    def test_display_renderer_single_and_display_proxy_renderer(self):
        widget = factory(
            'select2',
            name='single',
            value='foo',
            mode='display',
            props={
                'vocabulary': [('foo', 'Foo'), ('bar', 'Bar')],
                'display_proxy': True
            },
        )
        self.assertEqual(
            widget(),
            '<div class="display-select2" id="display-single">Foo</div>'
            '<input class="select2" id="input-single" name="single" type="hidden" value="foo" />'
        )

    def test_display_renderer_multiple_and_display_proxy_renderer(self):
        widget = factory(
            'select2',
            name='multi',
            value=['foo', 'bar'],
            props={
                'vocabulary': [('foo', 'Foo'), ('bar', 'Bar')],
                'multiple': True,
                'display_proxy': True
            },
            mode='display')
        self.assertEqual(widget(), (
            '<ul class="display-select2" id="display-multi"><li>Foo</li><li>Bar</li></ul>'
            '<input class="select2" id="input-multi" name="multi" type="hidden" value="foo" />'
            '<input class="select2" id="input-multi" name="multi" type="hidden" value="bar" />'
        ))

    def test_resources(self):
        factory.theme = 'default'
        resources = factory.get_resources('yafowil.widget.select2')
        self.assertTrue(resources.directory.endswith(np('/select2/resources')))
        self.assertEqual(resources.name, 'yafowil.widget.select2')
        self.assertEqual(resources.path, 'yafowil-select2')

        scripts = resources.scripts
        self.assertEqual(len(scripts), 2)

        self.assertTrue(
            scripts[0].directory.endswith(np('/select2/resources/select2'))
        )
        self.assertEqual(scripts[0].path, 'yafowil-select2/select2')
        self.assertEqual(scripts[0].file_name, 'select2.min.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        self.assertTrue(scripts[1].directory.endswith(np('/select2/resources/default')))
        self.assertEqual(scripts[1].path, 'yafowil-select2/default')
        self.assertEqual(scripts[1].file_name, 'widget.min.js')
        self.assertTrue(os.path.exists(scripts[1].file_path))

        styles = resources.styles
        self.assertEqual(len(styles), 2)

        self.assertTrue(
            styles[0].directory.endswith(np('/select2/resources/select2'))
        )
        self.assertEqual(styles[0].path, 'yafowil-select2/select2')
        self.assertEqual(styles[0].file_name, 'select2.css')
        self.assertTrue(os.path.exists(styles[0].file_path))

        self.assertTrue(styles[1].directory.endswith(np('/select2/resources/default')))
        self.assertEqual(styles[1].path, 'yafowil-select2/default')
        self.assertEqual(styles[1].file_name, 'widget.min.css')
        self.assertTrue(os.path.exists(styles[1].file_path))


if __name__ == '__main__':
    unittest.main()
