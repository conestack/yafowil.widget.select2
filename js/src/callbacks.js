const PREFIX = 'javascript:';

// Reachable through a path, but never meant to be a callback.
const REFUSED = ['eval', 'Function', 'setTimeout', 'setInterval'].map((name) => window[name]);

/**
 * Resolves option values using the deprecated ``javascript:`` prefix.
 *
 * Other values than functions stay possible, options like ``data`` take lists.
 *
 * @param {*} value - The option value.
 * @returns {*} - The object found at the path, any other value as it is.
 * @throws Will throw an error if the path cannot be resolved.
 */
export function extract_value(value) {
    if (typeof value !== 'string' || !value.startsWith(PREFIX)) {
        return value;
    }
    console.warn(`yafowil.widget.select2: "${PREFIX}" prefix is deprecated: ${value}`);
    const path = value.substring(PREFIX.length).split('.');
    // path.length is always at least 1, because split returns empty string in
    // array.
    if (!path[0].length) {
        throw 'No function defined';
    }
    let ctx = window;
    for (const name of path) {
        if (!Object.hasOwn(Object(ctx), name)) {
            throw `${name} not found`;
        }
        ctx = ctx[name];
    }
    if (REFUSED.includes(ctx)) {
        throw `${value} is no callback`;
    }
    return ctx;
}
