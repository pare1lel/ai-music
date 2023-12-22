import random
from deap import base, creator, tools, algorithms

# 定义旋律的范围和长度
MELODY_MIN = 53
MELODY_MAX = 79
MELODY_LENGTH = 64

# 定义遗传算法的参数
GEN_SIZE = 200
GEN_NUM = 400

# 定义适应度函数 - TODO
harmony = [1.0,0.0,0.25,0.5,0.5,1.0,0.0,1.0,0.5,0.5,0.25,0.0,1.0]
def evaluate(melody):
    intervals = []
    lst = 0
    for i in range(MELODY_LENGTH):
        if melody[i] > 0 and melody[i] != lst:
            dif = abs(melody[i] - lst)
            intervals.append(harmony[dif] if dif <= 12 else 0)
            lst = melody[i]
    return sum(intervals) / len(intervals),

# 定义变异算子 - 包括移调, 倒影, 逆行
def mutate(melody):
    choose = random.random()
    if choose < 0.25:   # 变异
        for i in range(MELODY_LENGTH):
            if random.random() < 0.1:
                melody[i] = random.choice([0] + list(range(MELODY_MIN, MELODY_MAX + 1)))
            elif random.random() < 0.1:
                melody[i] = melody[i - 1]
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

# 创建适应度类和个体类
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# 注册遗传算子
toolbox = base.Toolbox()
toolbox.register("note", random.randint, MELODY_MIN, MELODY_MAX)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.note, n=MELODY_LENGTH)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selBest)

# 设置初始种群
population = toolbox.population(n=GEN_SIZE)

# 运行遗传算法
for gen in range(GEN_NUM):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.15)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(population + offspring, k=GEN_SIZE)

# 输出最优旋律
best = tools.selBest(population, k=1)[0]
print("Best melody:", best)
print("Best value:", evaluate(best)[0])