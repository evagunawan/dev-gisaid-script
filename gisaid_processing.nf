// Think like this process is all local. 

 process GISAID_UPLOAD {

    label 'process_low'

    container "quay.io/wslh-bioinformatics/spriggan-pandas:1.3.2"

    input:
    path(wslh_viralrecon_report)
    path(consensus_directory)

    output:
    path "*.consensus.fa", emit:

    when:
    task.ext.when == null || task.ext.when

    script: //This script is bundled with the python script within bin.
   """
   pull_consensus.py $wslh_viralrecon_report
   """

 }