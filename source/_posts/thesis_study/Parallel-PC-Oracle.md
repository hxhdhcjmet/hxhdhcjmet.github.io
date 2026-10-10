---
title: Parallel_PC_Oracle
date: 2026-08-07 21:24:46
tags:
   - Kyber
   - 侧信道攻击
   - 论文学习
categories:
   - 论文学习
---
# <span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(238, 249, 253);">(2023-03-06) Pushing the Limits of Generic Side-Channel Attacks on LWE-based KEMs - Parallel PC Oracle Attacks on Kyber KEM and Beyond</span></span>

| <!-- --> |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Author:</span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"> Gokulnath Rajendran; Prasanna Ravi; Jan-Pieter D’Anvers; Shivam Bhasin; Anupam Chattopadhyay;</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Journal: </span></span><span style="color: rgb(255, 0, 0);"><span style="background-color: rgb(243, 250, 244);">IACR Transactions on Cryptographic Hardware and Embedded Systems, </span></span><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">418-446, 2023.</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Journal Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Local Link: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);"><a href="zotero://open-pdf/0_HC3ECQD7" rel="noopener noreferrer nofollow">Rajendran 等 - 2023 - Pushing the Limits of Generic Side-Channel Attacks on LWE-based KEMs - Parallel PC Oracle Attacks on.pdf</a></span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">DOI: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"><a href="https://doi.org/10.46586/tches.v2023.i2.418-446" rel="noopener noreferrer nofollow">10.46586/tches.v2023.i2.418-446</a></span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Abstract: </span></span>***<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">In this work, we propose generic and novel adaptations to the binary Plaintext-Checking (PC) oracle based side-channel attacks for Kyber KEM. These attacks operate in a chosen-ciphertext setting, and are fairly generic and easy to mount on a given target, as the attacker requires very minimal information about the target device. However, these attacks have an inherent disadvantage of requiring a few thousand traces to perform full key recovery. This is due to the fact that these attacks typically work by recovering a single bit of information about the secret key per query/trace. In this respect, we propose novel parallel PC oracle based side-channel attacks, which are capable of recovering a generic P number of bits of information about the secret key in a single query/trace. We propose novel techniques to build chosen-ciphertexts so as to eﬃciently realize a parallel PC oracle for Kyber KEM. We also build a multi-class classiﬁer, which is capable of realizing a practical side-channel based parallel PC oracle with very high success rate. We experimentally validated the proposed attacks (upto P = 10) on the fastest implementation of unprotected Kyber KEM in the pqm4 library. Our experiments yielded improvements in the range of 2.89× and 7.65× in the number of queries, compared to state-of-the-art binary PC oracle attacks, while arbitrarily higher improvements are possible for a motivated attacker, given the generic nature of the proposed attacks. We further conduct a thorough study on applicability to diﬀerent scenarios, based on the presence/absence of a clone device, and also partial key recovery. Finally, we also show that the proposed attacks are able to achieve the lowest number of queries for key recovery, even for implementations protected with low-cost countermeasures such as shuﬄing. Our work therefore, concretely demonstrates the power of PC oracle attacks on Kyber KEM, thereby stressing the need for concrete countermeasures such as masking for Kyber and other lattice-based KEMs.</span></span>* |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Note Date: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2026/8/4 14:47:01</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |


## <span style="color: rgb(224, 255, 255);"><span style="background-color: rgb(102, 205, 170);">📜 Research Core</span></span>

***

### Contributions

*   提出一种通用、新颖的使用SCA辅助的基于PC Oracle的攻击,即P路并行PC Oracle攻击，每次可以同时恢复Pbit信息，对比目前最先进的PC Oracle攻击每次只能恢复1bit信息。
*   发现现有基于二进制（一般的一次恢复一位的)PC Oracle的最佳选择密文查询对于本文所提出的并行PC Oracle并不一定是最优的，因此本文单独提出更优的构建方法(即Binary Decision Trees,BDTs)来确定查询次数的下界。
*   使用二进制PC Oraccle的分类器来实现P 路PC Oracle的总共 $2^P$ 种类的分类器，且在 $P = 10$ 时达到分类的完美准确率(更大 $P$ 只存在于理论中，实际很难评估 $P$ 的上界)。
*   实验验证基于pqm4的攻击效果是现有最先进二进制PC Oracle 的2.89倍和7.65倍。
*   分析了两种情况(1.有无克隆设备2.敌手离线计算能力)下的攻击情况。
*   实际验证了本文提出的攻击在低开销策略保护(如混洗)下的应用效果，显示为现有侧信道辅助的选择密文攻击的最好效果(需要的traces数最小)。

### ⚙️ Content

#### Prior Side-Channel Attacks and Motivation

##### TO\_Indep

*   PC Oracle-based SCA: 选择密文使得解密结果严格限制为只有 $m=0$ 和 $m=1$ 两种，利用时间侧信道攻击(即ECC\_Decode(0)与ECC\_Decode(1)的时间不同)实现PC Oracle, $m=0$ 和 $m=1$ 的1bit不同都会对re-encryption过程的计算造成巨大影响(即一条trace即可区分).。
*   DF Oracle-based SCA:攻击者能探测出解密失败(m=m\_valid or m = m\_invalid),这里探测方法如Guo等人利用密文比较的时间差异(re-encryption后的c == c’比较操作，是否相同的比较时间有差异。实际上不只可以利用比较操作，整个re-encryption过程都可利用)来构建DF Oracle。

##### TO Dep

*   Encoding/Decoding Operation:利用编码和解码操作操作泄露的信息，使得只利用极少的trace就能恢复完整信息m.但是这种方法有很大局限性:只利用单个时钟周期或非常少的采样点来恢复信息的一比特,因此对噪声(SNR,信噪比)非常敏感，同时也不清楚类似的泄露是否能在更复杂的设备，如重度平行、深流水线、固有抖动等特征下的设备。
*   NTT Operation:利用Kyber中的NTT操作，同样只需要少量trace。但是同样面临如需要复杂设置和强大侧信道攻击能力、难以实施、在复杂设备平台上运行效果未知等缺点。

#### Binary PC Oracle-based CCA

*   这部分是本片论文实现并行恢复的基础，重点参考了\[QCZ+21]这篇论文(该论文的阅读参见<a href="zotero://note/u/CT62S7VY/" rel="noopener noreferrer nofollow" zhref="zotero://note/u/CT62S7VY/" ztype="znotelink" class="internal-link">(2021) A Systematic Approach and Analysis of Key Mismatch Attacks on Lattice-Based NIST Candidate KEMs</a>)。

*   选择特定的$\mathbf u = k_u \cdot x^0 = (k_u,0,\cdots,0)$,$\mathbf v = k_v \cdot x^0 = (k_v ,0,\cdots,0)$，则

    $$
    \mathbf u \cdot s = \sum_{i=0}^{n-1} k_u s[i]x^i
    $$

故$(\mathbf u \cdot s)[i] = k_u s[i]$,因此$m[i] = \text{Decode}(v - u\cdot s)[i] = \text{Decode}(v[i] - (u \cdot s)[i])$:

$$
m[i]=
\begin{cases}
\text{Decode}(k_v - k_u \cdot s[0]),i=0\\
\text{Decode}(-k_u \cdot s[i]),i \in \{1,n-1\}
\end{cases}
$$

*   根据上篇论文中的方法，选择$\mathbf u = k_u \cdot x^p = (0,\cdots,k_u,\cdots,0),\mathbf v = k_v \cdots x^0 = (k_v ,0,\cdots,0)$,则

    $$
    \mathbf u \cdot s = \sum_{i=0}^{n-1} k_u s_{i}x^{p+i} = (k_u s_0,k_u s_1,\cdots,k_u s_{n-1})
    $$

    当$p+i = n$,$i = n-p$时，$x^{p+i} = x^{n} = -1$,对应系数$k_u s_{n-p}$,故此时:

$$
m_0 = \begin{cases}
k_v - k_u \cdot s[0],p=0\\
k_v - k_u \cdot (-s[n-p]),p \in \{1,n-1\}
\end{cases}
$$

#### P way parallel PC Oracle-based CCA

*   关键是构建密文使得信息 $m$ 的多( $P$ )比特信息与秘密私钥 $s_t$ 的 $P$ 比特系数有关。

*   令$\mathbf v = 208\cdot t \cdot(\sum_{i=0}^{P-1}x^i) = (208\cdot t ,208 \cdot t,\cdots,0,0,\cdots,0)$,$\mathbf u = 208 \cdot x^0$,此时同上，仍有$k_u = 208,(\mathbf u \cdot s)[i] = k_u s[i] = 208 \cdot s[i]$,故:

    $$
    m_i = \begin{cases}
    \text{Decode}(208 \cdot t - 208 \cdot s[i])\\
    \text{Decode}(- 208 \cdot s[i])
    \end{cases}
    $$
    以上是利用了$s[0]\sim s[P-1]$将特殊构造的密文解密到只有$m[0] \sim m[P-1]$位置上，其他位置上均为0.
* 当要处理/破解之后几块的私钥，比如$s[nP] \sim s[nP+P-1]$时，仍然希望解密结果至明文的$m[0] \sim m[P-1]$位置上，这样构造出来的模板只要能分辨$m[0] \sim m[P-1]$的$2^P$种可能即可，不论求解的是私钥的哪一块。此时需要利用环上的旋转性质，修改密文$\mathbf u = -k_u x^t$，满足:
    $$
    -k_u x^t \cdot s[nP] x^{nP} = -k_u \cdot s[nP] x^{t+nP} = -k_u \cdot s[nP] x^N = k_u \cdot s[nP]
    $$
    即满足$t = N - nP$，$\mathbf u$在这一位置上取值$-k_u$就能实现对任意指定位置的私钥解密结果旋转至$m[0] \sim m[P-1]$上。
*   Binary PC Oracle中使用BRT可以达到最少的查询次数，但是P way parallel PC Oracle中却并非如此，如二路并行,一次查询出 $(s[i],s[i+1])$ ，最少查询次数是这两个中的最大值。进一步地，对于 $P$ 路并行,恢复完整 $P$  set系数的最少查询次数是这 $P$ 系数中的最大者，因此此时追求整棵树的平衡(整体都较短，没有某一个节点距离根特别远)可能会比追求单次平均查询次数最少会更好。

![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Push_Limit_BRT_Kyber512.png)

*   比如上述为Binary PC Oracle构建的BRT,下面为本论文展示的一种适合P路并行的BDT:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Push_Limit_Pway_BDT.png)

*   令$\mathcal{Q}_{set}$表示$P$ 路并行时，一次恢复$P$个系数的最小查询次数，则不同参数下的Kyber算法在不同查询决策树下的该值是不同的：![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Push_Limit_Qset.png)
    可见本论文提出的决策树在$P$路并行查询恢复的情况下会有更少的查询次数(即更优秀的表现)。总查询次数:

$$
\mathcal Q_{attack} =  \lceil \frac{2^8}{P} \rceil \cdot K \cdot \mathcal Q_{set}
$$

![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Push_Limit_Qattack.png)

#### Binary classification

##### Pre-Procress

*   先收集多条($T$)$m=0$和$m=1$时的trace,将它们标准化($\frac{x-\bar x}{\sigma}$)后求t值:

    $$
    \text{t-value} = \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{T}+ \frac{\sigma_2^2}{T}}}
    $$

*   取出 $\text{t-value} > \text{threshold}$ 的那些点作为PoI(认为这些点包含了有关$m=0 \text{和}m = 1$ 的信息/$m=0$和$m=1$的差异导致这些点的大$\text{t-value}$，因此 $\text{t-value} > \text{threshold}$ ,其他点处两种 $m$ 下差异不大，有理由认为是噪声/信息量不足)，这里的阈值threshold使用经验值。

*   计算上述$m=0、m=1$下的PoI的均值作为简化模板。

##### Classification

*   上面Pre-Procress已经计算得到了简化模板，现在用来区分一个收集到的trace属于哪一类。将该trace标准化后分别与模板计算平方差:

    $$
    \Gamma_0 = (t'_{\mathcal {P}} - m_{0,\mathcal P})^T \cdot(t'_{\mathcal P} - m_{0,\mathcal P}),\Gamma_1 = (t'_{\mathcal {P}} - m_{1,\mathcal P})^T \cdot(t'_{\mathcal P} - m_{1,\mathcal P})
    $$
     平方差更小，说明该trace与对应模板更接近，便将该trace分类到对应模板,即:

$$
    \text{trace} \in \begin{cases}
    m_0,\Gamma_0 < \Gamma_1\\
    m_1,\Gamma_0 \ge \Gamma_1
    \end{cases}
$$

### 💡 Innovations

#### Multi-Class Classfication

*   如果能对 $m \in [0,2^{P-1}]$ 中任意一对 $m$ 做区分，那么就有可能单独辨别出所有的 $2^P$ 种的 $m$ 。

*   基于前面Binary Classifination的过程，这里Multi-Class Classfication也分为两步:

    *   Pre-Procress:对所有 $m \in [0,2^{P-1}]$ ,每种收集 $T$ 条re-encryption的trace(总共要收集 $2^P \cdot T$ 条trace )。
    *   Classification:采用两两比较的方式(pairwise binary classification)确定某条实验收集到的trace到底属于哪一类。

#### Partial Key Recovery

*   本论文提出的P-way Parallel PC Oracle可以只用来恢复 $st$ 的部分比特，剩下位的比特保留下来用离线方式计算出来，权衡在线查询的次数和离线计算的难度。

### 🧩 Shortcomings/FutureWork

*   完美分类的 $P$ 的上界尚不清楚，论文指出如果该上界存在，那么将很难通过实验来确定，因为它实际取决于很多因素，比如目标设备、目标设备实现、信噪比等，因此目前对 $P$ 的选择确定只能基于经验，具体确定作为未来工作。

## <span style="color: rgb(32, 178, 170);"><span style="background-color: rgb(175, 238, 238);">🔁 Research Content</span></span>

***


### 🔬 Experiment

#### With Clone Device

*   此时可以在克隆设备上构建分类器模板，无需在目标设备上收集已知明文解密的trace来训练模板，因此此时认为总的查询次数不包括构建模板时用到的trace(即$\mathcal Q_{template} = 0$):
    $$
    \mathcal Q_{target} = \mathcal Q_{attack} = \lceil \frac{2^8}{P} \rceil \cdot k \cdot \mathcal Q_{set}
    $$
    此时的总的查询次数取决于并行度$P$,实验验证在$P = 10$时，完整恢复密钥大约需要232次查询,性能约是最优Binary PC Oracle 的7.6倍。

![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Push_Limit_with_clone_device.png)

#### Without Clone Device

*   此时构建template也要在target device上查询，因此认为总的查询次数要包含构建模板的查询次数:

    $$
    \begin{aligned}
    \mathcal Q_{target} &= \mathcal Q_{template} + \mathcal Q_{attack}\\
    					&= 2^P \cdot T + \lceil  \frac{2^8}{P} \rceil \cdot k \cdot \mathcal Q_{set}
    \end{aligned}
    $$

    此时的总查询次数中，$\mathcal Q_{template}$随$P$呈指数增长，而$\mathcal Q_{attack}$与$P$成反比，此时不能为了改进$\mathcal Q_{target}$而盲目增大$P$,因为这会使得构建模板阶段的查询次数的代价过大而无法承受。![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Push_Limit_without_clone_device.png)

    实验选择的参数是$T = 5,P = 4$,所需的查询次数是613，较binary PC Oracle 优化约2.89倍。($T$ = 1,$P = 6$有更少的查询次数:437,优化约4倍，但此时可能由于构建模板查询过少导致分类准确率太低)。

#### Extension to Lightly Protected Implementations

*   masking技术用于LWE/LWR-based KEMs最高能造成3倍的时间开销，因此低开销的抵御已知攻击的保护手段备受关注，一种方式就是shuffing。它使得攻击者依然能恢复完整的信息，但是这些信息的比特顺序是乱序的，因而提供保护并去除了Full-Decryption Oracle结构。
*   Ravi提出一种选择密文攻击，可以每次查询恢复1bit信息(等同于binry PC Oracle)。

### 📜 Conclusion

*   本论文提出一种新颖的基于SCA的并行PC Oracle,可以一次性根据一条trace恢复(任意) $P$ bit信息，在基于pqm4的实现上实验证明该方法较目前最先进(之前论文中的mismatch attack)binary PC Oracle在查询次数上有了很大改进。
*   本论文提出的方法(P-way Parallel PC Oracle)在低成本保护(shuffling)的设备上同样达到了恢复密钥所需的最低查询次数，然而该方法能被掩码技术有效阻止，进一步证明了掩码技术在基于格的密码算法上的必要性。

## <span style="color: rgb(0, 77, 153);"><span style="background-color: rgb(135, 206, 250);">🤔 Personal Summary</span></span>

***

### 🙋♀️ Key Records

*   本论文提出的P way Parallel PC Oracle实现一条trace恢复多位 $sk$ 信息，使得最终完整恢复 $sk$ 所需要的trace数量较binary PC Oracle 大大减少。
*   本论文提出的新的BDT较binary PC Oracle中用到的BRT更适合于P way Parallel的情况(实质上就是本文的BDT更平衡，没有某一子树特别长的情况)。
*   本文考虑了各种情况(有无clone device、P way Parallel Oracle恢复 $sk$ 多少比特、有无简单抵御策略如shuffing)下所需的trace数量以及它们较原版Binary PC Oracle的性能优化程度。

### 📌 To be resolved

*   Muti-class Classification中的pairwise binary classification 指出 $2^P$ 类经过 $2^P- 1$ 次比较(可以从论文中的比较树中确认)即可实现精准分类，但是为什么不能算出所有与模板的平方差后直接取 $\Gamma$ 最小的为对应类别，还要两两比较？


### Code

- 由于这篇论文并没有给出具体实现代码，但论文一的binary PC-Oracle给出的具体代码结合本篇论文的描述，我们可以复现这篇论文的实现代码，结合代码再理解本论文。

- 总体上利用了论文一代码中kyber1024-3/中的实现，尤其是Kyber加密部分，关键修改体现在以下方面:
    - 定义阈值`H_ZERO`,代码如下
    ```c
    #if KYBER_DV == 4
    #define H_ZERO  5
    #elif KYBER_DV == 5
    #define H_ZERO  9
    #else
    #error "Unsupported KYBER_DV (must be 4 or 5)"
    #endif
    /*
    * Secret coefficient set.
    * For eta1=2 (Kyber768/1024): {-2, -1, 0, 1, 2}
    * For eta1=3 (Kyber512):      {-3, -2, -1, 0, 1, 2, 3}
    * Currently only eta1=2 is supported by the attack logic below.
    */
    #if KYBER_ETA1 == 2
    #define NVALUES   5
    static const int values[NVALUES] = { -2, -1, 0, 1, 2 };
    #else
    #error "Only eta1=2 (Kyber768/1024) is supported by this attack code"
    #endif
    ```
    这里的`H_ZERO`是这样用的，对$k = \text{H\_ZERO} + \text{value}$,其中`value`是私钥系数的可能取值(Kyber1024/768是$\{-2,-1,0,1,2\}$,Kyber512是$\{-3,-2,-1,0,1,2,3\}$),对于解密出来的明文位有:
    $$
    m = \lceil \frac{2}{q}(\lceil  \frac{k \cdot q}{2^{d_v}}  \rfloor- s \cdot \lceil \frac{q}{2^{d_v}} \rfloor   )\rfloor  \mod 2
    $$
    对于$s\le\text{value}$,$k=\text{H\_ZERO}+\text{value}$时,$m = 1$,否则若$s>\text{value}$ ,$m = 0$。这个使用Kyber1024,$q = 3329,k_v = 5$可以验证出来。比如对$k = 9 +(- 2) = 7$,只有当$s \le -2$时,$m = 1$,否则$m = 0$。因此这里Oracle的作用就是告诉我们，我们想验证的$s \le \text{value}$是否成立。这是因为这里的$\text{H\_ZERO}$是上式对$s=0$时，计算得到$m = 1$分界阈值(当$h < \text{H\_ZERO}$时$m = 0$;当$h \ge \text{H\_ZERO}$时,$m =  1$),即:
    $$
    m=
    \begin{cases}
    0,s = 0,k < \text{H\_ZERO},\\
    1,s = 0,k \ge \text{H\_ZERO}
    \end{cases}
    $$
    对于$k = \text{H\_ZERO + value}$,带入上述计算m的式子得到:
    $$
    \begin{aligned}
    m &= \lceil \frac{2}{q}(\lceil  \frac{k \cdot q}{2^{d_v}}  \rfloor- s \cdot \lceil \frac{q}{2^{d_v}} \rfloor   )\rfloor  \mod 2\\
      & =  \lceil \frac{2}{q}(\lceil  \frac{\text{H\_ZERO} \cdot q}{2^{d_v}}  \rfloor+ (\text{value}- s) \cdot \lceil \frac{q}{2^{d_v}} \rfloor   )\rfloor  \mod 2
    \end{aligned}
    $$
    显然当$\text{value} - s \ge 0$时($s \le \text{value}$)，上述计算结果$m=1$,反之若$\text{value} - s < 0$($s > \text{value}$)，则上述结果$m = 0$(等价于$s = 0$时,$h = \text{H\_ZERO} + (\text{value} - s)$，显然$\text{value}$与$s$的关系是会影响$h$与$\text{H\_ZERO}$的关系的)。

    - mv_pc oracle代码如下:
    ```c
    int oracle_mvpc(const unsigned char *ct,const unsigned char *sk,int pos,int n,double accuracy)
    {
    unsigned char m_dec[KYBER_SYMBYTES] = { 0 };
    int result = 0;
    int i;

    /* decrypt the ciphertext */
    indcpa_dec(m_dec, ct, sk);

    /* extract N bits from positions pos, pos+1, ..., pos+n-1 */
    for (i = 0; i < n; i++) {
        int coeff_idx = pos + i;
        int byte_idx = coeff_idx / 8;
        int bit_idx = coeff_idx % 8;
        int bit = (m_dec[byte_idx] >> bit_idx) & 1;
        result |= (bit << i);
    }

    /* simulate imperfect oracle if accuracy < 1.0 */
    if (accuracy < 1.0) {
        double r = (double)rand() / (double)RAND_MAX;
        if (r > accuracy) {
        /* return a random wrong class */
        int nclasses = 1 << n;
        int wrong;
        do {
            wrong = rand() % nclasses;
        } while (wrong == result);
        result = wrong;
        }
    }

    return result;
    }
    ```
    这里其实将Oracle和classifier 结合在一起了，解密明文`indcpa_dec(m_dec, ct, sk);`,由上述可以确定，测试的这一位密文系数$s$是$s \le \text{value}(m=1)$还是$s > \text{value}(m=0)$,根据结果缩小$s$的取值范围，为下一步测试提供信息。并行体现在将本次要测的$n$位结果整合成变量`result`。代码中`accuracy`是Oracle正确率，当正确率小于1时，就以$1-\text{accuracy}$的概率返回一个错误的(与正确`result`不同的)`result`。

    - 攻击部分代码(`PQCgenKAT_kem.c`):
       - 更新状态:
         ```c
            static void update_state(bdt_state_t *st, int threshold_index, int bit)
            {
                if (bit) {
                    st->hi = threshold_index;
                } else {
                    st->lo = threshold_index + 1;
                }
            }
         ```
        bit是攻击sk的某一位，得到的对应m的结果，如果为1，说明测试$s \le \text{value}$为真，此时应当缩小上界`st->hi = threshold_index;`,反之则应增大下界`st->lo = threshold_index + 1;`。
        - 选择树的构建:
        ```c
        static int choose_threshold(const bdt_state_t *st, tree_mode_t mode)
        {
            int lo = st->lo;
            int hi = st->hi;

            if (mode == TREE_BALANCED) {
                return (lo + hi - 1) / 2;
            }

            /* binary mode: split at value 0 if possible */
            if (values[hi] <= 0) {
                return hi - 1;
            }
            if (values[lo] > 0) {
                return lo;
            }
            /* find index of value 0 */
            {
                int i;
                for (i = lo; i <= hi; i++) {
                    if (values[i] == 0) return i;
                }
            }
            return (lo + hi) / 2;
        }
        ```
        当`mode == TREE_BALANCED`时构建平衡树，按照本片论文中的描述构建`BDT_depth`,为的是让整棵树的平均深度最小，使得parallel时的平均查询次数最小，因此从中间开始分叉`return (lo + hi - 1) / 2;`。否则按照论文一的方法，从概率大的私钥系数0处开始分叉，为的是让参数出现概率高的系数查询次数最少，即构建`BDT_ent`。上面的st存的是当前私钥系数的可能范围(如Kyber1024是$\{-2,-1,0,1,2\}$)下标,当$\text{st.lo} \ge \text{st.hi}$时即收敛，表示这一位系数可以确定了。
        - 单次平行(parallel位)恢复:
        ```c
        static void recover_group_mvpc(const unsigned char *sk,
                                    int select,
                                    int group_start,
                                    int n,
                                    tree_mode_t mode,
                                    double accuracy,
                                    int *recovered,
                                    int *query_count)
        {
            static bdt_state_t states[MAX_PARALLEL];
            static int klist[MAX_PARALLEL];
            static int threshold_indices[MAX_PARALLEL];
            static unsigned char ct[CRYPTO_CIPHERTEXTBYTES];
            int i;
            int active;

            /* initialise BDT states */
            for (i = 0; i < n; i++) {
                states[i].lo = 0;
                states[i].hi = NVALUES - 1;
            }

            /* main recovery loop */
            while (1) {
                active = 0;

                /* determine k values for each coefficient */
                for (i = 0; i < n; i++) {
                    if (states[i].lo < states[i].hi) {
                        /* still searching */
                        int th = choose_threshold(&states[i], mode);
                        threshold_indices[i] = th;
                        klist[i] = H_ZERO + values[th];
                        active = 1;
                    } else {
                        /* already recovered — use a dummy k */
                        threshold_indices[i] = -1;
                        klist[i] = H_ZERO;
                    }
                }

                if (!active) break;

                /* construct parallel ciphertext and query oracle */
                enc_mvpc(ct, klist, group_start, select, n);
                (*query_count)++;

                {
                    int result = oracle_mvpc(ct, sk, group_start, n, accuracy);

                    /* update each coefficient's state */
                    for (i = 0; i < n; i++) {
                        if (states[i].lo < states[i].hi) {
                            int bit = (result >> i) & 1;
                            update_state(&states[i], threshold_indices[i], bit);
                        }
                    }
                }
            }

            /* store recovered values */
            for (i = 0; i < n; i++) {
                recovered[i] = values[states[i].lo];
            }
        }

        ```
        每次平行查询恢复时确保所有位都收敛了才停止，只要有一位没有恢复都要继续查询。每一位都会根据Oracle的结果选择新的$k_i$,在代码中体现为`int th = choose_threshold(&states[i], mode)`和`klist[i] = H_ZERO + values[th]`这两句，构建特殊密文的函数`enc_mvpc(ct, klist, group_start, select, n)`代码如下:
        ```c
        void enc_mvpc(unsigned char *c,
                    const int *klist,
                    int pos,
                    int select,
                    int n)
        {
        static polyvec Pb;
        static poly v;
        int i;

        /* reset to zero (polyvec and poly are large, use static to avoid stack overflow) */
        memset(&Pb, 0, sizeof(Pb));
        memset(&v, 0, sizeof(v));

        /* u: fixed monomial at position 0 with value round(q/2^dv) */
        Pb.vec[select].coeffs[0] = (KYBER_Q + (1 << (KYBER_DV - 1))) >> KYBER_DV;
        polyvec_reduce(&Pb);

        /* v: place N k values at positions pos, pos+1, ..., pos+n-1 */
        for (i = 0; i < n; i++) {
            v.coeffs[pos + i] = klist[i];
        }

        pack_ciphertext_Attack(c, &Pb, &v);
        }
        ```
        按照论文中描述的,$\mathbf u = (\lceil \frac{q}{2^{d_v}} \rfloor,0,\cdots,0)$, $v = \sum_{i=0}^{n-1}k_i x^i$，$k_i$(即$v$的系数)是根据oracle结果会每一位在查询前特别调整的，在代码中体现为`v.coeffs[pos + i] = klist[i]`，`klist`即上一块代码中的根据oracle结果选择下一轮的$k_i$。

        - 完整恢复代码:
        ```c
        static int attack_paper2(const unsigned char *sk,
                         const polyvec *skpoly,
                         int parallel,
                         tree_mode_t mode,
                         double accuracy,
                         int *total_errors)
        {
            int select;
            int group;
            int query_count = 0;
            int errors = 0;
            int (*recs)[KYBER_N] = calloc(KYBER_K, sizeof(int[KYBER_N]));

            if (!recs) {
                *total_errors = -1;
                return -1;
            }

            for (select = 0; select < KYBER_K; select++) {
                for (group = 0; group < KYBER_N; group += parallel) {
                    int n = parallel;
                    if (group + n > KYBER_N) {
                        n = KYBER_N - group;
                    }

                    recover_group_mvpc(sk, select, group, n,
                                    mode, accuracy,
                                    recs[select] + group,
                                    &query_count);
                }
            }

            /* verify recovered key against true secret */
            for (select = 0; select < KYBER_K; select++) {
                int j;
                for (j = 0; j < KYBER_N; j++) {
                    if (recs[select][j] != skpoly->vec[select].coeffs[j]) {
                        errors++;
                    }
                }
            }

            free(recs);
            *total_errors = errors;
            return query_count;
        }
        ```
        实际就是根据Kyber安全参数遍历`KYBER_K`行，每行`KYBER_N`位，一次`parallel`地恢复完整密钥$sk$

    - 代码编译运行结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Parallel_PC_oracle.png)
可以看到在kyber768,并行度分别为1,10,12时完整恢复密钥的总查询次数分别约为1780、232、196，与论文中描述的Kyber786在with clone时(不把构建模板的查询次数算在恢复密钥的查询次数内)的结果一致。


