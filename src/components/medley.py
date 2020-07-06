import json
from collections import OrderedDict
from itertools import chain, starmap

def json2flat(dictionary):
    """Flatten a nested json file"""

    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!

        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = parent_key + '.' + key
                yield temp1, value
        elif isinstance(parent_value, list):
            i = 0
            for value in parent_value:
                temp2 = parent_key + '[' + str(i) + ']'
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value

            # Keep iterating until the termination condition is satisfied

    while True:
        # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        # Terminate condition: not any value in the json file is dictionary or list
        if not any(isinstance(value, dict) for value in dictionary.values()) and \
                not any(isinstance(value, list) for value in dictionary.values()):
            break

    return OrderedDict(sorted(dictionary.items()))

def build_query(query):
    if not isinstance(query, dict):
        query = dict(chromosome=query.chromosome,
                     position=query.position,
                     variant_reference=query.variant_ref,
                     variant_alternate=query.variant_alt)

    query['chromosome'] = 'chr' + str(query['chromosome']) if query['chromosome'].isnumeric() else query['chromosome']
    return query['chromosome'] + ':' + 'g.' + str(query['position']) + query['variant_reference'] + '>' + query[
        'variant_alternate']

def _filter(diffs):
    _types = ('str', 'int', 'list', 'dict', 'float', 'boolean')
    l = list()
    for i in range(0, len(diffs)):
        passed = True

        d = diffs[i]
        p = diffs[i-1] if i > 0 else None
        n = diffs[i+1] if i < len(diffs)-1 else None

        if d.get('current') in _types or d.get('previous') in _types:
            passed = False

        if d.get('field').endswith(']'):
            if p and p.get('field')[:-3] == d.get('field')[:-3]:
                if p.get('previous') == d.get('current') and p.get('current') == d.get('previous'):
                    passed = False

            if n and n.get('field')[:-3] == d.get('field')[:-3]:
                if n.get('previous') == d.get('current') and n.get('current') == d.get('previous'):
                    passed = False

        if passed:
            l.append(d)
    return l

def rehash_diff(diffs):
    l = list()
    for d in diffs:
        type = d.get('type')
        message = d.get('message')
        if type and message:
            if  '-' in message:
                m = message.split('-')
                field = m[0].strip()
                values = m[1].strip()
                if field in 'dbnsfp.aa.codon_degeneracy':
                    print("messages: "+str(message))
                    print("m: "+str(m))
                    print("values: "+str(values))

                if 'CHANGED' in type and '|' in values:
                        v = values.split('|')
                        previous = v[0].strip()
                        current = v[1].strip() if len(v)>1 else ''
                if 'CHANGED' in type and '|' not in values and ',' in values:
                        v = values.split(',')
                        previous = v[0].strip()
                        current = v[1].strip() if len(v) > 1 else ''
                if 'ADDED' in type:
                    current = values.strip()
                    previous = ''
                if 'REMOVED' in type:
                    current = values.strip()
                    previous = ''

            if '-' not in message:
                 field = message
                 previous = ''
                 current = ''

        l.append(dict(field=field, type=type,
                      current=current,
                      previous=previous))

    return  _filter(sorted(l, key=lambda k: k['field']))


def ret_query(query):
    query.result = json2flat(query.result)
    query.previous = json2flat(query.previous)
    query.difference = rehash_diff(query.difference)
    query.date = query.date.strftime("%b. %d, %Y")
    query.update = query.update.strftime("%b. %d, %Y")
    return query
