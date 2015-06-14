from unittest import TestCase

import xmltodict

from markdown import Markdown
from markdown.util import etree

from mdx_attr_cols import AttrColTreeProcessor, AttrColExtension, makeExtension


class XmlTestCaseMixin(object):
    def mk_doc(self, s):
        return etree.fromstring(
            "<div>" + s.strip() + "</div>")

    def assert_xml_equal(self, a, b):
        self.assertEqual(
            xmltodict.parse(etree.tostring(a)),
            xmltodict.parse(etree.tostring(b)))


class TestAttrColTreeProcessor(XmlTestCaseMixin, TestCase):
    def mk_processor(self, **conf):
        md = Markdown()
        return AttrColTreeProcessor(md, conf)

    def test_config_none(self):
        md = Markdown
        p = AttrColTreeProcessor(md, None)
        self.assertEqual(p.columns, 12)
        self.assertEqual(p.attr, 'cols')
        self.assertEqual(p.tags, set(['section']))

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
        self.assert_xml_equal(new_root, self.mk_doc("""
            <div class="row"><div class="col-md-4"><section>Foo</section>
            </div><div class="col-md-6"><section>Bar</section>
            </div><div class="col-md-2"><section>Beep</section>
            </div></div>
        """))


class TestAttrColExtension(TestCase):
    def mk_markdown(self, extensions=None):
        if extensions is None:
            extensions = ['attr_list', 'outline']
        md = Markdown(extensions)
        md_globals = {}
        return md, md_globals

    def assert_registered(self, md, md_globals):
        processor = md.treeprocessors['attr_cols']
        self.assertTrue(isinstance(processor, AttrColTreeProcessor))
        self.assertEqual(md_globals, {})

    def assert_not_registered(self, md, md_globals):
        self.assertFalse('attr_cols' in md.treeprocessors)
        self.assertEqual(md_globals, {})

    def text_create(self):
        ext = AttrColExtension({'a': 'b'})
        self.assertEqual(ext.conf, {'a': 'b'})

    def test_extend_markdown(self):
        md, md_globals = self.mk_markdown()
        ext = AttrColExtension({})
        ext.extendMarkdown(md, md_globals)
        self.assert_registered(md, md_globals)

    def test_missing_attr_list(self):
        md, md_globals = self.mk_markdown(['outline'])
        ext = AttrColExtension({})
        self.assertRaisesRegexp(
            RuntimeError,
            "The attr_cols markdown extension depends the following"
            " extensions which must preceded it in the extension list:"
            " attr_list, outline",
            ext.extendMarkdown, md, md_globals)
        self.assert_not_registered(md, md_globals)

    def test_missing_outline(self):
        md, md_globals = self.mk_markdown([])
        ext = AttrColExtension({})
        self.assertRaisesRegexp(
            RuntimeError,
            "The attr_cols markdown extension depends the following"
            " extensions which must preceded it in the extension list:"
            " attr_list, outline",
            ext.extendMarkdown, md, md_globals)
        self.assert_not_registered(md, md_globals)


class TestExtensionRegistration(TestCase):
    def test_make_extension(self):
        configs = {'a': 'b'}
        ext = makeExtension(configs)
        self.assertTrue(isinstance(ext, AttrColExtension))
        self.assertEqual(ext.conf, configs)
