# -*- coding: utf-8 -*-

__all__ = ['process_raw_genome_data', 'is_genotype_exist', 'is_wegene_format', 'get_mt', 'get_y', 'get_simple_mt', 'get_simple_y', 'to_markdown_table']

import re
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
def get_mt(inputs):
    return inputs['haplogroup']['mt']['haplogroup']


#这是一个获取用户y单倍群的函数
def get_y(inputs):
    return inputs['haplogroup']['y']['haplogroup']


#这是一个获取用户simple mt单倍群的函数
def get_simple_mt(inputs,length):
    inputs = get_mt(inputs)
    letter = re.split(r'\d+',inputs)
    number = re.split(r'\D+',inputs)
    while '' in letter:
        letter.remove('')
    while '' in number:
        number.remove('')
    #处理当指定切割长度比mt实际长度长的情况
    if  len(letter + number) <= length:
        output = inputs
    #处理特殊mt
    elif len(inputs) == 1 or "'" in inputs:
        output = inputs
    else:
        min_num = min(len(letter),len(number))
        output_list = []
        for element in range(min_num):
            output_list.append(letter[element])
            output_list.append(number[element])
        output = ''.join(output_list[0:length])    
    return output


#这是一个获取用户simple y单倍群的函数
def get_simple_y(inputs,length):
    inputs = get_y(inputs)
    letter = re.split(r'\d+',inputs)
    number = re.split(r'\D+',inputs)
    while '' in letter:
        letter.remove('')
    while '' in number:
        number.remove('')
    #处理当指定切割长度比y实际长度长的情况
    if  len(letter + number) <= length:
        output = inputs
    #处理边缘y
    elif len(inputs) == 1 or "~" in inputs or inputs.isalpha() is True:
        output = inputs
    else:
        min_num = min(len(letter),len(number))
        output_list = []
        for element in range(min_num):
            output_list.append(letter[element])
            output_list.append(number[element])
        output = ''.join(output_list[0:length])    
    return output


#这是一个将嵌套list转化为markdown表格形式的函数
def to_markdown_table(input_head,input_body,output_style):
    result_list = []
    column_num = len(input_head)
    for row in input_body:
        element_list = []
        for element in row:
            element_list.append(str(element))
        result_list.append('|'+'|'.join(element_list))
        body_md = '|\n'.join(result_list)+'|'
    if output_style == 'left':
        style = [':---']
    if output_style == 'right':
        style = ['---:']
    if output_style == 'center':
        style = [':---:']
    element_list = []
    for element in input_head:
        element_list.append(str(element))
    head_md = '|'+'|'.join(element_list)+'|\n'
    style_md = '|'+'|'.join(style * column_num)+'|\n'
    result = head_md + style_md + body_md
    return result
'''
在 to_markdown_table(input_head,input_body,output_style)函数中
input_head input_body output_style分别指的是 表格的表头 表格内容 以及 文字风格
文字风格 有三种选择，可以是 left right 或 center 分别代表 文字左对齐 文字右对齐 和 文字居中
如果输出结果中包含 整型 或 浮点型 无需对结果进行 str() 处理，函数中会自动处理

调用本函数的示例代码如下：

head = [1,2,3,4,5]
body = [
    [7,8,9,0,1],
    [4,7,9,10,4]
]
result = to_markdown_table(head,body,'center')
print(result)

本段代码输出结果如下

|1|2|3|4|5|
|:---:|:---:|:---:|:---:|:---:|
|7|8|9|0|1|
|4|7|9|10|4|

'''
