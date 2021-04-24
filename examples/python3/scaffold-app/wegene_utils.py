# -*- coding: utf-8 -*-

__all__ = ['process_raw_genome_data', 'is_genotype_exist', 'is_wegene_format']

import sys
import gzip
import base64
import re
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
                    base64.b64decode(raw_inputs['data']))).read())
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

#这是一个获取用户mt单倍群的函数
def Get_MT():
    body = sys.stdin.read()
    inputs = json.loads(body)['inputs']
    user_mt = inputs['haplogroup']['mt']['haplogroup']
    return user_mt

#这是一个可以获取用户Simple mt的函数，其中length值表示想要去的单倍群长度，例如length为2，用户的单倍群是A8a1，则Simple mt为A8
def Get_Simple_MT(length):
    Get_MT()
    if len(user_mt) == 1:
        Simple_mt = user_mt
    elif "'" in user_mt:
        Simple_mt = user_mt
    else:
        letter_list = re.split('\d',user_mt)
        number_list = re.split('\D',user_mt)
        counter = 0
        Simple_mt = ''
        while length - 1 == counter:
            if isinstance(counter,int) == True:
                Simple_mt += letter_list[counter]
                counter += 1
            else:
                Simple_mt += number_list[counter]
    return Simple_mt

#这是一个获取用户y单倍群的函数
def Get_Y():
    body = sys.stdin.read()
    inputs = json.loads(body)['inputs']
    user_gender = inputs['sex']
    if user_gender == 1:
        user_y = inputs['haplogroup']['y']['haplogroup']
        return user_y
    elif user_gender == 2:
        sys.stderr.write('女性没有Y染色体哦～')
    else:
        sys.stderr.write('性别数据缺失')

#这是一个可以获取用户Simple y的函数，其中length值表示想要去的单倍群长度，例如length为3，用户的单倍群是O2a2b1a1b，则Simple y为O2a
def Get_Simple_Y(length):
    Get_Y()
    if len(user_y) == 1:
        Simple_y = user_y
    else:
        letter_list = re.split('\d',user_y)
        number_list = re.split('\D',user_y)
        counter = 0
        Simple_y = ''
        while length - 1 == counter:
            if isinstance(counter,int) == True:
                Simple_y += letter_list[counter]
                counter += 1
            else:
                Simple_y += number_list[counter]
    return Simple_y
