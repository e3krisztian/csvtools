'''
Replace a set of fields with a reference to map.csv file rows

Usage:
extract_map map.csv map_fields_spec ref_field_spec

Technically:
- read original map from map.csv if that file exists
- remove input side of map_fields_spec from input
- append input side of ref_field_spec to input
- append new mappings to map.csv

'''

import argparse
import os.path
import sys
from csvtools.lib import FieldsMap, Header
from csvtools.exceptions import MissingFieldError
from csvtools.exceptions import ExtraFieldError
from csvtools.exceptions import InvalidReferenceFieldError

import csv


'''
parse params (map_file, field map, mapref fields)
read in map file -> existing map
open map file in append only mode
for every input line:
    get mapref for values, extend map if needed
    write output
'''

class Mapper(object):

    ''' Map attributes to entity reference number.

    The mapping might be [partially] pre-existing, in this case
    it is extended if new values are mapped, or not yet existing,
    then it is created.
    '''

    @classmethod
    def new(cls, ref_field, fields, appender):
        header = (ref_field,) + tuple(fields)
        appender.writerow(header)
        return cls(ref_field, fields, [header], appender)

    def __init__(self, ref_field, fields, reader, appender):
        self.appender = appender
        self.max_ref = 0
        self.values_to_ref = dict()
        reader = iter(reader)
        header = Header(reader.next())

        self._check_parameters(ref_field, fields, header)

        param_header = Header([ref_field] + fields)
        to_map_order_extractors = [
            param_header.extractor(field)
            for field in header]
        def to_map_order(ref_field_and_values):
            return tuple(
                x(ref_field_and_values)
                for x in to_map_order_extractors)
        self.to_map_order = to_map_order

        def permutated_reader():
            extractors = (
                [header.extractor(ref_field)]
                + [header.extractor(field) for field in fields])
            for row in reader:
                yield tuple(x(row) for x in extractors)

        self._read_existing_mappings(permutated_reader())

    def _check_parameters(self, ref_field, fields, header):
        all_fields = set(fields).union(set([ref_field]))
        header_fields = set(header)

        if ref_field in fields:
            raise InvalidReferenceFieldError(ref_field)

        if all_fields - header_fields:
            raise MissingFieldError(all_fields - header_fields)

        if header_fields - all_fields:
            raise ExtraFieldError(header_fields - all_fields)

    def _read_existing_mappings(self, reader):
        for ref_and_values in reader:
            ref = int(ref_and_values[0])
            values = tuple(ref_and_values[1:])
            self.max_ref = max(ref, self.max_ref)
            # XXX: check input map against multiple maps?
            self.values_to_ref[values] = ref

    def map(self, values):
        ''' Map attributes to entity reference number.

        Multiple calls for same values will return the same reference.
        New values and their assigned references are persisted.
        '''
        ref = self.values_to_ref.get(values)

        if ref is None:
            self.max_ref += 1
            ref = self.max_ref
            self.values_to_ref[values] = ref
            new_mapping = self.to_map_order((ref,) + tuple(values))
            self.appender.writerow(new_mapping)

        return ref


class MapExtractor(object):

    def __init__(self, fields_map, ref_field_map, keep_fields):
        pass

    def make_map(self, reader, appender):
        pass

    def make_map_for(self, filename):
        pass

    def extract(self, reader, writer):
        pass


def main():
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    map_file, map_fields, ref_field = sys.argv[1:]
    raise  NotImplementedError


if __name__ == '__main__':
    main()
