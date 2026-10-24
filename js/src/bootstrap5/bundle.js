import $ from 'jquery';
import { register_array_subscribers, Select2Widget } from './widget.js';

export * from './widget.js';

$(() => {
    if (window.ts !== undefined) {
        ts.ajax.register(Select2Widget.initialize, true);
    } else if (window.bdajax !== undefined) {
        bdajax.register(Select2Widget.initialize, true);
    } else {
        Select2Widget.initialize();
    }
    register_array_subscribers();
});
