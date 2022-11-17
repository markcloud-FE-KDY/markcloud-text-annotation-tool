from difflib import SequenceMatcher


def slicing(word):
    CHOSUNG_LIST = [
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]

    JUNGSUNG_LIST = [
        "ㅏ",
        "ㅐ",
        "ㅑ",
        "ㅒ",
        "ㅓ",
        "ㅔ",
        "ㅕ",
        "ㅖ",
        "ㅗ",
        "ㅘ",
        "ㅙ",
        "ㅚ",
        "ㅛ",
        "ㅜ",
        "ㅝ",
        "ㅞ",
        "ㅟ",
        "ㅠ",
        "ㅡ",
        "ㅢ",
        "ㅣ",
    ]

    JONGSUNG_LIST = [
        "*",
        "ㄱ*",
        "ㄲ*",
        "ㄳ*",
        "ㄴ*",
        "ㄵ*",
        "ㄶ*",
        "ㄷ*",
        "ㄹ*",
        "ㄺ*",
        "ㄻ*",
        "ㄼ*",
        "ㄽ*",
        "ㄾ*",
        "ㄿ*",
        "ㅀ*",
        "ㅁ*",
        "ㅂ*",
        "ㅄ*",
        "ㅅ*",
        "ㅆ*",
        "ㅇ*",
        "ㅈ*",
        "ㅊ*",
        "ㅋ*",
        "ㅌ*",
        "ㅍ*",
        "ㅎ*",
    ]

    char_list = []
    for char in list(word.strip()):
        if "가" <= char <= "힣":
            ch1 = (ord(char) - ord("가")) // 588
            ch2 = ((ord(char) - ord("가")) - (588 * ch1)) // 28
            ch3 = (ord(char) - ord("가")) - (588 * ch1) - 28 * ch2
            char_list.append(CHOSUNG_LIST[ch1])
            char_list.append(JUNGSUNG_LIST[ch2])
            char_list.append(JONGSUNG_LIST[ch3])
        else:
            char_list.append([char])
    return char_list


def kodexScoreConversion(korean_word):

    kodex_scores = {
        "ㄱ": "1",
        "ㄱ*": "1",
        "ㄲ": "1",
        "ㅋ": "1",
        "ㄴ": "2",
        "ㄴ*": "2",
        "ㅇ": "2",
        "ㅇ*": "2",
        "ㄷ": "3",
        "ㄸ": "3",
        "ㅌ": "3",
        "ㅅ*": "3",
        "ㅊ": "3",
        "ㄹ": "4",
        "ㄹ*": "4",
        "ㅁ": "5",
        "ㅁ*": "5",
        "ㅂ": "6",
        "ㅂ*": "6",
        "ㅃ": "6",
        "ㅍ": "6",
        "ㅎ": "6",
        "ㅅ": "7",
        "ㅆ": "7",
        "ㅈ": "7",
        "ㅉ": "7",
    }

    chosung_conversion = {"ㄲ": "ㄱ", "ㄸ": "ㄷ", "ㅃ": "ㅂ", "ㅆ": "ㅅ", "ㅉ": "ㅈ", "ㅎ": "ㅍ"}

    first_chosung = []
    code_list = []

    first_chosung.append(slicing(korean_word)[0][0])
    for f in first_chosung:
        if f in chosung_conversion.keys():
            code_list.append(
                chosung_conversion[f[0]]
            )  # Step 3. Replace the staring letter CHOSUNG to its subtituting CHOSUNG.
        else:
            code_list.append(f)

    char_list = [] + code_list

    for i, w in enumerate(slicing(korean_word)[1:]):
        try:
            if (
                w != "ㅇ" and w in kodex_scores.keys()
            ):  # Step 1. Remove 'ㅇ' from all CHOSUNG except the one in starting letter.
                char_list.append(w)
        except:
            pass

    for idx in range(
        1, len(char_list)
    ):  # Step 2. Remove same syllable from JONGSUNG-CHOSUNG continuum.
        try:
            if char_list[idx][1] == "*" and char_list[idx][0] == char_list[idx + 1]:
                char_list.pop(idx)

        except:
            pass

    for i, w in enumerate(char_list[1:]):
        try:
            if w in kodex_scores.keys():
                code_list.append(
                    kodex_scores[w]
                )  # Step 4. Replace remaining syllables to Kodex scores

        except Exception as e:
            print(e)

    return "".join(code_list)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


if __name__ == "__main__":
    print(kodexScoreConversion("에코나페엔"))
    print(kodexScoreConversion("에코나팬"))
    print(similar(kodexScoreConversion("에코나페엔"), kodexScoreConversion("에코나팬")))
