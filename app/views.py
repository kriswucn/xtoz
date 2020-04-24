import csv
import os
from flask import render_template, request, send_file
from app import app
from app.utils import file_utils as fu
from app.utils import xmind_utils as xu
from app.utils import logging_utils as lu
from app.utils import api_utils as au
import logging

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
# 所有通信协议
@app.route('/api/dev-com-protocols', methods=['GET'])
def dev_com_protocols():
    if request.method == 'GET':
        util = au.ApiUtils()
        protocols = util.get_all_dev_com_protocols()
        return protocols


@app.route('/api/atomic-actions', methods=['GET'])
def atomic_actions():
    if request.method == 'GET':
        ut = au.ApiUtils()
        dev_com_protocol_id = request.args.get('dev-com-protocol-id')
        i_id = int()
        actions = ut.get_atomic_action(dev_com_protocol_id)
        return actions


@app.route('/api/atomic-action-pairs', methods=['GET'])
def atomic_action_pairs():
    if request.method == 'GET':
        ut = au.ApiUtils()
        atomic_action_id = request.args.get('atomic-action-id')
        a_id = int(atomic_action_id)
        pairs = ut.get_frame_pairs(a_id)
        return pairs


@app.route('/api/protocol-frame')
def protocol_frame():
    if request.method == 'GET':
        ut = au.ApiUtils()
        protocol_frame_id = request.args.get('protocol-frame-id')
        pf_id = int(protocol_frame_id)
        frame = ut.get_protocol_frame(pf_id)
        return frame
