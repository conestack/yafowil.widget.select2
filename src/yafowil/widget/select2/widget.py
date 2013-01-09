from yafowil.base import (
    factory,
)
from yafowil.common import (
    select_extractor,
    generic_required_extractor,
    select_edit_renderer,
    select_display_renderer,
    input_generic_renderer,
)
from yafowil.utils import (
    managedprops,
    data_attrs_helper,
    attr_value
)


select2_options = [
    'allowClear',
    'placeholder',
    'minimumInputLength',
    'formatResult',
    'formatSelection',
    'query',
    'maximumSelectionSize',
    'data',
    'ajax',
    'tags',
    'maximumInputLength',
    'tokenSeparators',
    'matcher',
    ]

# TODO: allow data_attrs_helper to convert correctly lists
#       and let yafowil tag renderer support let support arrays
#

@managedprops('multiple', *select2_options)
def select2_edit_renderer(widget, data, inputtag=False):
    multiple = attr_value('multiple', widget, data)
    custom_attrs = data_attrs_helper(widget, data, select2_options)
    
    renderer = inputtag and input_generic_renderer or select_edit_renderer 
    return renderer(widget, data, multiple=multiple, **custom_attrs)

@managedprops('multiple', *select2_options)
def select2_edit_renderer_input(widget, data):
    return select2_edit_renderer(widget, data, inputtag=True)

 
factory.register(
    'select2',
    extractors=[select_extractor, generic_required_extractor],
    edit_renderers=[select2_edit_renderer],
    display_renderers=[select_display_renderer])

factory.register(
    'select2input',
    extractors=[select_extractor, generic_required_extractor],
    edit_renderers=[select2_edit_renderer_input],
    display_renderers=[input_generic_renderer])


factory.doc['blueprint']['select2'] = \
"""Add-on blueprint `yafowil.widget.select2
<http://github.com/bluedynamics/yafowil.widget.select2/>`_ .
"""

factory.defaults['select2.size'] = None
factory.defaults['select2.default'] = []
factory.defaults['select2.format'] = 'block'

factory.defaults['select2input.class'] = 'select2'
factory.defaults['select2.class'] = 'select2'

factory.defaults['select2input.multiple'] =\
factory.defaults['select2.multiple'] = False # HTML attribute

factory.defaults['select2input.placeholder'] =\
factory.defaults['select2.placeholder'] = None

factory.defaults['select2input.minimumInputLength'] =\
factory.defaults['select2.minimumInputLength'] = None

factory.defaults['select2input.formatResult'] =\
factory.defaults['select2.formatResult'] = None

factory.defaults['select2input.formatSelection'] =\
factory.defaults['select2.formatSelection'] = None

factory.defaults['select2input.query'] =\
factory.defaults['select2.query'] = None

factory.defaults['select2input.maximumSelectionSize'] =\
factory.defaults['select2.maximumSelectionSize'] = None

factory.defaults['select2input.data'] =\
factory.defaults['select2.data'] = None

factory.defaults['select2input.ajax'] =\
factory.defaults['select2.ajax'] = None

factory.defaults['select2input.tags'] =\
factory.defaults['select2.tags'] = None

factory.defaults['select2input.maximumInputLength'] =\
factory.defaults['select2.maximumInputLength'] = None

factory.defaults['select2input.tokenSeparators'] =\
factory.defaults['select2.tokenSeparators'] = None

factory.defaults['select2.matcher'] =\
factory.defaults['select2.matcher'] = None


factory.doc['props']['select2.ajax'] = \
"""
Example Code

    $("#e6").select2({
    placeholder: "Search for a movie",
    minimumInputLength: 1,
    ajax: { // instead of writing the function to execute the request we use Select2's convenient helper
    url: "http://api.rottentomatoes.com/api/public/v1.0/movies.json",
    dataType: 'jsonp',
    data: function (term, page) {
    return {
    q: term, // search term
    page_limit: 10,
    apikey: "ju6z9mjyajq2djue3gbvv26t" // please do not use so this example keeps working
    };
    },
    results: function (data, page) { // parse the results into the format expected by Select2.
    // since we are using custom formatting functions we do not need to alter remote JSON data
    return {results: data.movies};
    }
    },
    formatResult: movieFormatResult, // omitted for brevity, see the source of this page
    formatSelection: movieFormatSelection, // omitted for brevity, see the source of this page
    dropdownCssClass: "bigdrop" // apply css that makes the dropdown taller
    });


Example 2 Code: Ajax with infinite scrolling.

    $("#e7").select2({
    placeholder: "Search for a movie",
    minimumInputLength: 3,
    ajax: {
    url: "http://api.rottentomatoes.com/api/public/v1.0/movies.json",
    dataType: 'jsonp',
    quietMillis: 100,
    data: function (term, page) { // page is the one-based page number tracked by Select2
    return {
    q: term, //search term
    page_limit: 10, // page size
    page: page, // page number
    apikey: "ju6z9mjyajq2djue3gbvv26t" // please do not use so this example keeps working
    };
    },
    results: function (data, page) {
    var more = (page * 10) < data.total; // whether or not there are more results available
     
    // notice we return the value of more so Select2 knows if more results can be loaded
    return {results: data.movies, more: more};
    }
    },
    formatResult: movieFormatResult, // omitted for brevity, see the source of this page
    formatSelection: movieFormatSelection, // omitted for brevity, see the source of this page
    dropdownCssClass: "bigdrop" // apply css that makes the dropdown taller
    });
"""

factory.defaults['select2.allowClear'] = None;
factory.doc['props']['select2.allowClear'] = \
"""Allow adding new values.
For: select2
Values: [True|False|None (default)].
"""
