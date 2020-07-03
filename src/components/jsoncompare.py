import json
import sys
import types
from collections import OrderedDict

TYPE = 'TYPE'
PATH = 'PATH'
VALUE = 'VALUE'

# Borrowed from http://djangosnippets.org/snippets/2247/
# with some modifications.
class Diff(object):
  def __init__(self, first, second, with_values=False):
    self.difference = []
    self.seen = []
    not_with_values = not with_values
    self.check(first, second, with_values=with_values)

  def check(self, first, second, path='', with_values=False):
    if with_values and second != None:
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
          if sec != None:
            self.check(first[key], sec, path=new_path, with_values=with_values)
        else:
          # second is not dict. every key from first goes to the difference
          self.save_diff(new_path, PATH)
          self.check(first[key], second, path=new_path, with_values=with_values)

    # if object is list, loop over it and check.
    elif isinstance(first, list):
      for (index, item) in enumerate(first):
        new_path = '{}.{}'.format(path, index)
        # try to get the same index from second
        sec = None
        if second != None:
          try:
            sec = second[index]
          except Exception as e:
            # goes to difference
            self.save_diff('{} - {}'.format(new_path, type(item).__name__), TYPE)

        # recursive call
        self.check(first[index], sec, path=new_path, with_values=with_values)

    # not list, not dict. check for equality (only if with_values is True) and return.
    else:
      if with_values and second != None:
        if first != second:
          
          self.save_diff('{} - {} | {}'.format(path, first, second), VALUE)
      return

  def save_diff(self, diff_message, type_):
    if diff_message not in self.difference:
      self.seen.append(diff_message)
      self.difference.append((type_, diff_message))

def compare(json1, json2):
  json1 = json.loads(json1) if isinstance(json1, str) else json1
  json2 = json.loads(json2) if isinstance(json2, str) else json2
  diff1 = Diff(json1, json2, True).difference
  diff2 = Diff(json2, json1, False).difference
  diffs = []
  for type, message in diff1:
    newType = 'CHANGED'
    if type == PATH:
      newType = 'REMOVED'
    diffs.append({'type': newType, 'message': message.replace("'","")})
  for type, message in diff2:
    diffs.append({'type': 'ADDED', 'message': message.replace("'","")})
  return diffs


