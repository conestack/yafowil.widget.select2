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
    u'<select class="select2" id="input-multi" name="multi" required="required" />'

Render select2 in tag mode::

    >>> widget_input = factory('select2input', 'multi', props={'required': True})
    >>> widget_input()
    u'<input class="select2" id="input-multi" name="multi" required="required" />'

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
