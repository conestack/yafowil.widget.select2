# -*- coding: utf-8 -*-
from yafowil.base import factory


DOC_SELECT2_1 = """
select2
-------

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

DOC_SELECT2_2 = """
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


def get_example():

    vocab = sorted((u'Weißburgunder', u'Welschriesling',
                    u'Sauvingnon Blanc', u'Sämling', u'Scheurebe',
                    u'Traminer', u'Morrilon', u'Muskateller'))

    # single selection
    select2_1 = factory(u'fieldset', name='yafowil_select2_1')
    select2_1['text'] = factory('#field:select2', props={
        'placeholder': 'Select some items or type',
        'vocabulary': vocab,
        })

    # multiple selection
    select2_2 = factory(u'fieldset', name='yafowil_select2_2')
    select2_2['text'] = factory('#field:select2input', props={
        'placeholder': 'Select some items or type',
        'vocabulary': vocab,
        'multiple': 'multiple',
        'allowClear': True,
        'placeholder': 'select some items',
        'minimumInputLength': 1,
        'tags': '',
        })

    return [{'widget': select2_1,
             'doc': DOC_SELECT2_1,
             'title': 'Single Selection'},
            {'widget': select2_2,
             'doc': DOC_SELECT2_2,
             'title': 'Multi Selection'},
           ]
