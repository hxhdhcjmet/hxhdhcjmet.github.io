---
title: DL_SCAs_Covers
date: 2026-07-29 19:35:31
tags: [kyber,侧信道攻击,深度学习]
categories:
    - 论文学习
---
# Uncover Secrets Through the Cover: A Deep Learning-Based Side-Channel Attack Against Kyber Implementations With Anti-Tampering Covers

> 此篇按论文阅读顺序记录学习内容,而非按一般论文结构

leakage model:泄露模型->秘密到泄露的数学关系。 profiled attack:模板攻击,攻击者已经有一个与目标设备相同/相似的设备,训练阶段学习泄露特征,然后攻击目标设备。

- decryption failure oracle:向系统询问某个问题,得到回答密文解密是否失败。类似padding oracle,服务器回答padding是否合法。
    
- full decryption oracle:完全解密预言机,即选择密文攻击,输入密文得到对应的明文。
    
- plaintext checking oracle:明文检验预言机,攻击者给出(c,m'),预言机回答密文解出来是不是m'.三者强度对比(泄露的信息):Full Decryption > PC > Decryption Failure
    

TVLA(Test Vector Leakage Assessment):用于判断一个密码设备是否存在统计可检测的测信道泄露。基本思路为对于固定输入(fixed):$P = P0$,得到T1,T2,…;对于随机输入组(random):Pi = random,T1’,T2’…。如果设备没有泄露,则两组功耗分布应该类似:T_fixed ≈ T_random,如果存在泄露,则两组统计特征不同。

- TVLV经典使用Welch’s t-test即计算$t = \frac{\mu_1 - \mu_2}{ \sqrt{\frac{s_1^2}{n_1}+ \frac{s_2^2}{n_2}}}$
    
- 其中$\mu$为平均功耗,$s$为方差
    
- 通常$|t|>4.5$即认为存在泄露
    

Deep Learning-based Profiled Attack(DL-PA):

- 使用神经网络自学习来恢复密钥
    
- $NN(Trace) \to state$
    

Structural Slimming Ablation(结构化剪枝消融)

- 并非必须步骤，但常用于深度学习中，删除不重要卷积层、不重要channel 、不重要feature map
    
- 这样做的好处包括:降低模型复杂度，如使得参数从1M减少到100K，进而使推理更块、内存更低；减少过拟合，防止模型学习到过多噪声而不是密钥泄露；提高攻击成功率，通过删除无关特征使得模型虽然更小，但攻击更强。
    
- Slimming不一定有效，如原来模型本来就小，剪枝可能损失性能，同时误删关键泄露层会降低攻击能力，因此需要通过ablation来证明减少的这些层不会损失攻击效果。
    

T-test-based pre-processing:

- 预处理：原始能量迹的采样点非常多，但真正泄露的点很少，直接输入原始能量迹到DL模型中有训练慢、噪声大、容易过拟合等问题，因此需要先找泄露区域。
    
- T-test(Welch’s t-test):思想为比较两组trace的均值(类似上面谈到的TVLA),对固输入(如固定plaintext)得到$T_f$(即得到对应能量迹)，随机输入得到$T_r$,如果无泄漏,两组功耗分布类似：
    
    $$\mu_f \approx \mu_r $$
    
    如果泄露了则均值不同:
    
    $$\mu_f  \neq  \mu_r$$
    
- 对每个时间点$t$计算:
    
    $$T(t) = \frac{\mu_f(t) - \mu_r(t)}{\sqrt{\frac{s_f^2(t)}{n_f}+ \frac{s_r^2(t)}{n_r}}}$$
    
    通过设置阈值(如$|t| > 4.5$)认为该点存在泄露，对泄露区域剪枝保留得到存在泄露的那些点。
    
- 预处理好处在于:减少输入维度、提高训练速度、提高攻击效果
    

Anti-Tampering Covers:防篡改覆盖,这里论文中认为的防篡改覆盖是防止物理解除、篡改、探测芯片，直接影响是增大了EM探针与芯片之间的距离(18mm,24mm),因此降低了EM信号强度，降低SNR，使得能量迹特征泄露减弱，SCA攻击更困难。(本文指出DL-based distinguishers 依然有很高成功率)

With Clone Device:有克隆设备时,在模拟训练阶段使用克隆设备,不受高度限制,在测试阶段使用待攻击设备,因此受高度限制影响。但是该方法受cross-device 问题影响。

作者提出的攻击步骤:

- step0(Optional):对于有克隆设备的攻击者,使用t检测处理traces以获得高信息量的PoIs,后续训练、提取特征、攻击数据集等均基于这些PoIs,以此简化预处理。
    
- step1:使用原始traces训练得到原始模型。
    
- step2:使用Structure Slimming Ablation(参见[NICV:](zotero://note/u/R8RJS2E7/))删去某些层、某些参数以简化模型输入参数,同时还不影响(影响小)模型性能。
    
- step3:使用金字塔结构模型重新构建候选模型.不断以固定比例增加没层的容量,持续该过程直到模型性能降低至某阈值之下,此时停止增加每层的容量。
    

Adaptive Slimmed Pyramid Network Model:

- 第一部分循环:
    
    $$scaling\_factor = scaling\_factor \times (1 + \alpha)$$
    
    因此$scaling\_factor$是递增的,因此
    
    $$L.size = L.size \times scaling\_factor$$
    
    这里$L.size$也是递增的,即金字塔网络结构,从上往下每层增大
    
- 第二部分循环用以增大层的容量以提升提取特征的能力
    
    $$scaling\_factor \gets scaling\_factor \times(1 + \beta)\\
    L.size \gets L.size \times scaling\_factor$$
    
    当前准确率大于阈值($Acc'_{\mathcal{O}ASPN}>t \cdot Acc_{\mathcal{O}ASPN}$)时就尝试增大每层容量(比例为$\beta$)以提升对能量迹特征提取的能力。
    

Comparison of model evaluation:

- ASPN3的容量(3156.50KB)远大于9(980.93KB)主要因为前面算法中的capacity增大过程。

