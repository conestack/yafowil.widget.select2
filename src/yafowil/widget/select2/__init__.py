from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Default
##############################################################################

# webresource ################################################################

scripts = wr.ResourceGroup(name='yafowil-select2-scripts')
scripts.add(wr.ScriptResource(
    name='select2-js',
    depends='jquery-js',
    directory=os.path.join(resources_dir, 'select2'),
    resource='select2.js',
    compressed='select2.min.js'
))
scripts.add(wr.ScriptResource(
    name='yafowil-select2-js',
    depends='select2-js',
    directory=resources_dir,
    resource='widget.js',
    compressed='widget.min.js'
))

styles = wr.ResourceGroup(name='yafowil-select2-styles')
styles.add(wr.StyleResource(
    name='select2-css',
    directory=os.path.join(resources_dir, 'select2'),
    resource='select2.css'
))
styles.add(wr.StyleResource(
    name='yafowil-select2-css',
    depends='select2-css',
    directory=resources_dir,
    resource='widget.css'
))

# B/C resources ##############################################################

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


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    from yafowil.widget.select2 import widget  # noqa

    # Default
    factory.register_theme(
        'default', 'yafowil.widget.select2', resources_dir,
        js=js, css=css
    )
    factory.register_scripts('default', 'yafowil.widget.select2', scripts)
    factory.register_styles('default', 'yafowil.widget.select2', styles)
