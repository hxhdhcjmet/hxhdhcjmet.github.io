---
title: Elgamal加密中生成元g的选取与安全性分析
date: 2026-06-20 22:34:22
tags:
  - 密码学
  - Elgamal加密
  - 参数选取细节
category: 密码学
katex: true
---
# Elgamal加密参数g的选取

## Elgamal加密
该加密算法的课堂描述是这样的:
 - 密钥生成:
    - 设$p$为素数,$Z_p^*$是阶为$p-1$的乘法循环群,$g \in Z_p^*$是生成元。
    - 明文空间$P = Z_p^*$,密文空间$C = Z_p^* \times Z_p^*$,随机选取$x \in \{1,\cdots,p-1\}$,计算
  $ y = g^x \mod p $
  - 私钥:$x$
  - 公钥:$p,g,y$
- 加密:
    - 随机选取$k \in\{1,\cdots,p-1\}$
    - 计算$c_1 = g^k \mod p$和$c_2 = y^km \mod p$
    - 输出$(c_1,c_2)$
- 解密:
    - 计算
  $ m = c_2 / c_1^x \mod p $

这里解密正确性在于:
$$  \frac{c_2}{c_1 ^ x} = \frac{y^km}{(g^k)^x} = \frac{g^{xk}m}{g^{xk}} = m $$

再看一版更安全的Elgamal加密算法描述:
- Key Generation:
   - $q$ is a prime;$p = 2q + 1$ is a prime;
   - $g \in Z_p^*$ is a generation of $G$,which is a multiplicative cyclic group of order q.
   - Secret key : $x$(where $0 < x < q$)
   - Public key : $y = g^x \mod p$
   - Plaintext: $m \in G$
- Encryption:
   - Pick a number $k$ randomly from $\{q,\cdots,q-1\}$
   - Compute $c_1 = g^k \mod p$ and $c_2 = y^km \mod p$
   - Output $(c_1,c_2)$
- Decryption:
    - Compute 
  $$ m = c_2 /c_1^x \mod p $$
可以看到这两版本几乎一摸一样,唯一的不同点在于参数$g$的选取:一个是大群$G$的生成元,一个是阶为$q$的子群的生成元。那么为什么说后者更安全呢？

## Elgamal加密比特安全
原因在于Elgamal加密斜率了明文于密文之间的比特关系。
对于$Z_p^*$的生成元$g$,其阶为$p-1$且$g \in NQR$,因此对于
$$ y = g^x \mod p  $$
即使不知道$x$,依然可以判断$y$是否是二次剩余,因为
$$  （\frac{y}{p}） = （\frac{g^x}{p}） = (\frac{g}{p})^x = (-1)^x $$
上述为Jacobian符号,也就是说若$y \in NQR$,则$x$为奇数,否则若$y \in QR$,则$x $为偶数。

本质原因在于$Z_p^*$的阶为$p-1$是个偶数(因为$p$为奇素数,$p-1$自然就是偶数),含有因子$2$,因此存在阶为$2$的子群(即这里的Jacobin符号对群中所有元素作用后解果为$\pm 1$),这就是1比特信息泄露的原因。

而选取$p = 2q+1$,$g' = g^2$为$q$阶子群$\mathbb{G}$的生成元,注意这里$q$为素数,这样的群$\mathbb{G}$就不存在非平凡子群(因为它只有单位元构成的群和本身这两个平凡子群),其中
$$ ord(g^k) = \frac{ord{(g)}}{gcd(k,ord(g))} = \frac{kq}{gcd(k,kq)} = \frac{kq}{k} = q,p = kq+1    $$

## 参数选取
因此上述Elgamal加密算法版本二的参数选取是更安全的,除此之外,它还满足基于离散对数的参数选取时,群$Z_p^*$的阶$p-1 = 2q$含有足够大的素因子$q$,能有效抵抗Pohilig-Hellman算法的攻击。