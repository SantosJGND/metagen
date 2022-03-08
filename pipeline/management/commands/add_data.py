from django.core.management.base import BaseCommand
from pipeline.models import Software, Technology, Module #, Arg, Flag
import pandas as pd
import params_illumina as pai
import params_nanopore as pan
from sqlalchemy import create_engine

class pyparse():
    def __init__(self):
        self.Technology = [
            {
                "model": "pipeline.technology",
                "pk": 1,
                "fields": {
                    "name": "illumina"
                }
            },
            {
                "model": "pipeline.technology",
                "pk": 2,
                "fields": {
                    "name": "nanopore"
                }
            }
        ]
        self.Module = [
            {
                "model": "pipeline.module",
                "pk": ix + 1,
                "fields": {
                    "name": x
                }
            } for ix,x in enumerate(pai.SOFTWARE.keys())
        ]
        self.tech_pk= {"illumina": 1, "nanopore": 2}
        self.mod_pk= {x:ix+1 for ix, x in enumerate(pai.SOFTWARE.keys())}

        self.Software = []#pd.DataFrame(columns=["tech", "module", "name"])
        self.Arg = []#pd.DataFrame(columns=["tech", "module", "soft", "name"])
        self.Flag = []#pd.DataFrame(columns=["tech", "module", "soft", "arg", "name"])

        self.source_dict = {
            "illumina": pai,
            "nanopore": pan
        }

    def py2pandas(self):
        self.soft_pk= {}
        self.arg_pk= {}
        for tech, source in self.source_dict.items():
            soft_mdict = {
                "QC": source.ARGS_HD,
                "HD": source.ARGS_HD,
                "ASSEMBLY_SOFT": source.ARGS_ASS,
                "ASSEMBLE_CLASS": source.ARGS_CLASS,
                "CLASSM": source.ARGS_CLASS,
                "REMAP_SOFT": source.ARGS_REMAP
            }

            for mod, softl in source.SOFTWARE.items():
                for sf in softl:
                    nrow = {
                        "model": "pipeline.software",
                        "pk": len(self.Software)+1,
                        "fields": {
                            "tech": self.tech_pk[tech],
                             "module": self.mod_pk[mod],
                             "name": sf,
                        }
                    }
                    self.soft_pk[sf]= len(self.Software)+1
                    self.Software.append(nrow)
                    #self.Software = pd.concat([self.Software, nrow], ignore_index=True, axis=0)

            for mod, softl in source.SOFTWARE.items():
                argdict = soft_mdict[mod]
                for soft in softl:
                    if soft in argdict.keys():
                        for arg, flags in argdict[soft].items():
                            nrow = {
                                "model": "pipeline.Arg",
                                "pk": len(self.Arg) +1,
                                "fields": {
                                     "tech": self.tech_pk[tech],
                                     "module": self.mod_pk[mod],
                                     "soft": self.soft_pk[soft],
                                     "name": arg,
                                }
                            }
                            self.arg_pk[arg]= len(self.Arg) +1
                            self.Arg.append(nrow)
                            #self.Arg = pd.concat([self.Arg, nrow], ignore_index=True, axis=0)

                            for fl in flags:
                                nrow = {
                                    "model": "pipeline.flag",
                                    "pk": len(self.Flag) +1,
                                    "fields": {
                                        "tech": self.tech_pk[tech],
                                         "module": self.mod_pk[mod],
                                         "soft": self.soft_pk[soft],
                                         "arg": self.arg_pk[arg],
                                         "name": str(fl),
                                    }
                                }
                            self.Flag.append(nrow)
                            #self.Flag = pd.concat([self.Flag, nrow], ignore_index=True, axis=0)


class Command(BaseCommand):
    help = "command to add data from params files to the database."

    def handle(self, *args, **options):
        import json
        argdata= pyparse()
        argdata.py2pandas()
        out_dir= "pipeline/management/data/"

        with open(out_dir+"software.json", 'w') as fout:
            json.dump(argdata.Software, fout, indent= 4)
        with open(out_dir+"Technology.json", 'w') as fout:
            json.dump(argdata.Technology, fout, indent= 4)
        with open(out_dir+"Module.json", 'w') as fout:
            json.dump(argdata.Module, fout, indent= 4)
        with open(out_dir+"Arg.json", 'w') as fout:
            json.dump(argdata.Arg, fout, indent= 4)
        with open(out_dir+"Flag.json", 'w') as fout:
            json.dump(argdata.Flag, fout, indent= 4)

        #engine= create_engine('sqlite:///db.sqlite3')
        #argdata.Software.to_sql(Software._meta.db_table, con=engine, index= True, if_exists= 'replace')
        #argdata.Module.to_sql(Module._meta.db_table, con=engine, index=True, if_exists='replace')
        #argdata.Technology.to_sql(Technology._meta.db_table, con=engine, index=True, if_exists='replace')
        #argdata.Arg.to_sql(Arg._meta.db_table, con=engine, index=True, if_exists='replace')
        #argdata.Flag.to_sql(Flag._meta.db_table, con=engine, index=True, if_exists='replace')

