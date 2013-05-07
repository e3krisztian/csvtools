import sys
import csv

import argparse
from csvtools.lib import Header, list_extractor


class DuplicateFieldError(Exception):
    pass


def unzip(csv_in, fields, csv_out_spec, csv_out_unspec, zip_field='id'):
    input_csv = iter(csv_in)

    header_row = input_csv.next()
    header = Header(header_row)

    if zip_field in header:
        raise DuplicateFieldError(zip_field)

    extract_spec = list_extractor(header.extractors(fields))
    extract_unspec = list_extractor(
        header.extractor(field)
        for field in header_row
        if field not in fields)

    def extract_to(output, extract, row_id, row):
        output.writerow([str(row_id)] + extract(row))

    def unzip_row(row_id, row):
        extract_to(csv_out_spec, extract_spec, row_id, row)
        extract_to(csv_out_unspec, extract_unspec, row_id, row)

    unzip_row(zip_field, header_row)
    for zip_id, row in enumerate(input_csv):
        unzip_row(zip_id, row)


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--id', action='store', dest='zip_field', default='id',
        help='new field that matches rows in unzipped parts (%(default)s)')
    parser.add_argument(
        'fields', metavar='FIELDS',
        help='comma separated field names')
    parser.add_argument(
        'unspec_fields_filename', metavar='UNSPEC_FILENAME',
        help='Filename for unspecified fields')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    fields = args.fields.split(',')
    csv_in = csv.reader(sys.stdin)
    csv_out_spec = csv.writer(sys.stdout)

    with open(args.unspec_fields_filename, 'w') as out_unspec:
        csv_out_unspec = csv.writer(out_unspec)

        unzip(
            csv_in, fields, csv_out_spec, csv_out_unspec,
            zip_field=args.zip_field)


if __name__ == '__main__':
    main()
