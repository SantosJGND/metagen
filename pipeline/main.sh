#!/bin/bash

CONF_FILE=config.sh
source $CONF_FILE
source $CONDA/miniconda3/etc/profile.d/conda.sh


export CONDA
export ENVSDIR
export CONF_FILE

##
SECONDS=0
TIMESTAMP=`date +"%Y-%m-%d %T"`
WDH=""
FILTD=$WDH$FILTD
ASSD=$WDH$ASOUT$ASSEMBLY_SOFT"/"
export WDH

# PARAMS
OFQ=""

print_usage() {
  printf "Usage: ..."
}

## INPUT ##
if [ -z $INPUT ]; then echo "missing input"; exit 1; fi

IFILE=`basename $INPUT`
INAME=${IFILE%.f*}
CLEAN_R1=$WDH$CLEAND$INAME.fastq.gz
FILT_R1=$FILTD$INAME.$HD.filt.fq.gz
C1=$INPUT
export INAME

if [ ! -z $PAIR ]; then
PNAME=`basename $PAIR`
PNAME=${PNAME%.f*}
CLEAN_R2=$WDH$CLEAND$PNAME.fastq.gz
FILT_R2=$FILTD$PNAME.$HD.filt.fq.gz
C2=$PAIR
export PNAME
fi

###############################################
### PREPROCESS
echo $INPUT $PAIR

if $QCONTROL; then
if [ ! -f $CLEAN_R1 ]; then

echo $PAIR
$BIN"preprocess/process_data.sh" -a $INPUT -b $PAIR #2>> $LOGD$SUFFIX.preproc.log

fi

echo $C1 >  $LOGD$SUFFIX"_latest.fofn"
echo $C2 >> $LOGD$SUFFIX"_latest.fofn"
C1=$CLEAN_R1
C2=$CLEAN_R2

fi
################################################
##### HOST DEPLETION

if $DEPLETE; then

$BIN"classification/class_selector.sh" -a $C1 \
		-d $HDOUT -o $FILTD -m $HD -p f -s $SUFFIX -b $C2 #2>> $LOGD$SUFFIX.depletion.log

ELAPSED_HD=$SECONDS

if [ `zcat $FILT_R1 | wc -l` -gt 0 ]; then
C1=$FILT_R1
C2=$FILT_R2
echo $C1 >  $LOGD$SUFFIX"_latest.fofn"

if [ ! -z $PAIR ]; then
echo $C2 >> $LOGD$SUFFIX"_latest.fofn"
$BIN"preprocess/clean_unpaired.sh" -a $C1 -b $C2

fi

fi

fi

#################################################
##### ASSEMBLY
if $ASSEMBLE; then
touch $LOGD"assembly.fofn"

if [ $ASSEMBLY_SOFT == "spades" ]; then

$BIN"assembly/spades.sh" -a $C1 -d $ASSD -o $ASSD -b $C2 #2>> $LOGD$SUFFIX.assembly.log

elif [ $ASSEMBLY_SOFT == "velvet" ]; then

$BIN"assembly/velvet.sh" -a $C1 -d $ASSD -o $ASSD -b $C2 #2>> $LOGD$SUFFIX.assembly.log

fi

##################################################
### filter assembly
ASSEMBLY=$WDH$ASOUT$ASSEMBLY_SOFT"/"$INAME"/"$INAME.scaffolds.fasta.gz
ASSEMBLY_FILTERED=$WDH$ASOUT$ASSEMBLY_SOFT"/"$INAME.filtered.scaffolds.fasta

conda activate $ENVSDIR"Pyenv/pyenv"
echo $ENVSDIR

python $BIN"assembly/filter_fasta.py" $ASSEMBLY $ASSEMBLY_FILTERED $ASSEMBLY_LTRIM
gzip $ASSEMBLY_FILTERED
ASSEMBLY_FILTERED=$ASSEMBLY_FILTERED.gz

conda deactivate

###################################################
##### CLASSIFICATION

if [ `zgrep "^>" $ASSEMBLY_FILTERED | wc -l` -gt 0 ]; then

echo $CLASSD"assembly/"

if [ $ASSEMBLE_CLASS == "minimap-asm" ]; then
$BIN"classification/hd_minimapASM.sh" -a $ASSEMBLY -d $CLASSD"assembly/" \
                -o $CLASSD"assembly/" -r -s "assembly" #2>> $LOGD$SUFFIX.aclass.log


elif [ $ASSEMBLE_CLASS == "metamix" ]; then
$BIN"classification/hd_metamix.sh" -a $ASSEMBLY -d $CLASSD"assembly/" \
                -o $CLASSD"assembly/" -r -s "assembly" #2>> $LOGD$SUFFIX.aclass.log

else

$BIN"classification/hd_blastp.sh" -a $ASSEMBLY_FILTERED -d $CLASSD"assembly/" \
			-o $CLASSD"assembly/" -s "assembly" #2>> $LOGD$SUFFIX.aclass.log

fi

echo $ASSEMBLY_FILTERED > $LOGD"assembly.fofn"

$BIN"remap/virsorter2.sh" -a $ASSEMBLY_FILTERED

fi

fi
####################### END OF ASSSEMBLY
if $CLASSIFY; then

$BIN"classification/class_selector.sh" -a $C1 -d $CLASSD"reads/" \
		-m $CLASSM -p r -s $SUFFIX -b $C2 #2>> $LOGD$SUFFIX.rclass.log

fi

##### MAPPING

if $REMAP; then
mkdir -p $LOGD$SUFFIX"/"

conda activate $ENVSDIR"Pyenv/pyenv"

python $BIN"remap/merge_results.py" $CLASSD $SUFFIX $REF_FASTA$REMAP_REF \
        $REF_FASTA

conda deactivate

#####
conda activate $ENVSDIR"remap/remap"
PATTERN=$CLASSD$SUFFIX*.targets

if ls $PATTERN 1> /dev/null 2>&1; then
for REF in $PATTERN; do
REFN=`basename $REF`
REFN=${REFN%.targets}
REMAP_REF=`cat $CLASSD$REFN.file`
mkdir -p $LOGD$SUFFIX"/"$REFN"/"
echo $acc
echo $REF
echo $REMAP_REF

for acc in `cat $REF`; do
samtools faidx $REF_FASTA$REMAP_REF $acc >> $REMD$REFN.fasta
done

echo "ref here: " $REMD$REFN.fasta

if [ $REMAP_SOFT == "snippy" ]; then
$BIN"remap/snippy.sh" -a $C1 -r $REMD$REFN.fasta -d $REMD -b $C2 2> $LOGD$SUFFIX"remap.log"

elif [ $REMAP_SOFT == "rematch" ]; then

$BIN"remap/rematch.sh" -a $C1 -r $REMD$REFN.fasta -d $REMD -b $C2 2>$LOGD$SUFFIX"remap.log"

elif [ $REMAP_SOFT == "bowtie" ]; then

$BIN"remap/bowtie.sh" -a $C1 -r $REMD$REFN.fasta -d $REMD -b $C2  2> $LOGD$SUFFIX"remap.log"

elif [ $REMAP_SOFT == "minimap-rem" ]; then

$BIN"remap/minimap2.sh" -a $C1 -r $REMD$REFN.fasta -d $REMD -b $C2 2> $LOGD$SUFFIX"remap.log"

fi

if [ -s $LOGD"assembly.fofn" ]; then
ASSEMBLY=`cat $LOGD"assembly.fofn"`
$BIN"remap/minimapASM.sh" -a $ASSEMBLY -r $REMD$REFN.fasta -d $REMD

fi

rm $REMD$REFN.fasta

done


conda activate $ENVSDIR"Pyenv/pyenv"
echo "merging reports"
python $BIN"remap/merge_reports.py" $SUFFIX $CLASSD $REMD \
                $REF_FASTA $RDIR$SUFFIX.report.tsv $SECONDS

conda deactivate

fi

conda deactivate
fi

##### SUMMARY & REPORT PREP

####### CLEAN

if $CLEAN ; then

rm -r $CLASSD$SUFFIX* $CLASSD"reads/"$CLASSM"/" $CLASSD"reads/"$CLASSM"/"

fi


