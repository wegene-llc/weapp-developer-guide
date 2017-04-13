#!/usr/bin/Rscript
options(warn = -1)
source('wegene_utils.R')

# IMPORTANT if you wish to load dependencies, please load silently like below:
#   suppressMessages(library(base64enc))


# When required data is not whole genome, the input is a json string:
#    {"inputs": {"RS671": "AA", "RS12203592": "CA", "format": "wegene_affy_2"}}

# When required data is whole genome,
# the input is a json string contains the compressed genome data:
#    {"inputs": {"data": "xfgakljdflkja...", format: "wegene_affy_2"}}
# After decoding data, we will have the genotype: AACCTACCCCCC...


# Inputs always come from stdin
body <- readLines(file('stdin', 'r'), warn = F, n = 1)

tryCatch({
    # Assume the required data is whole genome, parse it into an R object first
    inputs <- fromJSON(json_str = body)

    # First, get genome string and genome format
    genome <- unzip_genome_data(inputs)

    # Next, get genome information which contains
    # rsid, chromosome, position and genotype in a data frame
    genome_info <- genome_info(genome$genome_str, genome$genome_format)


    # Else if you are requiring other data, simply parse input string
    # library(rjson)
    # inputs <- fromJSON(body)$inputs
    # Please be aware that RSIDs are in capital letters and may not exist if the
    #   SNP is not tested
    # if(!(is.null(inputs$RS671)){
    #  RS671 <- inputs$RS671
    # }

    # Now your calculation goes here, do whatever you like
    # result = do_something(user_genome)
    result = 'some calculation has been done!'


    # Return your results simply by cat it out.
    # Do not use print as it will contain line number.
    # You can only use cat for once - or the followed results will be ignored
    cat(result)
}, error = function(e) {
    # Any error msgs should be thrown out from stderr, so you will receive log
    write(conditionMessage(e), stderr())
})
