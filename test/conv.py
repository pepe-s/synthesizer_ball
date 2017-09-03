# -*- coding: utf-8 -*-


# 16進数を符号付きで変換する
def s16(val):
    return -(val & 0b1000000000000000) | (val & 0b0111111111111111)

# センサメダルの生データから値を取得する
def convData(raw_datas):
    cnt = 0
    datas = []
    # 2バイトずつにする
    lst = [raw_datas[i: i+4] for i in range(0, len(raw_datas), 4)]
    for e in lst:
        # 上位と下位バイトを入れ替えて変換
        lst[cnt] = lst[cnt][2:] + lst[cnt][:2]
        datas.append(long(lst[cnt], 16))
        cnt += 1
    return datas

if __name__ == "__main__":
    print convData("1122FF33EE44CC00")