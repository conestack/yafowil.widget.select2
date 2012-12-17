from yafowil.base import (
    factory,
)
from yafowil.common import (
    select_extractor,
    generic_required_extractor,
    select_edit_renderer,
    select_display_renderer,
)
from yafowil.utils import (
    managedprops,
    data_attrs_helper
)


select2_options = [
    'allowClear',
]

@managedprops(*select2_options)
def select2_edit_renderer(widget, data):
    custom_attrs = data_attrs_helper(widget, data, select2_options)
    return select_edit_renderer(widget, data, **custom_attrs)

factory.register(
    'select2',
    extractors=[select_extractor, generic_required_extractor],
    edit_renderers=[select2_edit_renderer],
    display_renderers=[select_display_renderer])


factory.doc['blueprint']['select2'] = \
"""Add-on blueprint `yafowil.widget.select2
<http://github.com/bluedynamics/yafowil.widget.select2/>`_ .
"""

factory.defaults['select2.multivalued'] = False
factory.defaults['select2.size'] = None
factory.defaults['select2.default'] = []
factory.defaults['select2.format'] = 'block'
factory.defaults['select2.class'] = 'select2'

factory.defaults['select2.allowClear'] = None;
factory.doc['props']['select2.'] = \
"""Allow adding new values.
For: select2
Values: [True|False|None (default)].
"""
