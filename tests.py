from unittest import TestCase

import xmltodict

from markdown import Markdown
from markdown.util import etree

from mdx_attr_cols import AttrColTreeProcessor


class XmlTestCaseMixin(object):
    def mk_doc(self, s):
        return etree.fromstring(
            "<div>" + s.strip() + "</div>")

    def assertXmlEqual(self, a, b):
        self.assertEqual(
            xmltodict.parse(etree.tostring(a)),
            xmltodict.parse(etree.tostring(b)))


class TestAttrColTreeProcessor(XmlTestCaseMixin, TestCase):
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

    def test_simple_rows(self):
        root = self.mk_doc("""
            <section cols='4'>Foo</section>
            <section cols='6'>Bar</section>
            <section cols='2'>Beep</section>
        """)
        p = self.mk_processor()
        new_root = p.run(root)
        self.assertXmlEqual(new_root, self.mk_doc("""
            <div class="row"><div class="col-md-4"><section>Foo</section>
            </div><div class="col-md-6"><section>Bar</section>
            </div><div class="col-md-2"><section>Beep</section>
            </div></div>
        """))
