# coding:utf-8
import json

ret_dict = {}

with open('h.json', 'r', encoding='utf-8') as f:
    ret_text = f.read()
    ret_dict = json.loads(ret_text)

# print(ret_dict)
parsed_fields = ret_dict.get('queueParams').get('parsedFields')
parsed_field_list = []

for k, v in parsed_fields.items():
    code = k
    hex_str = v.get('hexString')
    name = v.get('fieldDefinetion').get('fieldName')
    decoded_value = v.get('decodedValue')
    order = v.get('fieldDefinetion').get('frameOrder')
    index = v.get('fieldDefinetion').get('startIndex')
    length = v.get('fieldDefinetion').get('fieldLength')
    data_type = v.get('fieldDefinetion').get('dataType')
    data_format = v.get('fieldDefinetion').get('dataFormat')
    scale_method = v.get('fieldDefinetion').get('scaleMethod')
    filed_scale = v.get('fieldDefinetion').get('fieldScale')
    high_byte_preceding = v.get('fieldDefinetion').get('highBytePreceding')
    prefix_fill = v.get('fieldDefinetion').get('prefixFillChar')
    suffix_fill = v.get('fieldDefinetion').get('suffixFillChar')

    tmp = {'order': order, 'index': index, 'length': length, 'hex_str': hex_str, 'decoded_value': decoded_value,
           'code': code, 'name': name, 'data_type': data_type, 'data_format': data_format,
           'scale_method': scale_method, 'filed_scale': filed_scale, 'high_byte_preceding': high_byte_preceding,
           'prefix_fill': prefix_fill, 'suffix_fill': suffix_fill}

    parsed_field_list.append(tmp)

parsed_field_list.sort(key=lambda x: x.get('order'))

for p in parsed_field_list:
    print(p)
