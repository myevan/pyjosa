pyjosa
======

파이썬 한글 조사 처리

## 예제

#### 콘솔

    Python 2.7.2 (default, Jun 20 2012, 16:23:33) 
    [GCC 4.2.1 Compatible Apple Clang 4.0 (tags/Apple/clang-418.0.60)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pyjosa
    >>> print pyjosa.replace_josa(u"아노아(은)는 자루(와)과 오리(을)를 칭송하고 절(으)로 들어갔다.")
    아노아는 자루와 오리를 칭송하고 절로 들어갔다.
    >>>     

#### 코드

    # -*- coding:utf8 -*-
    import pyjosa

    print pyjosa.replace_josa(u"아노아(은)는 자루(와)과 오리(을)를 칭송하고 절(으)로 들어갔다.")
