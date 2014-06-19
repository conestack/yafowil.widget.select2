# -*- coding: utf-8 -*-
from yafowil.base import factory

TITLE_SELECT2_1 = "Single selection"
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
        'vocabulary': vocab,
    })

"""

TITLE_SELECT2_2 = "Multi selection"
DOC_SELECT2_2 = """
Select2 widget in multi selection mode.

.. code-block:: python

    select2 = factory('#field:select2', props={
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

    select2 = factory('#field:select2', props={
        'label': 'Select or add some items',
        'inputtag': True,
        'placeholder': 'Select or add some items',
        'minimumInputLength': 1,
        'multiple': True,
        'tags': vocab,
    })

"""


def get_example():

    vocab = sorted((u'Weißburgunder', u'Welschriesling',
                    u'Sauvingnon Blanc', u'Sämling', u'Scheurebe',
                    u'Traminer', u'Morrilon', u'Muskateller'))

    # single selection
    select2_1 = factory(u'fieldset', name='yafowil_select2_1')
    select2_1['text'] = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'vocabulary': vocab,
    })

    # multiple selection
    select2_2 = factory(u'fieldset', name='yafowil_select2_2')
    select2_2['text'] = factory('#field:select2', props={
        'label': 'Select some items',
        'placeholder': 'Select some items',
        'vocabulary': vocab,
        'multiple': True,
    })

    # input mode
    select2_3 = factory(u'fieldset', name='yafowil_select2_3')
    select2_3['text'] = factory('#field:select2', props={
        'label': 'Select or add some items',
        'inputtag': True,
        'placeholder': 'Select or add some items',
        'minimumInputLength': 1,
        'multiple': True,
        'tags': vocab,
    })

    return [{'widget': select2_1,
             'doc': DOC_SELECT2_1,
             'title': TITLE_SELECT2_1},
            {'widget': select2_2,
             'doc': DOC_SELECT2_2,
             'title': TITLE_SELECT2_2},
            {'widget': select2_3,
             'doc': DOC_SELECT2_3,
             'title': TITLE_SELECT2_3},
           ]
