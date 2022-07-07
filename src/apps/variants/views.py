# variants/views.py
from . import forms
from django.urls import reverse_lazy
from django.views import generic

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now

from . import models

from components.variants import Variants
from components.toolkit import Toolkit
from components.readers import CSVReader, VCFReader
from components.writers import xlsxWriter


class Query(LoginRequiredMixin, generic.CreateView):
    template_name = 'variants/query.html'
    form_class = forms.QueryForm

    def get_context_data(self, **kwargs):
        context = super(Query, self).get_context_data(**kwargs)
        v = Variants()
        context['sources'] = v.get_sources()
        return context

    def form_valid(self, form):
        v = Variants()
        sources = self.request.POST.getlist('sources')
        query = form.save(commit=False)
        query.fields = sources
        csv_file = form.cleaned_data['csv_file']
        vcf_file = form.cleaned_data['vcf_file']
        vcf_assembly = form.cleaned_data['vcf_assembly']

        if not csv_file and not vcf_file:
            query.query = Toolkit.build_query(query)
            query.result = v.get_variant(query=query.query,
                                         assembly=query.assembly,
                                         fields=query.fields)
            query.user_id = self.request.user.id
            query.save()
            return HttpResponseRedirect(reverse_lazy('details', args=[query.id]))

        elif csv_file:
            queries = CSVReader(csv_file)
            for row in queries.get_content():
                models.QueryModel.objects.create(
                    label=form.cleaned_data['csv_label'],
                    chromosome=row.get('chromosome'),
                    position=row.get('position'),
                    assembly=row.get('assembly'),
                    variant_ref=row.get('variant_reference'),
                    variant_alt=row.get('variant_alternate'),
                    query=Toolkit.build_query(row),
                    fields=query.fields,
                    result=v.get_variant(query=Toolkit.build_query(row),
                                         assembly=row.get('assembly'),
                                         fields=query.fields),
                    user_id=self.request.user.id,
                )
            return HttpResponseRedirect(reverse_lazy('history'))

        elif vcf_file:
            queries = VCFReader(vcf_file)
            for row in queries.get_content():
                row['assembly'] = vcf_assembly
                alts = row.get('variant_alternate')
                for alt in alts:
                    if alt:
                        row['variant_alternate'] = alt
                        models.QueryModel.objects.create(
                            label=form.cleaned_data['vcf_label'],
                            chromosome=row.get('chromosome'),
                            position=row.get('position'),
                            assembly=row.get('assembly'),
                            variant_ref=row.get('variant_reference'),
                            variant_alt=row.get('variant_alternate'),
                            query=Toolkit.build_query(row),
                            fields=query.fields,
                            result=v.get_variant(query=Toolkit.build_query(row),
                                                 assembly=row.get('assembly'),
                                                 fields=query.fields),
                            user_id=self.request.user.id,
                        )

            return HttpResponseRedirect(reverse_lazy('history'))


class History(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'variants/history.html'

    def get_queries(self, user_id, _filter=None):
        queries = models.QueryModel.objects.filter(user_id=user_id)
        if 'search_for' in _filter and _filter.get('search_for'):
            queries = queries.filter(label=_filter.get('search_for'))

        if 'sort_by' in _filter and _filter.get('sort_by'):
            queries = queries.order_by(_filter.get('sort_by'))

        if 'show' in _filter and 'alerts' in _filter.get('show'):
            queries = queries.filter(alert=True)

        return [Toolkit.ret_query(q) for q in queries]

    def get_context_data(self, **kwargs):
        context = super(History, self).get_context_data(**kwargs)
        queries = self.get_queries(self.request.user.id,
                                   _filter=self.request.GET)
        context['queries'] = queries
        context['labels'] = list(set([q.label for q in queries]))
        context['num_total'] = len(queries)
        context['filtering'] = self.request.GET
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super(History, self).render_to_response(context)


class Details(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'variants/details.html'

    def get_query(self, query_id):
        try:
            query = models.QueryModel.objects.get(pk=query_id)
            if query.user_id != self.request.user.id:
                return None
            query.alert = False
            query.save()
        except Exception as e:
            return None
        return Toolkit.ret_query(query)

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        context['query'] = self.get_query(context.get('query_id'))
        return context


class Rerun(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'variants/rerun.html'

    def get_query(self, query_id):
        try:
            query = models.QueryModel.objects.get(pk=query_id)
            if query.user_id != self.request.user.id:
                return None
        except Exception as e:
            return None
        return query

    def rerun(self, query_id):
        v = Variants()
        query = self.get_query(query_id)
        if query:
            query.previous = query.result
            query.result = v.get_variant(query.query, query.assembly, query.fields)
            query.difference = Toolkit.compare(query.previous, query.result)
            query.date = query.date
            query.alert = False
            if query.difference:
                query.update = now()
                query.alert = True
            query.save()
            return Toolkit.ret_query(query)
        return query

    def get_context_data(self, **kwargs):
        context = super(Rerun, self).get_context_data(**kwargs)
        context['query'] = self.rerun(context.get('query_id'))
        return context


class Delete(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'variants/delete.html'

    def get_query(self, query_id):
        try:
            query = models.QueryModel.objects.get(pk=query_id)
            if query.user_id != self.request.user.id:
                return None
        except Exception as e:
            return None
        return query

    def delete(self, query_id):
        query = self.get_query(query_id)
        if query:
            query.delete()
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        context['deleted'] = self.delete(context.get('query_id'))
        return context


class Download(LoginRequiredMixin, generic.base.View):

    def get_query(self, query_id):
        try:
            query = models.QueryModel.objects.get(pk=query_id)
            if query.user_id != self.request.user.id:
                return None
        except Exception as e:
            return None
        return query

    def get(self, request, *args, **kwargs):
        query_id = kwargs.get('query_id')
        query = Toolkit.ret_query(self.get_query(query_id))
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-{label}.xlsx'.format(
            date=now().strftime('%Y-%m-%d'), label=query.label
        )

        workbook = xlsxWriter(query)
        workbook.do()
        workbook.save(response)
        return response
