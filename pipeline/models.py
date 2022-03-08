from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone as tz
# Create your models here.

fofnpath = FileSystemStorage(location='files/fofn')
resultspath= FileSystemStorage(location= 'files/projects')

class Technology(models.Model):
    name= models.CharField(max_length= 15)

class Module(models.Model):
    name= models.CharField(max_length= 100)

class Software(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, related_name= "module", on_delete= models.CASCADE)
    tech= models.ForeignKey(Technology, related_name="tech", on_delete= models.CASCADE)

class Project(models.Model):
    user = models.ForeignKey(User, editable=False, on_delete= models.CASCADE)
    title= models.CharField(max_length= 100)
    created_on= models.DateTimeField(auto_now_add= True)
    technology= models.ForeignKey(Technology, on_delete= models.CASCADE, blank= True, null= True) #, choices= [(x.id, x.name) for x in Technology])
    samples = models.FileField(null=True, blank=True, storage= fofnpath)

    def __str__(self):
        return self.title

class ProjectSpecs(models.Model):

    project= models.ForeignKey(Project, on_delete= models.CASCADE)
    tech= models.ForeignKey(Technology, on_delete= models.CASCADE)
    QC= models.ForeignKey(Software, related_name= "qc", on_delete= models.CASCADE)
    HD= models.ForeignKey(Software, related_name= "hd", default= "", on_delete= models.CASCADE)
    CLASSM= models.ForeignKey(Software, related_name= "classm", default= "None", on_delete=models.CASCADE)
    ASSEMBLY= models.ForeignKey(Software, related_name= "assembly", default= "None", on_delete= models.CASCADE)
    CLASSA= models.ForeignKey(Software, related_name= "classa", default= "None",on_delete= models.CASCADE)
    REMAP= models.ForeignKey(Software, related_name= "remap", default= "None",on_delete= models.CASCADE)

    def __str__(self):
        return self.name


class Results(models.Model):
    project= models.ForeignKey(Project, on_delete= models.CASCADE)
    process= models.CharField(max_length= 20)
    results= models.FileField(null= True, blank= True, storage= resultspath)
    args= models.FileField(null= True, blank= True, storage= resultspath)


"""
class Results(models.Model):
    project= models.ForeignKey(Project, on_delete= models.CASCADE)
    process= models.CharField(max_length= 20)
    runtime= models.IntegerField()
    taxid= models.CharField(max_length=40)
    refseq= models.CharField(max_length= 30)
    description= models.TextField()
    rclass= models.BooleanField()
    alcass= models.BooleanField()
    coverage= models.FloatField()
    depth= models.FloatField()
    regions= models.IntegerField()
    gaps= models.IntegerField()

    def __str__(self):
        return self.name


class Flag(models.Model):
    #
    project= models.ForeignKey(Project, on_delete= models.CASCADE)
    process= models.CharField(max_length= 30)
    technology= models.ForeignKey(Technology, on_delete= models.SET_NULL, blank= True, null= True)
    module= models.ForeignKey(Module, on_delete=models.SET_NULL, blank=True, null=True)
    soft= models.ForeignKey(Software,  on_delete=models.SET_NULL, blank=True, null=True)
    arg= models.CharField(max_length= 15)
    name= models.CharField(max_length= 50)

    def __str__(self):
        return self.name


"""