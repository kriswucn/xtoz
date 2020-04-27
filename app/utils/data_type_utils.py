# coding:utf-8
import codecs
import binascii
import binhex

# data_type
'''
1. String
2. Integer
3. UnsignedInt
4. ShortInt
5. Float
6. DateTime
7. Date
8. Time
9. HexString
10. BinString
'''


# hex低位在左
def low_byte_left(hex_str):
    try:
        bs = codecs.decode(hex_str, 'hex')
        ret = codecs.encode(bs[::-1], 'hex').decode('utf-8')

        return ret
    except Exception:
        raise ValueError('参数错误')


# int to hex
def int_to_hex(num, length, scale_type=0, scale_value=1):
    # 16进制字符串
    # 倍数乘法和不缩放
    if scale_type == 2 or scale_type == 0:
        alt_num = int(num * scale_value)
        # 按长度来指定补位
        f_tmpl = '{0:0%dx}' % (2 * length)
        hex_str = f_tmpl.format(alt_num)
        hex_v = binascii.unhexlify(hex_str)

        while len(hex_v) < length:
            hex_str += '00'
            hex_v = binascii.unhexlify(hex_str)

        return binascii.hexlify(hex_v).decode()
    elif scale_type == 1:
        raise Exception('除法操作暂不支持')

    # hex_str = '{0:02x}'.format(int(num))
    # hex_v = binascii.unhexlify(hex_str)
    #
    # while len(hex_v) < length:
    #     hex_str += hex_str
    #     hex_v = binascii.unhexlify(hex_str)
    #
    # hex_b = binascii.hexlify(hex_v).decode()
    #
    # return hex_b


# float to hex
# scale_type:
#   2: 乘以
#   1: 除以
#   0: 不操作
def float_to_hex(num, length, scale_type, scale_value):
    if scale_type == 2:
        alt_num = int(num * scale_value)
        f_temp = '{0:0%dx}' % (2 * length)
        hex_str = f_temp.format(alt_num)
        hex_v = binascii.unhexlify(hex_str)

        while len(hex_v) < length:
            hex_str += '00'
            hex_v = binascii.unhexlify(hex_str)

        hex_b = binascii.hexlify(hex_v).decode()

        return hex_b

    elif scale_type == 1:
        pass
    else:
        raise Exception('不支持的缩放')


if __name__ == '__main__':
    # a = 6.14
    # b = float_to_hex(num=a, length=2, scale_type=2, scale_value=100)
    # c = low_byte_left(b)
    # print(c)
    version = 2
    hex_str1 = int_to_hex(version, length=2)
    hex_ret = low_byte_left(hex_str1)
    print(hex_ret)
