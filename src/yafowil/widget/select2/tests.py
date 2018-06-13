from collections import OrderedDict
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
import yafowil.loader


if not IS_PY2:
    from importlib import reload


class TestSelect2Widget(YafowilTestCase):

    def setUp(self):
        super(TestSelect2Widget, self).setUp()
        from yafowil.widget.select2 import widget
        reload(widget)

    def test_render_single(self):
        widget = factory(
            'select2',
            name='single',
            props={
                'required': True
            })
        self.assertEqual(widget(), (
            '<select class="select2" id="input-single" name="single" '
            'required="required" />'
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
            'multiple="multiple" name="multi" required="required" />'
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
        self.assertEqual(widget(),
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
        self.assertEqual(widget(),
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


if __name__ == '__main__':
    unittest.main()                                          # pragma: no cover
