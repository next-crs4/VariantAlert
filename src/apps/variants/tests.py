from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.utils.timezone import now
from . import  models

from components.variants import Variants
from components.toolkit import Handling

class VariantsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test-user',
                                        email='test.user@example.com',
                                        password="test-password")
        self.v = Variants()

        models.QueryModel.objects.create(
            label='label-4-test',
            chromosome='chr1',
            position=866422,
            assembly='hg19',
            variant_ref='C',
            variant_alt='T',
            query='chr1:g.866422C>T',
            fields=list(),
            result=self.v.get_variant(query='chr1:g.866422C>T',
                                      assembly='hg19',
                                      ),
            user_id=self.user.id,
        )

    def _login(self):
        self.client.force_login(self.user)

    def test_create_query(self):
        self._login()
        self.client.post("/variants/query/",
                         dict(label='new-label',
                              chromosome="chr1",
                              position=876664,
                              variant_ref='G',
                              variant_alt='T',
                              assembly='hg19',
                              )
                         )
        queries = models.QueryModel.objects.all().values()
        self.assertEqual(len(queries) > 1, True)
        query = models.QueryModel.objects.filter(label="new-label").values()[0]
        self.assertEqual(query.get("label"), "new-label")
        self.assertEqual(query.get("chromosome"), "chr1")
        self.assertEqual(query.get("position"), 876664)
        self.assertEqual(query.get("variant_ref"), "G")
        self.assertEqual(query.get("variant_alt"), "T")
        self.assertEqual(query.get("assembly"), "hg19")
        self.assertEqual(query.get("result"), self.v.get_variant(query='chr1:g.876664G>T', assembly='hg19'))
        self.assertEqual(query.get("previous"), dict())

    def test_history(self):
        self._login()
        resp = self.client.get('/variants/history/')
        self.assertEqual(resp.status_code, 200)
        queries = resp.context['queries']
        self.assertEqual(len(queries), 1)
        query = queries.pop()
        self.assertEqual(query.label, "label-4-test")
        self.assertEqual(query.chromosome, 'chr1')
        self.assertEqual(query.position, 866422)
        self.assertEqual(query.assembly, 'hg19')
        self.assertEqual(query.variant_ref, 'C')
        self.assertEqual(query.variant_alt,'T')
        self.assertEqual(query.query,'chr1:g.866422C>T')
        self.assertEqual(query.result,
                         Handling.json2flat(self.v.get_variant(query='chr1:g.866422C>T', assembly='hg19')))
        self.assertEqual(query.assembly, 'hg19')
        self.assertEqual(query.user, self.user)

    def test_details(self):
        self._login()
        query = models.QueryModel.objects.filter(label="label-4-test").values()[0]
        resp = self.client.get('/variants/query/'+str(query.get('id')))
        self.assertEqual(resp.status_code, 200)
        self._check(resp.context['query'])

    def test_rerun(self):
        self._login()
        query = models.QueryModel.objects.filter(label="label-4-test").values()[0]
        resp = self.client.get('/variants/query/'+str(query.get('id'))+'/rerun')
        self.assertEqual(resp.status_code, 200)
        self._check(resp.context['query'])

    def test_delete(self):
        self.test_create_query()
        query = models.QueryModel.objects.filter(label="new-label").values()[0]
        resp = self.client.get('/variants/query/' + str(query.get('id'))+'/delete')
        self.assertEqual(resp.status_code, 200)
        query = models.QueryModel.objects.filter(label="new-label").values()
        self.assertEqual(len(query), 0)



    def _check(self, query):
        self.assertEqual(query.label, "label-4-test")
        self.assertEqual(query.chromosome, 'chr1')
        self.assertEqual(query.position, 866422)
        self.assertEqual(query.assembly, 'hg19')
        self.assertEqual(query.variant_ref, 'C')
        self.assertEqual(query.variant_alt, 'T')
        self.assertEqual(query.query, 'chr1:g.866422C>T')
        self.assertEqual(query.result,
                         Handling.json2flat(self.v.get_variant(query='chr1:g.866422C>T', assembly='hg19')))
        self.assertEqual(query.assembly, 'hg19')
        self.assertEqual(query.user, self.user)
