# -*- coding: utf-8 -*-
from yafowil.base import factory


DOC_CHOSEN_SINGLE = """
select2
------

Select2 widget in single selection mode.

.. code-block:: python

    vocab = sorted((u'Weißburgunder', u'Welschriesling',
                    u'Sauvingnon Blanc', u'Sämling', u'Scheurebe',
                    u'Traminer', u'Morrilon', u'Muskateller'))

    select2 = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'required': 'Selection is required',
        'vocabulary': vocab,
        'multivalued': False,
        })

"""

DOC_CHOSEN_MULTI = """
Select2 widget in multi selection mode.

.. code-block:: python

    select2 = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'required': 'Selection is required',
        'vocabulary': vocab,
        'multivalued': True,
        })

"""

DOC_CHOSEN_MULTI_2 = """
.. code-block:: python

    select2 = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'required': 'Selection is required',
        'vocabulary': vocab,
        'multivalued': True,
        'allowClear': True,
        })

"""

def get_example():

    vocab = sorted((u'Weißburgunder', u'Welschriesling',
                    u'Sauvingnon Blanc', u'Sämling', u'Scheurebe',
                    u'Traminer', u'Morrilon', u'Muskateller'))

    # single selection
    select2_single = factory(u'fieldset', name='yafowil_select2_single')
    select2_single['text'] = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'required': 'Selection is required',
        'vocabulary': vocab,
        'multivalued': False,
        })

    # multiple selection
    select2_multi = factory(u'fieldset', name='yafowil_select2_multi')
    select2_multi['text'] = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'required': 'Selection is required',
        'vocabulary': vocab,
        'multivalued': True,
        })

    # multiple selection, search substrings, allow new values
    select2_multi2 = factory(u'fieldset', name='yafowil_select2_multi2')
    select2_multi2['text'] = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'required': 'Selection is required',
        'vocabulary': vocab,
        'multivalued': True,
        'allowClear': True,
        })

    return [{'widget': select2_single,
             'doc': DOC_CHOSEN_SINGLE,
             'title': 'Single Selection'},
            {'widget': select2_multi,
             'doc': DOC_CHOSEN_MULTI,
             'title': 'Multi Selection'},
            {'widget': select2_multi2,
             'doc': DOC_CHOSEN_MULTI_2,
             'title': 'Multi Selection, New Values, Search Substrings'},
           ]
