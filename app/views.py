import csv
import os
from flask import render_template, request, send_file
from app import app
from app.utils import file_utils as fu
from app.utils import xmind_utils as xu
from app.utils import logging_utils as lu
from app.utils import api_utils as au
import logging
import json

logger = lu.Logger(__name__, cmd_level=logging.INFO, file_level=logging.INFO)


# for page route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='首页')


@app.route('/xtoz', methods=['GET', 'POST'])
def xtoz():
    if request.method == 'GET':
        return render_template('xtoz.html', title='用例转换')
    elif request.method == 'POST':
        f = request.files['xmind']
        base_dir = app.config.get('BASE_DIR')
        uploads_dir = app.config.get('UPLOADS_DIR')
        upload_path = os.path.join(base_dir, uploads_dir, f.filename)
        f.save(upload_path)
        # 转换xmind to csv
        xm = xu.XmindUtils(upload_path)
        xm.parse_test_cases()
        cases = xm.testcases
        logger.logger.info('[Begin]待生成测试用例%d个' % len(cases))
        # 倒序，以便禪道能夠按照正常順序排列
        cases.reverse()

        if cases is None or len(cases) == 0:
            raise ValueError('未解析到测试用例，请检查xmind文件')

        csv_file = fu.get_csv_name_via_xmind(upload_path)

        case_counter = 0

        with open(csv_file, 'w', encoding='gbk', newline='') as f:
            ff = csv.writer(f)
            header = ['所属模块', '用例标题', '步骤', '预期', '关键词', '用例类型', '优先级']
            ff.writerow(header)
            for t in cases:
                ff.writerow(['', t.get('name'), t.get('step'), t.get('expecting'), '', '功能测试', t.get('priority')])
                logger.logger.info('%s - 完成' % t.get('name'))
                case_counter += 1

        logger.logger.info('[End]已生成测试用例%d个' % case_counter)

        # return render_template('xtoz.html', title='用例转换')
        return send_file(csv_file, as_attachment=True)


# for api
@app.route('/api/frame-parse', methods=['GET', 'POST'])
def frame_parse():
    if request.method == 'GET':
        hex_data = request.args.get('hex')
        ut = au.ApiUtils()
        resp = ut.get_parsed_frame(9, hex_data)
        tmp_dict = json.loads(resp)

        # print(ret_dict)
        parsed_fields = tmp_dict.get('data').get('queueParams').get('parsedFields')
        parsed_field_list = []

        for k, v in parsed_fields.items():
            code = k
            hex_str = v.get('hexString')
            name = v.get('fieldDefinetion').get('fieldName')
            field_value = v.get('fieldValue')
            decoded_value = v.get('decodedValue')
            order = v.get('fieldDefinetion').get('frameOrder')
            index = v.get('fieldDefinetion').get('startIndex')
            length = v.get('fieldDefinetion').get('fieldLength')
            data_type = v.get('fieldDefinetion').get('dataType')
            data_format = v.get('fieldDefinetion').get('dataFormat')
            encode_format = v.get('fieldDefinetion').get('encodeFormat')
            scale_method = v.get('fieldDefinetion').get('scaleMethod')
            filed_scale = v.get('fieldDefinetion').get('fieldScale')
            high_byte_preceding = v.get('fieldDefinetion').get('highBytePreceding')
            prefix_fill = v.get('fieldDefinetion').get('prefixFillChar')
            suffix_fill = v.get('fieldDefinetion').get('suffixFillChar')

            tmp = {'order': order, 'index': index, 'length': length, 'hex_str': hex_str, 'field_value': field_value,
                   'decoded_value': decoded_value, 'code': code, 'name': name, 'data_type': data_type,
                   'data_format': data_format, 'encode_format': encode_format, 'scale_method': scale_method,
                   'filed_scale': filed_scale, 'high_byte_preceding': high_byte_preceding,
                   'prefix_fill': prefix_fill, 'suffix_fill': suffix_fill}

            parsed_field_list.append(tmp)

        parsed_field_list.sort(key=lambda x: x.get('order'))

        ret_dict = {'code': 0, 'message': 'OK', 'data': {'records': parsed_field_list}}

        return json.dumps(ret_dict)
