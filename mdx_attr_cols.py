"""
Bootstrap 3 grid extension fo Python Markdown
=============================================

Allows creating bootstrap container rows and columns using
section attributes as provided by the attr_list and outline
extensions.

Markdown example::

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

Python usage::

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

* columns: Number of columns in a row. Default is 12.
* tags: List of HTML tags to look for attributes on. Default is ['sections'].
* attr: Name of column width attribute. Default is 'cols'.

"""

from markdown.util import etree
from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class AttrColTreeProcessor(Treeprocessor):
    """ The attr_col element tree processor. """

    CONF_DEFAULTS = {
        'columns': 12,
        'attr': 'cols',
        'tags': ['section'],
    }

    def __init__(self, md, conf):
        super(AttrColTreeProcessor, self).__init__(md)
        conf_vars = self.CONF_DEFAULTS.copy()
        conf_vars.update(conf)
        self.columns = int(conf_vars.get('columns'))
        self.attr = str(conf_vars.get('attr'))
        self.tags = set(conf_vars.get('tags'))

    def create_rows(self, node):
        row, row_cols = None, 0
        for i, child in enumerate(list(node)):
            if child.tag.lower() not in self.tags:
                continue

            if self.attr not in child.attrib:
                if row is None:
                    # if there currently isn't a row, search sub-sections
                    self.create_rows(child)
                else:
                    row, row_cols = None, 0
                continue
            cols = int(child.attrib[self.attr])

            if row is None:
                row = etree.Element("div", {"class": "row"})
                node.insert(i, row)

            col = etree.SubElement(row, "div", {
                "class": "col-md-%d" % (cols,),
            })
            row_cols += cols

            col.append(child)
            node.remove(child)

            if row_cols >= self.columns:
                row, row_cols = None, 0

    def run(self, root):
        self.create_rows(root)
        return root


class AttrColExtension(Extension):
    """ The attr_col markdown extension. """

    REQUIRED_EXTENSIONS = ('attr_list', 'outline')

    def __init__(self, configs):
        self.conf = configs

    def extendMarkdown(self, md, md_globals):
        """Initializes markdown extension components."""
        if any(x not in md.treeprocessors for x in self.REQUIRED_EXTENSIONS):
            raise RuntimeError(
                "The attr_cols markdown extension depends the following"
                " extensions which must preceded it in the extension"
                " list: %s" % ", ".join(self.REQUIRED_EXTENSIONS))
        processor = AttrColTreeProcessor(md, self.conf)
        md.treeprocessors.add('attr_col', processor, '_end')


def makeExtension(configs=None):
    """ Initialize the attr_col extension. """
    return AttrColExtension(configs=configs)
