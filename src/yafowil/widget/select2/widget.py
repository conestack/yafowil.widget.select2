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
    'width',
    'minimumInputLength',
    'maximumInputLength',
    'minimumResultsForSearch',
    'maximumSelectionSize',
    'placeholder',
    'placeholderOption',
    'separator',
    'allowClear',
    'multiple',
    'closeOnSelect',
    'openOnEnter',
    'id',
    'matcher',
    'sortResults',
    'formatSelection',
    'formatResult',
    'formatResultCssClass',
    'formatNoMatches',
    'formatSearching',
    'formatInputTooShort',
    'formatInputTooLong',
    'formatSelectionTooBig',
    'formatLoadMore',
    'createSearchChoice',
    'createSearchChoicePosition',
    'initSelection',
    'tokenizer',
    'tokenSeparators',
    'query',
    'ajax',
    'data',
    'tags',
    'containerCss',
    'containerCssClass',
    'dropdownCss',
    'dropdownCssClass',
    'dropdownAutoWidth',
    'adaptContainerCssClass',
    'adaptDropdownCssClass',
    'escapeMarkup',
    'selectOnBlur',
    'loadMorePadding',
    'nextSearchTerm',
]


@managedprops('inputtag', *select2_options)
def select2_edit_renderer(widget, data, inputtag=False):
    custom_attrs = data_attrs_helper(widget, data, select2_options)
    if widget.attrs['inputtag']:
        renderer = input_generic_renderer
    else:
        if widget.attrs['multiple'] and not widget.attrs['multivalued']:
            widget.attrs['multivalued'] = True
        renderer = select_edit_renderer
    return renderer(widget, data, custom_attrs=custom_attrs)


factory.register(
    'select2',
    extractors=[select_extractor, generic_required_extractor],
    edit_renderers=[select2_edit_renderer],
    display_renderers=[select_display_renderer])

factory.doc['blueprint']['select2'] = \
"""Add-on blueprint `yafowil.widget.select2
<http://github.com/bluedynamics/yafowil.widget.select2/>`_ .

Integrates <http://ivaynberg.github.io/select2/>`_ .

For detailed widget documentation see
<http://ivaynberg.github.io/select2/#documentation>`_ .
"""

factory.defaults['select2.size'] = None
factory.defaults['select2.default'] = []
factory.defaults['select2.format'] = 'block'

factory.defaults['select2.class'] = 'select2'

factory.defaults['select2.inputtag'] = False
factory.doc['props']['select2.inputtag'] = \
"""Render widget as input element instead of selection.
"""

factory.defaults['select2.width'] = None
factory.doc['props']['select2.width'] = \
"""Controls the width style attribute of the Select2 container div.
The following values are supported:

off
    No width attribute will be set. Keep in mind that the container div copies
    classes from the source element so setting the width attribute may not always be necessary.
element
    Uses javascript to calculate the width of the source element.
copy
    Copies the value of the width style attribute set on the source element.
resolve
    First attempts to copy than falls back on element.
other values
    if the width attribute contains a function it will be evaluated, otherwise
    the value is used verbatim.
"""

factory.defaults['select2.minimumInputLength'] = None
factory.doc['props']['select2.minimumInputLength'] = \
"""Number of characters necessary to start a search.
"""

factory.defaults['select2.maximumInputLength'] = None
factory.doc['props']['select2.maximumInputLength'] = \
"""Maximum number of characters that can be entered for an input.
"""

factory.defaults['select2.minimumResultsForSearch'] = None
factory.doc['props']['select2.minimumResultsForSearch'] = \
"""The minimum number of results that must be initially (after opening the
dropdown for the first time) populated in order to keep the search field.
This is useful for cases where local data is used with just a few results,
in which case the search box is not very useful and wastes screen space.

The option can be set to a negative value to permanently hide the search field.

Only applies to single-value select boxes.
"""

factory.defaults['select2.maximumSelectionSize'] = None
factory.doc['props']['select2.maximumSelectionSize'] = \
"""The maximum number of items that can be selected in a multi-select control.
If this number is less than 1 selection is not limited.

Once the number of selected items reaches the maximum specified the contents
of the dropdown will be populated by the formatSelectionTooBig function.
"""

factory.defaults['select2.placeholder'] = None
factory.doc['props']['select2.placeholder'] = \
"""Initial value that is selected if no other selection is made.

The placeholder can also be specified as a data-placeholder attribute on the
select or input element that Select2 is attached to.

Note that because browsers assume the first option element is selected in
non-multi-value select boxes an empty first option element must be provided
(<option></option>) for the placeholder to work.
"""

factory.defaults['select2.placeholderOption'] = None
factory.doc['props']['select2.placeholderOption'] = \
"""When attached to a select resolves the option that should be used as the
placeholder. Can either be a function which given the select element should
return the option element or a string first to indicate that the first option
should be used.

This option is useful when Select2's default of using the first option only if
it has no value and no text is not suitable.
"""

factory.defaults['select2.separator'] = None
factory.doc['props']['select2.separator'] = \
"""Separator character or string used to delimit ids in value attribute of the
multi-valued selects. The default delimiter is the , character.
"""

factory.defaults['select2.allowClear'] = None;
factory.doc['props']['select2.allowClear'] = \
"""Whether or not a clear button is displayed when the select box has a
selection. The button, when clicked, resets the value of the select box back
to the placeholder, thus this option is only available when the placeholder is
specified.

This option only works when the placeholder is specified.

When attached to a select an option with an empty value must be provided. This
is the option that will be selected when the button is pressed since a select
box requires at least one selection option.

Also, note that this option only works with non-multi-value based selects
because multi-value selects always provide such a button for every selected
option.
"""

factory.defaults['select2.multiple'] = False
factory.doc['props']['select2.multiple'] = \
"""Whether or not Select2 allows selection of multiple values.

When Select2 is attached to a select element this value will be ignored and
select's multiple attribute will be used instead.
"""

factory.defaults['select2.closeOnSelect'] = None
factory.doc['props']['select2.closeOnSelect'] = \
"""If set to false the dropdown is not closed after a selection is made,
allowing for rapid selection of multiple items. By default this option is set
to true.

Only applies when configured in multi-select mode.
"""

factory.defaults['select2.openOnEnter'] = None
factory.doc['props']['select2.openOnEnter'] = \
"""If set to true the dropdown is opened when the user presses the enter key
and Select2 is closed. By default this option is enabled.
"""

factory.defaults['select2.id'] = None
factory.doc['props']['select2.id'] = \
"""Function used to get the id from the choice object or a string representing
the key under which the id is stored.

    id(object)

The default implementation expects the object to have a id property that is
returned.
"""

factory.defaults['select2.matcher'] = None
factory.doc['props']['select2.matcher'] = \
"""Used to determine whether or not the search term matches an option when a
built-in query function is used. The built in query function is used when
Select2 is attached to a select, or the local or tags helpers are used.

    matcher(term, text, option)

The default implementation is case insensitive and matches anywhere in the
term:

    function(term, text) {
        return text.toUpperCase().indexOf(term.toUpperCase()) >= 0;
    }
"""

factory.defaults['select2.sortResults'] = None
factory.doc['props']['select2.sortResults'] = \
"""Used to sort the results list for searching right before display.
Useful for sorting matches by relevance to the user's search term.

    sortResults(results, container, query)

Defaults to no sorting:

    function(results, container, query) {
        return results;
    }
"""

factory.defaults['select2.formatSelection'] = None
factory.doc['props']['select2.formatSelection'] = \
"""Function used to render the current selection.

    formatSelection(object, container)

The default implementation expects the object to have a text property that is
returned.

The implementation may choose to append elements directly to the provided
container object, or return a single value and have it automatically appended.

When attached to a select the original <option> (or <optgroup>) element is
accessible inside the specified function through the property item.element:

    format(item) {
        var originalOption = item.element;
        return item.text
    }
"""

factory.defaults['select2.formatResult'] = None
factory.doc['props']['select2.formatResult'] = \
"""Function used to render a result that the user can select.

    formatResult(object, container, query)

The default implementation expects the object to have a text property that is
returned.

The implementation may choose to append elements directly to the provided
container object, or return a single value and have it automatically appended.

When attached to a select the original <option> (or <optgroup>) element is
accessible inside the specified function through the property item.element:

    format(item) {
        var originalOption = item.element;
        return item.text
    }
"""

factory.defaults['select2.formatResultCssClass'] = None
factory.doc['props']['select2.formatResultCssClass'] = \
"""Function used to add css classes to result elements.

    formatResultCssClass(object)

By default when attached to a select css classes from options will be
automatically copied.
"""

factory.defaults['select2.formatNoMatches'] = None
factory.doc['props']['select2.formatNoMatches'] = \
"""String containing "No matches" message, or
Function used to render the message

    formatNoMatches(term)
"""

factory.defaults['select2.formatSearching'] = None
factory.doc['props']['select2.formatSearching'] = \
"""String containing "Searching..." message, or
Function used to render the message that is displayed while search is in
progress.

    formatSearching()
"""

factory.defaults['select2.formatInputTooShort'] = None
factory.doc['props']['select2.formatInputTooShort'] = \
"""String containing "Search input too short" message, or Function used to
render the message.

    formatInputTooShort(term, minLength)
"""

factory.defaults['select2.formatInputTooLong'] = None
factory.doc['props']['select2.formatInputTooLong'] = \
"""String containing "Search input too long" message, or Function used to
render the message.

    formatInputTooLong(term, maxLength)
"""

factory.defaults['select2.formatSelectionTooBig'] = None
factory.doc['props']['select2.formatSelectionTooBig'] = \
"""String containing "You cannot select any more choices" message, or Function
used to render the message.

    formatSelectionTooBig(maxSize)
"""

factory.defaults['select2.formatLoadMore'] = None
factory.doc['props']['select2.formatLoadMore'] = \
"""String containing "Loading more results…" message, or Function used to
render the message.

    formatLoadMore(pageNumber)
"""

factory.defaults['select2.createSearchChoice'] = None
factory.doc['props']['select2.createSearchChoice'] = \
"""Creates a new selectable choice from user's search term. Allows creation of
choices not available via the query function. Useful when the user can create
choices on the fly, eg for the 'tagging' usecase.

    createSearchChoice(term)

If the function returns undefined or null no choice will be created. If a new
choice is created it is displayed first in the selection list so that user
may select it by simply pressing enter.

When used in combination with input[type=hidden] tag care must be taken to
sanitize the id attribute of the choice object, especially stripping , as it
is used as a value separator.
"""

factory.defaults['select2.createSearchChoicePosition'] = None
factory.doc['props']['select2.createSearchChoicePosition'] = \
"""Define the position where to insert element created by createSearchChoice.
The following values are supported:

top
    Insert in the top of the list
bottom
    Insert at the end of the list
<function>

    A custom function. For example if you want to insert the new item in the
    second position:

    $("#tags").select2({
        ...
        createSearchChoice: function(term) { ... },
        createSearchChoicePosition: function(list, item) {
            list.splice(1, 0, item);
        }
    });
"""

factory.defaults['select2.initSelection'] = None
factory.doc['props']['select2.initSelection'] = \
"""Called when Select2 is created to allow the user to initialize the
selection based on the value of the element select2 is attached to.

Essentially this is an id->object mapping function.

    initSelection(element, callback)

This function will only be called when there is initial input to be processed.
"""

factory.defaults['select2.tokenizer'] = None
factory.doc['props']['select2.tokenizer'] = \
"""A tokenizer function can process the input typed into the search field after
every keystroke and extract and select choices. This is useful, for example,
in tagging scenarios where the user can create tags quickly by separating
them with a comma or a space instead of pressing enter.

Tokenizer only applies to multi-selects.

    tokenizer(input, selection, selectCallback, opts)
"""

factory.defaults['select2.tokenSeparators'] = None
factory.doc['props']['select2.tokenSeparators'] = \
"""An array of strings that define token separators for the default tokenizer
function. By default, this option is set to an empty array which means
tokenization using the default tokenizer is disabled. Usually it is sensible
to set this option to a value similar to [',', ' '].
"""

factory.defaults['select2.query'] = None
factory.doc['props']['select2.query'] = \
"""Function used to query results for the search term.

    query(options)

In order for this function to work Select2 should be attached to a input
type='hidden' tag instead of a select.
"""

factory.defaults['select2.ajax'] = None
factory.doc['props']['select2.ajax'] = \
"""Options for the built in ajax query function. This object acts as a
shortcut for having to manually write a function that performs ajax requests.
The built-in function supports more advanced features such as throttling and
dropping out-of-order responses.

In order for this function to work Select2 should be attached to a input
type='hidden' tag instead of a select.
"""

factory.defaults['select2.data'] = None
factory.doc['props']['select2.data'] = \
"""Options for the built in query function that works with arrays.

If this element contains an array, each element in the array must contain id
and text keys.

Alternatively, this element can be specified as an object in which results
key must contain the data as an array and a text key can either be the name
of the key in data items that contains text or a function that retrieves
the text given a data element from the array.
"""

factory.defaults['select2.tags'] = None
factory.doc['props']['select2.tags'] = \
"""Puts Select2 into 'tagging' mode where the user can add new choices and
pre-existing tags are provided via this options attribute which is either an
array or a function that returns an array of objects or strings. If strings
are used instead of objects they will be converted into an object that has
an id and text attribute equal to the value of the string.
"""

factory.defaults['select2.containerCss'] = None
factory.doc['props']['select2.containerCss'] = \
"""Inline css that will be added to select2's container. Either an object
containing css property/value key pairs or a function that returns such an
object.
"""

factory.defaults['select2.containerCssClass'] = None
factory.doc['props']['select2.containerCssClass'] = \
"""Css class that will be added to select2's container tag.
"""

factory.defaults['select2.dropdownCss'] = None
factory.doc['props']['select2.dropdownCss'] = \
"""Inline css that will be added to select2's dropdown container. Either an
object containing css property/value key pairs or a function that returns such
an object.
"""

factory.defaults['select2.dropdownCssClass'] = None
factory.doc['props']['select2.dropdownCssClass'] = \
"""Css class that will be added to select2's dropdown container.
"""

factory.defaults['select2.dropdownAutoWidth'] = None
factory.doc['props']['select2.dropdownAutoWidth'] = \
"""When set to true attempts to automatically size the width of the dropdown
based on content inside.
"""

factory.defaults['select2.adaptContainerCssClass'] = None
factory.doc['props']['select2.adaptContainerCssClass'] = \
"""Function that filters/renames css classes as they are copied from the
source tag to the select2 container tag.

    adaptContainerCssClass(clazz)

The default implementation applies all classes without modification.
"""

factory.defaults['select2.adaptDropdownCssClass'] = None
factory.doc['props']['select2.adaptDropdownCssClass'] = \
"""Function that filters/renames css classes as they are copied from the
source tag to the select2 dropdown tag.

    adaptDropdownCssClass(clazz)

The default implementation always returns null thereby filtering out all
classes.
"""

factory.defaults['select2.escapeMarkup'] = None
factory.doc['props']['select2.escapeMarkup'] = \
"""String escapeMarkup(String markup)

Function used to post-process markup returned from formatter functions. By
default this function escapes html entities to prevent javascript injection.
"""

factory.defaults['select2.selectOnBlur'] = None
factory.doc['props']['select2.selectOnBlur'] = \
"""Set to true if you want Select2 to select the currently highlighted option
when it is blurred.
"""

factory.defaults['select2.loadMorePadding'] = None
factory.doc['props']['select2.loadMorePadding'] = \
"""Defines how many pixels need to be below the fold before the next page is
loaded. The default value is 0 which means the result list needs to be
scrolled all the way to the bottom for the next page of results to be loaded.
This option can be used to trigger the load sooner, possibly resulting in a
smoother user experience.
"""

factory.defaults['select2.nextSearchTerm'] = None
factory.doc['props']['select2.nextSearchTerm'] = \
"""Function used to determine what the next search term should be.

Function can be used when the dropdown is configured in single and
multi-select mode. It is triggered after selecting an item. In single mode
it is also triggered after initSelection (when provided).
"""


factory.defaults['select2.'] = None
factory.doc['props']['select2.'] = \
"""
"""
