import unittest
import csvtools.lib as m


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
