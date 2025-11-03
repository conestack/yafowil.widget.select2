Changes
=======

2.0.0 (unreleased)
------------------

- Update jQuery to version ``4.0.0-beta.2``.
  [lenadax]

- Implement custom ajax adapters in js.
  [lenadax]

- Update select2.js from version ``3.5.0`` to version ``4.1.0``.
  [lenadax]

- Utilize ``select2-bootstrap5-theme`` v1.3.0 (https://github.com/apalfrey/select2-bootstrap-5-theme).
  [lenadax]

- Remove unused locale files.
  [lenadax]

- Implement dark theme for ``Bootstrap5`` dark theme mode.
  [lenadax]

- Use rollup for bundling scss. Use ``make rollup`` to compile js and scss.
  [lenadax]

- Use ``webtestrunner`` instead of ``karma`` for js tests. Use ``make wtr`` to run tests.
  [lenadax]

- Use ``pnpm`` as package manager.
  [lenadax]

- Create Bootstrap5 widget version.
  [lenadax]


2.0a2 (2024-05-23)
------------------

- Fix deprecated imports.
  [rnix]


2.0a1 (2023-05-15)
------------------

- Add ``webresource`` support.
  [rnix]

- Extend JS by ``select2_on_array_add``, ``register_array_subscribers``
  to enable usage in ``yafowil.widget.array``.
  [lenadax]

- Rewrite JavaScript using ES6.
  [lenadax]


1.4 (2018-07-16)
----------------

- Python 3 compatibility.
  [rnix]

- Convert doctests to unittests.
  [rnix]


1.3 (2017-03-28)
----------------

- Catch and log exception if select2 cannot be initialized.
  [rnix, 2017-03-28]


1.2 (2017-03-01)
----------------

- Use ``yafowil.utils.entry_point`` decorator.
  [rnix, 2016-06-28]


1.1 (2015-01-23)
----------------

- ``select2`` provides key/term vocabularies for preselected items.
  [rnix, 2014-07-10]

- Remove ``select2input`` blueprint, use ``inputtag`` property of ``select2``
  blueprint instead.
  [rnix, 2014-06-19]

- Provide all available constructor options in blueprint.
  [rnix, 2014-06-19]

- Update select widget to 3.5.0.
  [rnix, 2014-06-19]

1.0
---

- Make it work.
  [thet]
