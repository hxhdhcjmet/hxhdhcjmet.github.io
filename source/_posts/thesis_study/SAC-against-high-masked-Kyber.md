---
title: SAC_against_high_masked_Kyber
date: 2026-08-08 11:59:42
tags:
  - Kyber
  - 侧信道攻击
  - 高阶掩码
  - 论文学习
categories:
  - 论文学习
---
# <span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(238, 249, 253);">(2024) A Side-Channel Attack on a Higher-Order Masked CRYSTALS-Kyber Implementation</span></span>

| <!-- --> |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Author:</span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"> Christina Pöpper; Lejla Batina; Ruize Wang; Martin Brisfors; Elena Dubrova;</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Journal: </span></span><span style="color: rgb(255, 0, 0);"><span style="background-color: rgb(243, 250, 244);">, </span></span><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">14585: 301-324, 2024.</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Journal Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Local Link: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);"><a href="zotero://open-pdf/0_FB22NMU5" rel="noopener noreferrer nofollow">Wang 等 - 2024 - A Side-Channel Attack on a Higher-Order Masked CRYSTALS-Kyber Implementation.pdf</a></span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">DOI: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"><a href="https://doi.org/10.1007/978-3-031-54776-8_12" rel="noopener noreferrer nofollow">10.1007/978-3-031-54776-8_12</a></span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Abstract: </span></span>***<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">In response to side-channel attacks on masked implementations of post-quantum cryptographic algorithms, a new bitsliced higherorder masked implementation of CRYSTALS-Kyber has been presented at CHES’2022. The bitsliced implementations are typically more difﬁcult to break by side-channel analysis because they execute a single instruction across multiple bits in parallel. However, in this paper, we reveal new vulnerabilities in the masked Boolean to arithmetic conversion procedure of this implementation that make the shared and secret key recovery possible. We also present a new chosen ciphertext construction method which maximizes secret key recovery probability for a given message bit recovery probability. We demonstrate practical shared and secret key recovery attacks on the ﬁrst-, second- and third-order masked implementations of Kyber-768 in ARM Cortex-M4 using proﬁled deep learning-based power analysis.</span></span>* |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Note Date: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2026/8/7 10:54:40</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |


## <span style="color: rgb(224, 255, 255);"><span style="background-color: rgb(102, 205, 170);">📜 Research Core</span></span>

***

### Contributions

*   发现了高阶掩码在Kyber上实现的新的易受攻击的点，即在re-encryption过程中Boolean to Arithmetic转变的过程。
*   提出了一种新的选择密文构建方法，对于一个给定的信息比特可以最大化密钥恢复的概率。
*   证明(实现)了现实中在ARM Cortex-M4上的基于profiled deep learning-based power analysis 的对Kyber768实现  $\omega$  阶掩码的密钥恢复攻击。

### ⚙️ Content

#### Attack Description
*   攻击者目标为提取共享信息$K$和/或恢复长期私钥$sk$，其中获取长期私钥$sk$自然蕴含着获取到了共享信息$K$，反之则不然(很自然，因为恢复了$sk$就能解密$ct$,能自行算出共享信息$K$,反之仅有共享信息$K$未必能恢复出$sk$)。

*   Profiling stage:构建模板阶段，攻击者多次重复以下过程:

    *   使用KYBER.CCAKEM.KeyGen()生成密钥对  $(pk,sk)$  ，均匀随机生成消息  $m_p$  ，使用KYBER.CCAPKE.Enc()加密  $m_p$  得到  $c_p$  。
    *   利用上述  $m_p,pk$  调用Encaps()计算得到  $(c,K)$  。
    *   在分析设备运行KYBER.CCAKEM.Decaps()，解封装每一个  $cp_i$  并测量得到对应能量消耗  $tr_i$  。
    > 注意，  $cp_i$  对应的明文信息  $mp_i$  我们是知道的，后面训练模型用的数据是  $mp$  和  $tr$

    重复过程足够多次，收集到足够多数据后，再利用数据集$(mp,tr)$训练一个神经网络模型$\mathcal M$，该模型可以从KYBER.CCAKEM.Decaps()的能量消耗泄露(trace)识别出对应的信息$m$。


## <span style="color: rgb(32, 178, 170);"><span style="background-color: rgb(175, 238, 238);">🔁 Research Content</span></span>

***

### 🔬 Experiment

#### Unprotected Message Encoding

*   将二进制信息  $m$  编码成能参与运算的多项式环中的形式  $f$  ，即  $f[i] = \lceil q/2 \cdot m[i] \rfloor$  ，未经保护实现的C代码如下:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_unprotected_code.png)查看[pqm4源代码](https://github.com/mupq/pqm4/blob/master/crypto_kem/ml-kem-768/m4fstack/poly.c#L556)如下:

```c
void poly_frommsg(poly *r, const uint8_t msg[KYBER_INDCPA_MSGBYTES])
{
  unsigned int i,j;

#if (KYBER_INDCPA_MSGBYTES != KYBER_N/8)
#error "KYBER_INDCPA_MSGBYTES must be equal to KYBER_N/8 bytes!"
#endif

  for(i=0;i<KYBER_N/8;i++) {
    for(j=0;j<8;j++) {
      r->coeffs[8*i+j] = 0;
      cmov_int16(r->coeffs+8*i+j, ((KYBER_Q+1)/2), (msg[i] >> j)&1);
    }
  }
}
```

具体实现差不多，以本论文中实现为例说明：刻意去掉if-else判断$m[i]$是0还是1的逻辑，改为直接移位和与操作，取该比特位到mask。转换成多项式形式对应的系数就是$\text{mask} \& \text{((KYBER\_Q + 1)/2)}$，这样的好处是能防止时间侧信道攻击。但是由于不同$m[i]$得到的mask(0(0x0000)或-1(0xFFFF))的汉明重量差别太大了，后续计算多项式系数也会用到mask，因此可以利用trace差异恢复$m$的比特信息。$m[i]$为0或1的差异如下图:

![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_mask_unprotected_m_diff.png)

可以看到差异很明显，两条线几乎没有重叠部分，也就是说想要从trace区分出$m[i] = 1$和$m[i]= 0$是容易的，前面所述的利用trace恢复$m$是可行的。

#### Masked Message Encoding

*   $\omega$阶掩码是指将原始信息$m$分成$\omega + 1$个份额:$\{m_0,m_1,\cdots,m_\omega\}$,满足$m = \oplus_{i=0}^{\omega}m_i$，每一个份额都可以计算对应的$f_i$，进一步可以恢复出对应的多项式系数:

    $$
    f[j] = \sum_{i=0}^{\omega}f_i[j] \mod q = \lceil q/2  \cdot m[j] \rfloor
    $$
    这里$\Sigma$表示多项式加法合成运算。

*   一种多阶掩码实现([18])的C代码如下：![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_order.png)    
    *   实际一位  $m[i]$  被分成了  $msg \to share[0][i]$  、  $msg\to share[1][i]...$  ，多项式系数也被拆分成了多份分别计算。
*   另一种多阶掩码实现([9])的C代码如下:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_multi_masked_Ccode.png)根本操作类似，都是将原始信息拆分成多份来分别计算，不同之处在于，这里将布尔掩码提取、布尔掩码转换成算数掩码分开了，即先有  $\text{t1[k]} = \text{(m[i + k * stride]>> j) \& 1}$  ，后面再有  $\text{secb2a\_1bit(NSHARES,t2,t1)}$  ；而前者是直接计算完整mask：  $\text{mask = -(msg -> share[k].u8[i] >> j) \& 1}$  。因此前者(mask)的汉明重量最大为16，而后者(t1\[k])的最大为1，因此更难从后者实现中的trace分析提取出Boolean share和明文信息。具体如下图：![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_mask_trace_compare.png)类似之前的图，可以看到下面的两条线([9]的实现)的重叠部分比上面的([18]的实现)更多，因而难以区分。

#### Finding New Leakage Points

*   \[9]的实现将计算Boolean 和 Boolean to Arithmetic给分开了，虽然每次$t1[k]$只泄露1bit信息，但不代表没有其他可利用泄漏点了，本论文就指出了另外两个(实际利用了三处泄漏点，第一处为trivial的Boolean extraction，在此不特意指出)：

    *   *direct-copy：*&#x5728;secb2a\_1bit()中第一句就是直接将x\[0]赋值给a\[0]:
    ```c
    a[0] = x[0];
    ```
    其中x是Boolean share,a是Arithmetic share。

    *   *additive：*&#x5728;secb2a\_qbit\_n()函数中，for循环内有一句：

    ```c
    c[j] -= 2 * b[j] *x
    ```
     这里同样会利用到Boolean share x。注意这么算的原因是异或运算与一般整数运算的关系：
    $$
    x_0 \oplus x_1 = x_0 + x_1 -2x_0 x_1
    $$

<!-- <div align="center"> -->

| x0 | x1 | xor | 右侧 |
| :-: | :-: | :-: | :-: |
| 0  | 0  | 0   | 0  |
| 0  | 1  | 1   | 1  |
| 1  | 0  | 1   | 1  |
| 1  | 1  | 0   | 0  |

<!-- </div> -->
所以Boolean to Arithmetic 需要减去$\text{2 * b[j] *x}$，因此能量消耗与$\text{x}$有关。但是注意到，当$x=0$时，$c[j]$值不发生变化，汉明重量也不发生变化；而当$x\neq0$时，$c[j]$通常会变化，但汉明重量却不一定变化（虽然说一般情况下是会变化的），也就是说，Boolean share $x$的变化不一定导致Arithmetic share $c$的汉明重量变化。而direct-copy中$a$与$x$直接相关，因此(可能)可以认为*direct-copy*的泄露强于*additive*。从以下图片:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_copy_compare_additive.png)
    也可以看出，*direct-copy*的重叠部分小于*additive*，因而更好区分利用。

*   还有一类特殊的泄露:*bit-extraction*，即在第一个函数中将原始  $m$  提取出来计算Boolean share部分涉及到的泄露，但这里无论做不做mask、几阶mask都会涉及到extract操作，因此比较特殊。本论文中后续实验同样会利用这一处的泄露。
*   如下图：![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_diffOrdered.png)

      从这里也可以看到：

*   黑线左侧的bit extraction部分是各种情况下都有且仅有一次的，而且较为明显。
*   右边的B2A阶段，*direct-copy*各阶mask都有且仅有一次，而*additive* 则与mask的阶数成正比(因为除了第一个是直接Boolean to Arithmetic),其他的都要进secb2a\_qbit\_n()；且*direct-copy*的峰要比*additive*的高(callback:即direct-copy的泄露强度高于additive)。

#### New Chosen Ciphertext Construction Method

*   对于Kyber768,私钥$\mathbf s = (s_0,s_1,s_2)$由三个256长的多项式($s_i$)组成，密文$(\mathbf u,v)$中

    $$
    u = \begin{cases} (k_1, 0, 0)^T & \text{for } i=0 \\ (0, k_1, 0)^T & \text{for } i=1 \\ (0, 0, k_1)^T & \text{for } i=2 \end{cases}, \quad v = k_0 \sum_{j=0}^{255} X^j
    $$

    即指在恢复$s_i$时，$\mathbf u$除了第$i$行为$k_1$,其他全为0，而始终为$v = (k_0,k_0,\cdots,k_0)$成立。

*   部分参数解释：  $p$  指恢复信息1bit的正确概率，  $x,x'$  均指代私钥的一位参数(  $\{-2, -1, 0, 1, 2\}$  )，  $d(x,x')$  指将私钥系数  $x,x'$  转变为codeword后的汉明距离，  $b$  指代一位私钥系数转变为codeword后的长度(由于$2^2 < 5 < 2^3$,因此对于私钥系数每一位5种可能，b至少为3)，  $p_x$  指具体一位私钥系数为  $x$  的概率:

$$
p_x = \begin{cases}  1/16, & \text{for } x = -2 \\  4/16, & \text{for } x = -1 \\  6/16, & \text{for } x = 0 \\  4/16, & \text{for } x = 1 \\  1/16, & \text{for } x = 2  \end{cases} 
$$

*   $$
    p_c = \sum_{x} p_x \cdot p^b = p^b
    $$
    这里$p_c$指一个codeword完全恢复正确的概率，这要求$b$个独立无关的codeword位都恢复正确且与具体私钥系数$x$无关。

*   $$
    p_u = \sum_{x} p_x \cdot \sum_{x' \neq x} (1-p)^{d(x,x')} p^{b - d(x,x')}
    $$ 
    $p_u$指恢复出现错误但未检测出来($x$对应的codeword变成$x'$对应的合法codeword)的概率，具体计算原理解释如下：

*  $p_x$  ：私钥系数取值为    $x$   的先验概率。
*  $d(x, x')$  ：系数  $x$  的码字变成系数  $x'$  的码字需要翻转的比特数。
* $(1-p)^{d(x,x')}$   ：这    $d(x,x')$   个比特**全部预测错误**(发生翻转)的概率(错比特概率为$1-p$)。
*  $p^{b - d(x,x')}$   ：剩余的    $b - d(x,x')$   个比特**全部预测正确**的概率。
*  两个    $\sum$   遍历了所有可能发生的“从真实系数  $x$  误判为另一个有效系数  $x'$  ”的转换，并按照  $x$  出现的先验概率  $p_x$  进行加权求和。

*   $$
    p_d = 1 - p_c - p_u
    $$

    $p_d$是指出现恢复错误但被检测出来的概率(合法codeword变成了非法codeword就能被检测出来，而上面的恢复出错但未检测出来就是codeword变成了另一个合法codeword)。

*   $$
    p_{sk} = \sum_{i=0}^{e} \binom{768}{i} p_d^i \cdot p_c^{768-i}
    $$

    $p_{sk}$是私钥全部$768$位恢复正确的概率，即$i$位出错但被检测出来($p_d^i$)，剩下的$768-i$位均完全恢复正确($p_c^{768-i}$)，$e$是可接受$sk$出现错误恢复的最大位数。

#### C\_best & C\_worst

*   由于Kyber768的密钥系数取自 $\{-2,-1,0,1,2\}$ 共 5位( $2^2 < 5 < 2^3$ )，因此采取的编码长度 $b = 3$ ，所谓 $\mathcal C_{best}$ 就是使得 $d(0,x) \ge 2,x \in \{-2,-1,1,2\}$ ，即其他系数与最高概率系数0的codeword的汉明距离最大，因而能使得codeword落入恢复错误但无法检测出来的概率减小(即 $p_u$ 减小)、 $p_d$ 增大，进而最终增大 $p_{sk}$ ；相反 $\mathcal C_{worst}$ 即使得 $d(0,x') = 1$ 对尽可能多的 $x'$ 成立(论文中的是$x' \in \{-1,1,2\}$)，进而使得 $p_{sk}$ 最小。一种可能(并不唯一)的编码方式如下图:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_Cbest_Cworst.png)

*   不同编码的全密钥恢复概率随单比特正确恢复概率( $p$ )的关系曲线如下图:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_CCP.png)在 $p = 0.9991$ 时两者差值达到最大为 $39\%$ 。

*   这个$\mathcal C_{best}、\mathcal C_{worst}$表应当是这么看的：

    *   对于Kyber768解密由$v - s^T u$得到$y = k_0 - k_1 \cdot x$，$x$是私钥系数，解密后按照$y$是更接近$q/2$还是远离$q/2$分别赋值1和0，即：

        $$
        y = \begin{cases}
        1,y \in [-q/4 + q/2,q/2+q/4]\\
        0,y \in [0,q/2-q/4] \cup [q/2+q/4]
        \end{cases}
        $$

    就本处$q = 3329$而言，当算出$y(x) \in [833, 2496]$时，解码为1；当算出$y(x) \in [0, 832] \cup [2497, 3328]$时，解码为0.

    *   以$\mathcal C_{best}$第一行部分为例，将$(k_1, k_0) = (1977, 208)$代入$y(x) = 208 - 1977 \cdot x \pmod{3329}$：

        *   当  $x = -2$  时，  $y(-2) = 208 - 1977 \times (-2) = 208 + 3954 = 4162$  ，模3329取余得  $4162 \pmod{3329} = 833$  ，由于  $833 \in [833, 2496]$  ，因此解码为1。
        *   $x = -1$  时，  $y(-1) = 208 - 1977 \times (-1) = 208 + 1977 = 2185$  ，由于  $2185 \in [833, 2496]$  ，因此解码为1。
        *   当  $x = 0$  时，  $y(0) = 208 - 1977 \times 0 = 208$  ，由于208 < 833，因此解码出来结果为0。
        *   $\cdots$

    *   这里精心挑选的($k_1,k_0$)可以暴力搜索出来，即对总共$3329 * 3329 \approx 1.1 \times 10^7$对$(k_1，k_0)$分别对$x$解码，目标是选出三组密文(即三对参数$\big((k_1^{(1)}, k_0^{(1)}), (k_1^{(2)}, k_0^{(2)}), (k_1^{(3)}, k_0^{(3)})\big)$)，三组参数组合在一起，纵向就构成了5个系数的3bit码字：

        $$
        C(x=-2), \quad C(x=-1), \quad C(x=0), \quad C(x=1), \quad C(x=2)
        $$

          从中筛选出符合要求(最基本要求是每个系数的codeword各不相同，即codeword与sk之间是一一映射)：输入单比特侧信道恢复准确率$p$后，分别计算当前候选参数矩阵产生的$p_c$、$p_u$、$p_d$，然后计算$p_{sk} = \sum_{i=0}^{e} \binom{768}{i} p_d^i \cdot p_c^{768-i}$。寻找$\mathcal C_{best}$就是找使得$p_{sk}$最大的三组$(k_1,k_0)$，算法的收敛条件是：高频出现的系数$x=0$映射出的码字与其它 4 个系数的码字之间的汉明距离满足$d(0, x') \ge 2$。满足此条件的组合之一就是左表中的$(1977,208), (627,208), (731,1040)$。寻找$\mathcal C_{worst}$的过程则正好相反。

#### Neural Network Training

*   本论文中使用在5块板子上收集到的标准化数据做为训练集，同时本论文使用了上述三个泄漏点的数据，因此实现起来会较为繁琐。
*   由于ChipWhisperer-Pro的缓冲区原因，无法采集masked\_poly\_frommsg()过程的所有数据，因此对于1、2阶掩码，收集包含前33bit信息的traces用于训练；而对3阶掩码，则收集包含前17bit信息的traces用于训练。
*   在\[9]中使用了true random number generator(TRNG)和范围检查机制，用于生成掩码，导致了traces的未对齐问题(相同操作在不同的时间点(即采样点)上发生，标准化后会被抹平)。本论文采用cross-correlating with templates的方法来对齐，即为每个泄露点建立模板，其他traces滑动并与模板计算互相关系数，得到的相关系数最大时就认为对齐了，以此方法实现所有traecs的对齐。

#### Experiment analysis

##### Message Recovery Attack
- 对于明文信息的恢复(即trace -> message),随着掩码阶数的增加而概率降低，体现在$p_{bit}$的降低。由于每次执行时随机掩码都会刷新，不同trace上的错误位基本独立，因此可以通过重复$N$次查询来提高$p_{bit}$。
- 通过在$D_{1\sim5}$收集到的trace训练神经网络，并在$D_6$上收集随机选择1000条明文加密过程的trace进行测试，得到的$p_{bit}$如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_ordered_msg_recovery.png)
可以看到:
    - 随着掩码阶数的增加，明文比特恢复的概率会降低($p_{bit}$的确呈下降趋势)；重复次数$N$的增加能有效提高该概率。
    - 完整明文恢复概率$p_m = (p_{bit})^{256}$，在较高阶mask时，当$N$增大至16时，$p_m$方能达到较大值。

#### Secret Key Recovery Attack

- 使用上面训练出来的神经网络，每一密钥系数向量(256位)需要3对密文查询，得到每一位的3长codeword，进而能恢复出密钥每一位系数。使用论文中上表配置的$C_{best}$和$C_{worst}$，得到结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_order_sk_recovery.png)
    可以看到只是编码方式不同($C_{best}$和$C_{worst}$)，在特定的$N$下的full key recovery 概率差异能非常大，总体来说都是$C_{best} > C_{worst}$(当然这种差异随着$N$的增大、$p_{bit}$的增大而会逐渐抹平，而且平均情况来看差别没有那么大，再结合大部分时候都不会达到这种极端情况，因此平均情况下的编码方式造成的full key recovery 概率差异更没有那么大)。





### Code
> 本论文的代码复现主要体现在暴力搜索$C_{best}$、$C_{worst}$和三次查询恢复密钥系数。


#### Bruteforce Search

- 暴力搜索的完整代码如下:
```python
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "tqdm",
# ]
# ///
"""Enumerate every legal 3-query (k1, k0) encoding of the Kyber secret key.

Each query pair (k1, k0) produces one message bit for each possible secret
coefficient x in {-2, -1, 0, 1, 2}.  Three queries therefore give a 3-bit
codeword for every x.  An encoding is legal when the five codewords are all
different.  Swapping the order of the three query pairs does not change p_sk,
so only one representative is kept for each unordered triple.
"""

import argparse
import csv
import math
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from tqdm import tqdm
Q = 3329
N_COEFFS = 768
KEY_VALUES = [-2, -1, 0, 1, 2]
P_X = {-2: 1 / 16, -1: 4 / 16, 0: 6 / 16, 1: 4 / 16, 2: 1 / 16}

# Compress_q(x, 1) = 1 exactly for x in [833, 2496].
LO = 832
HI = 2497

# Kyber-768 ciphertext compression parameters:
# u uses du = 10 bits, v uses dv = 4 bits.
DU = 10
DV = 4


def decompress(c: int, d: int) -> int:
    """Kyber Decompress_q(c, d) for d-bit code c."""
    return ((c * Q) + (1 << (d - 1))) >> d


def msg_bit(k1: int, k0: int, x: int) -> int:
    """One recovered message bit for secret coefficient x under (k1, k0)."""
    t = (k0 - k1 * x) % Q
    return 1 if LO < t < HI else 0


def pattern_of(k1: int, k0: int):
    return tuple(msg_bit(k1, k0, x) for x in KEY_VALUES)


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def compute_probs(codewords, p: float, e: int):
    """Formulas (3)-(6) from Paper 4, Section 9.2."""
    b = 3
    pc = p ** b

    pu = 0.0
    for i, x in enumerate(KEY_VALUES):
        for j, y in enumerate(KEY_VALUES):
            if i == j:
                continue
            d = hamming(codewords[i], codewords[j])
            pu += P_X[x] * ((1.0 - p) ** d) * (p ** (b - d))

    pd = 1.0 - pc - pu

    psk = 0.0
    for i in range(e + 1):
        psk += math.comb(N_COEFFS, i) * (pd ** i) * (pc ** (N_COEFFS - i))

    return pc, pu, pd, psk


def main():
    parser = argparse.ArgumentParser(
        description="Search all legal 3-query (k1,k0) encodings sorted by p_sk."
    )
    parser.add_argument("--p", type=float, default=0.99761,
                        help="per-bit message recovery probability (default: 0.99761, matching the secret-key pbit table)")
    parser.add_argument("--e", type=int, default=16,
                        help="max tolerable detected errors for p_sk (default: 16)")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent / "all_psk_sorted.csv",
                        help="output CSV path")
    args = parser.parse_args()

    if not (0.0 < args.p < 1.0):
        raise ValueError("p must be strictly between 0 and 1")
    if args.e < 0:
        raise ValueError("e must be >= 0")

    print("Building representable (k1,k0) -> 5-bit pattern lookup...")
    pat_map = defaultdict(list)
    # Only pairs that survive Kyber's Compress/Decompress are usable in a
    # real ciphertext.  Enumerate compressed codes and decompress them.
    for c1 in tqdm(range(1 << DU), desc="Pattern lookup"):
        k1 = decompress(c1, DU)
        for c0 in range(1 << DV):
            k0 = decompress(c0, DV)
            pat = pattern_of(k1, k0)
            pat_map[pat].append((k1, k0, c1, c0))

    patterns = sorted(pat_map)
    print(f"Realized patterns: {len(patterns)}")

    print("Enumerating legal unordered pattern triples...")
    results = []
    fail_count = 0
    for tri in tqdm(combinations(patterns, 3), desc="Triple search"):
        # Check if the codewords are all different.
        codewords = [
            (tri[0][i] << 2) | (tri[1][i] << 1) | tri[2][i]
            for i in range(5)
        ]
        if len(set(codewords)) < 5:
            fail_count += 1
            continue

        pc, pu, pd, psk = compute_probs(codewords, args.p, args.e)
        reps = [pat_map[pat][0] for pat in tri]
        rep_flat = [v for rep in reps for v in rep[:2]]
        code_flat = [v for rep in reps for v in rep[2:]]

        results.append({
            "patterns": tri,
            "codewords": codewords,
            "reps": reps,
            "rep_flat": tuple(rep_flat),
            "code_flat": tuple(code_flat),
            "pc": pc,
            "pu": pu,
            "pd": pd,
            "psk": psk,
        })
    print(f"falied try is {fail_count}")
    results.sort(key=lambda r: (-r["psk"], r["rep_flat"]))
    print(f"Legal encodings after removing query-order duplicates: {len(results)}")
    print(f"Distinct p_sk values: {len({r['psk'] for r in results})}")
    print(f"p = {args.p}, e = {args.e}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rank", "p_sk", "p_c", "p_u", "p_d",
            "k1_0", "k0_0", "k1_1", "k0_1", "k1_2", "k0_2",
            "c1_0", "c0_0", "c1_1", "c0_1", "c1_2", "c0_2",
            "pattern_0", "pattern_1", "pattern_2", "codewords",
        ])

        for rank, r in enumerate(results, 1):
            patterns = ["".join(map(str, pat)) for pat in r["patterns"]]
            cw_str = ",".join(
                f"{x}={r['codewords'][i]:03b}" for i, x in enumerate(KEY_VALUES)
            )
            writer.writerow([
                rank,
                f"{r['psk']:.17g}",
                f"{r['pc']:.17g}",
                f"{r['pu']:.17g}",
                f"{r['pd']:.17g}",
                r["reps"][0][0], r["reps"][0][1],
                r["reps"][1][0], r["reps"][1][1],
                r["reps"][2][0], r["reps"][2][1],
                r["code_flat"][0], r["code_flat"][1],
                r["code_flat"][2], r["code_flat"][3],
                r["code_flat"][4], r["code_flat"][5],
                patterns[0], patterns[1], patterns[2],
                cw_str,
            ])

    print(f"Saved {len(results)} encodings to {args.output}")


if __name__ == "__main__":
    # main()
    print(compute_probs([0b110,0b111,0b001,0b100,0b010],0.999,16))
    print(compute_probs([0b110,0b111,0b101,0b100,0b001],0.999,16))
```
- 这里使用了itertools包中的combination函数来枚举所有可能三元组。基本思路为:遍历所有合法$k_0.k_1$组合，得到$\text{Decomp}(k_0 - k_1 \cdot x),x \in \{-2,-1,0,1,2\}$,然后组合三元组，纵向就得到了各个私钥系数的codeword，要求这5个codeword要各不相同(这样才能确保每一个密钥系数唯一可区分)。然后分别对合法的codeword计算对应的$p_c$,$p_u$,$p_{sk}$等，按照$p_{sk}$排序并写入文件。
- 需要注意的是，这里并不是直接遍历$k_0$和$k_1$的$3329 \times 3329$种组合，而是令$k_1=\text{Decomp}(c_1),c_1 \in [0,2^{d_u}]$,$k_0 = \text{Decomp}(c_0),c_0 \in [0,2^{d_v}]$,这是因为后续使用的Kyber768实现中对$k_1$就是先压缩后解压而不是直接参与运算的。存在下面这种情况:
    $$
    \text{Comp}(1000,10) = \lceil    \frac{2^{10}}{3329} \cdot 1000 \rfloor \mod {2^{10}} = 308\\
    \text{Decomp}(308,10) =  \lceil   \frac{3329}{2^{10}} \cdot 308  \rfloor = 1001
    $$
    存在这种搜到的值和实际在Kyber768中参与运算不一样的情况($1000 \neq 1001$)，因此搜索时必须是先压缩后解压缩的范围内进行(一开始不是这样做的最终结果完全不符合预期)。


#### Kyber768

- 构建特殊密文
    ```c
    void enc_paper4(unsigned char *c, int k1, int k0, int select)
    {
    static polyvec Pb;
    static poly v;
    int i;

    memset(&Pb, 0, sizeof(Pb));
    memset(&v, 0, sizeof(v));

    /* k1 is a constant polynomial: only the X^0 term is non-zero. */
    Pb.vec[select].coeffs[0] = (int16_t)k1;
    for (i = 0; i < KYBER_N; i++) {
        v.coeffs[i] = (int16_t)k0;
    }

    polyvec_reduce(&Pb);
    poly_reduce(&v);
    pack_ciphertext(c, &Pb, &v);
    }
    ```
    按照论文中描述的构建密文:$v = (k_0,k_0,\cdots,k_0)$,$u = (k_1,0,\cdots,0)$。

- 密钥系数codeword
    ```c
    typedef struct {
        int k1[3];
        int k0[3];
        int cw[NVALUES];
    } p4_mapping_t;

    static const p4_mapping_t MAPPING_BEST = {
        { 1977, 627,731  },
        { 208, 208, 1040 },
        { 6, 7, 1, 4, 2 }
    };
    static const p4_mapping_t MAPPING_WORST = {
        { 104, 419, 940 },
        { 1040, 416, 1040 },
        { 6, 7, 5, 4, 1 }
    };
    ```
    这里使用的是论文中的$C_{best}$和$C_{worst}$，后续使用前面脚本暴力搜索出来的参数也得到了预期结果。

- **p_bit**
**这是本论文SCA on a Higher-Order  Masked CRYSTALS-Kyber  Implementation的精髓所在**，论文中提出使用掩码实现中Boolean to Arithmetic过程的三处泄露点，利用侧信道泄露训练模板，实现从traces恢复$m[i]$的能力，这个恢复正确的的概率就是$p_{bit}$，随着mask的阶数和重复次数变化而变化。这里由于没有硬件设备，就简化成了纯软件模拟，$p_{bit}$全部是从论文中抄过来的:
    ```c
    typedef struct {
        int order;
        int n;
        double pbit;
    } pbit_entry_t;

    /* Empirical pbit from the paper's Tables 3-5 (message recovery experiments). */
    static const pbit_entry_t MESSAGE_PBIT_TABLE[] = {
        { 1, 1, 0.99928 },
        { 1, 2, 0.99997 },
        { 1, 3, 1.00000 },
        { 2, 1, 0.97203 },
        { 2, 2, 0.99519 },
        { 2, 4, 0.99953 },
        { 2, 8, 0.99959 },
        { 2, 16, 0.99994 },
        { 3, 1, 0.95356 },
        { 3, 2, 0.98219 },
        { 3, 4, 0.99356 },
        { 3, 8, 0.99819 },
        { 3, 16, 0.99994 }
    };

    /* Empirical pbit from the paper's Tables 6-8 (secret key recovery experiments). */
    static const pbit_entry_t SECRET_PBIT_TABLE[] = {
        { 1, 1, 0.99761 },
        { 1, 2, 0.99987 },
        { 1, 3, 0.99995 },
        { 2, 1, 0.97466 },
        { 2, 2, 0.99600 },
        { 2, 4, 0.99970 },
        { 2, 8, 0.99975 },
        { 2, 16, 0.99997 },
        { 3, 1, 0.94794 },
        { 3, 2, 0.98108 },
        { 3, 4, 0.99290 },
        { 3, 8, 0.99793 },
        { 3, 16, 0.99977 }
    };
    ```

- 计算理论$p_c$,$p_u$,$p_{sk}$
    ```c
    static double theoretical_probs(const int *cw, double p, int e,
                                    double *pc_out, double *pu_out,
                                    double *pd_out, double *psk_out)
    {
        double pc = p * p * p;
        double pu = 0.0;
        double pd;
        long double psk = 0.0L;
        long double binom = 1.0L;
        int i, j;

        for (i = 0; i < NVALUES; i++) {
            for (j = 0; j < NVALUES; j++) {
                if (i == j) {
                    continue;
                }
                {
                    int d = hamming_distance(cw[i], cw[j]);
                    pu += PX[i] * pow(1.0 - p, d) * pow(p, 3 - d);
                }
            }
        }

        pd = 1.0 - pc - pu;
        if (pd < 0.0) {
            pd = 0.0;
        }

        for (i = 0; i <= e; i++) {
            if (i > 0) {
                binom *= (long double)(768 - i + 1) / (long double)i;
            }
            psk += binom * powl((long double)pd, i) *
                powl((long double)pc, 768 - i);
        }

        *pc_out = pc;
        *pu_out = pu;
        *pd_out = pd;
        *psk_out = (double)psk;
        return *psk_out;
    }
    ```
    这里是根据输入(论文中是model测得的)的$p_{bit}$计算全密钥系数恢复的概率$p_{sk}$,与之后模拟器运行测试结果做对比(模拟器恢复出来的$sk'$中，正确恢复$sk$的位数为correct，则模拟器测试的$p_{sk}'$就是correct / 768)。

- 测试主逻辑

    ```c
        for (t = 0; t < trials; t++) {
            static unsigned char pk[CRYPTO_PUBLICKEYBYTES];
            static unsigned char sk[CRYPTO_SECRETKEYBYTES];
            static unsigned char ct[CRYPTO_CIPHERTEXTBYTES];
            static polyvec skpoly;
            unsigned char entropy_input[48];
            int select;
            int j;
            int trial_detected = 0;
            int trial_undetected = 0;

            for (j = 0; j < 48; j++) {
                entropy_input[j] = rand() & 0xFF;
            }
            randombytes_init(entropy_input, NULL, 256);
            crypto_kem_keypair(pk, sk, &skpoly);

            for (select = 0; select < KYBER_K; select++) {
                unsigned char obs[3][KYBER_INDCPA_MSGBYTES];
                int q;

                for (q = 0; q < 3; q++) {
                    unsigned char m_true[KYBER_INDCPA_MSGBYTES];

                    enc_paper4(ct, m->k1[q], m->k0[q], select);
                    indcpa_dec(m_true, ct, sk);
                    memcpy(obs[q], m_true, KYBER_INDCPA_MSGBYTES);

                    for (j = 0; j < KYBER_N; j++) {
                        int bit = get_msg_bit(obs[q], j);
                        int true_bit = get_msg_bit(m_true, j);
                        double r = (double)rand() / ((double)RAND_MAX + 1.0);

                        total_bits++;
                        if (r >= pbit) {
                            bit ^= 1;
                        }
                        if (bit == true_bit) {
                            correct_bits++;
                        }
                        set_msg_bit(obs[q], j, bit);
                    }
                }

                for (j = 0; j < KYBER_N; j++) {
                    int idx = value_index(skpoly.vec[select].coeffs[j]);
                    int cw;
                    int kind;
                    int k;

                    if (idx < 0) {
                        continue;
                    }

                    cw = (get_msg_bit(obs[0], j) << 2) |
                        (get_msg_bit(obs[1], j) << 1) |
                        get_msg_bit(obs[2], j);

                    if (cw == m->cw[idx]) {
                        kind = 0;
                    } else {
                        kind = 2;
                        for (k = 0; k < NVALUES; k++) {
                            if (k != idx && cw == m->cw[k]) {
                                kind = 1;
                                break;
                            }
                        }
                    }

                    if (kind == 1) {
                        trial_undetected++;
                        total_undetected++;
                        total_coeff_errors++;
                    } else if (kind == 2) {
                        trial_detected++;
                        total_detected++;
                        total_coeff_errors++;
                    }
                }
            }

            if (trial_undetected == 0 && trial_detected <= e) {
                successes++;
            }

            if (trials >= 10 && (t + 1) % (trials / 10) == 0) {
                printf("  [%d/%d] pbit=%.6f psk=%.4f\n",
                    t + 1, trials,
                    (double)correct_bits / (double)total_bits,
                    (double)successes / (double)(t + 1));
            }
        }
    ```
- 这里利用$p_{bit}$的原理是，对每一位生成随机数$r$,如果$r \ge p_{bit}$,就将明文这一位翻转，最终得到模拟经由SCA训练得到的model恢复的、每一位恢复正确率为$p_{bit}$的原文信息。
- 利用实际正确的密钥系数位和三次查询出来的结果对比，将结果分为三类：`kind=0`恢复正确、`kind=1`恢复错误且无法检测出来、`kind=2`恢复错误且能检测出来。

#### Result
- 论文中给出的运行结果如下图：
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_masked_thesis_result.png)

- 用论文中参数测试3阶掩码下重复$8$次的结果如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_mask_simulation_result.png)
可以看到与论文中的结果相近，符合预期。其中较大的差异还是来自这里的$p_{bit}$是每一位随机翻转的，而实际实验中的恢复错误可能是集中在某些部分而不是平均分布在所有位上。

- 使用暴力搜索出来的$C_{best}$和$C_{worst}$运行测试结果如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/20260813163907905.png)
可以看到与论文的$C_{best}$和$C_{worst}$还是有些不同的，但整体趋势相同。


- 论文中参数下理论计算与模拟恢复出来的$p_{sk}$对比图如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_mask_thesis_data_results_psk_pbit.png)

- 使用脚本暴力搜索出来的参数测出的理论计算与模拟恢复结果的$p_{sk}$对比如如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_against_high_mask_BP_data_results_psk_pbit.png)

总体来软件模拟的结果与理论计算的结果符合得还不错.




### 📜Conclusion

*   使用基于深度学习的能量分析能恢复高阶掩码保护的Kyber私钥和共享秘密。
*   发现了新的任意阶掩码中Boolean to arithmetic实现的易攻击点所在，本论文中的攻击亦说明了为了抵御能量分析攻击，该掩码转换实现需要进一步加强。
*   选择密文的不同( $\mathcal C_{best}\quad \text{vs}\quad  \mathcal C_{worse}$ )造成完整私钥恢复概率的至多 $39\%$ 的差异。

## <span style="color: rgb(0, 77, 153);"><span style="background-color: rgb(135, 206, 250);">🤔 Personal Summary</span></span>

***

### 🙋♀️ Key Records

*   本论文提出针对 $\omega$ 阶masked Kyber实现中，Boolean to Arithmetic过程存在新的泄漏点，因而基于这些泄露点展开攻击。
*   本论文采用5块板做数据采集和训练并攻击另外的第6块板子的配置，以解决跨板(环境)攻击问题。同时为解决TRNG带来的未对齐问题，采用求相关系数的方法实现对齐。
*   本论文提出新的选择密文方法，透过构建对密钥系数的不同编码方式( $\mathcal C_{best},\mathcal C_{worse}$ )可以造成至多 $39\%$ 的全密钥恢复概率差异。

