---
title: 4_CPA
date: 2026-08-02 23:12:30
tags:
  - cw_experiment
  - CPA
  - 侧信道攻击
categories:
  - 密码学
---
# CPA

## Hamming Weight
比特串中1的个数即为该串的汉明重量(Hamming Weight,HW),python代码可以很容易实现:
```python
def calc_hamming_weight(n):
    return bin(n).count("1")
```
为什么认为汉明重量与能量消耗有关?这是因为微控制器的能量消耗与其内部的数据操作有关,即越多的数据操作(越多位的翻转)，对应的能量消耗就越大。因此可以认为，数据中'1'的个数(即汉明重量)与能量消耗之间必然有一定关系。

## 定位Sbox
首要目标是定位Sbox发生在哪个位置,即在能量迹trace中定位发生Sbox操作的地方,直接采集输入明文第一字节(bnum = 0)过Sbox后的汉明重量,将其绘制成图,代码如下:
```python
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import brewer

output_notebook()
p = figure()

plot_start = 0
plot_end = 2000
xrange = list(range(len(trace_array[0]))[plot_start:plot_end])
bnum = 0
color_mapper = brewer['PRGn'][9]

for tnum in range(len(trace_array)):
    hw_of_byte = HW[aes_internal(textin_array[tnum][bnum], key[bnum])]
    p.line(xrange, trace_array[tnum][plot_start:plot_end], line_color=color_mapper[hw_of_byte])
show(p)
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/origin_hw.png)

从中并不能得到什么有效信息,因为与Sbox操作输入部分的能量消耗实在是太小了,难以辨认,一个自然的想法就是平均化,去除噪音后再绘图,就能更有有效地定位Sbox操作的位置。具体而言:
 - 分别对所有输入明文的第一字节输出结果(aes_internal(textin_array[idx][bnum],key[bnum]))计算汉明重量,将其归类到对应的组中(输出一个字节,汉明重量至多0~8共9种)
 - 分别计算每组汉明重量的trace的平均值。
 - 分别计算所有trace(在相同sampling点上的)平均值$ave\_trace$.
 - 绘制图其横坐标为sampling点,纵坐标为**各汉明重量对应trace与$ave\_trace$的差值**(显然一张图上有9条线,对应9种不同的汉明重量)
  
具体代码如下:
```python

output_notebook()
p = figure()
# 计算所有traces的均值
import numpy as np
hw_groups = [[],[],[],[],[],[],[],[],[]] # 用来收集9种hamming weight 的trace
for idx in range(len(trace_array)):
    hw_of_byte = HW[aes_internal(textin_array[idx][bnum], key[bnum])]
    hw_groups[hw_of_byte].append(trace_array[idx])

hw_averages = []
for hw in range(9):
    if len(hw_groups[hw]) == 0:
        # 空组用零向量占位（形状与一条轨迹相同）
        hw_averages.append(np.zeros(len(trace_array[0])))
    else:
        hw_averages.append(np.average(hw_groups[hw], axis=0))
hw_averages = np.array(hw_averages) 
avg_trace = np.average(hw_averages,axis = 0)
xrange = np.arange(len(trace_array[0]))[plot_start:plot_end]
color_mapper = brewer['PRGn'][9]
for hw in range(9):  
    p.line(xrange, (hw_averages[hw]-avg_trace)[plot_start:plot_end], line_color=color_mapper[hw])

p.output_backend = "svg"
show(p)
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/hw_ave_diff.svg)
这里能很明显看出不同汉明重量下的差异,我们认为某汉明重量对应trace与整体平均值$ave\_trace$差值最大的地方即Sbox操作的位置(因为此位置的巨大差异来自Sbox操作而非其他的如噪声等),具体位置如下:
```python
sbox_loc = np.argmax(abs(hw_averages[0]-avg_trace))
```
现在我们可以绘制汉明重量与平均能量消耗之间的关系图了，代码如下:
```python
output_notebook()
p = figure(title="HW vs Voltage Measurement")
p.line(list(range(0, 9)), abs(hw_averages[:,sbox_loc]), line_color="red")
p.xaxis.axis_label = "Hamming Weight of Intermediate Value"
p.yaxis.axis_label = "Average Value of Measurement"
p.output_backend = "svg"
show(p)
```
注意这里对hw_average取了绝对值，因为原始测量出来的值可能是如电压降等的负值，原值没有特殊含义，但能表示能量消耗关系等。具体图形如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/HW_Power.svg)
可以看到的确大致呈线性关信息，汉明重量为8时的能量消耗大约为1时的8倍。

## 相关性
对于长度为$N$的随机变量$X、Y$,均值分别为$\bar X、\bar Y$，则两个二随机变量的相关系数为:
$$ 
r = \frac{cov (X,Y)}{\sigma_X \sigma_Y}
$$
$cov(X,Y)$是$X$与$Y$的协方差，计算方法为:

$$
cov(X,Y) = \sum_{n=1}^N [(Y_n - \bar Y)(X_n - \bar X)]
$$
$\sigma_X$和$sigma_Y$分别是$X、Y$的标准差，计算方法如下:
$$\
\sigma_X = \sqrt{\sum_{n=1}^{N}(X_n - \bar X)^2}
$$
python代码实现上述部分可以使用numpy库，将复杂计算简化为一个一个的简单模块，参考代码如下:
```python
def mean(X):
    return np.sum(X,axis = 0) / len(X)

def std_dev(X, X_bar):
    return np.sqrt(np.sum((X - X_bar)**2,axis = 0))

def cov(X, X_bar, Y, Y_bar):
    return np.sum((X - X_bar)*(Y - Y_bar),axis = 0)
```

## 相关攻击
现在我们已经收集到了用$sk$加密过程的50条trace(CPA比DPA用到的trace少得多)，计算这些trace的平均汉明重量，再遍历所有可能$sk$(这里先恢复第一字节，即共256种可能)，将输入的明文与猜测的密钥重新加密计算输出结果的平均汉明重量，两个平均汉明重量求相关性，认为最大相关性即真实密钥。代码实现如下:
```python
maxcpa = [0] * 256
t_bar = mean(trace_array) 
o_t = std_dev(trace_array, t_bar)

for kguess in trange(0, 256):
    hws = np.array([[HW[aes_internal(textin[0],kguess)] for textin in textin_array]]).transpose()
    hws_bar = mean(hws)
    hws_t = std_dev(hws,hws_bar)
    correlation = cov(trace_array,t_bar,hws,hws_bar)
    cpaoutput = correlation / (o_t * hws_t)
    maxcpa[kguess] = max(np.abs(cpaoutput)) 

guess = np.argmax(maxcpa)
guess_corr = maxcpa[guess]
print("Key guess: ", hex(guess))
print("Correlation: ", guess_corr)
```
运行结果为：
```
Key guess:  0x2b
Correlation:  0.6971778130438376
```
这恰好为AES测试基准中密钥的第一字节，说明CPA攻击成功(有时correlation最大的反而不是真实密钥，但一般而言真实密钥的相关性是比较高的，不是最高也一般在top5中)。

## 完整密钥恢复
- 上述为密钥一个字节的恢复，我们将其扩展至完整16个字节的密钥，即对第一字节求最大相关性的可能密钥改为对所有16个字节做相同操作，代码如下：
```python
t_bar = np.sum(trace_array, axis=0)/len(trace_array)
o_t = np.sqrt(np.sum((trace_array - t_bar)**2, axis=0))

cparefs = [0] * 16 
bestguess = [0] * 16 

for bnum in trange(0, 16):
    maxcpa = [0] * 256
    for kguess in range(0, 256):
        hws = np.array([[HW[aes_internal(textin[bnum],kguess)] for textin in textin_array]]).transpose()
        hws_t = std_dev(hws,hws_bar)
        correlation = cov(trace_array,t_bar,hws,hws_bar)
        cpaoutput = correlation / (o_t * hws_t)
        maxcpa[kguess] = max(np.abs(cpaoutput))
    bestguess[bnum] = np.argmax(maxcpa)
    cparefs[bnum] = maxcpa[np.argmax(maxcpa)]
print("Best Key Guess: ", end="")
bestguesslst  = [f"{a:02x}" for a in bestguess]
print(bestguesslst)
print()
real_key = [f"{a:02x}" for a in key] 
print(f"Real secret key:{real_key}") # 打印实际使用的密钥做对比

# 做一下结果对比评价:
match = 0
for i in range(16):
    if(bestguesslst[i] == real_key[i]):
        match += 1
print(f"Attack success for {match} bytes,failed for {16 - match} bytes")

print("\n", cparefs)
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/CPA_full_key_recovery.png)
正如前面所说，并不能完整恢复16个密钥，有不少字节其实是恢复错误的，但的确能恢复部分$sk$字节。

- 上述相关系数计算还有一个更高效的累计计算版本：
$$
r_{i,j} = \frac{D \sum_{d=1}^D h_{d,i}t_{d,j} - \sum_{d=1}^D h_{d,i} \sum_{d=1}^D t_{d,j}}{\sqrt{\left(D \sum_{d=1}^D h_{d,i}^2 - (\sum_{d=1}^D h_{d,i})^2\right) \left(D \sum_{d=1}^D t_{d,j}^2 - (\sum_{d=1}^D t_{d,j})^2\right)}}
$$
  对比一般的计算方式：
  $$r = \frac{\sum_{d=1}^{D} (h_d - \bar{h})(t_d - \bar{t})}{\sqrt{\sum_{d=1}^{D} (h_d - \bar{h})^2 \sum_{d=1}^{D} (t_d - \bar{t})^2}}$$
这里的更高效/累计计算/online版的相关系数计算方法，实际上是将一般方法计算的给拆开：
  - 对分子：
$$
\begin{aligned} \sum_{d=1}^{D} (h_d - \bar{h})(t_d - \bar{t}) &= \sum_{d=1}^{D} (h_d t_d - h_d \bar{t} - t_d \bar{h} + \bar{h}\bar{t}) \\ &= \sum_{d=1}^{D} h_d t_d - \bar{t} \sum_{d=1}^{D} h_d - \bar{h} \sum_{d=1}^{D} t_d + D \bar{h}\bar{t} \end{aligned}
$$
带入均值的定义$\bar{h} = \frac{\sum h}{D}$和$\bar{t} = \frac{\sum t}{D}$，得到：
$$
\sum_{d=1}^{D} (h_d - \bar{h})(t_d - \bar{t}) = \sum h t - \frac{(\sum h)(\sum t)}{D}
$$
  - 同理分母可以展开成：
  $$
  \sum_{d=1}^{D} (h_d - \bar{h})^2 = \sum h^2 - \frac{(\sum h)^2}{D}
  $$
  - 分子与分母同时乘以$D$，得到在线计算形式：
  $$
  r_{i,j} = \frac{D \sum_{d=1}^D h_{d,i}t_{d,j} - \sum_{d=1}^D h_{d,i} \sum_{d=1}^D t_{d,j}}{\sqrt{\left(D \sum_{d=1}^D h_{d,i}^2 - (\sum_{d=1}^D h_{d,i})^2\right) \left(D \sum_{d=1}^D t_{d,j}^2 - (\sum_{d=1}^D t_{d,j})^2\right)}}
  $$
   
   这样实现的高效性体现在我们实际计算时只需要维护5个累加器：
| 累加器变量 | 符号 | 矩阵维度 | 含义 |
|------------|------|----------|------|
| sum_t | $\sum t_{d,j}$ | (num_points,) | 所有波形在各个采样点上的电压和 |
| sum_t2 | $\sum t_{d,j}^2$ | (num_points,) | 所有波形在各个采样点上的电压平方和 |
| sum_h | $\sum h_{d,i}$ | (256,) | 256 个猜测密钥在所有明文下的假设功耗和 |
| sum_h2 | $\sum h_{d,i}^2$ | (256,) | 256 个猜测密钥在所有明文下的假设功耗平方和 |
| sum_ht | $\sum h_{d,i} t_{d,j}$ | (256, num_points) | 假设功耗与实际波形的交叉乘积和 |

当新产生一条波形后，数据更新过程如下：
$$
\begin{aligned} D_{new} &= D_{old} + 1 \\ \text{sum\_t} &\leftarrow \text{sum\_t} + t_{new} \\ \text{sum\_t2} &\leftarrow \text{sum\_t2} + t_{new}^2 \\ \text{sum\_h} &\leftarrow \text{sum\_h} + h_{new} \\ \text{sum\_h2} &\leftarrow \text{sum\_h2} + h_{new}^2 \\ \text{sum\_ht} &\leftarrow \text{sum\_ht} + h_{new}^T \cdot t_{new} \end{aligned}
$$
更新完累加器后带入上述公式即可很快计算出结果(实际ChipWhisperer中使用的就是这种累加计算方法)。

让AI写的一个对应代码如下:
```python
import numpy as np
from tqdm import trange

D = len(trace_array)  # Trace 的总数量 (对应公式中的 D)
num_points = trace_array.shape[1]  # 每条 Trace 的采样点数

# 1. 预先计算与 Trace 相关的累加量 (针对 t_d,j)
sum_t = np.sum(trace_array, axis=0)  # sum(t_d,j), 形状: (num_points,)
sum_t2 = np.sum(trace_array**2, axis=0)  # sum(t_d,j^2), 形状: (num_points,)

cparefs = [0] * 16
bestguess = [0] * 16

for bnum in trange(0, 16):
    # 2. 构建当前字节下所有 256 个密钥猜测的假设功耗矩阵 h，形状为 (D, 256)
    h = np.array(
        [
            [HW[aes_internal(textin[bnum], kguess)] for kguess in range(256)]
            for textin in textin_array
        ]
    )

    # 3. 计算与假设功耗 h 相关的累加量
    sum_h = np.sum(h, axis=0)  # sum(h_d,i), 形状: (256,)
    sum_h2 = np.sum(h**2, axis=0)  # sum(h_d,i^2), 形状: (256,)

    # 4. 计算交叉项 sum(h_d,i * t_d,j)
    # 通过矩阵乘法 h.T @ trace_array 快速完成, 形状: (256, num_points)
    sum_ht = np.dot(h.T, trace_array)

    # 5. 根据图中在线相关系数公式 r_i,j 进行计算
    # 分子: D * sum(h*t) - sum(h) * sum(t)
    numerator = D * sum_ht - np.outer(sum_h, sum_t)

    # 分母项展开: (D * sum(h^2) - (sum(h))^2) 和 (D * sum(t^2) - (sum(t))^2)
    denom_h = D * sum_h2 - sum_h**2
    denom_t = D * sum_t2 - sum_t**2

    # 构建分母矩阵并进行数值安全处理（避免除以零）
    denom_matrix = np.outer(denom_h, denom_t)
    denom_matrix[denom_matrix <= 0] = np.inf

    denominator = np.sqrt(denom_matrix)

    # 计算最终的相关系数矩阵 r_i,j, 形状: (256, num_points)
    cpaoutput = numerator / denominator

    # 6. 获取每个密钥猜测的最大相关系数绝对值
    maxcpa = np.max(
        np.abs(cpaoutput), axis=1
    )  # 每个密钥猜测在所有时间点上的最大相关系数
    bestguess[bnum] = np.argmax(maxcpa)
    cparefs[bnum] = maxcpa[bestguess[bnum]]

# 打印结果与评价
print("Best Key Guess: ", end="")
bestguesslst = [f"{a:02x}" for a in bestguess]
print(bestguesslst)
print()

real_key = [f"{a:02x}" for a in key]
print(f"Real secret key:{real_key}")

match = sum(1 for i in range(16) if bestguesslst[i] == real_key[i])
print(f"Attack success for {match} bytes, failed for {16 - match} bytes")
print("\nMax correlation per byte:", cparefs)
```
运行产生相同结果。

## ChipWhisperer Analyzer
- 使用ChipWhisperer Analyzer自带的功能可以实现对traces的高效自动化攻击。
- 打开保存的trace文件、配置攻击模型和参数如下:
```python
import chipwhisperer.analyzer as cwa
leak_model = cwa.leakage_models.sbox_output
attack = cwa.cpa(proj, leak_model)
```
- 攻击时可以调用回调函数(可以自己手动编写，也可以调用官方封装好的)实现计算的相关系数随处理Trace数量增加而动态变化的过程。
如下所示的官方封装回调：
```python
import chipwhisperer as cw
cb = cwa.get_jupyter_callback(attack)
results = attack.run(cb, 10)
```
结果如下图，标红的是真实密钥字节
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/CPA_autorun.png)
可以看到如我们之前手动计算的一样，部分比特能正确恢复，部分比特并未正确恢复但依然有较高的相关性。

### PGE
- PGE(Partial Guess Entropy)即据部猜测熵，是指正确密钥在所有候选你密钥中的排名偏移量(从0开始计数)。以AES-128的某一密钥字节为例，单密钥字节有256中可能，在CPA攻击中分别计算这256个猜测密钥对应的相关系数，并将这256个相关系数从大到小排名。如果正确密钥的相关系数最高，排名第0位(即前面有0个错误猜测比它高)则PGE = 0,代表攻击成功。如果有7个错误猜测的相关系数比正确密钥还要高，则正确密钥排名第8位，此时PGE = 7。

  这里绘制PGE随所处理的Trace数量变化的代码如下:
```python
ret = plot_data.pge_vs_trace(0)
curve = hv.Curve((ret[0],ret[1]), "Traces Used in Calculation", "Partial Guessing Entrop of Byte")
for bnum in range(1, 16):
    ret = plot_data.pge_vs_trace(bnum)
    curve *= hv.Curve((ret[0],ret[1])).opts(color=byte_to_color(bnum))
curve.opts(width=900, height=600)
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/PGE.png)
  大体而言PGE呈随着处理的Trace数量而下降的趋势(很自然的，处理的trace越多，结果越准确)。

 - 作用：
    - PGE可以用来衡量攻击的效率，可以用来帮助确定恢复密钥所需要的最少trace数量，即PGE首次稳定收敛在0的数量(比如上述图中虽然采集了50条trace,但有些密钥比特使用不到50条trace即可确定出正确的密钥比特(即PGE = 0)了)。
    - 评估防护机制，比如芯片加了掩码操作，则PGE可能下降非常缓慢甚至一直居高不下，这就说明防护机制有效。

### Correlation vs Traces
- 绘制相关系数随着处理trace数量的变化，这里的相关系数分为256个可能的密钥字节中中确的那一个和剩下的255个错误的中相关系数最大的那一个。即共16条错误密钥字节的黑线和16条正确密钥字节的彩线，代码如下:
```python
a = []
b = []
for bnum in range(0, 16):
    data = plot_data.corr_vs_trace(bnum)
    best = [0] * len(data[1][0])
    for i in range(256):
        if i == key[bnum]:
            a.append(np.array(data[1][i]))
        else:
            if max(best) < max(data[1][i]): best = data[1][i]
    b.append(np.array(best))

pda = pd.DataFrame(a).transpose().rename(str, axis='columns')
pdb = pd.DataFrame(b).transpose().rename(str, axis='columns')
curve = hv.Curve(pdb['0'].tolist(), "Iteration Number", "Max Correlation").options(color='black')
for i in range(1,len(pdb.columns)):
    curve *= hv.Curve(pdb[str(i)]).options(color='black')
    
for i in range(len(pda.columns)):
    curve *= hv.Curve(pda[str(i)]).options(color=byte_to_color(i))
            
curve.opts(width=900, height=600)
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/correlation_vs_trace.png)
可以看到，在一开始由于处理的trace数量极少，由于噪声等原因导致所有密钥字节的相关系数都比较高，甚至错误的黑色线一度在彩色线之上。随着处理的trace数量的增加，错误密钥字节的相关系数很快就下降了，而正确密钥字节的相关系数依然保持较高水平，最终与黑色线形成巨大差异，能被轻易区分开(并不是所有彩色线都是这样)，进而能识别出正确的密钥字节了。
