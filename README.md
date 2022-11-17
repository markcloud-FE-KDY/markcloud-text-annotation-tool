# Markcloud-Text-Review 정의서

1. 날짜 입력

       - ex. `python3 main.py –date 20221001-20221003` 이면, `[20221001,20221002,20221003]` 에 해당하는 날짜 들고 오기 

       - ex. `python3 main.py –date 20221001-20221001` 이면,`[20221001]` 에 해당하는 날짜 들고 오기 
    
       - ex. `python3 main.py –date 20221002` 이면,`[20221002]` 에 해당하는 날짜 들고 오기 

       - ex. `python3 main.py` 이면, `[오늘날짜]` 들고 오기 
       
<br>

2. 들고 온 날짜에 업데이트 된 `productNameEng` 데이터 들고오기 

       ```python
       def get_updated_data(coll, start_date, end_date):
           print(f"> get_updated_data... {start_date}-{end_date}")
   
           updated_data = list(
               coll.find(
                   {
                       "_dataUpdateDate": {"$gte": start_date, "$lte": end_date},
                       "productNameEng": {"$ne": None},
                   },
                   {"_id": 0, "productNameEng": 1},
               )
           )
   
           return updated_data
       ```
       
<br>

3. 가져 온 `productNameEng` 를 전처리

       1. `.lower()` 적용
       2. 공백 기준으로 split
       3. regular expression 적용 `[^a-zA-Z]`
       4. 중복 제거
       5. 전처리 된 `productNameEng` 를 저장하고 반환 ex.`['kipris', 'update']`

       ```python
       def data_preprocess(updated_data):
           print("> data_preprocess...")
           tmp = []
       
           for i in updated_data:
               pNE = i["productNameEng"]
               words = list(map(str, pNE.split(" ")))
               for word in words:
                   word2 = re.sub("[^a-zA-Z]", "", word)
                   if word2:
                       word3 = word2.lower()
                       tmp.append(word3)
   
           processed_data = list(dict.frokeys(tmp))
   
           return processed_d
       ```

<br>

4. 기존 `mark_dict` 데이터에 있는 `productNameEng` 항목들은 제거

       ```python
       def get_difference(processed_data, source_eng):
           print("> get_difference...")  #
           res = Counter(processed_data) - Counter(source_eng)
           diff_result = list(res.keys())
   
           return diff_result
       ```

<br>

5. 남은 `productNameEng`를 `model.py`를 이용해서 `modelResult`로 변환 

       - ex : `wwwyedinacomcn	예디나`, `lonseal	론씰`

<br>

6. `modelResult`를 마크서치에 검색 (`marksearch.py`)

       1. 일치하는 항목이 있으면 `mark_dict` 컬렉션에 바로 저장 
          1.  ex. `extremes	익스트림스` 에서 `익스트림스` 를 마크서치에 검색
          2. `['NORTHERN EXTREMES', 'NORTHERN EXTREMES', 'EXTREME SCREEN', 'extremesports']` 검색 결과  리스트 내에서  `productNameEng` 컬럼의 `extremes` 가 들어있는 문자열이 있거나 `extremes` or `EXTREMES` 등 완전일치하는 항목이 있으면,
          3. `mark_dict` 컬렉션에`['productNameEng', 'modelResult', 'similarWords', 'humanCheck']` 데이터를 저장 및 `humanCheck` 컬럼은 `true` 로 표시
          <br>
       2. 일치하는 항목이 없으면 `productNameEng` 를 마크서치에 검색 (`marksearch.py`)
          1. ex. `econapaen	에코나페엔` 에서 `econapaen` 을 마크서치에 검색
          2. `['에코나팬', 'ECONAPAEN']` 검색 결과 리스트 내에서 `modelResult` 컬럼의 `에코나페엔` 이 들어있는 문자열이 **있으면** 6-1-3 번 실행
             1. **없으면**  `['에코나팬', 'ECONAPAEN']` 의 한글 원소들을 `kodex` 로 변환 후 유사도 측정 후 **75%** 정확도 이상이면 `mark_dict` 컬렉션에`['productNameEng', 'modelResult', 'similarWords', 'humanCheck']` 데이터를 저장
                - `similarWords` 컬럼은 유사도 순으로 정렬
                - `humanCheck` 컬럼은 `false` 로 표시