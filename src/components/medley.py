import json


def build_query(query):
    if not isinstance(query, dict):
        query = dict(chromosome=query.chromosome,
                     position=query.position,
                     variant_reference=query.variant_ref,
                     variant_alternate=query.variant_alt)

    query['chromosome'] = 'chr' + str(query['chromosome']) if query['chromosome'].isnumeric() else query['chromosome']
    return query['chromosome'] + ':' + 'g.' + str(query['position']) + query['variant_reference'] + '>' + query[
        'variant_alternate']


def ret_query(query):
    query.result = json.dumps(query.result)
    query.previous = json.dumps(query.previous)
    query.difference = json.dumps(query.difference)
    query.date = query.date.strftime("%b. %d, %Y")
    query.update = query.update.strftime("%b. %d, %Y")
    return query
