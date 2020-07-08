import django.forms as forms
from prettyjson import PrettyJSONWidget
from . import models

from components.readers import CSVReader


class QueryForm(forms.ModelForm):

    csv_file = forms.FileField(label="Upload a csv file with your queries:",
                               required=False,
                               help_text='CSV file with 5 columns: chromosome, position, variant_reference, '
                                         'variant_alternate, assembly.</br>'
                                         'NO header is required!</br>'
                                         'Example:</br>'
                                         '1,866422,C,T,hg19</br>'
                                         '1,876664,G,A,hg19</br>'
                                         '1,69635,G,C,hg19</br>'
                                         '1,69869,T,A,hg19</br>'
                                         '1,881918,G,A,hg19</br>'
                                         '...</br>'
                                         'Up to a maximum of 25 rows are allowed!',
                               )

    csv_label = forms.CharField(max_length=50, required=False,
                                label='Label:',
                                help_text='All queries will have the same label')
    


    class Meta:
        model = models.QueryModel

        fields = ['label', 'chromosome', 'position', 'assembly', 'variant_ref',
                  'variant_alt', 'query', 'result', 'previous', 'difference',
                  'date', 'update', 'fields',
                  'csv_file', 'csv_label']

        labels = {
            'label': 'Label',
            'chromosome': 'Chromosome',
            'position': "Position",
            'assembly': "Assembly",
            'variant_ref': 'Variant Reference',
            'variant_alt': 'Variant Alternate',
        }

        help_texts = {
            'label': 'A descriptive label for your query',
            'position': 'Genomic Position',
            'variant_ref': 'Variant Reference',
            'variant_alt': 'Variant Alternate',
        }

        error_messages = {
            'label': {
                'max_length': 'This label is too long.',
            },
        }

    def clean(self):

        csv_file = self.cleaned_data.get('csv_file')
        csv_label = self.cleaned_data.get('csv_label')
        label = self.cleaned_data.get('label')
        position = self.cleaned_data.get('position')
        sources =self.cleaned_data.get('sources')

        if csv_file and not csv_label:
            msg = forms.ValidationError("This field is required.")
            self.add_error('csv_label', msg)

        if csv_label and not csv_file:
            msg = forms.ValidationError("This field is required.")
            self.add_error('csv_file', msg)

        if csv_file and csv_label:
            _csv = CSVReader(csv_file)
            if not _csv.is_valid():

                for error in _csv.get_errors():
                    msg = forms.ValidationError(error)
                    self.add_error('csv_file', msg)

        if not csv_file and (not label or not position):
            msg = forms.ValidationError("This field is required.")
            if not label:
                self.add_error('label', msg)
            if not position:
                self.add_error('position', msg)

        return self.cleaned_data
