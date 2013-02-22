from yafowil.base import (
    factory,
)
from yafowil.common import (
    select_extractor,
    generic_required_extractor,
    select_edit_renderer,
    select_display_renderer,
    input_generic_renderer,
)
from yafowil.utils import (
    managedprops,
    data_attrs_helper,
    attr_value
)


select2_options = [
    'allowClear',
    'minimumInputLength',
    'formatResult',
    'formatSelection',
    'query',
    'maximumSelectionSize',
    'data',
    'ajax',
    'tags',
    'maximumInputLength',
    'tokenSeparators',
    'matcher',
    ]

@managedprops('multiple', *select2_options)
def select2_edit_renderer(widget, data, inputtag=False):
    custom_attrs = data_attrs_helper(widget, data, select2_options)
    multiple = attr_value('multiple', widget, data)
    if multiple:
        custom_attrs['multiple'] = multiple
    renderer = inputtag and input_generic_renderer or select_edit_renderer
    return renderer(widget, data, **custom_attrs)

@managedprops('multiple', *select2_options)
def select2_edit_renderer_input(widget, data):
    return select2_edit_renderer(widget, data, inputtag=True)


factory.register(
    'select2',
    extractors=[select_extractor, generic_required_extractor],
    edit_renderers=[select2_edit_renderer],
    display_renderers=[select_display_renderer])

factory.register(
    'select2input',
    extractors=[select_extractor, generic_required_extractor],
    edit_renderers=[select2_edit_renderer_input],
    display_renderers=[input_generic_renderer])


factory.doc['blueprint']['select2'] = \
"""Add-on blueprint `yafowil.widget.select2
<http://github.com/bluedynamics/yafowil.widget.select2/>`_ .
"""

factory.defaults['select2.size'] = None
factory.defaults['select2.default'] = []
factory.defaults['select2.format'] = 'block'

factory.defaults['select2input.class'] = 'select2'
factory.defaults['select2.class'] = 'select2'

factory.defaults['select2input.multiple'] =\
factory.defaults['select2.multiple'] = False # HTML attribute

factory.defaults['select2input.placeholder'] =\
factory.defaults['select2.placeholder'] = None

factory.defaults['select2input.minimumInputLength'] =\
factory.defaults['select2.minimumInputLength'] = None

factory.defaults['select2input.formatResult'] =\
factory.defaults['select2.formatResult'] = None

factory.defaults['select2input.formatSelection'] =\
factory.defaults['select2.formatSelection'] = None

factory.defaults['select2input.query'] =\
factory.defaults['select2.query'] = None

factory.defaults['select2input.maximumSelectionSize'] =\
factory.defaults['select2.maximumSelectionSize'] = None

factory.defaults['select2input.data'] =\
factory.defaults['select2.data'] = None

factory.defaults['select2input.ajax'] =\
factory.defaults['select2.ajax'] = None

factory.defaults['select2input.tags'] =\
factory.defaults['select2.tags'] = None

factory.defaults['select2input.maximumInputLength'] =\
factory.defaults['select2.maximumInputLength'] = None

factory.defaults['select2input.tokenSeparators'] =\
factory.defaults['select2.tokenSeparators'] = None

factory.defaults['select2.matcher'] =\
factory.defaults['select2.matcher'] = None

factory.defaults['select2.allowClear'] = None;
factory.doc['props']['select2.allowClear'] = \
"""Allow adding new values.
For: select2
Values: [True|False|None (default)].
"""
