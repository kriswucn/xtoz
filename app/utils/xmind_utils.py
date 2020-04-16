# coding:utf-8
import xmind
import os


class XmindUtils(object):
    def __init__(self, path):
        self._roots = []
        self._test_cases = []

        if not os.path.exists(path):
            raise FileNotFoundError

        self._workbook = xmind.load(path)
        self._sheets = self._workbook.getSheets()

        for sh in self._sheets:
            self._roots.append(sh.getRootTopic().getData())

    @property
    def roots(self):
        return self._roots

    @property
    def testcases(self):
        return self._test_cases

    @staticmethod
    def is_test_case(topic):
        if topic is None:
            raise Exception

        markers = topic.get('markers')

        for m in markers:
            if m.find('priority') > -1:
                return True

        return False

    # 递归, topic is list type
    def _parse(self, topics, module_prefix):
        if topics is None or len(topics) == 0:
            # raise TypeError
            return

        for t in topics:
            # 如果是测试用例节点
            if self.is_test_case(t):
                # todo 解析测试用例的title, step and expecting
                # 测试用例标题
                case_name = '【%s】%s' % (module_prefix, t.get('title'))
                case_id = t.get('id')
                case_priority = t.get('markers')[0].split('-')[1]
                # 测试步骤
                step_dict = t.get('topics')
                step_str = ''
                expecting_str = ''

                i = 1

                if step_dict is None:
                    raise ValueError('未发现可用的测试用例')

                for s in step_dict:
                    step_str += '%d. %s\r\n' % (i, s.get('title'))

                    # ----- 期望是步骤的子节点 BEGIN -----
                    # exp_dict = s.get('topics')
                    # 该步骤有期望
                    # if exp_dict is not None:
                    #     只取第一个topic
                    #      expecting_str += '%s\r\n' % exp_dict[0].get('title')
                    # else:
                    #     expecting_str += '\r\n'
                    # ----- 期望是步骤的子节点 END -----
                    # ----- 期望是测试步骤的备注 BEGIN -----
                    tmp_expecting = s.get('note')

                    if tmp_expecting is not None:
                        expecting_str += '%d. %s' % (i, tmp_expecting.replace('\r\n', '#'))
                    else:
                        expecting_str += '%d. ' % i
                    # 统一加上\r\n
                    expecting_str += '\r\n'

                    i += 1
                    # ----- 期望是测试步骤的备注 END -----
                #
                # print(step_str.rstrip('\r\n'))
                # print(expecting_str.rstrip('\r\n'))
                test_case_dict = {'id': case_id, 'name': case_name, 'step': step_str.rstrip('\r\n'),
                                  'expecting': expecting_str.rstrip('\r\n'), 'priority': case_priority}
                self._test_cases.append(test_case_dict)
            else:
                self._parse(t.get('topics'), module_prefix)

    def parse_test_cases(self):
        if len(self.roots) == 0:
            raise TypeError()

        for root in self.roots:
            module_prefix = root.get('title')
            self._parse(root.get('topics'), module_prefix)
