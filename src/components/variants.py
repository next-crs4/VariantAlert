import myvariant
import json

class Variants(object):
    def __init__(self):
        self.mv = myvariant.MyVariantInfo()

    def get_variant(self, query, assembly='hg19', fields="all"):
        variant = self.mv.getvariant(query, assembly=assembly, fields=fields)
        return variant if variant else dict()

