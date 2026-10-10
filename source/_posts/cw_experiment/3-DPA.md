---
title: 3-DPA
date: 2026-08-08 17:16:13
tags:
  - cw_experiment
  - DPA
  - 侧信道攻击
categories:
  - 密码学
---
# DPA

## 能量消耗与数据的关系

- 我们认为微控制器运行时的能量消耗与所操作的数据有关，本实验采集100条随机输入明文加密过程的能量消耗(trace)，其中我们只关注输入明文的第一字节，将其特殊化处理:该字节的第0比特为0则将这一字节置为$\text{0x00}$，否则置为$\text{0xFF}$(由于消息是随机的，因此输入消息的第一字节的第0比特是0和1的概率应当是相等的均为1/2，也就是说处理后输入的数据的第一字节是全0和全1的概率是相等的均为1/2)。
- 将收集到的100条trace可以按照输入明文的第一字节不同分为两类:$\text{zero\_list}$和$\text{one\_list}$。
- 分别计算两类trace的能量消耗(在相同时间点/采样点)的均值并作差，将差值的绝对值作为纵坐标，采样点为横坐标，绘制能量消耗差异分布图。
具体代码如下:
```python
from tqdm.notebook import trange
import numpy as np
import time

ktp = cw.ktp.Basic()
trace_array = []
textin_array = []

key, text = ktp.next()

target.set_key(key)

N = 100
for i in trange(N, desc='Capturing traces'):
    scope.arm()
    if text[0] & 0x01:
        text[0] = 0xff
    else:
        text[0] = 0x00
    target.simpleserial_write('p', text)
    ret = scope.capture()
    if ret:
        print("Target timed out!")
        continue
    
    response = target.simpleserial_read('r', 16)
    trace_array.append(scope.get_last_trace())
    textin_array.append(text)
    
    key, text = ktp.next() 

# 分类
one_list , zero_list = [],[]
for i in range(len(trace_array)):
    if textin_array[i][0] == 0x00:
        zero_list.append(trace_array[i])
    else:
        one_list.append(trace_array[i])
print(f"the len of one_list:{len(one_list)}")
print(f"the len of zero_list:{len(zero_list)}")

import numpy as np
one_avg,zero_avg = np.mean(one_list,0),np.mean(zero_list,0) # 算均值
difference = zero_avg - one_avg 

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 5))
plt.plot(np.abs(difference)) # 标准差绘图
plt.xlabel("Samples")
plt.ylabel("Difference of Average Power")
plt.title("Differential Power Trace (0xFF - 0x00)")
plt.grid(True)
plt.show()
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/DPA_ff_00.png)
可以看到在接近采样点的开头部分出现了明显的高峰,这说明在加密处理的第一字节处，处理的是$\text{0x00}$还是$\text{0xFF}$是会造成很大的能量消耗差异的，验证了我们的想法。

- 事实上，可以对上述参数做一些修改，进一步得到更多样的结果:
    
    - 将原来的1个字节的差异扩展到4字节,代码如下:
```python
# 1,multiple bytes to 0x00 and 0xff
from tqdm.notebook import trange
import numpy as np
import time

ktp = cw.ktp.Basic()
trace_array = []
textin_array = []

key, text = ktp.next()

target.set_key(key)

N = 100
for i in trange(N, desc='Capturing traces'):
    scope.arm()
    if text[0] & 0x01:
        text[0:4] = [0xFF]*4 # 第一字节是1就前四字节都是1
    else:
        text[0:4] = [0x00]*4 # 反之前四字节都是0
    target.simpleserial_write('p', text)
    
    ret = scope.capture()
    if ret:
        print("Target timed out!")
        continue
    
    response = target.simpleserial_read('r', 16)
    
    trace_array.append(scope.get_last_trace())
    textin_array.append(text.copy())
    
    key, text = ktp.next() 

# 依然可以根据第一字节来归类
one_list , zero_list = [],[]
for i in range(len(trace_array)):
    if textin_array[i][0] == 0x00:
        zero_list.append(trace_array[i])
    else:
        one_list.append(trace_array[i])
print(f"the len of one_list:{len(one_list)}")
print(f"the len of zero_list:{len(zero_list)}")
import numpy as np
one_avg,zero_avg = np.mean(one_list,0),np.mean(zero_list,0)
difference = zero_avg - one_avg 
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 5))

plt.plot(np.abs(difference))

plt.xlabel("Samples")
plt.ylabel("Difference of Average Power")
plt.title("Differential Power Trace (4 bytes 0xFF - 0x00)")

plt.grid(True)
plt.savefig('DPA_4bytes_diff',dpi = 300,bbox_inches='tight')
plt.show()
```
结果如下图:
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/DPA_4bytes_diff.png)
  可以看到，相较于之前的只有明文一个字节的差异，这里扩展到前4字节。相比之下原来仅有一个明显的高峰，现在这里能看到大约4个明显的高峰，进一步说明了加密运算中的输入数据的差异会显著影响能量消耗(这里能分成4份可能是因为加密是一个字节一个字节进行的，中间那些较小的差异可能源自数据无关/低相关的噪声、数据移动等)。

  - 将差异减小到仅有1比特而非1个字节，代码如下:
```python
# 2 smaller hamming weight difference
from tqdm.notebook import trange
import numpy as np
import time

ktp = cw.ktp.Basic()
trace_array = []
textin_array = []

key, text = ktp.next()

target.set_key(key)

N = 100
for i in trange(N, desc='Capturing traces'):
    scope.arm()
    if text[0] & 0x01:
        text[0] = 0x01
    else:
        text[0] = 0x00
    # 00000000 与 00000001,仅差1bit
    target.simpleserial_write('p', text)
    
    ret = scope.capture()
    if ret:
        print("Target timed out!")
        continue
    
    response = target.simpleserial_read('r', 16)
    
    trace_array.append(scope.get_last_trace())
    textin_array.append(text)
    
    key, text = ktp.next() 

one_list , zero_list = [],[]
for i in range(len(trace_array)):
    if textin_array[i][0] == 0x00:
        zero_list.append(trace_array[i])
    else:
        one_list.append(trace_array[i])
print(f"the len of one_list:{len(one_list)}")
print(f"the len of zero_list:{len(zero_list)}")
import numpy as np
one_avg,zero_avg = np.mean(one_list,0),np.mean(zero_list,0)
difference = zero_avg - one_avg 
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 5))

plt.plot(np.abs(difference))

plt.xlabel("Samples")
plt.ylabel("Difference of Average Power")
plt.title("Differential Power Trace (0x01 - 0x00,only 1 bit difference of hamming weight )")

plt.grid(True)
plt.savefig("1bit_diff",dpi = 300,bbox_inches='tight')
plt.show()
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/1bit_diff.png)
可以看到将差异缩小到仅1bit时，图中不再有非常明显的高峰，取而代之的是很多但较低的峰，说明两种输入明文处理的能量消耗差别不明显，能解释得原因是因为两类明文数据本身差别不明显，造成能量消耗差异的更多是来自随机噪声。

- 增加收集的能量迹的条数，这里将原来收集100条改为收集5000条，代码如下：
```python
# 3 more trace
from tqdm.notebook import trange
import numpy as np
import time

ktp = cw.ktp.Basic()
trace_array = []
textin_array = []

key, text = ktp.next()

target.set_key(key)

N = 5000
for i in trange(N, desc='Capturing traces'):
    scope.arm()
    if text[0] & 0x01:
        text[0] = 0x01
    else:
        text[0] = 0x00
    # 00000000 与 00000001,仅差1bit
    target.simpleserial_write('p', text)
    
    ret = scope.capture()
    if ret:
        print("Target timed out!")
        continue
    
    response = target.simpleserial_read('r', 16)
    
    trace_array.append(scope.get_last_trace())
    textin_array.append(text)
    
    key, text = ktp.next() 

one_list , zero_list = [],[]
for i in range(len(trace_array)):
    if textin_array[i][0] == 0x00:
        zero_list.append(trace_array[i])
    else:
        one_list.append(trace_array[i])
print(f"the len of one_list:{len(one_list)}")
print(f"the len of zero_list:{len(zero_list)}")
import numpy as np
one_avg,zero_avg = np.mean(one_list,0),np.mean(zero_list,0)
difference = zero_avg - one_avg 
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 5))

plt.plot(np.abs(difference))

plt.xlabel("Samples")
plt.ylabel("Difference of Average Power")
plt.title("Differential Power Trace (0x01 - 0x00,only 1 bit difference of hamming weight,but more trace(5000) )")

plt.grid(True)
plt.savefig("DPA_more_trace",dpi = 300,bbox_inches='tight')
plt.show()
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/DPA_more_trace.png)
注意这里对比的是仅1bit差异时的图，可以看到与之前全是杂乱的小差异不同，现在能看到几个较为明显的高峰。这说明虽然当明文数据本身差异小、难以从微小的能量消耗差异中分辨出来时，可以通过增加收集的能量迹的数量来降低噪声(因为diff_noise基本不会随着输入明文的数量而变换，但是ave_diff = diff_noise/N的确会随着N的增大而减小)干扰、提高对能量消耗实际影响的相关参数的识别能力。

- 修改在不同位置明文字节下的能量消耗差异，即一开始是在明文第一字节镜像处理，现在改为在不同字节位置做处理，代码如下:
```python
from tqdm.notebook import trange
import numpy as np
import matplotlib.pyplot as plt

ktp = cw.ktp.Basic()

target.set_key(ktp.next()[0])

N = 100

def capture_byte(byte_index):
    one_list = []
    zero_list = []

    for i in trange(N, desc=f"Capturing byte {byte_index}"):
        key, text = ktp.next()

        scope.arm()

        if text[byte_index] & 0x01:
            text[byte_index] = 0xFF
            group = 1
        else:
            text[byte_index] = 0x00
            group = 0

        target.simpleserial_write('p', text)

        ret = scope.capture()
        if ret:
            print("Target timed out!")
            continue

        response = target.simpleserial_read('r', 16)

        trace = scope.get_last_trace()

        if group:
            one_list.append(trace)
        else:
            zero_list.append(trace)

    return one_list, zero_list


# 测试4个不同byte
num_bytes = 4
results = []

for i in range(num_bytes):
    one_list, zero_list = capture_byte(i)
    results.append((one_list, zero_list))


# 计算DPA difference并绘图
plt.figure(figsize=(12,5))

for i, (one_list, zero_list) in enumerate(results):
    print("Byte", i, "trace length:", len(one_list[0]))

    one_avg = np.mean(one_list, axis=0)
    zero_avg = np.mean(zero_list, axis=0)

    difference = zero_avg - one_avg

    plt.plot(np.abs(difference), label=f"byte {i}")

plt.xlabel("Samples")
plt.ylabel("|Difference|")
plt.title("DPA difference in different bytes")
plt.grid(True)
plt.legend()
plt.savefig("DPA_diff_in_diff_bytes",dpi = 300,bbox_inches='tight')
plt.show()
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/DPA_diff_in_diff_bytes.png)
可以看到这几条图线的形状非常类似，像是平移产生的，都是仅在一开始有一条明显的高峰，其他地方的差异都较小。而这些明显高峰的位置恰好随着所处理明文字节的推迟而在时间上推迟，这可以解释为该简单加密算法是对明文一个字节一个字节加密的，特殊处理的明文字节位置稍后，则加密算法处理到该字节的时间也稍后，因而差异高峰也来的靠后。

## 单比特恢复

- 这里以明文一个字节为例，输出明文字节与密钥字节异或后过S盒子得到输出结果，在这一简化模型中，输出结果的最后一比特被认为是泄露信息，可以利用这一比特的泄露来恢复整个密钥字节。
- 破解密钥方法依然是遍历，即遍历密钥字节所有256种可能，将输出改为所有明文和猜测的密钥，得到输出与实际$(\text{key,plaintex}$)输入得到的输出结果逐个做最后1比特比较，相同的计数加一，最终统计出总共的相同计数个数。
- 显然，猜测正确的密钥字节，输入后的输出结果将与实际密钥字节和明文的输出结果完全相同，计数结果为明文个数；而其他错误密钥则将使得输出结果随机，使得与实际密钥字节和明文的输出结果相比，最后1比特相同与不相同的概率相等，因此计数为明文个数的一半。简而言之，能轻易将正确密钥与其他密钥区分开来。示例代码如下:
```python
def aes_internal(inputdata, key):
    return sbox[inputdata ^ key] # 异或轮密钥并过s盒


def aes_secret(inputdata): # 简化加密算法，实际攻击的密钥就是这里的secret_key
    secret_key = 0xEF
    return aes_internal(secret_key, inputdata)

input_data = [random.randint(0,255) for _ in range(1000)] # 1000个随机input
leaked_data = [(aes_secret(a) & 0x01) for a in input_data]
def num_same(a, b):
    #Count how many list items match up
    same = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            same += 1
    return same

import numpy as np

guess_list = [0] * 256

for guess in range(0, 256):   
    
    #Get a hypothetical leakage list - use aes_internal(guess, input_byte) and mask off to only get value of lowest bit
    hypothetical_leakage =  [(aes_internal(a, guess) & 0x01) for a in input_data]
    
    #Use our function
    same_count = num_same(hypothetical_leakage, leaked_data)   
    
    #Track the number of correct bits
    guess_list[guess] = same_count

#Use np.argsort to generate a list of indicies from low to high, then [::-1] to reverse the list to get high to low.
sorted_list = np.argsort(guess_list)[::-1]

#Print top 5 only
for guess in sorted_list[0:5]:
        print("Key Guess {:02X} = {:04d} matches".format(guess, guess_list[guess]))

```
这里输出的匹配数最多的就是正确密钥字节。要恢复完整密钥，则只需要重复以上过程并切换泄露列表为对应明文字节即可，在此不做赘述。

## 能量分析破解AES密钥
- 将上述讲到的两节合起来就得到本节内容：利用traces泄露的比特信息0/1来恢复AES(简化实现)密钥。这一切建立在第一节提到的：**数据通路中的数据与具体能量消耗有密切关系**。
- 以破解一个密文字节为例，破解思路为：
    - 首先收集大量(此处是2500条)随机明文加密得到的trace(明文和对应的trace都记录下来)。
    - 遍历所有猜测密钥字节，用它和对应的明文重新加密得到密文，按照输出密文字节的最后1比特分类，为1则将对应trace归入$\text{one\_list}$,否则归入$\text{zero\_list}$。
    - 分别计算 $\text{one\_list}$和$\text{zero\_list}$的平均trace，然后平均值做差并取绝对值，以平均值差的绝对值中最大的那一个(一条trace如果有5000个采样点，则这里的最大就是这5000个里面最大的)代表该猜测密钥字节。
    - 正确密钥字节就如同上面第一节所说，应当是能有效区分$\text{one\_list}$和$\text{zero\_list}$的，因此上述中代表最大的(即以它重新加密后结果区分两类trace分的最明显的)即认为是正确密钥字节。代码如下:
```python
from tqdm import tqdm
mean_diffs = np.zeros(256)
results = {}
for guess in tqdm(range(256), desc="Guessing first key byte"):
    one_list,zero_list = [],[]
    for trace_idx in range(numtraces):
        hypothesis = aes_internal(guess,textin_array[trace_idx][0])
        # 后一个0表示此处攻击密钥第一字节，因此也只用明文第一字节来重新加密
        if hypothesis & 0x01:
            one_list.append(trace_array[trace_idx])
        else:
            zero_list.append(trace_array[trace_idx])
    one_avg = np.mean(one_list,axis = 0)
    zero_avg = np.mean(zero_list,axis = 0)
    max_diff = np.max(abs(one_avg - zero_avg))
    results[guess] = max_diff

# 排序
result_ordered = sorted(results.items(),key = lambda x : x[1],reverse= True)
for k,v in result_ordered:
    print(f"{k:02x}:{v:.4f}")
```
  这里省略了前面相同函数的定义以及收集trace的代码。同样的，恢复密钥所有比特只需要重复以上过程，作用于明文不同字节位置即可。但是同样的，依然会有恢复错误的情况出现。这种不是正确密钥字节却依然导致了很大的能量消耗差异(画成图就体现成有很大的峰)被称为ghost peak,一个普遍的解释原因是噪声，解决方法给出以下几类:
1. 增加收集的能量迹数量。就像第一节中描述的那样，求平均操作能随着收集能量迹数量的增加而减小噪声的影响。
2. 更改攻击的位置。示例中是以输出的最后1比特来区分两种trace的，但实际可能有更好的攻击点。
3. 使用窗口策略，即不是求整条trace的均值，而是只取一部分(比如已知数据相关的sbox操作在1000采样点附近进行，那我们就取1000左右的一个窗口内的数据来代替整条trace)窗口内的trace来参与运算。

其中经测试发现方法1效果最高好，将收集的能量迹从2500翻倍到5000后，恢复的密钥字节个数从3/16提升到15/16。其他两种方法本人实验未得到非常有效的结果(可能是因为这两种需要花时间确认攻击位和窗口位置等，而增加能量迹数量直观、简单有效，但实际攻击中能量迹数量是衡量攻击效率的一个重要因素)。
