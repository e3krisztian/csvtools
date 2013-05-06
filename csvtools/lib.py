from operator import itemgetter
from csvtools.exceptions import DuplicateFieldError


class Header(object):

    def __init__(self, header_row):
        self.fields_list = list(header_row)
        self.extractors_by_name = dict(
            (header_field, itemgetter(i))
            for (i, header_field) in enumerate(self.fields_list))

    def __contains__(self, name):
        return name in self.extractors_by_name

    def __iter__(self):
        '''iterator over field names'''
        return iter(self.fields_list)

    def __len__(self):
        return len(self.fields_list)

    def extractor(self, name):
        return self.extractors_by_name[name]


# FIXME: this duplicates functionality of FieldMaps in field_maps
# TODO: remove class field_map.field_maps
class FieldsMap(object):

    def __init__(self, output_input_field_pairs):
        self.field_maps = output_input_field_pairs
        if len(set(self.output_fields)) != len(self.field_maps):
            raise DuplicateFieldError(self.output_fields)

    @classmethod
    def parse(cls, field_maps_string):
        '''
        Parses list of field maps, where field maps are separated by comma (,)
        '''
        return cls(
            tuple(
                cls._parse_field_spec(field_spec)
                for field_spec in field_maps_string.split(',')))

    @classmethod
    def _parse_field_spec(cls, field_spec):
        '''
        Parses field specs format: [out=]in
        '''
        output_field_name, eq, input_field_name = field_spec.partition('=')
        input_field_name = input_field_name or output_field_name
        return (output_field_name, input_field_name)

    def __iter__(self):
        return iter(self.field_maps)

    @property
    def input_fields(self):
        return tuple(i for (o, i) in self.field_maps)

    @property
    def output_fields(self):
        return tuple(o for (o, i) in self.field_maps)
