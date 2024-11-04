import resource
from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Default
##############################################################################

# webresource ################################################################

resources = wr.ResourceGroup(
    name='yafowil.widget.select2',
    directory=resources_dir,
    path='yafowil-select2'
)
resources.add(wr.ScriptResource(
    name='select2-js',
    depends='jquery-js',
    directory=os.path.join(resources_dir, 'select2'),
    path='yafowil-select2/select2',
    resource='select2.js',
    compressed='select2.min.js'
))
resources.add(wr.ScriptResource(
    name='yafowil-select2-js',
    directory=os.path.join(resources_dir, 'default'),
    depends='select2-js',
    resource='widget.js',
    compressed='widget.min.js'
))
resources.add(wr.StyleResource(
    name='select2-css',
    directory=os.path.join(resources_dir, 'select2'),
    path='yafowil-select2/select2',
    resource='select2.css'
))
resources.add(wr.StyleResource(
    name='yafowil-select2-css',
    directory=os.path.join(resources_dir, 'default'),
    depends='select2-css',
    resource='widget.min.css'
))

# B/C resources ##############################################################

js = [{
    'group': 'yafowil.widget.select2.dependencies',
    'resource': 'select2/select2.js',
    'order': 20,
}, {
    'group': 'yafowil.widget.select2.common',
    'resource': 'default/widget.js',
    'order': 21,
}]
css = [{
    'group': 'yafowil.widget.select2.dependencies',
    'resource': 'select2/select2.css',
    'order': 20,
}, {
    'group': 'yafowil.widget.select2.common',
    'resource': 'default/widget.css',
    'order': 21,
}]


##############################################################################
# Bootstrap 5
##############################################################################

# webresource ################################################################

bootstrap5_resources = wr.ResourceGroup(
    name='yafowil.widget.select2',
    directory=resources_dir,
    path='yafowil-select2'
)
bootstrap5_resources.add(wr.ScriptResource(
    name='select2-js',
    depends='jquery-js',
    directory=os.path.join(resources_dir, 'select2'),
    path='yafowil-select2/select2-develop',
    resource='dist/js/select2.js'
))
bootstrap5_resources.add(wr.ScriptResource(
    name='yafowil-select2-js',
    directory=os.path.join(resources_dir, 'bootstrap5'),
    depends='select2-js',
    resource='widget.js'
))
bootstrap5_resources.add(wr.StyleResource(
    name='select2-css',
    directory=os.path.join(resources_dir, 'select2'),
    path='yafowil-select2/select2-develop',
    resource='dist/css/select2.css'
))
bootstrap5_resources.add(wr.StyleResource(
    name='select2-bootstrap5-css',
    directory=os.path.join(resources_dir, 'select2'),
    path='yafowil-select2/select2-bootstrap5-theme',
    resource='select2-bootstrap-5-theme.css'
))
bootstrap5_resources.add(wr.StyleResource(
    name='yafowil-select2-css',
    directory=os.path.join(resources_dir, 'bootstrap5'),
    depends='select2-css',
    resource='widget.min.css'
))

# B/C resources ##############################################################

bootstrap5_js = [{
    'group': 'yafowil.widget.select2.dependencies',
    'resource': 'select2/select2.js',
    'order': 20,
}, {
    'group': 'yafowil.widget.select2.common',
    'resource': 'bootstrap5/widget.js',
    'order': 21,
}]
bootstrap5_css = [{
    'group': 'yafowil.widget.select2.dependencies',
    'resource': 'select2/select2.css',
    'order': 20,
}, {
    'group': 'yafowil.widget.select2.common',
    'resource': 'bootstrap5/widget.min.css',
    'order': 21,
}]


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    from yafowil.widget.select2 import widget  # noqa

    widget_name = 'yafowil.widget.select2'

    # Default
    factory.register_theme(
        'default',
        widget_name,
        resources_dir,
        js=js,
        css=css
    )
    factory.register_resources('default', widget_name, resources)

    # Bootstrap 5
    factory.register_theme(
        ['bootstrap5'],
        widget_name,
        resources_dir,
        js=bootstrap5_js,
        css=bootstrap5_css
    )

    factory.register_resources(
        ['bootstrap5'],
        widget_name,
        bootstrap5_resources
    )
