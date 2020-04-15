import csv
import os
from flask import render_template, request, send_file
from app import app
from app.utils import file_utils as fu
from app.utils import xmind_utils as xu


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

        if cases is None or len(cases) == 0:
            raise ValueError('未解析到测试用例，请检查xmind文件')

        csv_file = fu.get_csv_name_via_xmind(upload_path)

        with open(csv_file, 'w', newline='') as f:
            ff = csv.writer(f)
            for t in cases:
                ff.writerow([t.get('id'), t.get('name'), t.get('step'), t.get('expecting'), t.get('priority')])
                # logger.logger.info('解析测试用例 -> %s' % t.get('name'))

        # return render_template('xtoz.html', title='用例转换')
        return send_file(csv_file, as_attachment=True)
