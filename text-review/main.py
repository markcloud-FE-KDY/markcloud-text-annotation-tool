from get_collection import *
from utils import *
from model import get_engtokor
from marksearch import marksearch
import argparse
import csv
from kodex import *


parser = argparse.ArgumentParser(description="date 입력")
parser.add_argument("-d", "--date", default="")
args = parser.parse_args()

pretrained_model_path = "../best_model"

if __name__ == "__main__":
    coll_brands_query = get_collection("markview", "brands_query")
    date_list = get_date_range(args.date)

    start_date, end_date = date_list[0], date_list[-1]

    # 주어진 날짜 구간 사이의 productNameEng 수집
    updated_data = get_updated_data(coll_brands_query, start_date, end_date)
    updated_data_list = []
    for ud in updated_data:
        updated_data_list.append(ud["productNameEng"])

    # productNameEng의 split, regex, lower처리
    processed_data = data_preprocess(updated_data)
    # (db) mark_dict 컬렉션에서 productNameEng 불러오기 (humanCheck true인 것만)
    coll_mark_dict = get_collection("text_review", "mark_dict")
    src_eng = get_markdict_eng(coll_mark_dict)

    # mark_dict에 없는 값만 (차집합)
    diff_result = get_difference(processed_data, src_eng)

    # model돌려서 model_result 얻기
    productNameEngList, modelResultList = get_engtokor(pretrained_model_path, diff_result)

    hc_true = []
    hc_false = []

    for productNameEng, modelResult in zip(productNameEngList, modelResultList):
        filter = {"productNameEng": productNameEng}

        # 6. modelResult를 마크서치에 검색
        marksearch_modelResult = list(set(marksearch(modelResult)))
        # [modelResult를 마크서치에 검색한 결과 리스트]에 productNameEng가 있으면
        check = [s for s in marksearch_modelResult if productNameEng in s]

        # 6.1. 일치하는 항목이 있으면 `mark_dict` 컬렉션에 바로 저장
        if check:
            # 컬렉션에 저장 (humanCheck: true)
            new_values = {
                "$set": {"modelResult": modelResult, "humanCheck": True},
                "$unset": {"similarWords": 1},
            }
            hc_true.append(productNameEng)

        # 6.2. 일치하는 항목이 없으면 `productNameEng` 를 마크서치에 검색 (`marksearch.py`)
        else:
            # 6.2.1. ex. `econapaen	에코나페엔` 에서 `econapaen` 을 마크서치에 검색
            marksearch_productNameEng = list(set(marksearch(productNameEng)))

            # 6.2.2. [productNameEng를 마크서치에 검색한 결과 리스트]에 modelResult가 있으면
            check2 = [s for s in marksearch_productNameEng if modelResult in s]
            if check2:
                # 컬렉션에 저장 (humanCheck: true)
                new_values = {
                    "$set": {"modelResult": modelResult, "humanCheck": True},
                    "$unset": {"similarWords": 1},
                }
                hc_true.append(productNameEng)

            # 6.2.2.1. 없으면  ['에코나팬', 'ECONAPAEN'] 의 한글 원소들을 kodex 로 변환 후
            # 유사도 측정 후 75% 정확도 이상이면
            # mark_dict 컬렉션에 ['productNameEng', 'modelResult', 'similarWords', 'humanCheck'] 데이터를 저장
            else:
                reg = re.compile(r"[a-zA-Z]")
                similar_words = []
                for word in marksearch_productNameEng:
                    if word and not reg.match(word) and (word != " "):
                        similarity = similar(
                            kodexScoreConversion(modelResult),
                            kodexScoreConversion(word),
                        )
                        if similarity >= 0.75:
                            similar_words.append([word, round(similarity, 2)])
                if similar_words:
                    similar_words.sort(key=lambda x: -x[1])

                # 컬렉션에 저장 (humanCheck: false)
                new_values = {
                    "$set": {
                        "modelResult": modelResult,
                        "similarWords": str(similar_words),
                        "humanCheck": False,
                    }
                }
                hc_false.append(productNameEng)
        coll_mark_dict.update_one(filter, new_values, upsert=True)

    # datetime, updated_data, processed_data, diff_result, humanCheck_true, humanCheck_false
    with open(f"../result_txt/update_data_count.csv", "a", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(
            [
                f"{start_date}-{end_date}",
                len(updated_data),
                len(processed_data),
                len(diff_result),
                len(hc_true),
                len(hc_false),
            ]
        )

    with open(f"../result_txt/update_data.csv", "a", encoding="utf-8-sig") as f2:
        wr2 = csv.writer(f2)
        wr2.writerow(
            [
                f"{start_date}-{end_date}",
                updated_data_list,
                processed_data,
                diff_result,
                hc_true,
                hc_false,
            ]
        )
