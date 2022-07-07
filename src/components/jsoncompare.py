TYPE = 'TYPE'
PATH = 'PATH'
VALUE = 'VALUE'


class Diff(object):
    def __init__(self, first, second, with_values=False):
        self.difference = []
        self.seen = []
        not_with_values = not with_values
        self.check(first, second, with_values=with_values)

    def check(self, first, second, path='', with_values=False):
        if with_values and second is not None:
            if not isinstance(first, type(second)):
                message = '{} - {}, {}'.format(path, type(first).__name__, type(second).__name__)
                self.save_diff(message, TYPE)

        if isinstance(first, dict):
            for key in first:
                # the first part of path must not have trailing dot.
                if len(path) == 0:
                    new_path = key
                else:
                    new_path = "{}.{}".format(path, key)

                if isinstance(second, dict):
                    if key in second:
                        sec = second[key]
                    else:
                        #  there are key in the first, that is not presented in the second
                        self.save_diff(new_path, PATH)

                        # prevent further values checking.
                        sec = None

                    # recursive call
                    if sec is not None:
                        self.check(first[key], sec, path=new_path, with_values=with_values)
                else:
                    # second is not dict. every key from first goes to the difference
                    self.save_diff(new_path, PATH)
                    self.check(first[key], second, path=new_path, with_values=with_values)

        # if object is list, loop over it and check.
        elif isinstance(first, list):
            first = self.retrieve_list(first)
            for (index, item) in enumerate(first):
                new_path = '{}.{}'.format(path, index)
                # try to get the same index from second
                sec = None
                if second is not None:
                    try:
                        second = self.retrieve_list(second)
                        sec = second[index]
                    except Exception as e:
                        # goes to difference
                        self.save_diff('{} - {}'.format(new_path, type(item).__name__), TYPE)

                # recursive call
                self.check(first[index], sec, path=new_path, with_values=with_values)

        # not list, not dict. check for equality (only if with_values is True) and return.
        else:
            if with_values and second is not None:
                if first != second:
                    self.save_diff('{} - {} | {}'.format(path, first, second), VALUE)
            return

    def save_diff(self, diff_message, type_):
        if diff_message not in self.difference:
            self.seen.append(diff_message)
            self.difference.append((type_, diff_message))

    def retrieve_list(self, _list):
        for item in _list:
            if isinstance(item, list) or isinstance(item, dict):
                return _list
        return sorted(_list)
