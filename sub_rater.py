import numpy as np

harmony = [2, 0, 1, 1, 1, 2, 0, 2, 1, 1, 1, 0, 2]
outsider = {1, 3, 6, 8, 10}

def rater_transition(melody: list) -> list:
    length = len(melody)
    res = [0.0] * 10
    valid = 0
    for i in range(0, length - 2):
        interval1 = abs(melody[i + 1] - melody[i])
        interval2 = abs(melody[i + 2] - melody[i + 1])
        if melody[i] == 0 or melody[i + 1] == 0 or melody[i + 2] == 0:
            continue
        valid += 1
        if interval1 > 19 or interval2 > 19:
            res[0] += 1
        else: 
            harmony1 = harmony[interval1 % 12]
            harmony2 = harmony[interval2 % 12]
            res[harmony1 * 3 + harmony2 + 1] += 1
    if valid == 0:
        return res
    for i in range(0, 10):
        res[i] /= valid
    return res

def rater_stability(melody: list) -> float:
    length = len(melody)
    res = 0.0
    tot = 0.0
    for i in range(0, length - 2):
        interval1 = melody[i + 1] - melody[i]
        interval2 = melody[i + 2] - melody[i + 1]
        if melody[i] == 0 or melody[i + 1] == 0 or melody[i + 2] == 0:
            continue
        if interval1 * interval2 < 0:
            res += abs(interval1 - interval2)
        tot += abs(interval1) + abs(interval2)
    return res / tot

def rater_density(melody: list) -> float:
    length = len(melody)
    res = 0
    for i in range(0, length):
        if (i == length - 1 or melody[i] != melody[i + 1]) and melody[i] != 0:
            res += 1
    return res / length

def rater_density_variation(melody: list) -> float:
    length = len(melody)
    cnt = 0
    min_density = 100000.0
    max_density = 0.0
    for i in range(0, length):
        if (i == length - 1 or melody[i] != melody[i + 1]) and melody[i] != 0:
            cnt += 1
        if i % 8 == 7 or i == length - 1:
            min_density = min(min_density, cnt / (i % 8 + 1))
            max_density = max(max_density, cnt / (i % 8 + 1))
            cnt = 0     
    return min_density / max_density

def rater_syncopation(melody: list) -> float:
    length = len(melody)
    res = 0
    tot = 0
    for i in range(0, length):
        if i % 4 == 3 and i != length - 1 and melody[i] == melody[i + 1] and melody[i] != 0:
            res += 1
        if (i == length - 1 or melody[i] != melody[i + 1]) and melody[i] != 0:
            tot += 1
    return res / tot

def rater_pitch_range(melody: list) -> float:
    length = len(melody)
    min_pitch = 100
    max_pitch = 0
    for i in range(0, length):
        if melody[i] == 0:
            continue
        min_pitch = min(min_pitch, melody[i])
        max_pitch = max(max_pitch, melody[i])
    return (max_pitch - min_pitch) / 100

def rater_max_silence(melody: list) -> float:
    length = len(melody)
    res = 0
    cnt = 0
    for i in range(0, length + 1):
        if i == length or melody[i] != 0:
            res = max(res, cnt)
            cnt = 0
        else:
            cnt += 1
    return res / length

def rater_unique_pitch(melody: list) -> float:
    length = len(melody)
    res = 0
    table = [False] * 120
    for i in range(0, length):
        table[melody[i]] = True
    for i in range(0, 120):
        if table[i]:
            res += 1
    return res / 120


def rater(melody: list) -> list:
    res = rater_transition(melody)
    res.append(rater_stability(melody))
    res.append(rater_density(melody))
    res.append(rater_density_variation(melody))
    res.append(rater_syncopation(melody))
    res.append(rater_pitch_range(melody))
    res.append(rater_max_silence(melody))
    res.append(rater_unique_pitch(melody))
    res = [float(i) for i in res]
    return res

def rater_outsider(melody: list) -> float:
    length = res = 0
    for i in melody:
        if i > 0:
            length += 1
            if i % 12 in outsider:
                res += 1
    return res / length