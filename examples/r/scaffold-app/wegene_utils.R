suppressMessages(library(base64enc))
suppressMessages(library(R.utils))
suppressMessages(library(rjson))

unzip_genome_data <- function(inputs) {
    genome_format <- inputs$inputs$format
    genome_binary <- base64decode(inputs$inputs$data)
    tmp <- tempfile()
    writeBin(genome_binary, tmp)
    genome_str <- strsplit(readLines(tmp, warn = F), '')[[1]]
    genome_str <- paste0(genome_str[c(TRUE, FALSE)], genome_str[c(FALSE, TRUE)])
    return(list(genome_str = genome_str, genome_format = genome_format))
}

genome_info <- function(genome_str, genome_format) {
    # Index files for all posible formats will be provided automatically
    # Do not change the default path below if you wish to use those
    index_file <- read.table(file = paste('./indexes/index_', genome_format, '.idx', sep = '', collapse = ''))
    genome_info <- cbind(index_file[, -1], genome_str)
    colnames(genome_info) <- c('rsid', 'chromosome', 'position', 'genotype')
    return(genome_info)
}
