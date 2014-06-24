Import requirements::

    >>> import yafowil.loader
    >>> from yafowil.base import factory

Render single::

    >>> widget = factory('select2', 'single', props={'required': True})
    >>> widget()
    u'<select class="select2" id="input-single" 
    name="single" required="required" />'

Render multiple::

    >>> widget = factory('select2', 'multi', props={
    ...     'required': True,
    ...     'multiple': True})
    >>> widget()
    u'<input id="exists-multi" name="multi-exists" type="hidden" 
    value="exists" /><select class="select2" id="input-multi" 
    multiple="multiple" name="multi" required="required" />'

Render single in tag mode::

    >>> widget = factory('select2', 'single', props={'inputtag': True})
    >>> widget()
    u'<input class="select2" id="input-single" name="single" value="" />'

Render multiple in tag mode::

    >>> widget = factory('select2', 'multi', value=['1', '2'], props={
    ...     'inputtag': True,
    ...     'multiple': True})
    >>> widget()
    u'<input class="select2" data-multiple=\'true\' id="input-multi" 
    name="multi" value="1,2" />'

Single value widget extraction::

    >>> widget = factory('select2', 'single', props={'required': True})
    >>> request = {}
    >>> data = widget.extract(request)
    >>> data.extracted
    <UNSET>

    >>> request = {'single': ''}
    >>> data = widget.extract(request)

    >>> data.errors
    [ExtractionError('Mandatory field was empty',)]

    >>> data.extracted
    ''

    >>> request = {'single': '1'}
    >>> data = widget.extract(request)
    >>> data.errors
    []

    >>> data.extracted
    '1'

    >>> widget = factory('select2', 'single', props={
    ...     'inputtag': True})

    >>> request = {}
    >>> data = widget.extract(request)
    >>> data.extracted
    <UNSET>

    >>> request = {'single': ''}
    >>> data = widget.extract(request)
    >>> data.extracted
    ''

    >>> request = {'single': '1'}
    >>> data = widget.extract(request)
    >>> data.extracted
    '1'

Multi value widget extraction::

    >>> widget = factory('select2', 'multi', props={
    ...     'multiple': True,
    ...     'inputtag': True})

    >>> request = {}
    >>> data = widget.extract(request)
    >>> data.extracted
    <UNSET>

    >>> request = {'multi': ''}
    >>> data = widget.extract(request)
    >>> data.extracted
    []

    >>> request = {'multi': '1,2'}
    >>> data = widget.extract(request)
    >>> data.extracted
    ['1', '2']

Display renderer::

    >>> widget = factory('select2', 'empty', mode='display')
    >>> widget()
    u'<div class="display-select2" id="display-empty"></div>'

    >>> widget = factory('select2',
    ...                  'single',
    ...                  value='foo',
    ...                  props={'vocabulary': [('foo', 'Foo'), ('bar', 'Bar')]},
    ...                  mode='display')
    >>> widget()
    u'<div class="display-select2" id="display-single">Foo</div>'

    >>> widget = factory('select2',
    ...                  'multi',
    ...                  value=['foo', 'bar'],
    ...                  props={
    ...                      'vocabulary': [('foo', 'Foo'), ('bar', 'Bar')],
    ...                      'multiple': True,
    ...                  },
    ...                  mode='display')
    >>> widget()
    u'<ul class="display-select2" 
    id="display-multi"><li>Foo</li><li>Bar</li></ul>'
