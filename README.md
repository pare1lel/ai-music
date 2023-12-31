# 实验报告 - 探索遗传算法在机器作曲中的应用

小组成员：陈东武、胡宇阳、黄培钧、吕敬一、张佳豪、韩潇

利用计算机生成音乐旋律是未来机器学习和音乐创作的重要关注热点. 我们小组以机器学习中经典的遗传算法为基础，结合简单的神经网络结构，通过自行收集训练数据和初始种群，对机器作曲进行了简单的探究.

# 实现思路
实现的主要考量在于旋律的表示, 以及适应度函数的选取.

旋律的表示需要利于遗传算法的实现, 我们的表示方法使得交叉和变异操作都比较容易实现.

适应度函数的选取主要有两种思路:

- 直接由人类指定一个特定的计算方法.
- 直接训练一个神经网络, 输入旋律片段, 拟合适应度函数.

我们认为这两种方法都有些极端：一方面，一段旋律是否好听很难用一些简单直观的指标直接衡量，人工设计适应度函数并分配指标的权重较为困难；另一方面，旋律片段的信息较为抽象, 要训练出好的模型需要大量数据和大规模的模型, 我们没有这样的条件. 因此，我们采取了折中策略：先通过人类智慧提取一些指标, 再在此基础上训练一个小的全连接神经网络, 得到最终的适应度值.

## 旋律的表示
对于 $4$ 个小节的乐曲片段，将每一个音分切为 $16$ 分音符，使用长为 $64$ 的整数列 $(a_0 , a_1,\ldots, a_{63})$ 表表示旋律片段, $0$ 表示休止符, 正整数表示固定音高 ($60$ 表示 $\mathrm C_4$, 相邻整数相差一个半音, 音级的范围从 $\mathrm F_3$ 到 $\mathrm G_5$), 每个相同音高的连续段表示一个音符.

## 初始种群
选取了 $10$ 首乐曲，在每个乐曲中选取 $4$ 个小节，将每一个小节通过移调变换转换为C大调，形成了 $10$ 个初始种群，即 $10$ 个长为 $64$ 的数组.

## 遗传算法
我们使用 python 的 DEAP 库实现遗传算法, 
- 交叉操作是 `cxTwoPoint`, 取出父本和母本的一段区间进行交换, 得到新的两段旋律.
- 变异操作有随机替换, 移调, 倒影, 逆行共四种, 每次对每段旋律分别以特定概率进行一种操作.
- 使用 DEAP 库的 `varAnd` 算法生成子代, 具体实现参见^[2]^, 简单来说就是随机地进行交叉, 然后随机地进行变异.
- 最后选取父代和子代中适应度值较大的一些存活, 作为新的子代.

## 特征提取
对于一段旋律 $(a_0, a_1, \cdots, a_{63})$，我们使用了许多指标 (sub_raters) 对音列的特征进行提取，有以下的几种 sub_raters:
（特征提取的设计思路部分参考自^[3]^）
- **调外音**
    方便起见，我们将在C大调上生成旋律，因此需要指标衡量非C大调的音符的数量的占比，若占比过高则不认为是一段好的旋律. 
- **音程转移分布**
    我们认为相邻两个音程是决定听感的重要因素. 对于旋律中相邻两个音符构成的音程，我们将其分为四类，一类是超过 $19$ 个半音的“大跳”音程，另外三类是根据音程和谐程度映射成 $0, 1, 2$ 三档. 对于两个相邻的音程 $T, S$, 如果 $T, S$ 中有大跳，则记为“大跳转移”，否则记为$\{0, 1, 2\}^2$ 中的一个. 如此我们将相邻的音程分为 $10$ 类，最终返回每一类的出现频率. 如果相邻的两个音中有一个是休止符则不构成有效音程，我们将其忽略. 
- **稳定程度**
    如果相邻的两个音程分别为上行和下行，则我们将其称为一个“转折”. 转折的幅度和频率是决定听感的重要因素. 对于相邻两个音程 $T_i=a_{i + 1} - a_{i}, T_{i + 1} = a_{i + 2} - a_{i + 1}$，如果 $T_i T_{i + 1} < 0$，则定义其转折程度为 $|T_i - T_{i + 1}|$，否则其转折程度为 $0$. 最后旋律的稳定指标定义为所有相邻音程的转折程度之和，除去归一化系数 $\sum (|T_i| + |T_{i + 1}|)$.
- **连续音符密度**
    如果我们将相邻的相同音符视为一个连续段（在原始的音乐中，它们可能是一个完整的长音），则连续段的密度对听感影响很大. 我们将连续段的数量除以 $64$ 作为衡量指标. 
- **音乐密度变化量**
    一段好的节奏除了音符密度要适中以外，它的节奏也不应是一成不变的；而是应该有一定的变化. 于是我们加入了音乐密度变化量这一指标：把每段四小节的旋律平均分为8块，计算每块中有多少个连续段的结尾，将数量最少的块除以数量最多的块作为指标，用于衡量节奏的变化程度. 
- **跨拍音**
    跨越不同拍子的连续段会给音乐带来特殊的听感（例如连续的切分音）. 我们将跨拍音指标定义为跨拍连续段占总连续段数量的比例. 
- **音列极差**
    好听的乐曲应当具有适中的音域范围. 我们取极差 $\max(a_i)-\min(a_i)$ 为对应的特征指标. 
- **沉默时间**
    好听的乐曲应当具有恰当的休止安排. 取最长的连续休止符长度占总长度之比作为对应的特征指标. 
- **音符个数**
    不同的音符种类数量对音乐总体的听感色彩有较大影响，我们将“样本中出现的不同音符种类数量”作为对应的衡量指标. 除去一个较大的常数以进行归一化. 

我们将**除了调外音以外的**所有指标连接成一个特征列表，输入神经网络进行训练和推断. 

## 数列向midi的转换
我们使用 python 的 mido 库和 pygame 库，使用内置的 MidiTrack 函数创建音符数组，再向数组中插入数字来形成 midi 文件，使用 pygame 库播放 midi 文件. 

## midi向数列的转换
我们使用 python 的 music21 库对 midi 文件进行处理，提取出其中的音符和空拍，并转换为数列. 

## 神经网络
- 数据收集：从网络上选取音乐的 midi 文件片段，将其转换为本实验中用于表示音乐片段的数组，并播放这一片段，人工对其旋律的好坏进行打分（评分最低为0，最高为1）
- 神经网络结构：最基础的全连接神经网络，输入层大小为 $17$（特征列表的长度），设置了一层大小为 $8$ 的隐藏层，输出评分值. 
- 输入：将每个歌曲片段生成的特征列表及其评分作为训练数据，训练神经网络. 

## 适应度函数

对于任意旋律个体，我们首先调用一系列 sub_rater 生成特征列表，输入神经网络，获得一个 $[0, 1]$ 的实数 $r$，与适应度正相关. 我们还可获取神经网络推断中未使用的调外音指标 $z$. 由此我们定义该个体的适应度 $\mathrm{fitness} = 4r + \ln(1 - 0.8\cdot z)$，此处的系数是可调的常数，决定了调外音对总体适应度的影响程度. 

# 实验结果

我们训练的模型数据、代码以及生成的音乐（格式为`.mid`）已经一并提交. 为查看方便，此处是生成结果的五线谱：

<div>			<!--块级封装-->
    <center>	<!--将图片和文字居中-->
    <img src="https://hackmd.io/_uploads/r1dQHZPD6.png"
         alt="无法显示图片时显示的文字"
         style="zoom:0.34"/>
    <br>		<!--换行-->
    </center>
</div>

<div>			<!--块级封装-->
    <center>	<!--将图片和文字居中-->
    <img src="https://hackmd.io/_uploads/B1UrB-wwp.png"
         alt="无法显示图片时显示的文字"
         style="zoom:2"/>
    <br>		<!--换行-->
    </center>
</div>

对其他文件说明如下：

- `midi_data` 和 `midi_data_new` 是从公开资源站下载的音乐.
- `select_midi.py` 和 `midi_to_list.py` 从 midi 文件中提取片段, 交由人类打分, 生成训练数据.
- `sub_rater.py` 定义了各种 sub_rater 的计算函数.
- `nn_newrater.py` 通过 `output-all.csv` 中的数据集训练神经网络, 将模型存入 `model.dat`.
- `main.py` 是实现遗传算法的主程序, 读取 `model.dat` 中的模型用于适应度函数, 将生成的最优旋律存入 `song.mid`.

## 结果分析

我们重点分析了不同的适应度函数对成品品质的影响. 
适应度函数的特性主要由神经网络训练中的参数决定，可调的参数有以下这几个:

- 遗传算法中一个种群的个体数量与进化次数: 个体数量与进化次数越多, 算法就需要运行更长时间, 但可以找出适应度更高的旋律. 经过实验, 我们发现当适应度足够高时, 再提高适应度很可能不会得到更好的旋律, 所以我们选取个体数量为 $200$, 进化次数为 $100$.
- 神经网络的隐藏层大小与训练轮数: 隐藏层大小与训练轮数越多, 神经网络在训练数据上的误差就越小, 但隐藏层太大会导致遗传算法运行太长时间, 而且由于训练数据较少, 过度训练会导致过拟合, 从而表现出非预期的偏好. 如果遗传算法给出适应度值很高但非常怪异的旋律, 就说明出现了过拟合, 所以我们选取隐藏层大小为 $8$, 训练次数为 $1000$.
- 遗传算法中调外音指标所占的比重: 比重越大, 生成的调外音就越少. 经过实验, 我们发现算法生成的旋律中的调外音一般比较难听, 所以我们调整系数使得最终旋律中几乎不出现调外音.

## 反思与展望

- 我们目前使用遗传算法与神经网络结合的方法，这种方法较为迂回，只要其中一个模型没有训练好，就会导致结果没有达到预期. 可以使用 diffusion model[4] 等更大型的模型直接生成音乐，如 suno.ai[5] 和 stable audio[6] 等音乐生成网站都使用了这个模型. 
- 我们的训练数据依赖手工收集, 听辨和处理, 并且每条数据也需要我们进行人工打分, 导致了我们的数据集容量不够大, 无法涵盖一种风格的很多优秀作品, 导致生成质量可能受到一定影响. 我们后续可以发展用脚本进行自动化收集, 以及构建不同指标(如: 生成结果与优秀作品的相似度)来进行自动化的评分, 这样可以增大数据集的规模, 以期生成更优秀的结果.

# 组员分工

- 查找文献：陈东武
- 初始种群的选取：吕敬一
- 阅读文献：黄培钧，吕敬一
- 讨论模型的构建：全体组员
- 遗传算法实现：陈东武
- 适应度函数的实现：吕敬一
- 数列与声音互相转换：张佳豪
- 数据的评价：陈东武，张佳豪，胡宇阳
- 神经网络的搭建：黄培钧，韩潇
- 运行程序：黄培钧，韩潇
- 写报告：全体组员

# 参考文献
[1]A genetic algorithm for composing music,Dragan Matić,https://www.researchgate.net/publication/47394069_A_genetic_algorithm_for_composing_music
[2]Deap 1.4.1 documentation,https://deap.readthedocs.io/en/master/api/algo.html#deap.algorithms.varAnd
[3]Anderling V, Andreasson O, Olsson C, et al. Generation of music through Genetic Algorithms[J]. Goteborg, Sweden: Chalmers University of Technology, 2014.
[4]Levy M, Di Giorgi B, Weers F, et al. Controllable Music Production with Diffusion Models and Guidance Gradients[J]. arXiv preprint arXiv:2311.00613, 2023.
[5]https://www.suno.ai/
[6]https://stability.ai/stable-audio