---
title: Grafted_Tree
date: 2026-08-06 17:59:09
tags:
    - Kyber
    - 侧信道攻击
categories:
    - 论文学习
---
# <span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(238, 249, 253);">Grafted Trees Bear Better Fruit: An Improved MV-PC SCA against Kyber</span></span>

| <!-- --> |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Author:</span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);"> Jinnuo Li ,Chi Cheng ,Muyann Shen ,Peng Chen ,Qian Guo ,Dongsheng Liu ,Liji Wu ,Jian Weng;</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Journal: </span></span><span style="color: rgb(255, 0, 0);"><span style="background-color: rgb(243, 250, 244);">,</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Journal Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Local Link: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);"><a href="zotero://open-pdf/0_6AXIJJ9X" rel="noopener noreferrer nofollow">Grafted Trees Bear Better Fruit An Improved MV-PC SCA against Kyber.pdf</a></span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">URL:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Abstract: </span></span>***<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">As a prominent category of side-channel attacks (SCAs), plaintext-checking (PC) oracle-based SCAs offer the advantages of generality and operational simplicity on a targeted device. At TCHES 2023, Rajendran et al. and Tanaka et al. independently proposed the multiple-valued (MV) PC oracle, significantly reducing the required number of queries (a.k.a., traces) in the PC oracle. However, in practice, when dealing with environmental noise or inaccuracies in the waveform classifier, they still rely on majority voting or the other technique that usually results in three times the number of queries compared to the ideal case.</span></span>* |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(219, 238, 221);">Tags:</span></span>**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">Note Date: </span></span>**<span style="color: rgb(25, 60, 71);"><span style="background-color: rgb(243, 250, 244);">2026/8/6 10:49:31</span></span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |


## <span style="color: rgb(224, 255, 255);"><span style="background-color: rgb(102, 205, 170);">📜 Research Core</span></span>

***

### Contributions

*   提出一种针对Kyber的高效的基于侧信道的MV-PC oracle attack,且专门设计在非完美oracle上，关键创新点在提出了一种新颖的方式来有效探测并纠正MV-PC oracle的错误。
*   研究重点为Kyber,但本论文方案实际有通用性，能用于类似结构的方案如Saber、Frodo等。
*   在高噪声环境中改进方案以适应这种情况，后续的分析证明相较 majority voting，本论文方案可以有效减少查询次数同时保持较高的准确率。

### ⚙️ Content

#### Binary PC Oracle

*   具体参考先前文章[Mismatch-lower-bound.md](http://localhost:4000/2026/08/04/thesis_study/Mismatch-lower-bound/),同样的特别选择  $m、c_1、c_2$  ,利用  $m_0$  来恢复  $s[i]$

#### MV-PC oracle

*   具体参考先前文章[MV_PC_Oracle.md](http://localhost:4000/2026/08/07/thesis_study/Parallel-PC-Oracle/),特别选择构造的$u、c_2、v$来实现将$s$的前$N$位与$m$的前$n$位有关，其中$N$为并行度：

    $$
    m'[i] = \begin{cases}
    \lceil (2/q)(\lceil (q/32)k_i  \rfloor) -s_0[i](\lceil q/32 \rfloor)\rfloor \mod 2 ,i = 1,2,\cdots,N-1\\
    \lceil (2/q)( 0 -s_0[i](\lceil q/32 \rfloor)\rfloor \mod 2 = 0,i \ge N
    \end{cases}
    $$

### 💡 Innovations
#### Challeges and Solutions
- 无论是PC Oracle还是MV_PC oracle，都是基于侧信道攻击的，实际使用中其准确度是可能会受环境噪声和针对侧信道攻击的保护措施影响的，分类器自身的性能也会影响oracle准确率。传统解决方法为使用majority voting:假设oracle返回每一位的准确率为$\alpha$,在经过$t$轮的majority voting后，准确率变为:
    $$
    \alpha' = 1 - \sum_{s=0}^{\lfloor t/2 \rfloor}\begin{pmatrix}
    t\\s
    \end{pmatrix}\alpha^s(1-\alpha)^{t-s}
    $$
    以上式子是说经过$t$轮的majority voting 后准确率变为1减去$t$次投票中正确次数少于一半的概率。该函数绘制成图如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/20260812110501668.png)
  可以看到随着投票轮数$t$的增加，oracle的准确率也会增加，(可以说,majority voting能放大/增强oracle的效果，即原本oracle具有较大(大于50%)的准确率时，majority voting能增大准确率；原本oracle准确率较低时，majority voting则会降低准确率)，但查询次数也会随着$t$的增大而大大增加。

#### Grafted tree for key recovery

*   考虑到噪声等影响，认为第一轮MV-PC oracle出来的$sk$是不完全正确的，只是一个大致正确的结果，还需要进一步验证。具体本论文的操作步骤分为三轮:

    *   Round1:MV-PC Oracle 获得初步大致的  $sk$  (这一步实际上是完整恢复所有密钥位)。
    *   Round2:基于上述的大致恢复结果  $sk$  ,**为每一位选择特定的两轮grafted tree**,再做parallel key recovery验证，结果如果  $\text{Round2} == \text{Round1}$  ,则认为这些部分是正确的  $sk$  (的部分比特)，如果  $\text{Round2} != \text{Round1}$  ，就将这一块标记为suspicious(只要parallel的块中有某一位在一二轮结果不同就整块标记为suspicious)，待$\text{Round3}$进一步验证。
    *   Round3:对那些标记suspicious的块再做一次recovery，三轮结果做majority voting确定最终结果，至此就能(较精准地)恢复完整  $sk$

*   上述过程中提到选择特定的两轮grafted tree,就是指对这一位做两次(不同 $k$ )验证就能确定具体值，因为的确对每一位系数都能找到深度为2的BRT(准确来说是对第一轮恢复出来的$s[i]$,都存在特定选择密文实现两轮验证它到底是不是$s[i]$)，如下表格：![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_illustrate.png)

> 比如对kyber1024,某一位在Round1恢复出来是-2,那么两轮对 *k* 就分别是( 7,8 )(见Kyber-1024第一行)，如果Oracle结果是两次都是1，则 $Round2 == Round1$ ，否则标记为suspicious。

*   以Kyber1024,Round1结果为$(1,-2,2,0)$为例解释后续创建grafted tree 和Round2、Round3的具体操作:

    *   首先对照上表： $1、2$ 应选择( $k_1 = 9,k_2 = 10$ )， $-2、-1$ (虽然本例没有-1)应选择( $k_1 = 7,k_2 = 8$ )， $0$ 应选择( $k_1 = 8,k_2 = 9$ )。
    * > 注意事实上 $k_1，k_2$ 是可以调换顺序的，但此时对应的Oracle结果也得调换过来看，比如 $k_1 = 8,k_2 = 7$ 时 $-1$ 对应的Oracle 结果就应该是(10)，本论文中对-2的两个参数选择就与表中的不一致，但不妨碍正确性。

    *   按照上述选择原则，Round2的第一层grafted tree( $k_1$ )指导我们选择 $c_2 = (9,8,9,8,0,\cdots,0)$ ，以此做Oracle得到序列 $m_1'$ 。

    *   同样依照上述原则选择第二层( $k_2$ ),此时为 $c_2 = (10,7,10,9,0,\cdots,0)$ ，同样做Oracle得到序列 $m_2'$ 。

    *   对于上表的kyber1024总结成以下表:

        | -2 | -1 | 0 | 1 | 2 |
        | -- | -- | - | - | - |
        | 1  | 1  | 0 | 0 | 0 |
        | 1  |  0 | 1 | 1 | 0 |


        所以如果对于原来$(1(01),-2(11),2(00),0(01))$,如果$,m_1' = 0100$且$m_2' = 1101$，那么就认为Round2恢复出来的$sk$也是$(1,-2,1,0)$，与Round1的相匹配。否则两轮不一样的就认为不匹配并标记为suspicious，需要Round3以进一步确定。

#### Comparison in Round 2

*   本论文较前面(binary PC Oracle、P-way Parallel PC Oracle)的关键优化在于Round2,其他方案依然重复做完整的key recovery，平均每一块(一位或是多位组成的一块)恢复的平均查询次数是随着  $N$  变化的，而本文使用grafted tree,无论  $N$  如何变化，查询次数始终为2，具体对比如下图:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_trace_compare_round2.png)

#### Threshold for accuracy

*   计算最小可接受(**#EvError** <1)的准确度(PC Oracle的准确度)，该准确度作阈值，当accuracy低于该阈值时，恢复出来的密钥  $sk$  的平均错误位数大于1，认为结果可靠性差、此时是高噪声低准确度环境，反之就认为此时是低噪声环境。
*   计算阈值方法就是手动调整Oracle 的准确度，并在此时做attack，统计恢复的  $sk$  的平均错误位数(**#EvError**)，结果如下图:![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_accuracy_threshold.png)

 这里可以看到几个(大致)的Oracle accuracy阈值都在97%以上，后文的95%、90%都是高噪声低主准确度环境。

## <span style="color: rgb(32, 178, 170);"><span style="background-color: rgb(175, 238, 238);">🔁 Research Content</span></span>
### 📜 Conclusion

*   本论文提出的优化MV-PC oracle-based side-channel attack利用grafted tree在高噪声、低精度(需要多轮来提高最终准确率)的其概况下能有效减少恢复完整密钥的Oracle 查询次数(较TCHES 2023有超过42.5%的减少)。同时对FireSaber、Frodo-1344的实验攻击进一步证实了本论文提出的方法的通用性。
*   为进一步验证本论文所述方法的通用性，还补充了在更低(Oracle)准确度(平均  $sk$  错误位数大于1)的情况下的实验，此时本方法需要结合majority vote，实验结果证明在更高噪声和更低准确度条件下本论文方法依然能有效减少总的查询次数(超过22.8%的减少)。
*   实际攻击破解时可以结合本论文方法与offline 暴力破解，即Oracle恢复  $sk$  部分比特，剩下部分暴力计算，这样能进一步减少所需的查询次数。

## <span style="color: rgb(0, 77, 153);"><span style="background-color: rgb(135, 206, 250);">🤔 Personal Summary</span></span>

***

### 🙋♀️ Key Records

*   在有噪声的真实环境中为了提高恢复出来的密钥 $sk$ 的准确度，一般方法是做重复的全文恢复和majority voting，此时恢复每一位的平均查询次数与第一次的相同(如P-way parallel PC Oracle都是$\text{2.xxx}$)。而本文提出的grafted oracle则指出在这种情况下，Round2并不需要做与Round1相同的参数配置，而是针对Round1的结果选择特定的grafted tree的参数配置，此时Round2平均一位恢复的查询次数都是2( 小于前两篇文献中的$\text{2.xxx}$ ，且该确定值2能有效证明).
*   本论文中的Round3只需要对Round1和Round2中不相匹配而被标记为suspicious的块再次恢复并对三轮结果做majority voting。一般方法几轮中做的$sk$ recovery方法完全相同,查询次数各轮也完全相同,因此本论文方法的总查询次数较一般方法明显减少。

### Code
- 类似于Parallel PC Oracle那篇论文，本论文同样没有给出代码，这边尝试复现了本论文的代码，与前篇论文的高度类似，重叠部分在此不做赘述，重点阐述新加部分代码。

- Round2根据Round1的粗略结果$sk$,每一位有针对地选择两位参数$(k_1,k_2)$:
  ```c
    static void grafted_pair(int prior, int *h1, int *h2)
    {
        int t1, t2;

        if (prior <= -1) {
            t1 = -2; t2 = -1;
        } else if (prior == 0) {
            t1 = -1; t2 = 0;
        } else {
            t1 = 0;  t2 = 1;
        }
        *h1 = H_ZERO + t1;
        *h2 = H_ZERO + t2;
    }
  ```
  这里是针对Kyber1024/768实现的，不支持Kyber512。符合论文中描述的，$(-2,-1)$一组参数$(k_1,k_2) = (7,8)$、$0$一组参数$(k_1,k_2) = (8,9)$、$(1,2)$一组参数$(k_1,k_2) = (9,10)$.
- 根据Round2的两轮查询结果确定$s$:
    ```c
    static int decode_unique_from_pair(int h1, int h2, int bit1, int bit2)
    {
        int found = INVALID_COEFF;
        int i;

        for (i = 0; i < NVALUES; i++) {
            int s = values[i];
            int b1 = (s <= (h1 - H_ZERO)) ? 1 : 0;
            int b2 = (s <= (h2 - H_ZERO)) ? 1 : 0;

            if (b1 == bit1 && b2 == bit2) {
                if (found != INVALID_COEFF)
                    return INVALID_COEFF;  /* ambiguous */
                found = s;
            }
        }

        return found;
    }
    ```
    这里以Kyber1024,$(-2,-1)$对应的$(7,8)$为例，`s <= (h_1 - H_ZERO) = s<=(7-9)=-2`、`s <= (h_2 - H_ZERO)  = s <= (8-9) = -1`,显然 $-2$ 对应结果为 $(11)$,$-1$ 对应结果为$(01)$,恰好符合论文中的表，其他都是错误情况，返回`INVALID_COEFF`。

- Round2具体查询函数:
    ```c
    static void recover_group_grafted(const unsigned char *sk,
                                    int select,
                                    int group_start,
                                    int n,
                                    double accuracy,
                                    const int *round1,
                                    int *recovered,
                                    int *suspicious,
                                    int *query_count)
    {
        static int hlist1[MAX_PARALLEL];
        static int hlist2[MAX_PARALLEL];
        static int klist[MAX_PARALLEL];
        static unsigned char ct[CRYPTO_CIPHERTEXTBYTES];
        int i;
        int block_mismatch = 0;

        /* determine h1, h2 for each coefficient based on Round 1 prior */
        for (i = 0; i < n; i++) {
            grafted_pair(round1[i], &hlist1[i], &hlist2[i]);
        }

        /* ---- Query 1: klist = hlist1 ---- */
        for (i = 0; i < n; i++) klist[i] = hlist1[i];
        enc_mvpc(ct, klist, group_start, select, n);
        (*query_count)++;

        {
            int class1 = oracle_mvpc(ct, sk, group_start, n, accuracy);

            /* ---- Query 2: klist = hlist2 ---- */
            for (i = 0; i < n; i++) klist[i] = hlist2[i];
            enc_mvpc(ct, klist, group_start, select, n);
            (*query_count)++;

            {
                int class2 = oracle_mvpc(ct, sk, group_start, n, accuracy);

                /* decode each coefficient and check for mismatches */
                for (i = 0; i < n; i++) {
                    int bit1 = (class1 >> i) & 1;
                    int bit2 = (class2 >> i) & 1;
                    int prior = round1[i];

                    /* expected bits if Round 1 were correct */
                    int t1 = hlist1[i] - H_ZERO;
                    int t2 = hlist2[i] - H_ZERO;
                    int exp1 = (prior <= t1) ? 1 : 0;
                    int exp2 = (prior <= t2) ? 1 : 0;

                    recovered[i] = decode_unique_from_pair(hlist1[i], hlist2[i],
                                                        bit1, bit2);

                    /* flag block-level mismatch */
                    if (bit1 != exp1 || bit2 != exp2) {
                        block_mismatch = 1;
                    }
                }

                /* block-level suspicious: all coefficients in this group */
                if (block_mismatch) {
                    for (i = 0; i < n; i++)
                        suspicious[i] = 1;
                }
            }
        }
    }
    ```
    这里符合论文中提到的Round2做两次查询:`int class1 = oracle_mvpc(ct, sk, group_start, n, accuracy);`和`int class2 = oracle_mvpc(ct, sk, group_start, n, accuracy);`,提取出这两轮每一位的查询结果存在`bit1`和`bit2`中，`exp1`和`exp2`分别存第一轮恢复出来的$s$测试$t_1$和$t_2$的结果，如果第一轮恢复的是正确的,那么必然有`bit1 == exp1 && bit2 == exp2 `,否则这一位在round1和round2的恢复结果就不同，此时将当前恢复块(parallel处理的所有私钥系数)全部标注为suscipious。

- 完整三轮攻击流程:
    ```c
    static int attack_paper3(const unsigned char *sk,
                         const polyvec *skpoly,
                         int parallel,
                         tree_mode_t mode,
                         double accuracy,
                         int *total_errors,
                         int *r1_errors,
                         int *r2_errors,
                         int *suspicious_count,
                         int *r1_queries,
                         int *r2_queries,
                         int *r3_queries)
    {
        int select, j;
        int total_queries = 0;
        int r1_q = 0, r2_q = 0, r3_q = 0;
        int ncoeffs = KYBER_K * KYBER_N;

        /* allocate per-coefficient arrays: r1, r2 (grafted), r3 (re-run), susp */
        int *r1   = calloc((size_t)ncoeffs, sizeof(int));
        int *r2   = calloc((size_t)ncoeffs, sizeof(int));
        int *r3   = calloc((size_t)ncoeffs, sizeof(int));
        int *susp = calloc((size_t)ncoeffs, sizeof(int));

        if (!r1 || !r2 || !r3 || !susp) { *total_errors = -1; return -1; }

        /* mark r2, r3 as INVALID initially */
        {
            int idx;
            for (idx = 0; idx < ncoeffs; idx++) {
                r2[idx] = INVALID_COEFF;
                r3[idx] = INVALID_COEFF;
            }
        }

        /* ---- Round 1: Standard MV-PC ---- */
        for (select = 0; select < KYBER_K; select++) {
            int group;
            for (group = 0; group < KYBER_N; group += parallel) {
                int n = parallel;
                if (group + n > KYBER_N) n = KYBER_N - group;
                int *dst = r1 + select * KYBER_N + group;
                recover_group_mvpc(sk, select, group, n,
                                mode, accuracy, dst, &r1_q);
            }
        }

        /* ---- Round 2: Grafted pair ---- */
        for (select = 0; select < KYBER_K; select++) {
            int group;
            for (group = 0; group < KYBER_N; group += parallel) {
                int n = parallel;
                if (group + n > KYBER_N) n = KYBER_N - group;

                const int *r1_slice = r1 + select * KYBER_N + group;
                int *r2_slice      = r2 + select * KYBER_N + group;
                int *susp_slice    = susp + select * KYBER_N + group;

                recover_group_grafted(sk, select, group, n, accuracy,
                                    r1_slice, r2_slice, susp_slice, &r2_q);
            }
        }

        /* count suspicious coefficients (block-level: entire blocks flagged) */
        {
            int idx;
            *suspicious_count = 0;
            for (idx = 0; idx < ncoeffs; idx++) {
                if (susp[idx]) (*suspicious_count)++;
            }
        }

        /* ---- Round 3: Standard MV-PC on suspicious blocks only ---- */
        for (select = 0; select < KYBER_K; select++) {
            int group;
            for (group = 0; group < KYBER_N; group += parallel) {
                int n = parallel;
                if (group + n > KYBER_N) n = KYBER_N - group;

                /* check if this block is suspicious (any coeff flagged) */
                if (susp[select * KYBER_N + group]) {
                    int *dst = r3 + select * KYBER_N + group;
                    recover_group_mvpc(sk, select, group, n,
                                    mode, accuracy, dst, &r3_q);
                }
            }
        }

        /* ---- Final decision: 2-out-of-3 majority voting (paper 3 Algorithm) ---- */
        {
            int errors = 0;
            int er1 = 0, er2_orig = 0;

            for (select = 0; select < KYBER_K; select++) {
                for (j = 0; j < KYBER_N; j++) {
                    int idx  = select * KYBER_N + j;
                    int true_val = (int)skpoly->vec[select].coeffs[j];
                    int final_val;

                    if (r1[idx] != true_val) er1++;
                    if (r2[idx] != true_val) er2_orig++;

                    if (!susp[idx]) {
                        /* non-suspicious block: R1 and R2 agree */
                        final_val = r1[idx];
                    } else {
                        /* suspicious block: 2-out-of-3 voting */
                        if (r3[idx] != INVALID_COEFF && r3[idx] == r1[idx]) {
                            /* R3 agrees with R1 → R1 wins (2 votes) */
                            final_val = r1[idx];
                        } else {
                            /* R3 disagrees with R1 → R2 as tie-breaker
                            * (if R3==R2: 2 votes for R2; else: default R2) */
                            final_val = r2[idx];
                        }
                    }

                    if (final_val != true_val) errors++;
                }
            }

            *total_errors = errors;
            *r1_errors    = er1;
            *r2_errors    = er2_orig;
        }

        total_queries = r1_q + r2_q + r3_q;
        *r1_queries = r1_q;
        *r2_queries = r2_q;
        *r3_queries = r3_q;

        free(r1); free(r2); free(r3); free(susp);
        return total_queries;
    }
    ```
    这里严格按照论文中描述的三轮攻击:
    - Round1:标准的MV-PC Oracle,得到初步解果r1.
    - Round2:根据Round1结果r1,调用`recover_group_grafted()`函数，得到r2和susp标记块
    - Round3:对susp标记块重做一遍`recover_group_mvpc()`,得到r3
    - vote:根据r1,r2,r3结果来投票:`r1==r2`的(即未被标记为suspicious)的系数块取r1;`r3==r1`的取`r1`,其他情况取`r2`。

- 最终代码编译运行结果如下图:
  - Kyber768,parallel = 4,accuracy = 0.999
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_kyber768_p4.png)
  - Kyber768,parallel = 8,accuracy = 0.9992
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_kyber768_parallel8.png)
  - Kyber1024,parallel = 4,accuracy = 0.999
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_kyber1024_parallel4.png)
  - Kyber1024 parallel = 8,accuracy = 0.9992
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_Kyber1024_parallel8.png)
  - 对比论文中的结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_result.png)
可以看到各组的查询总次数与论文中的结果相符合.

#### Experiments for low accuracy

- 论文中还描述了在高噪声低准确度条件下与MV PC oracle的对比实验,其中后者是专用于低噪声高准确度环境的,因为并行查询恢复的目的就是为了减少查询次数和提高性能,而不是提高准确度.
- 具体来说,MV PC oracle采用一般的majority voting来提高结果的准确度,而本论文方案采用在`Round1,Round2,Round3`中据情况而定地采取majority voting(accuracy = 95%时,MV PC oracle 采用5轮投票,Grafted tree采用`Round2,Round3`做3轮投票;accuracy = 90时,MV PC oracle采用7轮投票,Grafted tree采用`Round1,Round2,Round3`做3轮投票).
- 修改代码后编译运行结果如下图:
  - MV PC oracle:
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_95_majority_MV_PC.png)
  ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Graftedd_tree_90_MV_PC.png)
  - Grafted tree:
   ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_95_grafted_tree.png)
   ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_90_grafted_tree.png)
  - 对比一下论文中的结果:
    ![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/Grafted_tree_thesis_reuslt_low_accuracy.png)
   发现MV PC oracle的majority voting得到的总查询次数与论文中给到的结果符合地很好,但是Gradted tree的结果与论文中的次数有一定差异,可能是纯软件模拟与实际收集trace做oracle的差异(但差异整体来看不是很大,大概几十条trace的差异,但是`#Everror`相差的稍微有点多).