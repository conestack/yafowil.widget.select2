from yafowil.base import factory
from yafowil.utils import entry_point
import os


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')
js = [{
    'group': 'yafowil.widget.select2.dependencies',
    'resource': 'select2/select2.js',
    'order': 20,
}, {
    'group': 'yafowil.widget.select2.common',
    'resource': 'widget.js',
    'order': 21,
}]
css = [{
    'group': 'yafowil.widget.select2.dependencies',
    'resource': 'select2/select2.css',
    'order': 20,
}, {
    'group': 'yafowil.widget.select2.common',
    'resource': 'widget.css',
    'order': 21,
}]


@entry_point(order=10)
def register():
    from yafowil.widget.select2 import widget  # noqa
    factory.register_theme('default', 'yafowil.widget.select2',
                           resourcedir, js=js, css=css)
