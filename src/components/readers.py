import csv
import vcf
import codecs

MAX_LEN = 25
FIELDNAMES = ('chromosome', 'position', 'variant_reference',
              'variant_alternate', 'assembly')
AGCT = ['A', 'G', 'C', 'T']
ASS = ['hg19', 'hg38']


class VCFReader(vcf.Reader):
    def __init__(self, f):
        self.errors = list()
        self.content = self.__validate(f)

    def __validate(self, f):
        try:
            content = vcf.Reader(codecs.iterdecode(f, 'utf-8'))

        except Exception as e:
            self.__set_error(e)

        return vcf.Reader(codecs.iterdecode(f, 'utf-8')) if self.is_valid() else None

    def __set_error(self, msg):
        self.errors.append(msg)

    def is_valid(self):
        return False if self.errors else True

    def get_errors(self):
        return list(set(self.errors))

    def get_content(self):
        return [dict(chromosome=r.CHROM,
                     position=r.POS,
                     variant_reference=r.REF,
                     variant_alternate=r.ALT,
                     ) for r in self.content]



class CSVReader(csv.DictReader):
    def __init__(self, f):

        self.errors = list()
        self.content = self.__validate(f)

    def __validate(self, f):
        try:

            content = csv.DictReader(codecs.iterdecode(f, 'utf-8'),
                                     fieldnames=FIELDNAMES,
                                     delimiter=',')
            rows = list(content)

            if len(rows) > MAX_LEN:
                self.__set_error("CSV file must have a maximum of 25 lines")

            for row in rows:
                if len(row) != 5:
                    self.__set_error("CSV file must have 5 columns")

                chromo = row.get('chromosome')
                if not chromo.isnumeric() or int(chromo) not in range(1, 22):
                    self.__set_error("Chromosome field must be between 1 and 21")

                pos = row.get('position')
                if not pos.isnumeric() or int(pos) < 0:
                    self.__set_error("Position must be a positive integer")

                if row.get('variant_reference') not in AGCT or row.get('variant_alternate') not in AGCT:
                    self.__set_error("Variants must be in {}".format(AGCT))

                if row.get('assembly') not in ASS:
                    self.__set_error("Assembly must be in {}".format(ASS))

        except csv.Error as e:
            self.__set_error(e)

        return csv.DictReader(codecs.iterdecode(f, 'utf-8'),
                              fieldnames=FIELDNAMES,
                              delimiter=',') if self.is_valid() else None

    def __set_error(self, msg):
        self.errors.append(msg)

    def is_valid(self):
        return False if self.errors else True

    def get_errors(self):
        return list(set(self.errors))

    def get_content(self):
        return self.content
