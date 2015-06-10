# -*- coding:utf8 -*-
import re

JOSA_PAIRD = {
    u"(이)가" : (u"이", u"가"),
    u"(와)과" : (u"과", u"와"),
    u"(을)를" : (u"을", u"를"),
    u"(은)는" : (u"은", u"는"),
    u"(으)로" : (u"으로", u"로"),
    u"(아)야" : (u"아", u"야"),
    u"(이)여" : (u"이여", u"여"),
    u"(이)라" : (u"이라", u"라"),
}

JOSA_REGEX = re.compile(u"\(이\)가|\(와\)과|\(을\)를|\(은\)는|\(아\)야|\(이\)여|\(으\)로|\(이\)라")


def choose_josa(prev_char, josa_key, josa_pair):
    """
    조사 선택

    :param prev_char 앞 글자
    :param josa_key 조사 키
    :param josas 조사 리스트
    """
    char_code = ord(prev_char)

    # 한글 코드 영역(가 ~ 힣) 아닌 경우 
    if char_code < 0xac00 or char_code > 0xD7A3: 
        return josa_pair[1]

    local_code = char_code - 0xac00 # '가' 이후 로컬 코드
    jong_code = local_code % 28

    # 종성이 없는 경우
    if jong_code == 0: 
        return josa_pair[1]
        
    # 종성이 있는 경우
    if josa_key == u"(으)로":
        if jong_code == 8: # ㄹ 종성인 경우
            return josa_pair[1]

    return josa_pair[0]

def replace_josa(src):
    tokens = []
    base_index = 0
    for mo in JOSA_REGEX.finditer(src):
        prev_token = src[base_index:mo.start()]
        prev_char = prev_token[-1]
        tokens.append(prev_token)

        josa_key = mo.group()
        tokens.append(choose_josa(prev_char, josa_key, JOSA_PAIRD[josa_key]))

        base_index = mo.end()

    tokens.append(src[base_index:])
    return ''.join(tokens)

if __name__ == '__main__':
    import unittest

    class JosaTestCase(unittest.TestCase):
        def test(self):
            self.assertEquals(replace_josa(
                u"아노아(이)가 공격했다"), 
                u"아노아가 공격했다")

            self.assertEquals(replace_josa(
                u"주펫(이)가 공격했다"), 
                u"주펫이 공격했다")

            self.assertEquals(replace_josa(
                u"아노아(은)는 자루(와)과 오리(을)를 칭송하고 절(으)로 들어갔습니다."), 
                u"아노아는 자루와 오리를 칭송하고 절로 들어갔습니다.")

            self.assertEquals(replace_josa(
                u"네(이)가 잘못했어. 확률(이)가 이상해. 덫(이)가 깔렸어."),
                u"네가 잘못했어. 확률이 이상해. 덫이 깔렸어.")
            
            self.assertEquals(replace_josa(
                u"너(와)과 함께 할게. 글(와)과 그림. 빛(와)과 어둠."),
                u"너와 함께 할게. 글과 그림. 빛과 어둠.")

            self.assertEquals(replace_josa(
                u"수녀(을)를 존경했어. 남자들(을)를 입히다. 버튼(을)를 만지지 마."),
                u"수녀를 존경했어. 남자들을 입히다. 버튼을 만지지 마.")

            self.assertEquals(replace_josa(
                u"우리(은)는 끝이야. 쌀(은)는 필요없어. 갑옷(은)는 찢었다."),
                u"우리는 끝이야. 쌀은 필요없어. 갑옷은 찢었다.")

            self.assertEquals(replace_josa(
                u"진우(아)야, 그것도 몰라? 경렬(아)야, 진정해. 상현(아)야, 뭐해?"),
                u"진우야, 그것도 몰라? 경렬아, 진정해. 상현아, 뭐해?")

            self.assertEquals(replace_josa(
                u"진우(이)여, 닥쳐라. 경렬(이)여, 이리 오라. 상현(이)여, 아무 일도 아니다."),
                u"진우여, 닥쳐라. 경렬이여, 이리 오라. 상현이여, 아무 일도 아니다.")

            self.assertEquals(replace_josa(
                u"부두(으)로 가야 해. 대궐(으)로 가거나. 집(으)로 갈래?"),
                u"부두로 가야 해. 대궐로 가거나. 집으로 갈래?")

            self.assertEquals(replace_josa(
                u"나(이)라고 어쩔 수 있겠니? 별(이)라고 불러줘. 라면(이)라고 했잖아."),
                u"나라고 어쩔 수 있겠니? 별이라고 불러줘. 라면이라고 했잖아.")

            self.assertEquals(replace_josa(
                u"라면(이)라면 어떨까? 밥(이)라능~"),
                u"라면이라면 어떨까? 밥이라능~")

            self.assertEquals(replace_josa(
                u"너(이)라면 어떨까? 나(이)라능~"),
                u"너라면 어떨까? 나라능~")

    unittest.main()

