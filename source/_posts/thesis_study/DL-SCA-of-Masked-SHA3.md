---
title: DL-SCA-of-Masked-SHA3
date: 2026-09-02 18:40:14
tags:
    - DeepLearning
    - 侧信道攻击
    - 论文学习
categories:
    - 论文学习
---
# (2026) Deep-Learning-Based Side-Channel Security Evaluation of Masked SHA-3 Implementation for Post-Quantum KEMs

<table><tbody><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Author:</span></span></strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"> Hibiki Ishikawa; Rei Ueno; Naofumi Homma;</span></span></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Journal: </span></span><span style="color: rgb(255, 0, 0);"><span style="background-color: rgb(243, 250, 244);">IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences, </span></span><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2026CIP0028, 2026.</span></span></strong></p></td></tr><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Journal Tags:</span></span></strong></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Local Link: </span></span></strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);"><a href="zotero://open-pdf/0_XCSP87SM" rel="noopener noreferrer nofollow">Ishikawa 等 - 2026 - Deep-Learning-Based Side-Channel Security Evaluation of Masked SHA-3 Implementation for Post-Quantum.pdf</a></span></span></p></td></tr><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">DOI: </span></span></strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"><a href="https://doi.org/10.1587/transfun.2026CIP0028" rel="noopener noreferrer nofollow">10.1587/transfun.2026CIP0028</a></span></span></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Abstract: </span></span></strong><em><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">This paper presents the security evaluation of masking countermeasures against a deep-learning-based side-channel attack (DLSCA) which targets many post-quantum key encapsulation mechanisms (KEMs). The attack proposed in 2022 exploits side-channel information leaked during the re-encryption process of the Fujisaki–Okamoto (FO) transformation in the decapsulation phase using deep learning techniques. The obtained sensitive information is then used in a chosen-ciphertext attack (CCA) to recover the secret key. Since the FO transformation is commonly used in most post-quantum KEM schemes, the effectiveness of countermeasures against the DL-SCA is critical for tamper-resistant post-quantum KEM implementation. We apply the attack to a set of implementations with masking countermeasures for the post-quantum KEM and experimentally analyze the impact of various factors on the attack success rate, including side-channel information acquisition methods (e.g., sampling rate, points of interest, and segmentation) and neural network architectures. Finally, we demonstrate that masking of at least the 3rd order is required to ensure sufficient security against the DL-SCA.</span></span></em></p></td></tr><tr><td style="background-color: rgb(219, 238, 221);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Tags:</span></span></strong></p></td></tr><tr><td style="background-color: rgb(243, 250, 244);"><p><strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Note Date: </span></span></strong><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2026/9/2 10:28:36</span></span></p></td></tr></tbody></table>

## 📜 Research Core

### ⚙️ Content

- 量化masked KEM的抗SCA特性是很重要的。
    
- 本文完整评估 post-quantum KEMs对DL SCAs的抵抗能力，具体针对SHA-3，综合考虑了神经网络结构、参数设置、trace获取方法等。
    
- PC Oracle $\mathcal O(c;m)$返回$c$是否由$m$加密而来，由于FO变换，攻击者正常情况下无法获知特殊构造密文$c'$的明文$m'’$的任何信息从Decaps过程，但是可以通过SCA构造出这样的Oracle，即比较$\mathcal G(m)$与$\mathcal G(m')$的tracec实现比较$m$与$m'$。
    

#### DL-SCA

- Profiled DL-SCA是现有最有效的SCA工具，包括profiling 和 attack 两个阶段：
    
    - profiling：使用profiling devices和中间变量运行过程中的traces作为数据，训练一个神经网络。这些数据(trace)使用已知、可控制的密钥，拥有与目标设备相同的大量泄露信息(比如前一篇密码学报论文中1阶SHA-3的两份share 的xor操作联合泄露)。
        
    - attack：利用训练好的NN，通过收集target device运行时的trace实现密钥恢复攻击。
        
    
    参数定义如下:
    
    $$\begin{cases}
    \mathcal S_p = \{ (X_i^{(p)},M_i^{(p)}) | 1 \le i \le n_p \}\\
    \mathcal S_a = \{ (X_i^{(a)},M_i^{(a)}) | 1 \le i \le n_a \}
    \end{cases}$$
    

    上述分别代表profiling数据集和attack数据集。定义NN和参数$\theta$：$q(Z | X;\theta)$。profiling阶段的目的就是找 最优参数$\hat \theta$使得NLL(negative log-likelihood，负对数形式损失函数)最小，其定义如下:  
    $L(\theta) = -\frac{1}{n_p} \sum_{i=1}^{n_p} \log {q(M_i^{(p)}X_i^{p});\theta} $

    attack阶段定义所有可能的标签集合为$\mathcal M$，对所有候选$m \in \mathcal M$，计算以下NLL:

$$L^{m}(\hat \theta) = -\frac{1}{n_a} \log {q(m | X_j^{(a)};\hat \theta)}
$$

    标签被用以评价$\hat m = \text{arg} \min_{m \in \mathcal M} L^{(m)} (\hat \theta)$。

- 神经网络结构和超参数会大大影响攻击阶段的表现，因此有多种专门针对SC的神经网络结构被提出(专做CV的CNN结构如VGG就被认为不用于SCA)。同时，标准化方法的差异也被认为会影响攻击阶段的效果。
    

### 💡 Innovations

#### Motivation

- 传统的DL-SCA评估masking 策略时往往集中于整个的复杂操作，比如AES的密钥恢复。Uneo等提出的DL-SCA构造重点实现binary  classifications，利用SHA-3的能量迹，确定PKE解密结果是否是特定明文(特殊构造的密文，解密对应特殊的明文，如全0 or 仅第一bit为1)。这种二分类NN显然比AES的全分类NN更易于构造。
    
- masking countermeasures对SHA-3的保护对于抵御这类DL-SCAs是否依然有效？具体而言，masked SHA-3实现对这类基于DL-SCA的binary classifications的抵御程度如何?
    
- 本论文评估针对ML-KEM在不同场景下的攻击，不同参数包括trace-acquisition settings(采样率、traces数量、采样点数)、masking-order(1、2、3阶)、NN architecture/hyperparameters。
    
## 🔁 Research Content

* * *

### 💧 Data

### 👩🏻💻 Method

#### Trace Acquisition Methods

- Ueno的binary classification使用SHA-3的整个运行过程的trace作为NN的输入。但是在masked implementations时，往往需要结合不同share的泄露来实现攻击(masked能有效抵御DSA，联合share的泄露信息则是针对masked策略的攻击方式)。由于一份share通常在不同的时间点有所泄露(如密码学报的first order masked SHA-3中第一份share先xor，然后padding，然后才是第二份share xor，在SHA-3的trace中精确辨认出这两份share的xor操作是能否实现成功攻击的一大重要因素)。因此trace acquisition settings如sample rate、trarce length等被认为是会对攻击表现有重要影响的。
    
- 本论文实验重点关注三类参数：sampling rate、the number of traces、the number of sample points。
    

#### Masking Order and NN Architecture

- 本论文测试的masking范围为1~3，对应的shares的份额为2~4。
    
- 本论文同时测试了Wouters等提出的NN 结构和Hajar等提出的EstraNet结构。
    

### 🔬 Experiment

#### Trace Acquisition Methods
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/09/DL_Based_SCA_trace_acquisition_methods_result.png)
- 其中蓝线是采样自整个SHA-3过程，结果表现最差(Validation Loss最大)，攻击失败。
    
- 仅采样自最后一轮且采样频率为80MHZ的表现效果最好，最终攻击成功。
    
- 作者在论文中对此的解释为：当有限采样点在长串操作中实施时，相对于时钟频率的采样变得非常低效，因为不同share和不同操作在不同时间点处的泄露都会被整合在一个sample上（也就是没法把这么多的泄漏点都给采到），因此难以提取出有效信息和实现分类。
    
- 因此，仅对SHA-3的最后一轮做采样，有效采样率（effective sampling）能大大提高（后续实验均是该配置，即80MHZ采样率，仅对SHA-3的最后一轮做采样）。
    

##### The number of Traces
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/09/DL_SCA_profile_traces_number.png)

上图展示training data时使用的traces数对Validation Loss的影响，可以看到，从十万增大到三十万条，对Validation Loss的变化（优化）并不明显。注意寻找最小有效攻击的训练所需trace数也是很有必要的（成功攻击的下界）。

##### The number of samples
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/09/DL_SCA_number_of_samples.png)

上述展示了采样的点数对Validation Loss和实际攻击时每次恢复所需要的trace数，可以看到，采样点数的增加对上述攻击性能有极大的影响(优化)。这被认为是trace中更多时序的泄露信息被采集到了，在保持采样率不变的情况下，提高采样数量，不同shares在不同时间上的泄露可以被分别收集到，因此traces中更多的信息泄露点在training 中被利用，这能有效提升学习过程。

##### Masking Order and NN Architecture
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/09/DL_SCA_Model_masked_order_results.png)

上表展示了不同NN architecture和masked order对攻击成功率、每次恢复所需trace数的影响。

- 其中当masked order增加到3（shares为4）时，攻击瞬间失败，成功率骤降。其中随着shares数量的增加，对DL-SCAs的抵御也在增强（论文中提到作者实验时遇到对标签偏向类$1$的回答，而不管实际标签值，这意味着模型自身学习的失败。）对于从二阶掩码到三阶掩码的攻击难度的陡然提升，一个可能的解释是“攻击难度随着掩码阶数成指数增长”；信息论的一种解释为，traces和secret information之间的信息分别随着掩码阶数的增加而呈非线性地降低，导致了所需traces数量地陡然增加 。同时masked order的增加也会使得DL-SCA的训练过程更加困难，从而增强安全性。
    ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/09/DL_SCA_validation_loss.png)

- 上图展示了不同模型的Validation Loss随着迭代次数的变化曲线，可以看到，三阶掩码（四份share）下Validation  Loss并没有减少，一直保持着一个较高的值（而1、2阶掩码的validation loss随着迭代次数的增加而迅速降低并趋近于0）。
    

##### Impact of Training Dataset Size
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/09/DL_SCA_data_size.png)

上图展示了不同阶掩码下攻击成功率随着训练traces数量的变化。

- 可以看到对于二阶和 三阶掩码下，攻击成功率随着训练条数的减少而减少，尤其当traces数降到只有500条时，攻击直接失败了。这种现象可以解释为总的可利用泄露信息（随着训练traces数量减少）的减少。
    

### 📜 Conclusion

- 本论文考察了DL-SCA对maksed implementations of SHA-3 used in pqc KEMs based on the FO transformatoin，实验过程中使用了多种NN模型（包括state-of-the-art,即最先进的模型），结果证明随着masked order 的增加 ，攻击变的越来越困难（尤其是3-order masked直接攻击失败），证明了higher-order masking 是对抗DL-SCAs的有效措施。
    
- 本文最后提出三点未来工作方向：
    
    - 使用更高级深度学习模型和训练技巧等对更高阶掩码的攻击是否变得可行？
        
    - 进一步分析pqc-KEM实现过程中的泄漏点将会对可能的攻击提供更全面的理解。
        
    - 本论文聚焦于软件实现，对于硬件实现是否有其特殊泄漏点（如硬件并行、电路级操作等），因此类似的攻击在硬件实现场景下的攻击分析有待进一步探讨。
        

## 🤔 Personal Summary

* * *

### 🙋♀️ Key Records

- 就本论文的实验结果来看，采样率(采哪一轮、采样频率)、采样点数、训练数据对攻击能够成功影响非常重要，掩码实现的阶数影响也非常重要（比如三阶掩码、四项shares时成功率腰斩，直接攻击失败）。
    
- NN模型分类成功率/攻击成功率在masked order由2变成3后迅速降低，为什么在此处有如此巨大的变化（成功与失败之别），还有待进一步更科学更完整的解释。