select2 widget
=============

Features
--------

- renders select box with select2 css class and provides select2 resources.

Load requirements::

    >>> import yafowil.loader
    >>> import yafowil.widget.select2

Test widget::

    >>> from yafowil.base import factory

Render widget::

    >>> widget = factory('select2', 'multi', props={'required': True})
    >>> widget()
    u'<input id="exists-multi" name="multi-exists" type="hidden" 
    value="exists" /><select class="select2" id="input-multi" 
    multiple="multiple" name="multi" required="required" />'

Widget extraction::

    >>> request = {'multi': []}
    >>> data = widget.extract(request)

    >>> data.errors
    [ExtractionError('Mandatory field was empty',)]

    >>> data.extracted
    []

    >>> request = {'multi': ['1']}
    >>> data = widget.extract(request)
    >>> data.errors
    []

    >>> data.extracted
    ['1']

Display renderer::

    >>> widget = factory('select2',
    ...                  'multi',
    ...                  value=['foo', 'bar'],
    ...                  props={'vocabulary': [('foo', 'Foo'), ('bar', 'Bar')]},
    ...                  mode='display')
    >>> widget()
    u'<ul class="display-select2" 
    id="display-multi"><li>Foo</li><li>Bar</li></ul>'

    >>> widget = factory('select2', 'multi', mode='display')
    >>> widget()
    u'<div class="display-select2" id="display-multi"></div>'
