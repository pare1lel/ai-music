import random
import pickle
import torch
import numpy as np
from deap import base, creator, tools, algorithms
from sub_rater import rater, rater_outsider
from nn_newrater import net
from player import ConvertToMidi

# 定义旋律的范围和长度
MELODY_MIN = 53
MELODY_MAX = 79
MELODY_LENGTH = 64

# 定义遗传算法的参数
GEN_SIZE = 200
GEN_NUM = 100

# 定义适应度函数
def evaluate(melody):
    ts = torch.tensor(rater(melody))
    return model.forward(ts)[0] * 4 + np.log(1 - 0.8 * rater_outsider(melody)),

# 定义变异算子 - 包括移调, 倒影, 逆行
def mutate(melody):
    choose = random.random()
    if choose < 0.25:   # 变异
        for i in range(MELODY_LENGTH):
            if random.random() < 0.1:
                melody[i] = random.choice([0] + list(range(MELODY_MIN, MELODY_MAX + 1)))
    elif choose < 0.5:  # 移调
        l = MELODY_MIN - min(filter(lambda x: x > 0, melody))
        r = MELODY_MAX - max(melody)
        pos = random.randint(l, r)
        for i in range(MELODY_LENGTH):
            if melody[i] > 0:
                melody[i] = melody[i] + pos
    elif choose < 0.75: # 倒影
        for i in range(MELODY_LENGTH):
            if melody[i] > 0:
                melody[i] = MELODY_MIN + MELODY_MAX - melody[i]
    else:   # 逆行
        for i in range(MELODY_LENGTH // 2):
            j = MELODY_LENGTH - i - 1
            melody[i], melody[j] = melody[j], melody[i]
    return melody,

if __name__ == '__main__':
    model = pickle.load(open("model.dat", "rb"))
    # 创建适应度类和个体类
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # 注册遗传算子
    toolbox = base.Toolbox()
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selBest)

    # 设置初始种群
    population = [
        creator.Individual([64, 64, 72, 71, 72, 72, 71, 71, 72, 72, 72, 72, 74, 74, 74, 74, 76, 76, 76, 76, 76, 76, 69, 69, 69, 69, 69, 69, 71, 71, 72, 72, 71, 71, 71, 71, 71, 71, 71, 71, 72, 72, 72, 72, 74, 74, 74, 74, 77, 77, 76, 76, 76, 76, 67, 67, 67, 67, 67, 67, 0, 0, 0, 0]),
        creator.Individual([65, 64, 64, 62, 64, 64, 0, 55, 65, 64, 64, 62, 64, 64, 0, 55, 65, 64, 64, 62, 64, 64, 64, 64, 64, 64, 58, 58, 57, 57, 57, 57, 67, 65, 65, 64, 65, 65, 0, 53, 67, 65, 65, 64, 65, 65, 0, 55, 67, 65, 65, 64, 65, 65, 65, 65, 65, 65, 64, 62, 62, 62, 0, 0]),
        creator.Individual([69, 69, 69, 69, 72, 72, 72, 72, 71, 71, 71, 71, 67, 67, 67, 67, 64, 64, 64, 64, 69, 69, 69, 69, 67, 67, 67, 67, 60, 60, 60, 60, 62, 62, 62, 62, 62, 62, 60, 60, 64, 64, 64, 64, 64, 64, 64, 64, 62, 62, 62, 62, 62, 62, 60, 60, 64, 64, 64, 64, 0, 0, 0, 0]),
        creator.Individual([72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 64, 64, 65, 65, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 71, 71, 71, 71, 0, 0, 0, 0, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 62, 62, 64, 64, 71, 71, 71, 71, 71, 71, 71, 71, 69, 69, 69, 69, 69, 69, 71, 71, 71, 71]),
        creator.Individual([64, 64, 67, 67, 69, 69, 69, 69, 69, 69, 67, 69, 69, 67, 67, 69, 69, 67, 64, 62, 64, 67, 67, 67, 64, 64, 64, 64, 0, 0, 0, 0, 57, 57, 64, 62, 62, 60, 60, 57, 60, 64, 64, 62, 62, 0, 0, 0, 60, 60, 60, 67, 67, 67, 67, 69, 63, 62, 60, 62, 62, 60, 60, 60]),
        creator.Individual([69, 69, 72, 72, 74, 74, 72, 74, 74, 72, 76, 76, 76, 76, 76, 76, 69, 69, 72, 72, 74, 74, 72, 74, 74, 72, 76, 76, 76, 76, 76, 76, 76, 76, 77, 77, 76, 76, 77, 76, 76, 77, 76, 76, 75, 76, 74, 74, 74, 74, 72, 72, 74, 74, 72, 74, 74, 72, 74, 74, 75, 75, 76, 76]),
        creator.Individual([64, 64, 64, 64, 69, 69, 69, 69, 62, 62, 62, 62, 0, 0, 0, 0, 60, 60, 60, 60, 65, 65, 65, 65, 64, 64, 64, 64, 0, 0, 0, 60, 62, 60, 62, 60, 62, 60, 62, 60, 62, 64, 0, 60, 60, 60, 60, 60, 62, 62, 60, 60, 62, 62, 64, 64, 65, 65, 65, 64, 64, 64, 0, 0]),
        creator.Individual([72, 72, 72, 72, 71, 71, 72, 72, 72, 72, 72, 72, 71, 71, 72, 72, 72, 72, 72, 72, 76, 76, 76, 76, 0, 0, 0, 0, 76, 76, 74, 74, 74, 74, 74, 74, 71, 71, 67, 67, 67, 67, 67, 67, 67, 67, 77, 77, 77, 77, 77, 77, 79, 79, 79, 79, 76, 76, 76, 76, 74, 74, 72, 72]),
        creator.Individual([67, 67, 64, 64, 64, 62, 64, 64, 0, 0, 64, 64, 62, 62, 65, 65, 64, 64, 64, 65, 65, 65, 67, 67, 67, 67, 0, 0, 65, 65, 65, 65, 67, 67, 64, 64, 64, 62, 64, 64, 0, 0, 65, 65, 64, 64, 60, 60, 59, 59, 59, 64, 64, 64, 68, 68, 68, 68, 68, 68, 66, 66, 68, 68]),
        creator.Individual([79, 79, 79, 79, 74, 74, 77, 77, 77, 77, 77, 77, 74, 74, 77, 77, 79, 79, 79, 79, 77, 77, 74, 74, 72, 72, 72, 70, 72, 72, 74, 74, 70, 70, 70, 70, 67, 67, 69, 69, 72, 72, 72, 72, 72, 72, 74, 74, 77, 77, 74, 74, 72, 72, 70, 70, 72, 72, 72, 72, 72, 72, 70, 70])]
    fits = toolbox.map(toolbox.evaluate, population)
    for fit, ind in zip(fits, population):
        ind.fitness.values = fit

    # 运行遗传算法
    for gen in range(GEN_NUM):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(population + offspring, k=GEN_SIZE)

    # 输出最优旋律
    best = tools.selBest(population, k=1)[0]
    print("Best melody:", best)
    print("Best value:", evaluate(best)[0])
    ConvertToMidi("song.mid", best)