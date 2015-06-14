""" Bootstrap 3 grid extension fo Python Markdown
"""

from markdown.util import etree
from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class AttrColTreeProcessor(Treeprocessor):
    """ The attr_cols element tree processor. """

    CONF_DEFAULTS = {
        'columns': 12,
        'attr': 'cols',
        'tags': ['section'],
    }

    def __init__(self, md, conf):
        super(AttrColTreeProcessor, self).__init__(md)
        conf_vars = self.CONF_DEFAULTS.copy()
        conf_vars.update(conf or {})
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
            del child.attrib[self.attr]

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
    """ The attr_cols markdown extension. """

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
        md.treeprocessors.add('attr_cols', processor, '_end')


def makeExtension(configs=None):
    """ Initialize the attr_cols extension. """
    return AttrColExtension(configs=configs)
