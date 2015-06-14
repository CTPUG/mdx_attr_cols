mdx_attr_cols
=============

|attr-cols-ci-badge|

.. |attr-cols-ci-badge| image:: https://travis-ci.org/CTPUG/mdx_attr_cols.png?branch=master
    :alt: Travis CI build status
    :scale: 100%
    :target: https://travis-ci.org/CTPUG/mdx_attr_cols

A Markdown extension to add support for Bootstrap 3 rows and columns.

Licensed under the `ISC License`_.

.. _ISC License: https://github.com/CTPUG/mdx_attr_cols/blob/master/LICENSE


Requirements
============

The mdx_attr_cols plugin requires the following additional Markdown
plugins:

*  `attr_list`_ (built-in to the markdown library)
*  `outline`_

.. _attr_list: http://pythonhosted.org/Markdown/extensions/attr_list.html
.. _outline: https://pypi.python.org/pypi/mdx_outline


Installation
============

Install with ``pip install mdx_attr_cols``.


Documentation
=============

Allows creating bootstrap container rows and columns using section
attributes as provided by the attr_list and outline extensions.

Markdown example:

.. code:: markdown

  Header 1 {: cols=6 }
  ====================

  Some paragraphs go here.

  Header 2 {: cols=2 }
  ====================

  More paragraphs go here.

  Header 3 {: cols=4 }
  ====================

  Final column.

  Header 4
  ========

  This is not in a row or column.

Python usage:

.. code:: python

  md = markdown.Markdown(
      extensions=[
          'outline',
          'attr_list',
          'attr_cols',
      ],
      extension_configs={
          'attr_cols': {
              'columns': 12,
              'attr': 'cols',
              'tags': ['section'],
          }
      })

Configuration options:

* ``columns``: Number of columns in a row. Default is ``12``.
* ``tags``: List of HTML tags to look for attributes on. Default is
  ``['sections']``.
* ``attr``: Name of column width attribute. Default is ``'cols'``.
