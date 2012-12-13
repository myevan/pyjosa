# -*- coding:utf8 -*-
import re

JOSA_PAIRD = {
    u"(이)가" : (u"이", u"가"),
    u"(을)를" : (u"을", u"를"),
    u"(은)는" : (u"은", u"는"),
}

def has_jong(char):
    code = ord(char) - 0xac00
    return code % 28

def replace_josa(src):
    tokens = []
    base_index = 0
    for mo in re.finditer(u"\(이\)가|\(을\)를|\(은\)는", src):
        prev_token = src[base_index:mo.start()]
        prev_char = prev_token[-1]
        tokens.append(prev_token)

        josa = mo.group()
        josa1, josa2 = JOSA_PAIRD[josa]
        tokens.append(josa1 if has_jong(prev_char) else josa2)

        base_index = mo.end()

    tokens.append(src[base_index:])
    return ''.join(tokens)

if __name__ == '__main__':
    import unittest

    class JosaTestCase(unittest.TestCase):
        def test(self):
            self.assertEquals(replace_josa(u"아노아(이)가 공격했다"), u"아노아가 공격했다")
            self.assertEquals(replace_josa(u"주펫(이)가 공격했다"), u"주펫이 공격했다")
            self.assertEquals(replace_josa(u"아노아(은)는 자루(을)를 칭송했다"), u"아노아는 자루를 칭송했다")

    unittest.main()

