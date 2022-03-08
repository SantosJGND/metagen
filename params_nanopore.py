#!/usr/bin/python3
################################# DIRS

SOURCE= {
	"ENVSDIR": "/home/artic/Desktop/mngs_environments/",
	"DBDIR_MAIN": "/home/artic/Desktop/databases/ref_db/",
	"REF_FASTA": "/home/artic/Desktop/databases/ref_fasta/",
        "BIN": "../depo/scripts/"

}


DIRS= {
        "CLEAND": "reads/clean/",
	"FILTD": "reads/hd_filtered/",
	"HDOUT": "host_depletion/output/",
	"ASOUT": "assembly/output/",
	"CLASSD": "classification/",
	"REMD": "remap/",
	"LOGD": "logs/",
	"OUTD": "output/"
}

################################## MODULES

ACTIONS= {
	"CLEAN": ["false"],
	"QCONTROL": ["true"],
	"DEPLETE": ["true", "false"],
	"ASSEMBLE": ["true", "false"],
	"CLASSIFY": ["true"],
	"REMAP": ["true"]
}

################################## SOFTWARE

SOFTWARE= {
	"QC": ["nanofilt"], # "nanofilt", trimmomatic
	"HD": ["dvf","minimap2","centrifuge", "kaiju", "kuniq","kraken2"],
	"ASSEMBLY_SOFT": ["flye", "raven"],
	"ASSEMBLE_CLASS": ["blast", "minimap-asm"],
	"CLASSM": ["kraken2", "desamba","minimap2","centrifuge", "kaiju", "kuniq"],
	"REMAP_SOFT": ["minimap-rem"]
}

################################## PARAMS

ARGS_HD= {
	"trimmomatic": {
		"TRIM_ARGS": ["SLIDINGWINDOW:5:20 LEADING:3 TRAILING:3 TOPHRED33: MINLEN:35"],
		"TRIM_THREADS": [8],
		"FQ_THREADS": [8]
	},
	"nanofilt": {
		"NANOFILT_ARGS": ["-q20"]
	},
	"kuniq": {
		"KUNIQ_ARGS": ["--threads 4 --gzip-compressed --fastq-input --hll-precision 12",
				   "--threads 4 --gzip-compressed --fastq-input --quick"]
	},
        "kraken2": {
                "KRAKEN_ARGS": ["--threads 4 --gzip-compressed  --confidence .5 "]
        },
	"centrifuge": {
		"CENTRIFUGE_ARGS": ["-p 4 --time -k 3 --out-fmt sam"]
	},
	"diamond": {
		"DIAMOND_ARGS": ["-p 5 --top 5 -e 0.01 --id 65 --query-cover 50 --fast",
				 "-p 5 --top 5 -e 0.01 --id 65 --query-cover 50 --sensitive",
				 #"-p 5 --top 5 -e 0.01 --id 65 --query-cover 50 --very-sensitive"
						],

		"DIAMOND_DB":["RVDB","swissprot"]
	},
	"kaiju": {
		"KAIJU_ARGS": ["-z 4 -e 5 -s 65 -X -v"]
	},
	"minimap2": {
		"MINIMAP_ARGS": ["-t 4"],
		"MINIMAP_QCF":[20],  # filter for alignment score
		"MINIMAP_AX": ["map-ont"],
		"MINIMAP_DB": ["refseq_viral.genomic.fna.gz", "virosaurus90_vertebrate-20200330.fas.gz"] ##NCBIrs_ViralCG.dustmasked.fna.gz, virosaurus90_vertebrate-20200330.fas.gz
	},
	"dvf": {
		"DVF_CORES": ["4"],
		"DVF_MODEL": ["BASE"]
	}
}


############################  ASSEMBLY PARAMS

ARGS_ASS= {
	"spades": {
		"SPADES_ARGS": ["--meta -t 8 --phred-offset 33 --only-assembler",
				#"--metaviral -t 3 -k 75 --phred-offset 33 --only-assembler",
				#"--metaviral -t 3 -k 95 --phred-offset 33 --only-assembler",
				#"--meta -t 5 -k 55 --phred-offset 33 --only-assembler",
				#"--meta -t 5 -k 75 --phred-offset 33 --only-assembler",
				"--metaviral -t 8 --phred-offset 33 --only-assembler"],
		"ASSEMBLY_LTRIM": [50]
	},
	"velvet": {
		"VELVET_K": [51],
		"VELVET_OPTS":["-s 53 -e 65 -t 3"],
		"VELVET_ARGS":["-exp_cov auto -cov_cutoff auto"],
		"VELVET_FILES":["-fastq.gz"],
                "ASSEMBLY_LTRIM": [50]

	},
	"flye": {
		"FLYE_ARGS": ["--threads 4 --scaffold --nano-raw"],
                "ASSEMBLY_LTRIM": [50]
	},
	"raven": {
		"RAVEN_ARGS": ["-t4 -p2" ],
                "ASSEMBLY_LTRIM": [50]

	},
        "minimap-asm": {
                "MINIMAP_ARGS": ["-t 4"],
                "MINIMAP_QCF":[20],  # filter for alignment score
                "MINIMAP_DB": ["refseq_viral.genomic.fna.gz", "virosaurus90_vertebrate-20200330.fas.gz"]
        }
}


############################# CLASSIFICATION PARAMS


ARGS_CLASS= {
	"Trim": {
		"TRIM_ARGS": ["SLIDINGWINDOW:5:20 LEADING:3 TRAILING:3 TOPHRED33: MINLEN:35"],
		"TRIM_THREADS": [4],
		"FQ_THREADS": [4]
	},
	"kuniq": {
		"KUNIQ_ARGS": ["--threads 4 --gzip-compressed --fastq-input"]
	},
        "kraken2": {
                "KRAKEN_ARGS": ["--threads 4 --gzip-compressed --confidence .5"]
        },
	"centrifuge": {
		"CENTRIFUGE_ARGS": ["-p 4 --time -k 3 --out-fmt sam"]
	},
	"diamond": {
		"DIAMOND_ARGS": ["-p 4 --top 5 -e 0.01 --id 60 --query-cover 60 --fast",
				 "-p 4 --top 5 -e 0.01 --id 60 --query-cover 60 --sensitive"],
		"DIAMOND_DB":["swissprot"]
	},
	"kaiju": {
		"KAIJU_ARGS": ["-z 3 -e 5 -s 50 -X -v",
				"-z 3 -e 5 -s 65 -x -v"]
	},
	"minimap2": {
		"MINIMAP_ARGS": ["-t 4"],
        "MINIMAP_AX": ["map-ont"],
		"MINIMAP_QCF":[20],  # filter for alignment score
		"MINIMAP_DB": ["refseq_viral.genomic.fna.gz", "virosaurus90_vertebrate-20200330.fas.gz"] ##NCBIrs_ViralCG.dustmasked.fna.gz
	},
	"desamba": {
		"DESAMBA_PROC": ["-t 4"],
		"DESAMBA_DB": ["refseq", "virossaurus"],
		"DESAMBA_QFC": [20]
	}
}


############################# REMAP PARAMS

ARGS_REMAP= {
	"snippy": {
		"SNIPPY_ARGS": ["--mapqual 60 --mincov 10"],
		"SNIPPY_RESOURCES": ["--cpus 3 --ram 8"],
		"REMAP_REF": ["refseq_viral.genomic.fna.gz"],
		"MIN_COVERAGE_DEPTH": [1]
	},
	"rematch": {
		"REMATCH_RESOURCES": ["-j 4"],
		"REMATCH_ARGS": ["--minCovCall 10 --minCovPresence 5 --reportSequenceCoverage"],
		"REMATCH_ENV": ["/home/artic/Desktop/mngs_environments/remap/ReMatCh/ReMatCh/"],
		"REMAP_REF": ["refseq_viral.genomic.fna.gz"],
		"MIN_COVERAGE_DEPTH": [1]
	},
	"bowtie": {
		"BOWTIE_RESOURCES": ["--threads 4"],
		"BOWTIE_ARGS": ["--sensitive-local"],
		"REMAP_REF": ["refseq_viral.genomic.fna.gz"],
		"MIN_COVERAGE_DEPTH": [1]
	},
	"minimap-rem": {
        "MINIMAP_ARGS": ["-t 4"],
		"MINIMAP_DB": ["refseq_viral.genomic.fna.gz"],
		"MINIMAP_AX": ["map-ont"],
        "REMAP_REF": ["refseq_viral.genomic.fna.gz",],
		"MIN_COVERAGE_DEPTH": [1]
	}
}
