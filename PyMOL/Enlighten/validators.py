import os
from qt_wrapper import WITH_PYMOL


class Validator:

    def __init__(self):
        self.value = ''

    def __call__(self, value):
        self.value = value
        return self.validate(value)

    @staticmethod
    def validate(value):
        raise NotImplementedError

    def tooltip(self):
        return ''


class NotEmptyValidator(Validator):

    def __init__(self, name='Field'):
        self.name = name

    @staticmethod
    def validate(value):
        return len(value) > 0

    def tooltip(self):
        return "{} must not be empty".format(self.name)


class IntegerValidator(Validator):

    def __init__(self, name='Field'):
        self.name = name

    @staticmethod
    def validate(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def tooltip(self):
        return "{} '{}' is not an integer".format(self.name, self.value)


class FileValidator(Validator):

    @staticmethod
    def validate(value):
        return os.path.isfile(value)

    def tooltip(self):
        return "{} is not a valid file".format(self.value)


class DirectoryValidator(Validator):

    @staticmethod
    def validate(value):
        return os.path.isdir(value)

    def tooltip(self):
        return "Not a valid directory"


class PdbValidator(Validator):

    @staticmethod
    def validate(value):
        ext = os.path.splitext(value)[-1]
        return os.path.isfile(value) and ext.lower() == '.pdb'

    def tooltip(self):
        return "'{}' is not a valid PDB file".format(self.value)


class AtomValidator(Validator):

    @classmethod
    def validate(cls, value):
        if not value:
            return True
        try:
            res, name = cls._split_value(value)
        except AttributeError:
            return False

        if WITH_PYMOL:
            return cls._validate_with_pymol(res, name)
        else:
            return True

    @staticmethod
    def _split_value(value):
        import re
        number_query = '([+-]?\d+(?:\.\d+)?)'
        return re.match(' '.join([number_query]*3) + '$', value).groups()

    @staticmethod
    def _validate_with_pymol(res, name):
        import pymol
        selection = 'resi {} and name {}'.format(res, name)
        return pymol.cmd.count_atoms(selection) == 1

    def tooltip(self):
        return "Selection {} has zero or more than one atom.".format(self.value)
