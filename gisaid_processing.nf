process GISAID_PROCESSING {
  tag"$wslh_viralrecon_report"
  container "quay.io/wslh-bioinformatics/spriggan-pandas:1.3.2"

  label 'process_single'

  input:
  path(wslh_viralrecon_report)
  path(consensus_directory)

  output:
  path "*.consensus.fa", emit: consensus

  when:
  task.ext.when == null || task.ext.when

  script: //This script is bundled with the python script within bin.
  """
  pull_consensus.py $wslh_viralrecon_report
  """

 }