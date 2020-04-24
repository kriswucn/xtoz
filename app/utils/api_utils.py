# coding:utf-8
import requests
import config
from urllib.parse import urljoin
import json


class ApiUtils(object):
    def __init__(self):
        login_url = urljoin(config.UMC_URL, 'login')
        params = {'username': config.USERNAME, 'password': config.PASSWORD}
        resp = requests.post(login_url, params=params)
        # print(resp.text)
        self._user_info = json.loads(resp.text)
        self._cookies = requests.utils.dict_from_cookiejar(resp.cookies)
        # print(self._cookies)

    @property
    def user_info(self):
        return self._user_info

    @property
    def cookies(self):
        return self._cookies

    # 协议
    def get_all_dev_com_protocols(self):
        url = urljoin(config.UMC_URL, '/admin/operate/get-all-protocol-without-tenant')
        resp = requests.get(url, cookies=self._cookies)
        return resp.text

    # 原语（只包含单条上报）
    def get_atomic_action(self, dev_com_protocol_id):
        url = urljoin(config.UMC_URL, '/admin/conf/protocol-atomic-actions')

        params = {'devComProtocolId': dev_com_protocol_id, 'size': -1, 'protocolAtomicActionName': '单条'}
        resp = requests.get(url, params=params, cookies=self._cookies)
        return resp.text

    # 帧匹配
    def get_frame_pairs(self, protocol_atomic_action_id):
        url = urljoin(config.UMC_URL, '/admin/conf/atomic-action-frame-pairs')
        params = {'protocolAtomicActionId': protocol_atomic_action_id}
        resp = requests.get(url, params=params, cookies=self._cookies)
        return resp.text

    # 协议帧
    def get_protocol_frame(self, protocol_frame_id):
        url = urljoin(config.UMC_URL, '/admin/conf/protocol-frame/%s' % protocol_frame_id)
        resp = requests.get(url, cookies=self._cookies)
        return resp.text

    # 帧字段
    def get_frame_field(self, frame_field_id):
        url = urljoin(config.UMC_URL, '/admin/conf/frame-field/%s' % frame_field_id)
        resp = requests.get(url, cookies=self._cookies)
        return resp.text


if __name__ == '__main__':
    au = ApiUtils()
    # res = au.get_atomic_action(9)
    # res = au.get_frame_pairs(1042)
    res = au.get_protocol_frame(3240)
    # print(res)
    d = json.loads(res)
    field_list = []

    fs = d.get('data').get('fields')
    for field in fs:
        tmp_field = {'id': field.get('frameFieldId'), 'order': field.get('frameOrder'),
                     'value': field.get('fixedValue'), 'start': field.get('startIndex'),
                     'length': field.get('fieldLength'), 'code': field.get('fieldCode'),
                     'name': field.get('fieldName')}
        field_list.append(tmp_field)
        print(tmp_field)
