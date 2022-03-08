import pandas as pd
import json
from django.shortcuts import render, redirect
from pipeline.models import Project, Technology, Software, Results, ProjectSpecs
from pipeline.forms import CreateProject, SoftwareSelect
from django.core.files import File
from pathlib import Path
import threading
import os
from pipeline.metaruns_django import meta_orchestra
# Create your views here.

def dashboard(request):
    return render(request, "users/dashboard.html")


def project_index(request):
    print(request.user)
    projects= Project.objects.filter(user= request.user)

    context= {
        "projects": projects,
        "user": request.user
    }

    return render(request, "project_list.html", context)

def profile_detail(request, pk):
    project= Project.objects.get(pk= pk)
    specs= ProjectSpecs.objects.get(project= pk)
    context= {
        "project": project,
        "specs": {
            "Quality Control": specs.QC.name,
            "Host Depletion": specs.HD.name,
            "Read classification": specs.CLASSM.name,
            "Assembly": specs.ASSEMBLY.name,
            "Contig classification": specs.CLASSA.name,
            "Remapping software": specs.REMAP.name
        }
    }

    if Results.objects.filter(project= pk).exists():
        rf= Results.objects.get(project= pk).results.path
        rf= pd.read_csv(rf, sep= "\t")
        rf= rf[rf.ID == "total"]
        rf= rf.rename(columns= {"Hdepth%": "depth", "%>2": "coverage"})
        rf= rf.reset_index().to_json(orient='records')
        rf= json.loads(rf)

        #
        af=  Results.objects.get(project= pk).args.path
        af= pd.read_csv(af, sep= "\t")

        #
        context["results"]= rf
        context["args"]=af.to_html()

    return render(request, "profile_view.html", context)


def ProjectSetup(request):
    form= CreateProject(request.POST or None, request.FILES or None)
    #
    if request.method == 'POST':

        if form.is_valid():

            tech = form.cleaned_data["technology"]

            p1= Project(
                technology= Technology(id= tech),
                title= form.cleaned_data["title"],
                samples= form.cleaned_data["samples"],
                user= request.user,
            )
            p1.save()

            request.session["my_project"]= p1.pk
            print(f"this session pid is {p1.pk}")
            return redirect('pipeline:project_specs')

    return render(request, "create_project_form.html", {'form': form})


def meta_run(params, fofn, tech, pid):
    title = Project(id=pid).title
    title = title.replace(" ", "_")

    event= meta_orchestra(sup= 1, down=1, odir= "RUNS_django/")
    event.param_prepare(tech, filters= params)
    event.sup_deploy(fofn, project_name= title)
    event.low_deploy()
    event.record_runs()

    for process, td in event.processes.items():
        with open(td["results"], "r") as fr:
            with open(td["params"], "r") as fp:
                p1= Results(
                    project= Project(id= pid),
                    process= process,
                    results= File(fr, name= Path(td["results"]).name),
                    args= File(fp, name= Path(td["params"]).name)
                )
                p1.save()

    event.clean()


def SoftwareSetup(request):
    pid= request.session.get("my_project")
    #
    tech= Project.objects.filter(pk= pid).values_list("id", "technology")[0][1]
    form= SoftwareSelect(tech,request.POST or None)
    #
    if request.method == 'POST':
        if form.is_valid():


            params = {
                "HD": form["HD"].value(),
                "ASSEMBLY_SOFT": form["ASSEMBLY"].value(),
                "ASSEMBLE_CLASS": form["CLASSA"].value(),
                "CLASSM": form["CLASSM"].value(),
                "REMAP_SOFT": form["REMAP"].value(),
            }

            p1= ProjectSpecs(
                project= Project(id= pid),
                tech = Technology(id= tech),
                QC= Software.objects.get(name= "trimmomatic", tech= tech, module__name= "QC"),
                HD = Software.objects.get(name=params["HD"], tech= tech, module__name= "HD"),
                CLASSM= Software.objects.get(name= params["CLASSM"], tech= tech, module__name= "CLASSM"),
                ASSEMBLY= Software.objects.get(name= params["ASSEMBLY_SOFT"], tech= tech, module__name= "ASSEMBLY_SOFT"),
                CLASSA= Software.objects.get(name= params["ASSEMBLE_CLASS"], tech= tech, module__name= "ASSEMBLE_CLASS"),
                REMAP= Software.objects.get(name= params["REMAP_SOFT"], tech= tech, module__name= "REMAP_SOFT"),
            )
            p1.save()

            fofn= Project.objects.get(pk= pid).samples.path
            techname= Technology.objects.get(id= tech).name

            t= threading.Thread(target= meta_run,
                                args= [params, fofn, techname, pid])

            t.setDaemon(True)

            if 'DYNO' not in os.environ:
                t.start()
            else:
                Project.objects.filter(id= pid).delete()

            return redirect('pipeline:project_index')
            #       
    return render(request, "create_project_form.html", {'form': form})

