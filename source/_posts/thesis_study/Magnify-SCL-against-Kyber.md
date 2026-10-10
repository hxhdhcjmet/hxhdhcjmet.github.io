---
title: Magnify-SCL-against-Kyber
date: 2026-08-18 17:41:29
tags:
   - FD Oracle
   - Kyber
   - 侧信道攻击
   - 论文学习
categories:
    - 论文学习
---
# <span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(238, 249, 253);">(2020) Magnifying Side-Channel Leakage of Lattice-Based Cryptosystems With Chosen Ciphertexts: The Case Study of Kyber</span></span>

| <!-- --> |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Author:</span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"> Zhuang Xu; Owen Pemberton; Sujoy Sinha Roy; David Oswald; Wang Yao; Zhiming Zheng;</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Journal: </span></span><span style="color: rgb(255, 0, 0);"><span style="background-color: rgb(243, 250, 244);">, </span></span><span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2020.</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Journal Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Local Link: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);"><a href="zotero://open-pdf/0_SYTRZ4HU" rel="noopener noreferrer nofollow">Xu 等 - 2020 - Magnifying Side-Channel Leakage of Lattice-Based Cryptosystems With Chosen Ciphertexts The Case Stu.pdf</a></span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">URL: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"><a href="https://eprint.iacr.org/2020/912" rel="noopener noreferrer nofollow">https://eprint.iacr.org/2020/912</a></span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Abstract: </span></span>***<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Lattice-based cryptography, as an active branch of post-quantum cryptography (PQC), has drawn great attention from side-channel analysis researchers in recent years. Despite the various side-channel targets examined in previous studies, detail on revealing the secret-dependent information efficiently is less studied. In this paper, we propose adaptive EM side-channel attacks with carefully constructed ciphertexts on Kyber, which is a finalist of NIST PQC standardization project. We demonstrate that specially chosen ciphertexts allow an adversary to modulate the leakage of a target device and enable full key extraction with a small number of traces through simple power analysis. Compared to prior research, our techniques require fewer traces and avoid building complex templates. We practically evaluate our methods using both a reference implementation and the ARM-specific implementation in pqm4 library. For the reference implementation, we target the leakage of the output of the inverse NTT computation and recover the full key with only four traces. For the pqm4 implementation, we develop a message-recovery attack that leads to extraction of the full secret key with between eight and 960 traces, depending on the compiler optimization level. We discuss the relevance of our findings to other lattice-based schemes and explore potential countermeasures.</span></span>* |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Note Date: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2026/8/18 11:15:12</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |


## <span style="color: rgb(224, 255, 255);"><span style="background-color: rgb(102, 205, 170);">📜 Research Core</span></span>

> 这篇论文时间过于久远，甚至Kyber512的私钥系数还是取自$\{-2,-1,0,1,2\}$，因此本篇仅粗略参考学习思路。

***

### Contributions

*   通过自适应策略构建密文，使得仅需极少量trace即可恢复完整私钥。
*   使用SPA在只利用少量trace的情况下验证C implementation 和 pqm4的ARM-specific 均泄露信息因而可以恢复完整私钥（前者泄露多于后者）。

### ⚙️ Content

#### Modular Reduction in Inverse NTT

*   重点考察Kyber解密时的操作：

    $$
    \text{NTT}^{-1}(\text{NTT}(s^T) \circ \text{NTT}(\mathbf u) ) := s^T \circ \mathbf u \mod {^{\pm}q} 
    $$

其中$s^T = (s_0,s_1)$，$\mathbf u^T = (u_0,u_1)$，在Inverse NTT中最后实现逐点模乘，使用Montgomery reduction，在代码实现上使用`fqmul()`函数，而且这个函数是一个(私钥)系数一个系数作为参数调用的，一个重要的发现是，这一函数操作的电磁泄露与输出结果的汉明重量大致呈正相关。以trace的局部泄露最小值为PoI，大致有:

$$
|p(\text{PoI}_i)| \approx a \times \text{HW} ((s^T \cdot \mathbf u \mod {^{\pm}q})[i]) + \mathcal N
$$

这里$a$是放大系数，$\mathcal N$是高斯噪声，关键是利用trace与数据的依赖关系。但这里需要特别挑选$\mathbf u$才能使得不同$s$算出来的结果的汉明重量区别明显，进而可以从traec上区分出来。

#### Constructing Chosen Ciphertexts

*   注意到加密时$u$、$v$是经过`Compress`得到$c_1$、$c_2$；在解密时会先有$c_1,c_2$经过`Decompress`还原得到$u',v'$进行接下来的解密操作，也就是说:

    $$
    \begin{cases}
    u' = \text{Decompress(Compress(u))}\\
    v' = \text{Decompress(Compress(v))}
    \end{cases}
    $$

$u'$在$u$经过压缩和解压缩后可能与原始值不相同！而解密关键操作实际是与$u',v'$密切相关的，因此构建密文直接使用解及压缩后的值。

> 这也是为什么前面那篇”“A Side-Channel Attack on a Higher-Order Masked CRYSTALS-Kyber Implementation”  中搜索私钥系数的编码时$k_0,k_1$不能直接在$\mathbb Z_q$上搜，而应当在压缩后的范围内并解压缩后的范围内搜。

![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/u_v_after_dcompress.png)

*   下面重点考察不同  $u,s$  下的汉明重量  $\text{HW}(s^T \cdot u)$  如下图:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_recovery_full_key_HW1.png)
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_recovery_full_key_HW2.png)

可以看到，通过调整$u_0[0]$的值，当$u_0[0]$非常大或非常小时，利用$\text{HW}(s\cdot u_0 \mod { ^{\pm}q })$(这里实际是模$q$后做中心化(使得最终范围在$-q/2\sim q/2$)并取补码得到最终汉明重量，具体参见复现代码)可以将私钥系数区分成三类：$\text{H}(-2,-1),\text{M}(1,2),\text{L}(0)$。当$u_0[0]$处于中间值时能将$\{-2,-1\}$以及$\{1,2\}$进一步区分开(区分指乘出来的结果的汉明重量差别显著，因而EM trace的PoI上能直接看出明显差别，进而反推出私钥系数每一位)。

*   类似的构建出恢复树如图:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_recovery_full_key_recovery_tree.png)

按照上述恢复树，对于私钥每一位仅需构造两次密文/两条trace即可区分出到底是哪一位。因此理想情况下恢复一维完整的256位私钥系数仅需两条trace，kyber512的完整私钥恢复仅需4条trace。

*   trace分析如下图：
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_recovery_full_key_trace_analysis.png)
对于同一个私钥位置(注意这里 $s[i]$ 对不同 $i$是独立的，可以分别考察)在上图如果为M，在下图为H，最终实际结果就是取上面M和下面H的交集，结果为2，其他情况同理考虑。

#### SPA on ARM-Specific Implementation

*   在pqm4中实现的kyber很多操作都是为了缓存和实现速度而直接写成汇编代码，前面提出的可利用操作包括Inverse NTT、addition 、subtraction都进行了重组，因此此时前一节提到的攻击方式无法应用在本节ARM中实现的Kyber。同样重要的是找到逐系数操作(不同系数之间彼此独立无关)，这里提到的是Encoding/Decoding操作，即将多项式系数编码成易于传输和存储的二进制串，相关操作伪代码如下:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_recovery_full_key_Encoding_Decoding_pseudocode.png)
翻找[pqm4仓库](https://github.com/mupq/pqm4/blob/84c5f91/crypto_kem/kyber768/m4/poly.c#L518)具体代码，对应的两个操作的代码如下:

    ```c
    void poly_frommsg(poly *r, const uint8_t msg[KYBER_INDCPA_MSGBYTES])
    {
      unsigned int i,j;
      #if (KYBER_INDCPA_MSGBYTES != KYBER_N/8)
      #error "KYBER_INDCPA_MSGBYTES must be equal to KYBER_N/8 bytes!"
      #endif
      for(i=0;i<KYBER_N/8;i++) {![\<img alt="" width="821" height="809" data-attachment-key="G8IHUU7Z" src="attachments/G8IHUU7Z.png" ztype="zimage"> | 821](attachments/G8IHUU7Z.png)
        for(j=0;j<8;j++) {
          r->coeffs[8*i+j] = 0;
          cmov_int16(r->coeffs+8*i+j, ((KYBER_Q+1)/2), (msg[i] >> j)&1);
        }
      }
    }
    void poly_tomsg(unsigned char msg[KYBER_SYMBYTES], poly *a) {
      uint32_t t;
      int i, j;
      for (i = 0; i < KYBER_SYMBYTES; i++) {
          msg[i] = 0;
          for (j = 0; j < 8; j++) {
              t  = a->coeffs[8*i+j];
              t <<= 1;
              t += 1665;
              t *= 80635;
              t >>= 28;
              t &= 1;
              msg[i] |= t << j;
          }
      }
    }
    ```

从上述代码和伪代码可以看到，只有当多项式系数在$[q/4,3q/4]$的范围内，对应的二进制串的位才是1，否则是0。相应的，将二进制串转换为多项式系数时，考察二进制串这一位是0(则对应多项式系数$0$)还是1(对应多项式系数$q/2$)。实际攻击既可以利用Encoding操作，也可以使用Deccoding操作，但实验验证Decoding操作的泄露会更适合于SPA，因为mask的HW差异更大(毕竟要么0x00，要么0xff，而t仅1位)更便于区分。

##### O0

*   注意到$m[8i \cdot j]$即$t_{8i+j}$为

    $$
    t_{8i+j}=
    \begin{cases}
    1,\text{if} (q-1)/4 < \text{coeffs}[8 \cdot i + j] < (3q+1)/4\\
    0,\text{otherwise}
    \end{cases}
    $$

    而这里面的$\text{coeff[]}$是我们解密操作解密出来的:

$$
 
\begin{aligned}
\text{coeffs} &= v - \text{NTT}^{-1}(\hat s \circ \text{NTT}(u))\\
			  &= v - (s_0 \cdot u_0 + s_1 \cdot u_1)\\
			  &= v - s_0 \cdot u_0 (\text{let} u_1 = 0)
\end{aligned}
$$

    由于$v,u$都是我们可以选择控制的，因此明文信息位$t_{8i+j}$唯一与密钥系数有关(**而且是一位对一位地、独立地**有关)。

*   选择精心挑选的$u,v$可以实现至多两次查询(两条trace)即可恢复出$s$($m$亦同)的一位：

    $$
    \begin{cases} 
    m_i^{211} = 1, & \text{iff } s_0[i] = -2; \\ 
    m_i^{419} - m_i^{211} = 1, & \text{iff } s_0[i] = -1; \\ 
    m_i^{2705} - m_i^{2913} = 1, & \text{iff } s_0[i] = 1; \\ 
    m_i^{2913} = 1, & \text{iff } s_0[i] = 2; \\ 
    \text{else,} & \text{iff } s_0[i] = 0.
    \end{cases}
    $$

     而想从trace中区分出$m$的某一位是0还是1非常明显直观：

![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_full_key_recovery_trace_distinguish01.png)
在`poly\_frommsg()`编译优化为-O0时从trace上能轻易辨别位为0或1的信息。

*   具体过程分为两步，第一步为选取PoI和阈值T，第二步为从一条收集到的trace分辨出具体明文信息$m$，伪代码如下:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_recovery_full_key_pqm4_O0_persudocode.png)上述这里第一步选取PoI和构建阈值T一般是在样板设备/克隆设备上进行，也可以直接在目标设备上进行，这样可以避免可移植性问题(论文中指出克隆设备一般不会造成这一步的失败)。第二步也可以采用将PoI处的值做二元聚类(K-means)来实现区分。

##### O3
*    O0中选取PoI和计算阈值同时使用了$PoI_{min}$和$PoI_{max}$，而在这里O3优化条件下只利用了$PoI_{min}$，因此后续攻击分类时也只用了$trace_{min}$，且利用阈值的方式也不太一样。

*   相较于O0优化，私钥系数在O3优化下的逐系数操作泄露的信息更不明显，此时使用重复$N$次测量取平均的方式来实现优化和利用trace泄露的信息。具体的伪代码如下:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/SCA_full_key_recovery_O3_persudocode.png)本实验中的重复次数$R = 400$($r_0,r_1$各400)。在第二步正式攻击时同样使用对一个构造出来的密文重复$N$次测量的trace取平均来解密具体信息$m$。结果显示，在大约超过$960$条(每次攻击取$120$次的平均，总共需要$120 \times 4 \times 2 = 960$条，$4$为具体恢复一位所需的trace数，$2$为Kyber512私钥有两个256系数多项式)trace后，完整恢复的成功率稳定在$100\%$。当然也可权衡恢复私钥的准确性(完整性)和暴力计算的复杂度，比如达到$98\%$的准确率($502/512$，每条trace取$23$次后的平均值，总共$23 \times 4 \times 2 = 184$条trace)后，剩下$10$位私钥系数可以直接通过$5^{10}$次的暴力计算给算出来。

## <span style="color: rgb(32, 178, 170);"><span style="background-color: rgb(175, 238, 238);">🔁 Research Content</span></span>

***

### 📜 Conclusion

*   攻击者选定特殊的操作阶段，构造特定的密文，利用解密时所选定的操作阶段泄露的侧信道信息，实现恢复完整信息和私钥。
*   简单的C实现Kyber可以利用解密时Inverse NTT操作泄露的信息，利用少量的trace以极高的概率( $\sim 100\%$ )恢复出完整私钥；在汇编优化的pqm4实现的Kyber，虽然无法直接利用SCA恢复出私钥，但可以以极高概率恢复出完整明文，再利用明文信息与私钥之间的关系恢复出完整私钥。

### Countermeasures

*   私钥不重用/较少私钥的重复使用，这样即使恢复出完整私钥也无法用于下一次攻击。
*   利用masking-based countermeasure或shuffling技术(但这些技术会使得密码算法整体运行开销大大增加)。
*   利用检测机制，当检测到恶意密文时直接丢弃而不直接进行解密操作。因为特殊构建的密文相较于正常密文在结构上有很明显的差异，比如特殊构建的密文会有很多特定位总是0。同时，正常的真实密文本质上应当是LWE上的采样样本，与随机采样不可区分，因此可以通过测量收到的密文的熵来决定丢弃某些恶意密文(比如那些墒值较低的密文)。

## <span style="color: rgb(0, 77, 153);"><span style="background-color: rgb(135, 206, 250);">🤔 Personal Summary</span></span>

***

### 🙋♀️ Key Records

*   这篇论文本质是通过构造FD Oracle来实现利用极少数trace即可恢复完整密钥的攻击方式。因为这里最终是需要恢复出完整的明文信息。
*   本论文中利用的泄漏点都是逐比特/系数操作，即独立性很强的操作，每一位比特/系数只利用该操作处理到它这一位的那一段trace泄露，即可恢复出有关信息。与MV-PC oracle那篇论文对比(以及那篇论文中提到的本篇的FD Oracle的缺点)，本方法只需要（也只能）利用某一时钟周期或少数采样点的数据，因此对噪声非尝敏感，且在更高度优化的如高度平行化、深度流水、固有抖动、深度优化等场景下使用效果大打折扣。
*   该论文中第一种攻击方法之所以可以实现少数几条trace就能恢复完整私钥，是因为一条trace的某一小部分专门反应了 $s$ / $m$ 的一位比特(系数)，具有很高的独立性。这里，如何确定trace中的某一部分就是私钥/明文的这一位(精准定位双射$sk$/$m$ $\leftrightarrow$ precise trace samples)、如何精准的捕获poly\_frommsg()、fqmul()这种很短的操作(相较于前一篇整个的re-encryption过程)是需要解决的问题。


