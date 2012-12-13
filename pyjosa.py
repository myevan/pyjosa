# -*- coding:utf8 -*-
import re

JOSA_PAIRD = {
    u"(이)가" : (u"이", u"가"),
    u"(을)를" : (u"을", u"를"),
    u"(은)는" : (u"은", u"는"),
    u"(으)로" : (u"으로", u"로"),
}

JOSA_REGEX = re.compile(u"\(이\)가|\(을\)를|\(은\)는|\(으\)로")

def has_jong(char):
    char_code = ord(char)
    if char_code >= 0xac00 and char_code <= 0xD7A3: # 가 ~ 힣까지
        local_code = char_code - 0xac00 # '가' 이후 로컬 코드
        jong_code = local_code % 28
        if jong_code: # 종성이 있는 경우
            if jong_code == 8: # ㄹ 종성인 경우
                return False
            else:
                return True
        else: # 종성이 없는 경우
            return False
    else: # 한글이 아닐 경우
        return False

def replace_josa(src):
    tokens = []
    base_index = 0
    for mo in JOSA_REGEX.finditer(src):
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
            self.assertEquals(replace_josa(u"아노아(은)는 자루(을)를 칭송하고 절(으)로 들어갔습니다."), u"아노아는 자루를 칭송하고 절로 들어갔습니다.")

    unittest.main()

