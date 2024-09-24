import cleanup from 'rollup-plugin-cleanup';
import {terser} from 'rollup-plugin-terser';

const out_dir = 'src/yafowil/widget/select2/resources';
const out_dir_bs5 = 'src/yafowil/widget/select2/resources/bootstrap5';

const outro = `
window.yafowil = window.yafowil || {};
window.yafowil.select2 = exports;
`;

export default args => {
    let conf = {
        input: 'js/src/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            name: 'yafowil_select2',
            file: `${out_dir}/widget.js`,
            format: 'iife',
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        }],
        external: [
            'jquery'
        ]
    };
    if (args.configDebug !== true) {
        conf.output.push({
            name: 'yafowil_select2',
            file: `${out_dir}/widget.min.js`,
            format: 'iife',
            plugins: [
                terser()
            ],
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        });
    }

    // Bootstrap 5
    let conf2 = {
        input: 'js/src/bootstrap5/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            name: 'yafowil_select2',
            file: `${out_dir_bs5}/widget.js`,
            format: 'iife',
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        }],
        external: [
            'jquery'
        ]
    };
    if (args.configDebug !== true) {
        conf2.output.push({
            name: 'yafowil_select2',
            file: `${out_dir_bs5}/widget.min.js`,
            format: 'iife',
            plugins: [
                terser()
            ],
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        });
    }

    return [conf, conf2];
};
