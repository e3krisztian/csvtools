import unittest
import csvtools.lib as m
from operator import itemgetter


class TestHeader(unittest.TestCase):

    @property
    def header(self):
        return m.Header('a b c'.split())

    def test_len(self):
        self.assertEqual(3, len(self.header))

    def test_in(self):
        header = self.header
        self.assertTrue('a' in header)
        self.assertTrue('b' in header)
        self.assertTrue('c' in header)

    def test_not_in(self):
        self.assertTrue('d' not in self.header)

    def test_iter(self):
        self.assertEqual(['a', 'b', 'c'], list(self.header))

    def test_extractor(self):
        extractor = self.header.extractor('b')
        self.assertEqual(2, extractor([1, 2, 3]))

    def test_extractors(self):
        extractors = self.header.extractors(['b', 'a'])
        self.assertEqual([2, 1], [x([1, 2, 3]) for x in extractors])


class Seq_extractor_Tests(object):
    # Mixin class adding tests for sequence extractors

    seq_type = 'any sequence type'
    function_under_test = 'seq extractor creator function'

    def skip_if_mixin(self):
        if not isinstance(self, unittest.TestCase):
            raise unittest.SkipTest(
                '... test runner erroneously picks up mixins')

    def test(self):
        self.skip_if_mixin()
        extract = self.function_under_test([itemgetter(0), itemgetter(2)])

        self.assertEqual(self.seq_type([1, 3]), extract([1, 2, 3]))
        self.assertEqual(self.seq_type(['a', 'c']), extract('abcdefg'))

    def test_works_with_iterator_parameter(self):
        self.skip_if_mixin()
        item_extractors_iterator = iter([itemgetter(0), itemgetter(2)])
        extract = self.function_under_test(item_extractors_iterator)

        self.assertEqual(self.seq_type([1, 3]), extract([1, 2, 3]))
        self.assertEqual(self.seq_type(['a', 'c']), extract('abcdefg'))


class Test_list_extractor(Seq_extractor_Tests, unittest.TestCase):

    seq_type = list
    function_under_test = staticmethod(m.list_extractor)


class Test_tuple_extractor(Seq_extractor_Tests, unittest.TestCase):

    seq_type = tuple
    function_under_test = staticmethod(m.tuple_extractor)


class TestFieldsMap_parse(unittest.TestCase):

    def test_input_fields(self):
        fm = m.FieldsMap.parse('aout=a,b,cout=c')

        self.assertTupleEqual(('a', 'b', 'c'), fm.input_fields)

    def test_output_fields(self):
        # [out=]in
        fm = m.FieldsMap.parse('aout=a,b,cout=c')

        self.assertTupleEqual(('aout', 'b', 'cout'), fm.output_fields)

    def test_duplicate_output_field_raises_error(self):
        with self.assertRaises(m.DuplicateFieldError):
            m.FieldsMap.parse('a=b,a')
