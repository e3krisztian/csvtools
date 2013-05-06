class DuplicateFieldError(Exception):
    '''Invalid CSV - duplicate field in a header'''


class MissingFieldError(Exception):
    '''Expected field not found in header'''


class ExtraFieldError(Exception):
    '''Unexpected extra field in header'''


class InvalidReferenceFieldError(Exception):
    '''Can not use this reference field'''
