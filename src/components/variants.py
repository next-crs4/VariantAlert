import myvariant
import json

class Variants(object):
    def __init__(self):
        self.mv = myvariant.MyVariantInfo()

    def get_variant(self, query, assembly='hg19', fields="all"):
        variant = self.mv.getvariant(query, assembly=assembly, fields=fields if fields else "all")
        return variant if variant else dict()

    def get_sources(self):
        sources = self.mv.get_fields()
        return [s for s in sources.keys() if '.' not in s]

    def get_fields(self):
        fields = self.mv.get_fields()
        return [f for f in fields.keys() if '.' in f]

    def get_fields_group_by_source(self):
        d = dict()
        sources = self.get_sources()
        fields = self.get_fields()
        for s in sources:
            d[s] = [f for f in fields if f.startswith(s+'.')]
        return d





