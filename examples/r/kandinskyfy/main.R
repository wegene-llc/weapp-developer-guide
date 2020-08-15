#!/usr/bin/Rscript
options(warn = -1)
source('wegene_utils.R')

load.pkgs <- function(...){
  tmp <- suppressPackageStartupMessages(suppressWarnings(
    lapply(unlist(list(...)), library, character.only=T,
           warn.conflicts=F, quietly=T, verbose=F)))
}

load.pkgs('base64enc', 'dplyr', 'data.table', 'kandinsky', 'purrr')

# Inputs always come from stdin
body <- readLines(file('stdin', 'r'), warn = F, n = 1)

tryCatch({
    # Assume the required data is whole genome, parse it into an R object first
    inputs <- fromJSON(json_str = body)
    if(!(is.null(inputs$inputs$data))){
      genome <- unzip_genome_data(inputs)
      genome_info <- genome_info(genome$genome_str, genome$genome_format)
    }

    genome_info <- genome_info %>%
      select(-chromosome, -position) %>%
      mutate(genotype=as.character(genotype))

    rsids <- fread('rsids.txt', col.names="rsid", header=F)

    df <- rsids %>%
     ## Extract the required rsid from raw data
    left_join(., genome_info, by='rsid') %>%
    # If rsid not in data index, replace with --
    mutate(genotype=ifelse(is.na(genotype), '--', genotype)) %>%
    ## Replace __ in some data format to --
    mutate(genotype=ifelse(genotype=='__', '--', genotype))

    png()
    kandinsky(df)
    dev.off()
    txt <- base64enc::base64encode("Rplot001.png")
    md <- sprintf('### 使用您的基因组数据生成的康定斯基风格抽象画如下：\n\n![result](data:image/png;base64,%s)\n\n---\n\n#####[阅读更多关于康定斯基](https://baike.baidu.com/item/瓦西里·康定斯基/1531894)', txt)
    cat(md)
}, error = function(e) {
    # Any error msgs should be thrown out from stderr, so you will receive log
    write(conditionMessage(e), stderr())
})
