import $ from 'jquery';

// Mock Select2 AMD API before any modules that depend on it are imported.
// Select2 uses an AMD module system for extending adapters.
export const amd_modules = {};

// Mock implementations for Select2 internal modules
const mockAjaxAdapter = function($element, options) {
    this.$element = $element;
    this.options = options;
};
mockAjaxAdapter.prototype.select = function(data) {};

const mockUtils = {
    Extend: function(Child, Parent) {
        Child.__super__ = { constructor: Parent };
        Child.prototype = Object.create(Parent.prototype);
        Child.prototype.constructor = Child;
    }
};

$.fn.select2 = function() { return this; };
$.fn.select2.amd = {
    define: function(name, deps, factory) {
        // Resolve dependencies and call factory
        const resolved = deps.map(dep => {
            if (dep === 'select2/data/ajax') return mockAjaxAdapter;
            if (dep === 'select2/utils') return mockUtils;
            return amd_modules[dep];
        });
        amd_modules[name] = factory.apply(null, resolved);
    },
    require: function(name) {
        return amd_modules[name];
    }
};

export { $ };
