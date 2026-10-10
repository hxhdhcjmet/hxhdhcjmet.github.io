---
title: MV_PC_oracle_experiment
date: 2026-08-17 10:53:29
tags:
    - 论文复现
    - Kyber
    - 侧信道攻击
categories:
   - 论文学习
---
# MV PC Oracle Experiment
> 本文记录对MV PC oracle论文中的实验复现过程，目前仅测试了Kyber768，后文Kyber专指Kyber768


## 实验环境
- ChipWhisperer Husky Kit
- Kyber高性能库pqm4
- 本机计算机
> 实验过程中大部分代码为指导AI工具辅助生成


## 实验过程

### 主机实现Kyber
为了后续实验训练模板获取数据、验证目标板上Kyber运行是否正确等，需要在本主机上实现Kyber。这里借助软件模拟复现的代码实现Kyber，关键在于能根据指定并行数$P$，生成对应$2^P$种明文对应的密文，数据送往目标板收集trace并训练模板。

这里为了便于生成确定的密钥，将原来使用opessl库的随机数生成器替换为自行实现、自行指定种子的简易随机数生成器。实际随机数仅在生成Kyber的参数($A$,$s$,$e$)时使用，目标板上使用的是主机同一套密钥，在目标板运行时由主机上传。

### 训练模板

#### 收集trace
在主机生成$2^P$对明文和对应密文，将其传入目标板，收集目标板re-encryption过程中的能量泄露。目标板上main.c代码如下:
```c
#include "hal.h"
#include "simpleserial.h"
#include "kyber_src/api.h"
#include "kyber_src/params.h"
#include "kyber_src/indcpa.h"
#include "kyber_src/symmetric.h"
#include "keypair.h"
#include <stddef.h>
#include <string.h>

static uint8_t g_ct[KYBER_CIPHERTEXTBYTES];
static uint8_t g_sk[KYBER_SECRETKEYBYTES];

static void send_bytes(char marker, const uint8_t *data, int n)
{
    int i;
    putch(marker);
    for (i = 0; i < n; i++) {
        putch((char)data[i]);
    }
}

int main(void)
{
    uint8_t m_dec[KYBER_INDCPA_MSGBYTES];
    uint8_t buf[2 * KYBER_SYMBYTES];
    uint8_t kr[2 * KYBER_SYMBYTES];
    const uint8_t *pk = g_sk + KYBER_INDCPA_SECRETKEYBYTES;
    unsigned char fail;
    uint16_t len;
    int i;

    platform_init();
    init_uart();
    trigger_setup();
    memcpy(g_sk, default_sk, KYBER_SECRETKEYBYTES);

    while (1) {
        uint8_t cmd = (uint8_t)getch();
        if (cmd == 'K') {
            uint16_t klen = (uint16_t)((uint8_t)getch() << 8);
            klen |= (uint8_t)getch();
            if (klen != KYBER_SECRETKEYBYTES) {
                send_bytes('E', NULL, 0);
                continue;
            }
            for (i = 0; i < KYBER_SECRETKEYBYTES; i++) {
                g_sk[i] = (uint8_t)getch();
            }
            putch('R');
            putch(0x01);
            continue;
        }
        if (cmd != 'C') {
            continue;
        }

        len = (uint16_t)((uint8_t)getch() << 8);
        len |= (uint8_t)getch();
        if (len != KYBER_CIPHERTEXTBYTES) {
            send_bytes('E', NULL, 0);
            continue;
        }

        for (i = 0; i < KYBER_CIPHERTEXTBYTES; i++) {
            g_ct[i] = (uint8_t)getch();
        }

        /* Decryption happens before the trigger window. */
        indcpa_dec(m_dec, g_ct, g_sk);
        memcpy(buf, m_dec, KYBER_SYMBYTES);
        memcpy(buf + KYBER_SYMBYTES,
               g_sk + KYBER_SECRETKEYBYTES - 2 * KYBER_SYMBYTES,
               KYBER_SYMBYTES);

        /* Re-encryption is the measured region. */
        trigger_high();
        hash_g(kr, buf, 2 * KYBER_SYMBYTES);
        fail = indcpa_enc_cmp(g_ct, buf, pk, kr + KYBER_SYMBYTES);
        trigger_low();
        (void)fail;

        send_bytes('R', m_dec, KYBER_INDCPA_MSGBYTES);
    }
}
```
上述$K$命令用于接收新的私钥(由主机上传本次解密所使用的私钥)，$C$命令用于接收待解密密文$ct$,能量泄露的收集范围(`trigger_high()`与`trigger_low()`之间)为计算

$$
(\bar K,r) = \mathcal G(m,\mathcal H(pk))\\
ct' = \text{CPA.Encrypt}(pk,m,r)
$$
的过程,其中$m$提前由`indcpa_dec(m_dec,g_ct,g_sk)`解密而来，该过程不再能量泄露利用范围内。

训练模板时共需要$2^P \cdot T$次查询(条trace),本实验只有一套设备，因此相当于论文中的without clone,总恢复密钥的查询次数需要包括训练模板时的查询次数(远大于正式攻击时的查询次数)。


#### 构建分类器

- **疑问**：论文中描述的是利用二元分类器，对待分类trace分别用一个二元分类器确定出结果，不断缩小范围，最终实现多元分类器的功能。也就是说，对于$2^P$中明文，需要
$$
\begin{pmatrix}
 2^P\\
2
\end{pmatrix} = \frac{2^P(2^P-1)}{2} = 2^{P-1}(2^P-1)
$$

种模板，即任意两种明文之间都要建立一对模板。当$P = 4$时需要120种模板，此时尚可接收；当$P=10$时，需要$512 \times (1024-1) = 523776$种模板，此时构建五十多万种模板，计算和存储都需要不小的开销；当$P=12$时，需要$2048\times(4096-1) = 8386560$，八百多万套模板，计算和存储几乎不可接受。

显然这里模板的构建是与分类器的原理密切相关的，**为什么不能用待分类trace与$2^P$种模板分别计算SSD/SAD,取最小者为分类结果?** 这种多元分类器只需要构建$2^P$种模板($P=10$时为$2^{10} = 1024$种)，计算和存储开销都能低很多。因此本实验后续同时实现了这两种方法并做了比较。

- 同时比较分类器
##### 提取PoI
- 以$P=8,T=5$为例详述过程，首先收集$2^8 \times  5 =1280$条trace，将所有数据归一化$\frac{x-\bar x}{\sigma}$后，先绘制原始轨迹和类间均值，查看数据是否有效，结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/p8t5_sample_traces.png)
    可以看到结果有效，可以继续下一步。
- 先以`class0`和`class1`为例，逐点计算Welch t-test:
    $$
    \text{t-value} = \frac{\mu_1 - \mu_2}{ \sqrt{\frac{\sigma^2_1}{T} + \frac{\sigma^2_2}{T}}}
    $$
    分别绘制`abs(t-value) —— time`在前50000和所有采样点上的图如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/t-value-time.png)
    这里以论文中的t-threadhold为5作为参考红线，有如下观察结果:
  - 几乎所有的点的`abs(t-value)`都在5以上，以此为阈值挑选PoI必然不可行，因为数量太多了，必须要提高阈值。这里的结果也说明本实验收集到的trace具有丰富的信息，有大量的泄露点可以利用。
  - 后约10万采样点(约3万个左右)部分的`abs(t-value)` 显著地大于前10万个采样点的`abs(t-value)`，这说明信息/能量主要在采样的后半程($ct' = \text{CPA.Encrypt}(pk,m,r)$)偏结束处泄露，这部分操作数据相关远远大前面部分($(\bar K,r) = \mathcal G(m,\mathcal H(pk))$)。 

- 此时的一个问题是如何选取PoI，这里我采用的方法是:分别令所有其他类的trace与类0计算`t-value`并提取大于阈值的点作为PoI，这些PoI取并集，作为分类器运行分类时参与计算的点。
- 之所以使用并集是考虑到PoI既要满足精简，又要能有丰富的信息，取交集无法提取到$2^P$类共有的特征点，但注意到取并集时使用论文中的阈值能提取到约6万个PoI,这个数量还是太多了，虽然能非常有效地提取信息，实现精准分类，但计算和存储的开销显得太大了，为解决这一问题，可以采用继续提高阈值或收集`abs(t-value)`最大的前$k$个点作为PoI等方法，本实验考虑采用后者，因为这样能明确指定PoI的个数且无需根据具体配置($P,T$)判断阈值的选取。
##### 模板与分类
- 共$2^P$种模板为每种用于训练的trace的PoI上的能量消耗的均值。
- 先采用非论文中的两两比较分类器，对于一个待分类trace，取PoI处的部分数据，做归一化后分别与$2^P$种模板计算SSD/SAD,最小者即表示trace为那一类。
- 上述每类$T=5$条trace中，3条用于训练模板，2条用于测试模板分类效果，结果均得到100%的准确性。
  
##### 进一步精简PoI
- 用每一类与类零计算`t-value`，则`t-value`为$2^P-1 \times \text{samples}$的二维数组，让这个数组在每个sample点上取$2^P-1$个`abs(t-value)`的最大值作为参考值，得到一个新的一维`score`数组，该数组的每一位记录着该采样点下与类0的`abs(t-value)`的最大值。

- 取`score`中共计$k$个`abs(t-value)`最大的、彼此间距大于`min_dis`的点作为PoI。
    - 注意到后约10万个点的`abs(t-value)`显著大于前面，因此也可将取的$k$个PoI局限在后10万采样点中。但实际这一步没有必要，全局前$k$个最大与后10万点的前$k$个最大是完全一致的，缩小搜索范围需要自己指定大约从哪里开始搜，这个位置实际是不固定的，**实验过程中还遇到了**一开始将这个搜索范围限制的太小，导致漏掉了一些特征点，分类准确率下降的问题。
- 使用精简后的PoI作为模板并进行分类测试，同样取得了100%的分类准确率。这套精简模板作为后续真正展开攻击使用的模板。采样的PoI位置如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/p8t5_refinePOI.png)
使用的是从0开始搜索，PoI大小为200。


### 攻击恢复密钥
> 由于不同构建分类器方式不影响攻击恢复步骤，因此先介绍攻击恢复密钥，后面再介绍两两比较分类器，这也符合实际实验过程

#### 恢复一块
- 先测试恢复一块密钥一块$P=8$，检测是否能恢复成功。此时使用Python脚本，根据分类结果作为并行Oracle的返回结果来构建下一步密文，该过程与论文中描述以及软件模拟操作相同(完整详细代码参见仓库)。一块(8位私钥)仅3次查询就能恢复，结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/P_block_recovery.png)
可以看到，一块恢复完全成功，共$2^8 \times 5 + 3 = 1280+3 = 1283$次查询。

#### 密钥一行恢复和完整密钥恢复
- 由上面能成功恢复密钥一块，考虑继续恢复剩下的完整密钥，结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/recovery_s0.png)
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/recovery_full_key.png)
可以看到能成功正确恢复Kyber768的完整$256 \times 3 = 768$位密钥，其中攻击查询次数不超过$\frac{768}{8} \times 3 = 288$次(实际为283)，总共的密钥恢复总查询次数为1563次。


### 构建二元比较分类器
- 再考虑实现论文中的二元比较分类器。$2^P$分类器需要$\begin{pmatrix}
 2^P\\
2
\end{pmatrix}$种模板，此时PoI(同样做了精简)不再是所有其他类与类0计算`t-value`并取PoI并集，而是两个要比较的类间单独计算`t-value`并取出前$k$大的作为PoI。也就是说，每一对模板需要(作为二元分类器那样)单独取PoI，不同类之间的PoI(大概率)是不同的。
> 一个很明显的不同是，此时一对间的PoI不需要考虑与其他对之间的关系，因此可以只考虑这一对之间的特别的差别，因而PoI的数量大大降低，往往50左右就有精确的效果，而全类别考虑的分类器PoI在$P=10$时$PoI=250$都无法实现精确分类，这在后续的进一步实验中发现。

- 就如同前面的疑问中所述，这种分类方式最然每一对的一个模板的PoI很小(比如这里$P=8$,$T=5$时，$k=30$即可达到完整攻击恢复密钥需求，后续$P=10$,$T=3$时，$k=30$亦可完成精确恢复密钥)，但由于所需模板数量过多，因而计算和存储开销也较大。
- 攻击恢复密钥效果类似，同样能完全正确恢复768位私钥，具体截图就不贴了，跟前面一样的。

## 进一步测试
### P=10,T=3
- 进一步测试论文中$P=10$的情况，考虑到此时收集的trace数量和存储巨大，而本实验环境与论文中的不完全相同(论文中用的是EM探针)，可以认为本实验收集到的能量泄露更精确、$SNR$更大，因此未使用论文中的$T=5$，而是$T=3$来构建模板(后续实验结果证明，$T=3$在本实验环境中已经够用了)。
- 构建模板时首先使用我提出的全分类法，选择$k=300$，即300个$PoI$，分类与测试结果如下:
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/k_500.png)
  可以看到$k=200$时无法达到100%准确率，而$k=300$及往后就都能达到100%的分类准确率，因此此时有必要将PoI数量提升到至300。
- 恢复完整密钥结果及查询次数：
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/p10t3_full_key_recovery.png)
  显示不含构建模板的查询次数为233，与论文中给出的232是相符合的。

- 再考虑二元比较式分类器，此时使用的两类间PoI为50(注意这种方式训练模板数量多，耗时也比前者多得多)， 同样能实现完整密钥的恢复,不含构建模板的查询次数与使用全分类器相同，为$233$。


### P=6,T=1

- 测试论文中提到的without clone device 的最少总查询次数的配置，此时由于每一类仅收集一条trace，因此没有测试trace用来评价训练出来的模板的准确性。
- 完整密钥恢复的结果如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/p6t1_ful_key_recovery.png)
包括构建模板共计437次查询，与论文中的结果完全一样。



## 实验总结

- 本实验遵照MV PC oracle的论文描述复现了不同并行度下对Kyber768的密钥侧信道密钥恢复攻击，取得了与论文中(几乎完全)相同的预期结果。
- 论文中提出的二元比较式分类器和我想到的全分类器有各自不同的特点:
    - pairwise 比较式需要为每两对间都构造一套模板，总计需要$\begin{pmatrix}
 2^P\\
2
\end{pmatrix}$份模板，随着$P$的增大，该数量增长非常快，导致构建模板时的计算与存储开销较大。但这种方式能充分利用比较的两类之间的特殊差异来选取PoI,因此每套模板所需要的PoI个数往往很少。
    - 全比较式分类器统一提取所有类与类别0计算的`t-value`来提取PoI的并，并取前$k$位(pairwise也会取前$k$位)作为PoI，仅需构建$2^P$套模板即可，分类时令待分类trace分别与这$2^P$套模板计算SSD/SAD，取最小者即为对应类别。整体计算和存储开销会小很多，但需要选取的PoI个数比pairwise的大得多，才能取得相同的分类准确度(pairwise一般$30 \sim 50$个点即可，全分类器需要$200$个以上的点)。
- t-test结果显示后半程有更多更显著的泄露点/差异，此阶段显然为加密阶段，结合论文中的原文:

> In particular, there are two distinct peaks (over multiple samples) with very high t-test values. Upon inspection, we identified it to be the sampling of polynomials of r from the CBD distribution (Line 11 of CPA.Encrypt in Alg.1). The attacker however does not require this information to perform the attack.

- 实验结果也验证了这一点，加密过程中采样$r$造成了大量的信息泄露，显然这里$r$的采样与待加密明文$m$有关(虽然攻击者不需要知道这一点，只需要知道re-encryption有大量可利用PoI即可)。
    - 阅读板子中实现的源代码可以发现，噪声的产生源自链路coins->PRF->CBD,这里
    $$
    \text{coins} = (\text{SHA3-512}(m' || h)) \text{last 32 bytes}
    $$
    即取上述后32字节作为coins,由于SHA3-512的强雪崩效应，$m′$的1比特差异都会造成coins的巨大差异，因此可以说m′决定了$(r,e1,e2)$，噪声是明文$m′$的确定性函数，中间隔了一层SHA3-512。
---
# 关于本论文的一些思考
- 以Kyber768为例，我们发现对于每次并行恢复一块$P$位的私钥系数时，这一块总的查询次数取决于最多需要查询的那一位。也就是说，即使$P-1$位两次查询就能确定具体私钥系数，剩下一位还需要一次查询时，整块其他系数都要陪着它再查一次，参考Kyber768BDT:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Parallel_PC_Oracle_BDTkyber768_1024png)

    也就是说虽然一块里面大部分系数两次查询就能恢复，但由于少数系数($-2,-1$)的存在需要第三次查询，恢复整块$P$个系数的查询次数基本上就是$3$。那么，**能否每一块将两次查询后未恢复的系数标记出来，直接进入下一次查询，依此类推，直到最后再统一最后一次查询来恢复这些还差一次查询就能确定的系数呢？** 换句话说，**是否必须完全恢复当前块私钥系数后，才能进入下一块私钥系数的恢复？**。

- 关于上述疑问，我的思考回答是：**必须完整恢复完一整块私钥系数后才能进入下一块的恢复**。这是因为特殊密文的构造方式，当我们希望恢复第$k$块系数时，即私钥系数:
$$ 
(s_{kP},s_{kP+1},\cdots s_{kP+i},\cdots,s_{kP+P-1})
$$
此时我们构造的密文是：
$$
\begin{cases}
v = \sum_0^{P-1} \lceil \frac{q}{2^{d_v}} \rfloor \cdot t\\
u = -\lceil \frac{q}{2^{dv}} \rfloor \cdot x^{N -kP}
\end{cases}
$$
也就是说，$\mathbf u$仅在第 $N-kP$ 处取系数$k_u = -\lceil \frac{q}{2^{dv}} \rfloor$，只有这样，才能将这一块私钥对应解密结果旋转到信息的$0\sim P-1$位上：
$$
\begin{aligned}
u\cdot s_{kP+i} &= k_u \cdot s_{kP+i} x^{N-kP} \cdot x^{kP+i}\\
                &= k_u \cdot s_{kP+i} x^{N+i}\\
                &= -k_u \cdot s_{kP+i} x^i  \quad (x^N=-1)\\
                &= \lceil \frac{q}{2^{dv}} \rfloor \cdot s_{kP+i}x^i
\end{aligned} 
$$
上述推导说明了，这样的$u$能将私钥$s$的第$k$块中的第$i$个系数旋转至明文第$i$位(或者说第0块的第$i$位)，解密结果只可能是$m$的前$P$位有不为0的值，其他明文位置均为0，这也就能利用起分类器并进行后续攻击。
而上述的疑问则是能否将不同块的不同位置的私钥都旋转到第一块来，这显然是不行的，假设待处理的私钥位为:
$$
    (s_{k_1P + i_1},s_{k_2P + i_2},\cdots,s_{k_nP+i_n})
$$
则第$k_1$块的需要$k_u[N-k_1P]$,第$K_1$块上的需要$k_u[N-k_2P]$,...最终$\mathbf u$变成:
$$
    \mathbf u = \sum_{i=1}^{n}k_u[N-k_iP]x^{N-k_iP}
$$
此时$\mathbf u \cdot s$存在这样的项:
$$
    k_u[N-k_mP]x^{N-k_mP} \cdot s_{k_nP + i_n}x^{k_nP + i_n},n \neq m
$$
不失一般性的，我们令$m=1,n=2$，则结果如下:
$$
    \begin{aligned}
    k_u[N-k_1P]\cdot s_{k_2P+i_2}x^{N-k_1P+k_2P+i_2} =k_u\cdot s_{k_2+i_2}x^{k_2P-k_1P+i_2} 
    \end{aligned}
$$
显然我们不知道这次的这个项$k_2P-k_1P+i_2$对应哪一块，即这个私钥将影响明文哪一位是不确定的。如果它落到明文$0\sim P$之外，那没特别影响，解密出来还是0；如果它落入$0\sim P$中，再加上这样的项还有很多，还有很多其他可能的项也落入$0 \sim P$中，也就是说，此时$0 \sim P$位的明文中，**可能一位明文不止受到一位私钥系数的影响，这与本论文要求的明文一位受到私钥一位的影响相矛盾**，因此上述修改方法完全无法继续采用本论文的攻击方法。


## 与FD Oracle的对比
-  在阅读完本论文、做完实验复现后，又进一步阅读了论文中提到的FD Oracle的两篇论文(分别是"Magnifying Side-Channel Leakage of Lattice-Based Cryptosystems With Chosen Ciphertexts: The Case Study of Kyber"和"On Exploiting Message Leakage in (few) NIST PQC Candidates for Practical Message Recovery and Key Recovery Attacks")，我对本论文使用的MV-PC oracle和FD oracle的不同点有了更多理解，整理出来大致如下:

| 对比维度                        | MV-PC Oracle                                                                                       | FD Oracle                                                                                                |
| --------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **基本思想**                    | 通过 chosen ciphertext 让多个 message bits 同时依赖多个 secret coefficients，再利用一个较长计算过程中的侧信道泄露构建多分类 PC oracle | 通过 chosen ciphertext 使完整 decrypted message 的各 bit 与对应 secret coefficient 建立关系，再利用特定操作中的细粒度泄露恢复整个 message |
| **Oracle 本质**               | Parallel Plaintext-Checking Oracle；一次 oracle response 可提供 (P) bit 信息                               | Full-Decryption Oracle；一次 trace 可恢复整个 256-bit decrypted message                                          |
| **目标泄露**                    | **Target-Operation Independent**：不依赖某个特定操作的某一个精确泄露，可综合利用多个操作/较长计算过程中的 leakage                      | **Target-Operation Dependent**：依赖特定操作中稳定、可定位、与敏感数据直接相关的细粒度 leakage                                       |
| **目标操作范围**                  | 较宽，可利用整个 re-encryption 等较长过程中的大量 PoI                                                               | 较窄，通常针对 message encoding/decoding、NTT/fqmul 等特定操作                                                        |
| **敏感数据与泄露关系**               | 不要求某一个 PoI 与某一个 secret coefficient 建立直接一一映射；主要通过整体 leakage 区分不同 message class                      | 通常要求建立 **PoI ↔ message bit ↔ secret coefficient** 的明确对应关系                                                |
| **一次 trace 的信息量**           | 可恢复 (P) bits；论文实验中达到 (P=10)，即最多区分 (2^{10}=1024) 类                                                  | 理想情况下可恢复完整 256-bit message                                  |
| **每个 bit 的泄露窗口**            | 不要求单个 bit 只有一个极窄的泄露窗口，可以综合多个 PoI                                                                   | 通常非常窄，一个 bit 可能只有一个 clock cycle 或少量 samples 的泄露                                                          |
| **Trace 中有效信息的分布**          | **较分散、较宽**：很多时间区域/PoI 都可能参与分类                                                                      | **较集中、较细粒度**：存在大量局部 PoI，但每个 bit 对应的有效窗口很短                                                                |
| **Trace 对齐要求**              | 通常相对宽松；重点是找到能够稳定进行分类的 leakage region / PoI                                                         | 通常更严格，需要准确定位不同 bit/coefficient 对应的操作位置；尤其需要建立 trace 时间位置与具体处理对象之间的对应关系                                   |
| **对噪声/SNR 的敏感程度**           | 相对较低：可综合多个 PoI，并可通过 averaging/classification 抵抗部分噪声                                      | 相对较高：单 bit 的有效 leakage 可能只有很少 samples，因此低 SNR 很容易破坏对应关系                                                  |
| **所需 trace/query 数量**       | 相比传统 binary PC 大幅降低，但通常仍多于理想 FD；第一篇实验中不同场景下可达到数百次 query                                            | 通常极少；例如 Xu 等人的 Kyber512 attack 可用 8 次 query 完成 key recovery，第一篇引用其 FD attack 为 6 queries 的改进结果           |
| **为什么 trace 数量较少/较多**       | 虽然每次可以获得 (P) bit，但分类能力受到 (P)、SNR、template 数量等限制                                                    | 一次 trace 本身携带大量 bit 信息，因此 query efficiency 极高                                                            |
| **对具体实现的依赖**                | **较低**；重点依赖算法层面的 chosen-ciphertext / message-secret 关系，因此可迁移性较强                                    | **较高**；目标操作的具体实现、编译优化、指令序列、pipeline、jitter 等都可能改变或消除细粒度 leakage                                          |
| **对微架构差异的适应性**              | 相对更好；第一篇强调其 generic / implementation-agnostic 特性                                                   | 相对较差；第一篇特别指出复杂平台上的 heavy parallelism、deep pipelining、jitter 可能使这类攻击更加困难                                  |
| **Profiling / Template 需求** | 可以使用 clone device 建立多分类 templates；没有 clone device 时也可以直接在 target 上完成 preprocessing，但成本会快速增加        | 不一定需要 template；例如 Xu 2021 使用 SPA 避免复杂 templates；但基于 message-storage 的 FD 实现通常需要 profiling/template       |
| **预处理成本**                   | 当 (P) 增大时 template 数量为 (2^P) 级增长，因此 preprocessing 成本可能成为主要瓶颈                                       | 如果使用 profiling，需要为不同 message/bit 建立模板；但具体方法差异很大                                                          |
| **Chosen ciphertext 的作用**   | **同时控制多个 secret-dependent message bits 的位置和数量**，实现 parallelization                                 | **建立 (m_i=F(s_i)) 的逐 bit/逐 coefficient 对应关系**，从而让完整 message 成为 secret 的“代理”                              |
| **主要攻击对象**                  | PC oracle；也可用于 re-encryption / decapsulation 中较宽范围的 leakage                                        | FD oracle；典型为 message encoding/decoding/storage，也包括某些直接 key recovery 的细粒度操作                              |
| **典型 leakage**              | re-encryption 过程中的综合 leakage；第一篇实验甚至不需要 message encoding leakage                                   | message encoding/decoding/storage 的 bit-wise leakage；或者 inverse NTT/fqmul 等逐 coefficient leakage         |
| **Countermeasure 影响**       | 对针对特定操作的 countermeasure 具有较强绕过能力；例如第一篇实验表明 message encoding shuffling 不影响其攻击，因为它不依赖该 leakage       | 与目标操作直接相关，因此针对该操作的 shuffling/masking 等防御通常更可能直接影响攻击；但 ciphertext malleability 等方法也可能进一步绕过这些防御            |
| **算法泛化性**                   | **较强**；第一篇认为可推广到类似 LWE/LWR KEM，如 Saber、FrodoKEM | **相对较弱**；必须找到目标算法/实现中具有足够稳定性的具体操作泄露(如精细到fqmul()、Encoding/Decoding中取mask的操作等)                                                                     |
| **实现泛化性**                   | 较强：同类算法不同实现通常只需重新寻找合适 leakage/classifier                                                           | 较弱：操作实现稍有改变，都可能导致原来的 PoI、leakage model 或 timing 关系失效                                                     |


## 两类分类器的对比
- 就所需模板数量而言，两种方式所需模板数量随并行度$P$变化结果如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/compare_2P_C2P.png)
    很明显论文中提到的构建模板方式所需的模板数量随着$P$增大而增大的速度远大于我所提出的方案。同时实验也验证了，论文方案每对模板所需的PoI数量远小于我的方案，这是因为，论文方法每一对类别单独做 t-test，所以 PoI 只需要关注这两个类别之间最有区分度的地方；我的方案所有类别相对于 class 0 的 t-test 来寻找 PoI，因此这些 PoI 必须能够同时区分大量类别。所以单个 PoI 的“局部针对性”下降了，需要更多 PoI 才能获得同样准确率。
  
- 总结成一句话大概就是：**Pairwise classifier 以大量 templates 为代价，换取每个 classifier 对 PoI 的高度针对性；Global classifier 则以更多 PoI 为代价，将大量pairwise templates 压缩为仅 2P个 class templates。**

- 除此之外还有构建模板阶段的计算开销，对于$M = 2^P$个模板、$K$个`PoI`：
   - Global:
    $$
    O(MK)
    $$
    因为一条trace分别与M个template计算SSD/SAD。
   - Pairwise:
  $$
    O(\binom{M}{2}K_{pair})
  $$
  虽然实际二分类过程不一定要把所有pair都跑一遍，但模板构建/存储规模依然是$O(M^2)$。

- 综上，对比使用情况推荐大致如下表
 
| 场景 | 推荐 |
|---|---|
| (P) 较小，例如 (P=$4\sim6$) | Pairwise 可以接受，PoI 少，分类针对性强 |
| (P) 较大，例如 (P=$8\sim10$) | Global 更有实际意义，可避免 ($\binom{2^P}{2}$) 模板爆炸式增长 |
| Trace SNR 较低 | Pairwise 更有优势，因为可以集中使用解释性最强的PoI |
| 存储/模板训练成本受限 | Global 更有优势 |
| 希望最大限度减少 PoI | Pairwise |
| 希望减少模板数量 | Global |
| 希望简单实现 | Global |
| 希望严格复现论文方法 | Pairwise |


---
# 关于复现实验代码
> 二编自8.22日，上述首次实验是在8.15


- 在后续审查代码的过程中(一编是用deepseek v4 flash 接入Codex写的代码（17号涨价前抓紧完成代码撰写）；二编用claude opus 4.8接claude code修的代码)，发现代码实现偏离论文和我的预期，关键在于训练模板时$2^P$种明文对应的密文的构造方式上。一开始，代码采用类似正式攻击时密文的构造方法，对明文每一位，选取本次会旋转的私钥$s[n]$，查找使得$v[i] - u[N-n]s[n]$对应$m_i[i]$符合要求的$u$，比如对于$m = 5 = \text{0b}0101$，代码会想办法使得构造出来的密文旋转至第0位解密结果为1，第1位为0，第二位为1，其余位都为0。诚然这样构造能实现构造出$2^P$种明文对应的密文，且训练时的密文与最终攻击时的密文结构类似，但这里在构造训练数据时居然要知道私钥???这显然不合理！正如论文原文中描述二元分类器时提到的:
>At no point during any of the two phases, does the attacker require to operate the target device with known secret keys.

- 因此正确的构造私钥方法是:选取$2^P$中明文，各自调用加密机得到对应密文，拿这组数据做训练，这样构造密文时完全不需私钥，符合论文描述和现实攻击要求。
-  两种情况下构造出来的训练阶段数据如下图，上图为错误构造，下图为正确构造
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/MV_PC_oracle_experiment_wrong_train_ciphertext.png)
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/MV_PC_oracle_experiment_right_train_ciphertext.png)
    可以看到，后者杂乱无章的密文才符合我们的预期。
- 后续重复上述实验，得到的结果几乎完全相同(因为我们采集训练数据是解密后明文重加密过程，解密后的明文都是一样的，后续过程可以说完全一样，且攻击阶段是没问题的)，因此不再修改替换上述实验过程描述。这里也印证了，我们利用的是re-encryption过程，与公钥$pk$密切相关，而与其他因素关系不大(密文是如何构造的，以及解密过程)，修改密钥(公钥)时必须重新训练模板。
- 实际写代码时与我的提示词有关，因为后者修改我也是经过与claude反复确认、验证(看过代码还嘴硬说第一版是对的)和提示后才修改正确的。这说明**想要AI写出正确的代码，前提是自身完全明晰实现细节与逻辑，同时后期代码审计必不可少！**

---
# 关于实验的讨论
>  三编自8.24，实验完与师兄讨论后对实验过程的一些问题做了探讨，因此后续继续补充部分实验

- 在做完实验与师兄讨论后被指出实验的一些问题:
    1. 如何保证目前采集的trace就是论文中提到的re-encryption部分？因为实际上CWHUSKY的捕获逻辑是这样的,triger_high()后触发开始捕获的信号，直到采集满指定数量的sample即停止，而不管tirger_low(),也就是说,triger_low()并不是采集停止的信号，当triger_high()和triger_low()包裹的范围太长，我们指定的采样点个数无法将这期间的操作全部采集下来，将只能采集一部分操作的点；当triger_high()和triger_low()包裹范围的操作太短，采集完了还没有达到指定的采集点个数，则会继续采集trigher_low()后面的操作，直到采满。（根据师兄的经验，目前13w个采样点完全不足以覆盖G(m,H(pk))和Enc(pk,m,r)两个操作的，只不过这个实验较为简单，可利用/泄露点过多，实验总能取得很好的结果）。
    2. 考虑添加一些空转、噪音以及使trace未对齐等操作，降低trace质量，看看此时神经网络分类器与简单的SAD/SSD分类器相比，是否会有准确率的提升(后续实验可能采用EM trace且面对高噪声环境，NN的更高分类准确率可能更适合未来的实验)。

## 修改捕获范围
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/only_G.png)
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/only_recryption.png)
以上两张分别为将trigher_high()放在$(K,r) = \mathcal G(m,\mathcal H(pk))$前面和后面的两种采集到的trace的类0与类1的`t-test`曲线，可以看到两条曲线稍有平移关系，后者的高`t-test-value`部分来的更早、更长，这说明:
1. 主要的泄露来自后面`re-encryption`且是来自较后面的操作。
2. 两种情况都没有完整采集`re-encryption`的(IND_enc_cmp()操作)过程，因为如果完整采集，后面应当是一些空转噪声，`t-test-value`在采集后面必然不会这么高，而应当趋于0.
   
## 添加空转噪声
- 在$\mathcal G$函数处理完毕后、重新加密之前添加了一段100w次的空转循环，试图将重加密过程排除在采样范围外，部分代码如下:
```c
trigger_high();
hash_g(kr, buf, 2 * KYBER_SYMBYTES);
for (volatile int i = 0; i < 1000000; i++);// empty function
trigger_low();
fail = indcpa_enc_cmp(g_ct, buf, pk, kr + KYBER_SYMBYTES);
```
此时采集到的trace类0与类1计算`t-test`得到的曲线如图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/100wempty_function.png)
可以看到整段都是`t-test-value`不太大的trace，明显将后面的加密过程排除在采样范围之外。空转操作与具体解密数据关系不大，因此`t-test-value`差别很小。主要是前面的$\mathcal G$函数计算处有少许较明显(泄露强度远远低于重加密)泄露。