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
                for s in step_dict:
                    step_str += '%d. %s\n\r' % (i, s.get('title'))
                    i += 1
                    exp_dict = s.get('topics')
                    # 该步骤有期望
                    if exp_dict is not None:
                        # 只取第一个topic
                        expecting_str += '%s\n\r' % exp_dict[0].get('title')
                    else:
                        expecting_str += '\n\r'
                #
                # print(step_str.rstrip('\n\r'))
                # print(expecting_str.rstrip('\n\r'))
                test_case_dict = {'id': case_id, 'name': case_name, 'step': step_str.rstrip('\n\r'),
                                  'expecting': expecting_str.rstrip('\n\r'), 'priority': case_priority}
                self._test_cases.append(test_case_dict)
            else:
                self._parse(t.get('topics'), module_prefix)

    def parse_test_cases(self):
        if len(self.roots) == 0:
            raise TypeError()

        for root in self.roots:
            module_prefix = root.get('title')
            self._parse(root.get('topics'), module_prefix)
