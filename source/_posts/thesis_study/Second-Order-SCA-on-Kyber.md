---
title: Second-Order-SCA-on-Kyber
date: 2026-08-26 11:15:10
tags:
  - Kyber
  - 掩码侧信道攻击
  - 论文学习
categories:
   - 论文学习
---
# Second-Order Side-Channel Attacks on Kyber: Targeting the Masked Hash Function

<table><tbody><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Author:</span></span></strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"> WANG Ya-Qi; HUANG Fan; DUAN Xiao-Lin; HU Hong-Gang;</span></span></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Journal: </span></span><span style="color: rgb(255, 0, 0);"><span style="background-color: rgb(243, 250, 244);">,</span></span></strong></p></td></tr><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Journal Tags:</span></span></strong></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Local Link: </span></span></strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);"><a href="zotero://open-pdf/0_SWAW9FKD" rel="noopener noreferrer nofollow">Ya-Qi 等 - Second-Order Side-Channel Attacks on Kyber Targeting the Masked Hash Function.pdf</a></span></span></p></td></tr><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">URL:</span></span></strong></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Abstract: </span></span></strong><em><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Recently, several PC oracle based side-channel attacks have been proposed against Kyber. However, most of them focus on unprotected implementations and masking is considered as a countermeasure. In this study, we extend PC oracle based side-channel attacks to the second-order scenario and successfully conduct key-recovery attacks on the first-order masked Kyber. Firstly, we analyze the potential joint information leakage. Inspired by the binary PC oracle based attack proposed by Qin et al. at Asiacrypt 2021, we identify the 1-bit leakage scenario in the masked Keccak implementation. Moreover, we modify the ciphertexts construction described by Tanaka et al. at CHES 2023, extending the leakage scenario from 1-bit to 32-bit. With the assistance of TVLA, we validate these leakages through experiments. Secondly, for these two scenarios, we construct a binary PC oracle based on t-test and a multiple-valued PC oracle based on neural networks. Furthermore, we conduct practical side-channel attacks on masked Kyber by utilizing our oracles, with the implementation running on an ARM Cortex-M4 microcontroller. The demonstrated attacks require a minimum of 15 788 and 648 traces to fully recover the key of Kyber768 in the 1-bit leakage scenario and the 32-bit leakage scenario, respectively. Our analysis may also be extended to attack other post-quantum schemes that use the same masked hash function. Finally, we apply the shuffling strategy to the first-order masked implementation of the Kyber and perform leakage tests. Experimental results show that the combination strategy of shuffling and masking can effectively resist our proposed attacks.</span></span></em></p></td></tr><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Tags:</span></span></strong></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Note Date: </span></span></strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2026/8/26 09:47:17</span></span></p></td></tr></tbody></table>

## 📜 Research Core

* * *

### Contributions

- 扩展了基于PC Oracle的SCA，用于second-order attack的场景。利用联合信息泄露，攻击者可以区分$m_0$和$m_1$，进而展开Kyber的密钥恢复攻击。
    
- first-order masked implementation中，两份share过哈希函数时使用的是Keccak，且存在逐字节异或操作。在binary PC Oracle中这种异或操作会泄露1比特信息，而实际输入信息有32字节，因此一次最多可以泄露32比特信息。调整密文的构建可以创造出一次泄露32比特的场景（使用TVLA可以实验验证这种泄露的存在）。
    
- binary PC Oracle scenario 实验验证得到参数$t$、$th_{high}$、$th_{low}$分别为7，3.0，0.5，结果平均每query的所需trace数量为$8.9$。32-bit leakage scenario 对每次Oracle query 所需的trace数量是$9$。
    

### ⚙️ Content

#### Masked Kyber

- 在加密部分不涉及私钥$sk$，因此重点在解密/解封装部分涉及mask操作。
    
- 对密文$ct$，私钥的share分别为$sk^0,sk^1$，解密得到$m^0,m^1$，然后分别过masked hash function计算 $\mathcal G(m^0,h^0)$、$\mathcal G(m^1,h^1)$。此处masked hash function是分析与攻击的重点。
    

#### Vulnerability under Second-Order Attacks

##### Extend PC Oracle Based Attacks to Second-Order Scenario

- first order masked下，$m$被分为两份share，分别为$m^0,m^1$,满足
    
    $$m = m^0 \oplus m^1$$
    

    其中$m^0,m^1$满足:

- 当$m=m_0$时，$m^0$与$m^1$的第一字节相同，即$m^0[0] = m^1[0]$，且$m^0[0] \oplus m^1[0] = \text{0x00}$。
    
- 当$m= m_1$时，$m^0$与$m^1$的第一字节仅一个比特不同，即$m^0[0] \oplus m^1[0] = \text{0x01}$。
    
- $m^0、m^1$的剩余字节均相同，即$m^0[i] = m^1[i] ,i \in \{1,2,\cdots 31\}$。
    
    > 注，以上场景是binary PC oracle 扩展到first order masked上的情况，$m$被构造成第一字节第一比特要么为0，要么为1的情况，即$m_0 = (\text{0x00,0x00,...,0x00})$,$m_1 = \text{(0x01,0x00,…,0x00)}$。
    
- 后续如果$m^0$,$m^1$有过相同的操作，根据能量泄露模型，攻击者可以分别检出汉明重量泄露。使用SCA泄露$m^0、m^1$的第一字节的汉明重量，分别记为$HW(m^0[0])、HW(m^1[0])$，有以下两种情况：
    
    - 如果$m= m_0$(根据上文有此时$m^0$与$m^1$的第一字节相同)，则$|HW(m^0[0]) - HW(m^1[0])| = 0$，相应的能量泄露几乎相同。
        
    - 如果$m=m_1$(同上，此时$m^0$与$m^1$仅第一字节的第一比特不同)，则$|HW(m^0[0]) - HW(m^1[0])| = 1$，相应的能量泄露仅1比特不同。
        

    攻击者若能区分以上两种情况，利用能量消耗的差异就能构造出一个PC  Oracle，那么这个first-order masking implementation就能被SCA攻破。

>     可以发现，这类攻击关键都是要构造出对应的Oracle。

##### Vulnerability in the Masked Keccak Implementation

- Kyber中使用的哈希函数SHA-3是Keccak算法(海绵结构哈希函数，不同于以前的MD结构)，分为吸收和挤压两个阶段，内部包含一个$5\times 5 \times 8$字节的矩阵$st$，该矩阵首先初始化为全0，然后与输入逐字节异或，填充后作为Keccak-f置换的输入，该置换操作将执行$N_{round}$轮迭代。
    
- 在first-order masked hash function中，内部状态$st$被分为两份share：$st^0,st^1$并分别为初始化为0。这两份share会分别与输入$\text {buf}^0,\text{buf}^1$做逐字节异或操作。具体算法可见下图:
    ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Second_Order_SCA_simplified_masked_hash_function.png)
    这里的两份share分别就是$m^0$和$m^1$，作为masked Keccak function的输入。在吸收阶段的逐字节异或操作中，这两份share会泄露对应的能量信息。由于$m$仅取两种可能的值（即$m = m_0$或$m= m_1$），攻击者可以利用两个share各自的第一字节的异或操作的泄露获取丰富的信息。即联合利用$m^0[0]$、$m^1[0]$来区分$m=m_0$ or $m=m_1$。因为攻击者每次观察可以获取一比特信息，当下场景称为1-bit leakage scenario.
    
- 32bit leakage：可以发现上述masked hash function中的两份share的异或操作是逐字节进行的，即对$m^0$和$m^1$的操作将分别逐字节进行。因此修改构建的密文如下，使得每一字节都能泄露关于明文对应字节的一比特信息：
    
    $$\mathbf u = 0 \in R^{k}_q,\text{except}\quad \mathbf u_0[0] = \lceil \frac{q}{2^{d_v}}\rfloor\\ 
    v[i]=
    \begin{cases}
    \lceil \frac{q}{2^{d_v}}   \rfloor \cdot h,i \in \{0,8,\cdots,248\}\\
    0,\quad \text{therwise}
    \end{cases}$$
    
- 以上构造方法是将$s[0]、s[8]、s[16],\cdots,s[248]$映射到$m$的每一字节第一位上去。若希望恢复$s[8\times i + j]$,$i \in \{0,1,\cdots 31\},j\in \{0,1,\cdots,7\}$，只需要令$\mathbf u_0[n-j] = \lceil \frac{q}{2^{d_u}} \rfloor$，因为此时
    
    $$\begin{aligned}
    u_0[n-j] \cdot s[8i+j] &= u_0[n-j] x ^{n-j} \cdot s[8i+j] x^{8i+j}\\
    					   &= u_0[n-j] \cdot s[8i+j]  x^{n+8i}\\
    					   &= -u_0[n-j] \cdot s[8i+j]x^{8i} 
    \end{aligned}$$
    这就将$s[8i+j]$旋转到$m[8i]$上去了。
    

##### Experimental Validation

- 收集做share0和share1分别做XOR操作得到的trace如下图:
    ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Second_Order_SCA_on_Kyber_original_trace.png)

    图中可以看出，两部分分别逐字节的异或操作是很容易辨认出来的。

- 首先验证1bit leakage :首先构建两个特殊密文，使得解密结果分别为$m_0 = (\text{0x00,0x00….,0x00})$、$m_1= \text{(0x01,0x00,...,0x00)}$。（注意，每一种特殊密文在过first-order masked 实现时会被分成两份share，在masked hash function中分别做逐字节异或，这里就是要对齐这两个share的逐字节异或）。对$m=m_0$和$m=m_1$分别收集100条trac，得到$tr_0,tr_1$。如下图:
    ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Second_Order_SCA_on_kyber_tr_0_1.png)

    上图蓝框为$tr_i$的share0的逐字节异或trace，橙框为share1的逐字节异或trace。下面为将share1的平移使得与share0的对齐得到的结果。此时将蓝色trace称为$\text{tr}_i$，橙色trace称为$\text{tr}_{i,sft}$，通过计算绝对值差得到两种XOR操作的差别，即计算

$$\begin{cases}
\text{tr}_{0,prc} = | \text {tr}_0 - \text{tr}_{0,sft}  |\\
\text{tr}_{1,prc} = | \text {tr}_1 - \text{tr}_{1,sft}   | 
\end{cases}$$

    使用TVLA检测两组trace，即分别对两条$\text{tr}_{i,prc}$计算t-test，得到下图

![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/second_order_SCA_on_kyber_1bit_leakage.png)
    可以看到t-test中有一点高于阈值4.5，作为PoI。也就是说做了预处理的组trace是不同的（能被检测出来的），vulnerability得以验证。

- 验证32bit leakage时，构建特殊密文使得解密得到$m_0 = (\text{0x00,0x00,...,0x00})$和$m_1 = \text{(0x01,0x01,…,0x01)}$。同样的利用TVLA检测两组预处理后的trace得到t-test结果如下图：
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Second_SCA_on_kyber_32bit_leakage.png)
    可以看到32个不同的peak超过阈值4.5，验证了32-bit leakage的可行性。

## 🔁 Research Content

* * *

### 🔬 Experiment

#### The Construction of PC Oracle

- 本实验的一大关键也是构建出Oracle。
    

##### Binary PC Oracle

- 首先以构建1-bit leakage scenario下的Binary PC Oracle。不同于一般采用t-majority voting提高分类准确率（这种方法的最小$t$为21，还是太大了）。本论文提出一种新方法，能进一步减少查询次数。
    
- 首先构建密文使得解密结果为$m = m_0$，收集500条trace来获取PoI，作为参考数据集。然后收集$t$条traces来创建一个由$t$ Points组成的测试集合（其中$t$是待实验确定的参数）。使用one-tailed test method 使得有更高的把握接收或拒绝原假设。测试时对$m=m_0$和$m=m_1$分别重复1w次 测试，设置双阈值$\text{th}_{high}$和$\text{th}_{low}$，对m的恢复策略如下:
    
    $$m = 
    \begin{cases}
    m_0 ,\text{t-value} \le \text{th}_{low}\\
    \text{Uncertain},\quad  \text{th}_{low} < \text{t-value} < \text{th}_{high}\\
    m_1,\text{t-value} \ge \text{th}_{high}
    \end{cases}$$
    

    对于分类结果是`Uncertain`的还需要重新收集$t$条trace，再次做分类，直到能确定$m$的确为$m_0$或$m_1$ 。因此查询oracle所需的平均traces数量将大于等于$t$，有

$$n_{ave} = \sum_{i=0}^{N_{test}} \frac{n_i}{N_{test}}$$

    $n_i$表示第$i$次测试时实际的查询次数。实验验证最终得到的参数结果为$t=7$，$\text{th}_{high} = 3.0$，$\text{th}_{low} = 0.5$，分类准确率为$99.95\%$，平均每次Oracle查询次数为$8.9$。

- 上述binary PC Oracle创建的算法如下:
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/second_SCA_on_kyber_binary_PC_oracle.png)
    
    - 上述$tr$指待分类的密文收集$t$条trace。
        
    - `TraceAligment()`指前文将后一份share的XOR的部分移动到前一份share的XOR 部分对齐，所得结果为$\text{tr}_{sft}$。
        
    - $\text{tr}_{prc}$指第一份share XOR部分与第二份share XOR部分的差的绝对值。
    - $GetPoIs$指根据一开始测得的PoI位置，对$t$条$\text{tr}_{prc}$分别取PoI处的值，得到测试向量$TestSet$。
    - $MessageDistinguisher$是根据根据500条reference trace取PoI得到的500长reference向量和上述得到的$t$长的测试向量，计算`t-test value`,根据`t-test value`进行分类(归为$m_0$、$m_1$或无法准确分类，有待进一步测试)。
        
    - 以上构建 PC Oracle的方法称为`t-test`方法。
        

##### 32-bit leakage scenario

- 攻击者试图构建32-bit泄露场景下的Oracle时，使用上述方法将会变得很低效，因为re-measurement将会使得平均每次Oracle所需traces数量大大增加 (毕竟这次只要一个字节的某一位分类失败，就要重新收集trace并作分类)。
    
    - 一个发现是，这里32字节中，任意一个字节的能量迹分布对比（$m[i] = 0$和$m[i] = 1$）都极其类似，如下图:
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Second_order_on_kyber_different_pos_leakage.png)
        
        因此不必为32个字节分别训练不同的分类器，相反，只需要训练一个通用的字节分类器，对32字节每一个输入进去都能输出正确分类结果即可，具体过程如下：
        
    - 收集 $t_1$条trace，对每一信息字节获取$t_1$个PoI，结果得到一个二维的PoI矩阵：$PoI[i][j]$，$i \in \{0,\cdots,31\},j \in \{0,\cdots ,t_1-1\}$。
        
    - $PoI[i]$作为neural network的输入，输出为分类结果（0 or  1）。
        
    - 重复上述过程$t_2$次作为majority voting，获得最终分类结果。
        
- 为了训练上述的neural network，需要使用上述方法构建特殊密文，使得解密结果分别为$m= (\text{0x00,0x00,…,0x00})$和$(\text{0x01,0x01,...,0x01})$。对每种密文收集 $t_1 \times \tau$条traces，对每$t_1$trace，都能提取$32$samples(每个字节一个sample,每个sample$t_-1$个PoI)。因此总共需要$N_{samples} = \tau \times 32 \times 2$training samples（2是因为有两种明文形式）。这里每个输入可以看作矩阵:
    
    $$\begin{pmatrix}
      PoI_{0,0}&PoI_{0,1}  &\cdots  &PoI_{0,t_1 - 1} \\
      PoI_{1,0}&PoI_{1,1}  &\cdots  &PoI_{0,t_1 - 1}  \\
      \vdots& \vdots &\ddots  &\vdots \\
      PoI_{31,0}&PoI_{31,1}  &\cdots  &PoI_{31,t_1 - 1}
    \end{pmatrix}$$
    
    每一种明文（一共就两种）重复$\tau$次。具体参数见论文为$t_1 = 3,t_2 = 3,\tau = 100$（注意这里的$t_2$是训练好后，具体分类时做majority voting时的重复次数，与训练阶段无关）。
    
- 这里的构建Multiple-Valued Plaintext-Checking Oracle算法如下：
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/second_order_on_kyber_mvpc_oracle.png)
    
- 最终的攻击结果如下图：
    ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/second_order_on_kyber_result.png)

#### Countermeasures

- Shuffling：结合masking和Shuffling，即使得在masked hash function 中的XOR操作的顺序被打乱，这样将使得不同share对相同字节的操作难以对齐。也就是说，shuffling操作打乱leakage points，使得攻击者更难提取出有意义的信息。masking + shuffling保护下的t-test结果如下图：
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/second_order_on_kyber_shuffling_masked.png)
    
    可以看到，t-test value均小于阈值。
    
- Higher-order Masking：本实验的攻击方法未必对更高阶的掩码有效，不过更高阶的掩码也意味着更高的开销。
    
- Key Refreshment：在攻击成功所需的查询次数之前就将私钥刷新，这样攻击者也无法及时恢复完整私钥。
    

### 📜 Conclusion

- 本论文将PC oracle based SCA key recovery对Kyber的攻击扩展到一阶掩码的攻击上。论文展开了对masked hash function泄露的分析，发现masked  hash function一次至多可能泄露32bit明文信息（取决于密文的构建）。定义并验证了1-bit leakage  scenario和32-bit leakage scenario。
    
- 1-bit leakage scenario中使用基于t-test的binary oracle，每次查询oracle的平均traces数为8.9，正确率为$99.95\%$。32-bit leakage scenario中oracle构建综合了neural network 和 majority-voting，得到平均每次查询所需traces为9。
    

## 🤔 Personal Summary

* * *

### 🙋♀️ Key Records

### 📌 To be resolved

### 💭 Thought Inspiration