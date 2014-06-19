# -*- coding: utf-8 -*-
import json
import urlparse
from yafowil.base import factory


def json_response(url):
    purl = urlparse.urlparse(url)
    qs = urlparse.parse_qs(purl.query)
    data = json_data(qs.get('q', [''])[0])
    return {'body': json.dumps(data),
            'header': [('Content-Type', 'application/json')]
    }


def json_data(term):
    vocab = sorted((u'Weißburgunder', u'Welschriesling',
                    u'Sauvingnon Blanc', u'Sämling', u'Scheurebe',
                    u'Traminer', u'Morrilon', u'Muskateller'))
    data = list()
    if term:
        for val in vocab:
            if val.lower().startswith(term.lower()):
                data.append({
                    'id': val,
                    'text': val,
                })
    print term
    print data
    return data


TITLE_SELECT2_1 = "Single selection"
DOC_SELECT2_1 = """
select2
-------

Select2 widget in single selection mode.

.. code-block:: python

    vocab = sorted((u'Weißburgunder', u'Welschriesling',
                    u'Sauvingnon Blanc', u'Sämling', u'Scheurebe',
                    u'Traminer', u'Morrilon', u'Muskateller'))

    select2 = factory('#field:select2', value='Traminer', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'vocabulary': vocab,
    })

"""

TITLE_SELECT2_2 = "Multi selection"
DOC_SELECT2_2 = """
Select2 widget in multi selection mode.

.. code-block:: python

    value = [u'Sauvingnon Blanc', u'Sämling']
    select2 = factory('#field:select2', value=value, props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'vocabulary': vocab,
        'multiple': True,
    })

"""

TITLE_SELECT2_3 = "Input Mode"
DOC_SELECT2_3 = """
Select2 widget in input mode.

.. code-block:: python

    value = [u'Sämling', u'Scheurebe']
    select2 = factory('#field:select2', value=value, props={
        'label': 'Select or add some items',
        'inputtag': True,
        'placeholder': 'Select or add some items',
        'minimumInputLength': 1,
        'multiple': True,
        'tags': vocab,
    })

"""


TITLE_SELECT2_4 = "Single selection from ajax URL"
DOC_SELECT2_4 = """
Select2 single selection widget fetching data from URL.

.. code-block:: python

    select2 = factory('#field:select2', value='Welschriesling', props={
        'label': 'Select ajax item',
        'inputtag': True,
        'placeholder': 'Select some item',
        'ajaxurl': 'yafowil.widget.select2.json',
    })

The server answers with a JSON response, here the example does it using WSGI
and ``webob`` way. This code needs modification depending on the framework
used

.. code-block:: python

    def json_response(environ, start_response):
        data = lipsum
        if environ['QUERY_STRING'].startswith('q='):
            term = environ['QUERY_STRING'][3:]
            data = list()
            if term:
                for val in vocab:
                    if val.lower().startswith(term.lower()):
                        data.append({
                            'id': val,
                            'text': val,
                        })
        response = Response(content_type='application/json',
                            body=json.dumps(data))
        return response(environ, start_response)

"""


TITLE_SELECT2_5 = "Multi selection from ajax URL"
DOC_SELECT2_5 = """
Select2 multi selection widget fetching data from URL.

.. code-block:: python

    value = [u'Sämling', u'Traminer']
    select2 = factory('#field:select2', value=value, props={
        'label': 'Select multiple ajax items',
        'inputtag': True,
        'minimumInputLength': 1,
        'multiple': True,
        'placeholder': 'Select some items',
        'ajaxurl': 'yafowil.widget.select2.json',
    })

"""


def get_example():

    vocab = sorted((u'Weißburgunder', u'Welschriesling',
                    u'Sauvingnon Blanc', u'Sämling', u'Scheurebe',
                    u'Traminer', u'Morrilon', u'Muskateller'))

    # single selection
    select2_1 = factory(u'fieldset', name='yafowil_select2_1')
    select2_1['text'] = factory('#field:select2', value='Traminer', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'vocabulary': vocab,
    })

    # multiple selection
    select2_2 = factory(u'fieldset', name='yafowil_select2_2')
    select2_2_val = [u'Sauvingnon Blanc', u'Sämling']
    select2_2['text'] = factory('#field:select2', value=select2_2_val, props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'vocabulary': vocab,
        'multiple': True,
    })

    # input mode
    select2_3 = factory(u'fieldset', name='yafowil_select2_3')
    select2_3_val = [u'Sämling', u'Scheurebe']
    select2_3['text'] = factory('#field:select2', value=select2_3_val, props={
        'label': 'Select or add some items',
        'inputtag': True,
        'placeholder': 'Select or add some items',
        'minimumInputLength': 1,
        'multiple': True,
        'tags': vocab,
    })

    # ajax single
    select2_4 = factory(u'fieldset', name='yafowil_select2_4')
    select2_4_val = 'Welschriesling'
    select2_4['text'] = factory('#field:select2', value=select2_4_val, props={
        'label': 'Select ajax item',
        'inputtag': True,
        'placeholder': 'Select some item',
        'ajaxurl': 'yafowil.widget.select2.json',
    })
    select2_4_routes = {'yafowil.widget.select2.json': json_response}

    # ajax multiple
    select2_5 = factory(u'fieldset', name='yafowil_select2_5')
    select2_5_val = [u'Sämling', u'Traminer']
    select2_5['text'] = factory('#field:select2', value=select2_5_val, props={
        'label': 'Select multiple ajax items',
        'inputtag': True,
        'minimumInputLength': 1,
        'multiple': True,
        'placeholder': 'Select some items',
        'ajaxurl': 'yafowil.widget.select2.json',
    })
    select2_5_routes = {'yafowil.widget.select2.json': json_response}

    return [{'widget': select2_1,
             'doc': DOC_SELECT2_1,
             'title': TITLE_SELECT2_1},
            {'widget': select2_2,
             'doc': DOC_SELECT2_2,
             'title': TITLE_SELECT2_2},
            {'widget': select2_3,
             'doc': DOC_SELECT2_3,
             'title': TITLE_SELECT2_3},
            {'widget': select2_4,
             'routes': select2_4_routes,
             'doc': DOC_SELECT2_4,
             'title': TITLE_SELECT2_4},
            {'widget': select2_5,
             'routes': select2_5_routes,
             'doc': DOC_SELECT2_5,
             'title': TITLE_SELECT2_5}
           ]
