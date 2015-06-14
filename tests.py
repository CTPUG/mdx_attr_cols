from unittest import TestCase

from markdown import Markdown

from mdx_attr_cols import AttrColTreeProcessor


class TestAttrColTreeProcessor(TestCase):
    def mk_processor(self, **conf):
        md = Markdown()
        return AttrColTreeProcessor(md, conf)

    def test_config_defaults(self):
        p = self.mk_processor()
        self.assertEqual(p.columns, 12)
        self.assertEqual(p.attr, 'cols')
        self.assertEqual(p.tags, set(['section']))

    def test_config_overrides(self):
        p = self.mk_processor(
            columns=16,
            attr='columns',
            tags=['section', 'div'],
        )
        self.assertEqual(p.columns, 16)
        self.assertEqual(p.attr, 'columns')
        self.assertEqual(p.tags, set(['section', 'div']))
