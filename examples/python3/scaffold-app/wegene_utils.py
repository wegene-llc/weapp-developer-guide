# -*- coding: utf-8 -*-

__all__ = ['process_raw_genome_data', 'is_genotype_exist', 'is_wegene_format']

import sys
import gzip
import base64
from io import BytesIO


def sort_genotype(genotyope):
    return ''.join(sorted(genotyope))


'''
Reads the genome string anmd format and parse into a dict of
    {'rs1234': {'genotype': 'AA', 'chromosome': '1', position: '123456'}, ...}
'''


def parse_genome_string(genome_str, genome_format):
    try:
        genome_dict = {}
        # Index files for all posible formats will be provided automatically
        # Do not change the default path below if you wish to use those
        with open('./indexes/index_' + genome_format + '.idx', 'r') as idx_f:
            for line in idx_f:
                if not line.startswith('NA'):
                    fields = line.strip().split('\t')
                    index_pos = fields[0]
                    rsid = fields[1]
                    chromosome = fields[2]
                    position = fields[3]
                    start_pos = int(index_pos) * 2
                    genome_dict[rsid] = {
                        'genotype': sort_genotype(
                                        genome_str[start_pos:start_pos+2]),
                        'chromosome': chromosome,
                        'position': position
                    }
        return genome_dict
    except Exception as e:
        sys.stderr.write('Error on file {} line {} '.format(
                            sys.exc_info()[-1].tb_frame.f_code.co_filename,
                            sys.exc_info()[-1].tb_lineno)
                         + str(e))


def process_raw_genome_data(raw_inputs):
    try:
        genome = str(gzip.GzipFile(fileobj=BytesIO(
                    base64.b64decode(raw_inputs['data']))).read(), encoding="utf8")
        genome_format = raw_inputs['format']
        return parse_genome_string(genome, genome_format)
    except Exception as e:
        sys.stderr.write('Error on file {} line {} '.format(
                            sys.exc_info()[-1].tb_frame.f_code.co_filename,
                            sys.exc_info()[-1].tb_lineno)
                         + str(e))


def is_genotype_exist(input, rsid):
    return rsid in input and input[rsid] != '--' and input[rsid] != '__'


def is_wegene_format(format_str):
    return 'wegene_' in format_str
