from django import forms
from pipeline.models import (Project, Technology,
                             Software, ProjectSpecs)
from django.utils import timezone as tz

class SoftwareSelect(forms.Form):

    def __init__(self, tech, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['HD'].widget=forms.Select(
            choices= [('', '--------')] + list(Software.objects.filter(module= 2, tech= tech).values_list("name","name"))
        )
        self.fields['ASSEMBLY'].widget= forms.Select(
            choices= [('', '--------')] + list(Software.objects.filter(module= 3, tech= tech).values_list("name","name"))
            )
        self.fields['CLASSA'].widget= forms.Select(
            choices= [('', '--------')] + list(Software.objects.filter(module= 4, tech= tech).values_list("name","name"))
        )
        self.fields['CLASSM'].widget= forms.Select(
            choices= [('', '--------')] + list(Software.objects.filter(module= 5, tech= tech).values_list("name","name"))
        )
        self.fields['REMAP'].widget= forms.Select(
            choices= [('', '--------')] + list(Software.objects.filter(module= 6, tech= tech).values_list("name","name"))
        )


    HD= forms.CharField(
        label= "Host Depletion"
    )

    ASSEMBLY= forms.CharField(
        label= "Assembly",

    )

    CLASSA= forms.CharField(
        label= "Assembly Classification",
    )

    CLASSM= forms.CharField(
        label= "Read Classification",
    )

    REMAP= forms.CharField(
        label= "Remapping",

    )



class CreateProject(forms.Form):
    #
    title = forms.CharField(required=True)
    #
    technology= forms.CharField(
        label= "Technology"
    )
    #
    samples = forms.FileField(required= True)
    #
    def __init__(self, *args, **kwargs):
        super(CreateProject, self).__init__(*args,**kwargs)

        self.fields['technology'].widget= forms.Select(
            choices= [('', '--------')] + list(Technology.objects.all().values_list("id","name"))
        )
        #




