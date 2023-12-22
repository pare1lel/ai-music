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
            if dif <= 12:
                intervals.append(harmony[dif])
            lst = melody[i]
    return sum(intervals) / len(intervals),

# 定义变异算子 - 包括移调, 倒影, 逆行

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
toolbox.register("mutate", tools.mutUniformInt, low=MELODY_MIN, up=MELODY_MAX, indpb=0.1)
toolbox.register("select", tools.selBest)

# 设置初始种群
population = toolbox.population(n=GEN_SIZE)

# 运行遗传算法
for gen in range(GEN_NUM):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(population + offspring, k=GEN_SIZE)

# 输出最优旋律
best = tools.selBest(population, k=1)[0]
print("Best melody:", best)
print("Best value:", evaluate(best)[0])