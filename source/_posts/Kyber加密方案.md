---
title: Kyber加密方案
date: 2026-07-14 15:24:53
tags:
  - Kyber
  - 后量子密码
categories:
  - 密码学
---
# Kyber加密
>本篇为Kyber加密方案的学习记录,可能存在错误,欢迎指正

## 前置知识

- 多项式环: 定义$R$为多项式环$\mathbb{Z}[X] / (X^n + 1)$,$R_q$为环$\mathbb{Z}_q[X] / (X^n + 1)$.

- 取整: 定义$x \in Q$,$\lfloor x \rceil$为取$x$距离最近的整数,等价定义为
$$  \lfloor x \rceil  = \lfloor x + \frac{1}{2} \rfloor $$
如$\lfloor 3.2 \rceil = \lfloor 3.2 + 0.5 \rfloor = 3$,$\lfloor 3.7 \rceil 
= \lfloor 3.7 + 0.5 \rfloor = 4$.

- 元素的大小: 对元素$w \in \mathbb{Z}_q$,定义$|| w ||_{\infty} = |w \mod ^{\pm}  q|$;对$w = w_0 + w_1X + \cdots + w_{n-1}X^{n-1} \in R$,定义$\ell_{\infty}$和$\ell_2$范数:
$$  ||w||_{\infty} = \max_i{|| w_i ||_{\infty}},||w|| = \sqrt{||w_0||_{\infty}^2 + ||w_1||_{\infty}^2 + \cdots + ||w_{n-1}||_{\infty}^2}$$
对$\mathbf{w} = (w_1,w_2,\cdots,w_k) \in R^k$,定义:
$$  ||\mathbf{w}_{\infty}|| = \max_i||w_i||_{\infty},||\mathbf{w}|| = \sqrt{||w_1||^2 + ||w_2||^2 + \cdots + ||w_k||^2}   $$

- 压缩与解压缩(Compression and Decompression):
  - 压缩(compression):定义$\texttt{Compress}_q(x,d)$为将输入$x \in \mathbb{Z}_q$输出为在$\{0,1,\cdots,2^{d-1}\}$中的整数,其中$d < \lceil  \log_2(q)\rceil$
  $$  \texttt{compress}_q(x,d) = \lfloor (2^d / q) \cdot x \rceil \mod 2^d $$
  - 同样地可以定义解压缩(decompression):$\texttt{Decompress}_q$:
$$ \texttt{Decompress}_q(x,d) = \lfloor (q / 2^d) \cdot x \rceil  $$

- 集合与分布(Sets and Distribution):对于集合$S$,$s \gets S$表示$s$独立随机地取自$S$,如果$S$表示概率分布,则$s$表示根据$S$的分布取元素。

- 对称原语(Symmetric primitives):Kyber方案中使用随机数生成器$\texttt{PRF}$、哈希函数$\texttt{H}$和$\texttt{G}$、密钥派生函数$\texttt{KDF}$等,此处不做详细说明。

- 中心二项分布(binomial distribution):$\texttt{Kyber}$中的噪声采样自中心二项分布$\beta_{\eta}$,其中$\eta = 2$或$\eta = 3$。$\beta_{\eta}$定义如下:
$$  \text{Sample}(a_1,\cdots,a_{\eta},b_1,\cdots,b_{\eta} \gets \{0,1\}^{2\eta})   \\
\text{and output} \sum_{i=1}^\eta (a_i - b_i)
$$
在$\texttt{Kyber}$中我们说多项式$f \in R_q$或者向量采样自$B_\eta$,意思是指每一个系数采样自$B_\eta$.

## 密钥生成算法(Keyber KeyGen)
- 生成随机矩阵$\mathbf{A} \gets R_q^{k \times k}$,其中$A = (\mathbf{a_1}^T,\cdots ,\mathbf{a_k}^T)^T$,$\mathbf{a}_i \gets R_q^k$。

- 根据分布$B_\eta$ 采样生成$(\mathbf{s},\mathbf{e}) \gets \beta_\eta^{k} \times \beta_\eta^{k}$,其中$\mathbf{e} = (e_1,\cdots,e_k)^T$.
- 计算$\mathbf{t} = \mathbf{As} + e$,即
$$   t =
\begin{pmatrix}
\mathbf{a}_1^T\mathbf{s} + e_1 \mod q\\
\vdots
 \\
\mathbf{a}_k^T\mathbf{s} + e_k \mod q
\end{pmatrix}
$$
- 输出公钥$pk = (\mathbf{A},\mathbf{t})$,私钥$sk = \mathbf{s}$.
![密钥生成算法](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/07/Kyber_KeyGen.png)


## 加密算法(Kyber.Enc)
- 输入公钥$pk$与明文$m \in \{0,1\}^n$
- 根据分布$B_{\eta}$采样生成$\mathbf{r} \gets \beta_{\eta}^k$,$\mathbf{e_1} \gets \beta_{\eta}^k$,$e_2 \gets \beta_\eta$.
- 计算
$$  \mathbf{u} = \mathbf{A}^T\mathbf{r} + \mathbf{e_1} \mod q  \\
v = \mathbf{t}^T\mathbf{r} + e_2 + \lfloor \frac{q}{2} \rceil\cdot m \mod q 
$$
其中$m$理解为$\mathbb{Z}_2^n$上的$n$维向量$\mathbf{m} = (m_1,m_2,\cdots,m_n)$;$\lfloor \frac{q}{2}\rceil m = Encode(m)$实际上为原始比特消息映射为多项式系数:
$$
\begin{cases}
0 \to 0\\
1 \to \frac{q}{2}
\end{cases}
$$
将消息映射为多项式系数后才能参与与前面式子的加法运算。
- 输出密文$(\mathbf{u},v)$

![加密算法](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/07/kyber_enc.png)
上述实际使用算法会对$\mathbf{u}、v$做$\texttt{Compress}$(如将每个系数12比特压缩为10比特)操作,目的是为了减少密文的大小,提高传输效率。这一步不影响算法描述,属于工程实现优化。
## 解密算法(Kyber.Dec)
- 输入密文$c$与私钥$sk$.
- 计算$ m' = v - \mathbf{s}^T \mathbf{u}$;
- 判断$m' = (m'_1,m'_2,\cdots,m'_n)$的每个分量是更接近$0$还是$\lfloor \frac{q}{2} \rceil$.对于$i = 1,\cdots,n$，如果$m_i'$更接近0,则输出$m_i = 0$;如果更接近$\lfloor \frac{q}{2}\rceil$,则输出$m_i = 1$。
- 输出明文$m = (m_1,m_2,\cdots,m_n)$.
![解密算法](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/07/Kyber_dec.png)

## 正确性
对于按上述密钥生成算法与加密算法生成的密钥与密文,考虑解密结果:

$$
\begin{aligned}
m' &= v - \mathbf{s}^T\mathbf{u}\\
   &= \mathbf{t}^T\mathbf{r} + e_2 + \lfloor \frac{q}{2} \rceil \cdot m - \mathbf{s}^T(\mathbf{A}^T\mathbf{r} + e_1)\\
   &= (\mathbf{As})^T\mathbf{r} +\mathbf{e}^T\mathbf{r} + e_2 + \lfloor \frac{q}{2} \rceil \cdot m - (\mathbf{AS})^T \mathbf{r} - \mathbf{s}^T\mathbf{e}_1\\
   &= \lfloor   \frac{q}{2} \rceil + (\mathbf{e}^T\mathbf{r} + e_2 - \mathbf{s}^T\mathbf{e}_1)\\
   &= \lfloor \frac{q}{2}  \rceil \cdot m + e'
\end{aligned}
$$
其中令$e' = \mathbf{e}^T\mathbf{r} + e_2 - \mathbf{s}^T\mathbf{e}_1$,通过适当设置$LWE$问题的相关参数,$e'$以高概率满足$||e'||_{\infty} < \lfloor \frac{q}{4} \rceil$,此时有:
 - 当$m_i = 0$时,$m_i' = e' \in (-\lfloor \frac{q}{4} \rceil,+\lfloor \frac{q}{4} \rceil)$.
 - 当$m_i = 1$时,$m_i' \in (\lfloor \frac{q}{2} \rceil-\lfloor \frac{q}{4} \rceil,\lfloor \frac{q}{2} \rceil + \lfloor \frac{q}{4} \rceil)$.
   
因此可以根据判断$m'$的每个分量$m_i'$是在$0$还是$\lfloor \frac{q}{2} \rceil$附近来判断$m_i = 0$还是$m_i = 1$,从而得到正确的$m$.

## 解密错误
$\texttt{Kyber}$将$m$映射为$\lfloor \frac{q}{2} \rceil \cdot m$而不是$\{0,1\}$是为了能正确滤除噪声$e'$的干扰(前提是$|| e'||_{\infty} <  \lfloor \frac{q}{4} \rceil$).然而由于$e'$的生成收概率分影响,有可能出现$||e'||_{\infty} \ge  \lfloor \frac{q}{4} \rceil$的情况,此时会得到错误的解密结果.合理设置参数能使得解密错误降为可忽略的概率。

---
上述为$\texttt{Kyber.CPAPKE}$,即"抗选择明文攻击的公钥加密"(Chosen Plaintext Attack-Public Key Encryption),将$\texttt{Fujisaki-Okamoto(FO)}$变换应用于上述$\texttt{Kyber}$加密,可以得到IND-CCA安全的密钥封装算法KEM.


# Kyber.CCAKEM
FO变换作用于$\texttt{Kyber.CPAPKE}$即可得到"抗选择密文攻击的密钥封装机制"(Chose Ciphertext Attack-Key Encapsulation Mechanism),是一个更高级的密钥封装机制,核心功能包括$\texttt{Encapsulation}$(封装)和$\texttt{Decapsulation}$(解封装)。其运行流程同$\texttt{Kyber.CPAPKE}$.由密钥派生、加密和解密组成。

## 密钥派生算法(Kyber.CCAKEM.KeyGen())

![密钥派生](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/07/Kyber-KEM_KeyGen.png)
- 关键不同在于$sk$,由原始$\texttt{Kyber.CPAPKE.KeyGen()}$生成的$sk'$链接上$pk$、$H(pk)$和随机数$z$共同构成:
$$ sk = sk' || pk || H(pk) || z$$
随机数$z$将随密文一同发送给接收方,在验证失败时作为输出的一部分。

## 加密算法(Kyber.CCAKEM.Enc())
![加密算法](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/07/Kyber-CCAKEM_Enc.png)

- 注意到这里的$m$不再是消息,而是一个随机数,真正要封装的是共享秘密$K$,其生成又与$m$有关.
- 接收者解密密文$c$得到明文(随机数$m$)用来计算共享秘密$K$,同时还能自己再计算一遍$c'$,通过判断$c = c'$是否成立来推断密文是否被篡改。


## 解密算法(Kyber.CCAKEM.Dec())

![解密算法](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/07/Kyber_CCAKEM_Dec.png)

- 解密算法中关键体现$\texttt{FO}$变换的就是再次计算
$$  (\bar K',r') = G(m' || h)  \\
c' = \texttt{Kyber.CPAPKE.Enc}(pk,m'r')\\
$$
以及验证$c = c'$,这里正确才输出$K$,否则也并不报错或输出空,而是输出预定值(用预先存储的随机值$z$计算)$K=\texttt{KDF}(z||H(c))$,这样对于攻击者而言,无法知道自己修改的密文$c$是否合法,因此能抵御$\texttt{Oracle}$攻击;输入$\texttt{KDF}$时拼接$H(c)$是为了使不同修改后的密文得到不同的随机密钥,比输出固定的$\texttt{KDF}(k)$更安全。

- 合法或不合法的$c$都经过了比较$c == c'$、计算$\texttt{KDF}$返回密钥的过程,因此两种情况下的计算量和计算时间大致相同,攻击者无法通过返回值、返回时间、是否返回等信息来构造攻击。


## 参数设置

![参数设置](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/07/Kyber_parameter_set.png)


## FO变换
- FO变换能将IND-CPA的kyber变成IND-CCA的KEM算法，该变换的关键是引入两个哈希函数$\mathcal H$、$\mathcal  G$和重加密过程，对于以下情况:
  - 攻击者将合法密文$ct$修改部分位置变成非法密文$ct' = ct + \Delta$。对于合法密文$ct$，自然有对应明文$m$，满足:
$$
(K,r) = \mathcal  G(m,\mathcal H(pk))\\
ct = Enc(pk,m,r)
$$
且满足$m = Dec(sk,ct)$。但对这里篡改过的$ct'$有:
$$
m' = Dec(sk,ct')
$$
通常有$m' \neq m$。又由于随机数$r$的是由哈希函数使得与明文$m$和公钥绑定的，因此$r' = \mathcal G(m',\mathcal H(pk))$，一般有$r' \neq r$。此时这里的$(m',r')$经过重加密很难得到与原来$ct'$相同的结果。
   - 对于攻击者自行构造的特殊密文$ct$，其本身不由已知合法$(m,r)$计算得到，那么经过解密和计算随机数得到的$(m,r)$如下:
$$
\begin{cases}
m = Dec(sk,ct)\\
r = \mathcal G(m,\mathcal H(pk))
\end{cases}
$$
这里算出来的$(m,r)$很难真正用去加密最终得到的$ct'$能满足$ct' ==  ct$。

- 综上，一句话总结：**FO 通过将消息 m、随机性 r 与 ciphertext ct 绑定，并利用重加密检查验证这种绑定关系，使攻击者难以构造能够通过验证的恶意 ciphertext，从而阻止攻击者利用解封装接口作为有效的 CCA 解密 oracle。**


