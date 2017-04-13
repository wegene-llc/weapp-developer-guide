'''
这是一个脚手架应用，你可以直接将你的计算代码嵌入其中以便于快速开发
'''

# -*- coding: utf-8 -*-
import sys
import json
# wegene_utils 库会包含在每个应用的环境当中，无需自行打包上传
# 这里提供源代码以供应用完整运行
from wegene_utils import process_raw_genome_data

'''
当输入是部分位点时, 基因位点数据以 json 形式输入:
    {"inputs": {"rs671": "AA", "rs12203592": "CA"}}

当输入全部位点时，全部位点对应的字符串序列会被 gzip 压缩并以 base64 转码，
转码前的数据在 data 域中
    {"inputs": {"data": "xfgakljdflkja...", format: "wegene_affy_2"}}
你需要解码并解压该数据，解压后的字符串如下:
    AACCTACCCCCC...
进一步，你需要利用相应格式的索引文件对每个位点进行解析
我们提供了整个流程的示例代码以及索引文件
'''

# 从 stdin 读取输入数据
body = sys.stdin.read()

try:
    # 如果输入的数据是全部位点数据，可以使用 wegene_utils的方法进行解析后使用
    inputs = json.loads(body)['inputs']
    # 使用 wegene_utils 解析以后，数据会被解析成下面这样的 json 格式:
    #   {'rs123': {'genotype': 'AA', 'chromosome': '1', position: '1236'}, ...}
    user_genome = process_raw_genome_data(inputs)

    # 如果输入的数据是部分位点数据，你可以直接进行使用，注意 RSID 是大写且要求的位点在没有检测
    # 的情况下 key 可能不存在
    # inputs = json.loads(body)['inputs']
    # if 'RS671' in inputs.keys():
    #   rs671 = inputs['RS671']

    # 现在你可以开始根据输入数据进行实际的计算并输出结论了
    # result = do_something(user_genome)
    result = '我是一个结论\n我是结论的第二行'

    # 输出给用户的结果只需要通过 print 输出即可，print只可调用一次
    print result
except Exception as e:
    # 错误信息需要被从 stderr 中输出，否则会作为正常结果输出
    sys.stderr.write('这是一段错误信息，可能对用户可见，建议友好输出')
