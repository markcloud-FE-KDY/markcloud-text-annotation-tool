from collections import OrderedDict


class MarkdictCache:
    def __init__(self):
        self._cache = OrderedDict()
        self._cache_key_list = []

    def find_by_oid(self, oid):
        return self._cache.get(oid)

    def show_cache(self):
        print(self._cache)
        return self._cache
    
    def show_cache_2(self):
        for k in self._cache_key_list:
            print(self._cache.get(k)['modelResult'])
        print()
        print(len(self._cache_key_list))

    def insert_data(self, datas):
        check = False
        for data in datas:
            oid = data["id"]
            # 캐시에 새로 들어간 값이 있는지 체크
            if oid not in self._cache_key_list:
                self._cache_key_list.append(oid)
                self._cache[oid] = data
                check = True
        return check
    
    def insert_data_front(self, datas):
        check = False
        datas.reverse()
        for data in datas:
            oid = data["id"]
            # 캐시에 새로 들어간 값이 있는지 체크
            if oid not in self._cache_key_list:
                self._cache_key_list.insert(0, oid)
                self._cache[oid] = data
                check = True
        return check

    def clear_cache(self):
        self._cache = {}
        self._cache_key_list = []
