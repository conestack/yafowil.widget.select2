import $ from 'jquery';

import {Select2Widget} from './widget.js';
import {register_array_subscribers} from './widget.js';

export * from './widget.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(Select2Widget.initialize, true);
    } else if (window.bdajax !== undefined) {
        bdajax.register(Select2Widget.initialize, true);
    } else {
        Select2Widget.initialize();
    }
    register_array_subscribers();
});
