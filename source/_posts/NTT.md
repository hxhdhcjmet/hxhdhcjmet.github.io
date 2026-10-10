---
title: NTT
date: 2026-07-15 15:32:37
tags:
    - NTT
    - 密码学
    - 快速计算
categories:
    - 密码学
---
# NTT

## 问题描述
给定两个多项式
$$  A(x) = a_0 + a_1x + \cdots + a_n x ^n \\
    B(x) = b_0 + b_1x + \cdots + b_m x ^m \\
$$
要求$C(x) = A(x)B(x)$,当不用$\texttt{NTT(number theory transform)}$时,$C(x)$的每一项系数都需要卷积计算:
$$ c_k = \sum_{i = 0}^k a_ib_{k-i}  $$
如$c_0 = a_0b_0$,$a_1 = a_0b_1 + a_1 + b_0$等,对于$n$长项式的乘法,这样操作的时间复杂度达到$O(n^2)$.注意,我们一般使用系数向量来表示多项式和多项式的运算,如$\mathbf{A} = (a_0,a_1,\cdots,a_n)$,$\mathbf{B} = (b_1,b_2,\cdots,b_m)$,$\mathbf{C} = (c_0,c_1,\cdots,c_{n+m})$.

## NTT运算优化
$\texttt{NTT}$的优化思路为将上述用向量存系数改为直接存函数值,即
$$   \mathbf{A} = (a_0,a_1,\cdot a_n) \to \mathbf{A} = (A(1),A(a),A(a^2),\cdots,A(a^n))   $$
其好处在于,函数运算满足:
$$  (A \times B)(x) = A(x)B(x)   $$
因此此时$C_t = A_t \times B_t$,直接用$A、B$对应的项相乘即可得到$C$对应的项。

这里利用的是多项式与点值的互推。即给定一个多项式$A(x)$,对于任意$x_i$,都可以求出在多项式上的点$(x_i,A(x_i))$;同样的,只要给定足够的点$(x_i',A(x_i'))$也同样能反求出原始多项式。因此这里优化的根本原理在于将多项式变为足够多的点,点的运算替代原始多项式系数运算,得到结果的点再恢复成多项式系数。

### 正向NTT
正向NTT(Forward NTT):
$$  X(m) = \sum_{n=0}^{N-1}x(n)a^{mn} \mod M$$
这里$X(m) = A(a^m)$,$a$是原根。
- 为什么这里要用$a$不能用任意数,比如$1,2,\cdots$这样的一般的数?
  
实际是完全可以用一般的数的,此时就是矩阵运算:
$$ 
\begin{pmatrix}
  1&  1^2&  \cdots&1^n \\
  2&  2^2&  \cdots&2^n \\
  \vdots& \vdots &\ddots  &\vdots \\
  t&  t^2& \cdots &t^n
\end{pmatrix}
\begin{pmatrix}
 a_0\\
 a_1\\
 \vdots\\
 a_n
\end{pmatrix}
=\begin{pmatrix}
 A(1)\\
 A(2)\\
 \vdots\\
 A(t)
\end{pmatrix}
$$
左边
$$
\begin{pmatrix}
  1&  1^2&  \cdots&1^n \\
  2&  2^2&  \cdots&2^n \\
  \vdots& \vdots &\ddots  &\vdots \\
  t&  t^2& \cdots &t^n
\end{pmatrix}
$$
是一个$\texttt{Vandermonde}$矩阵,是可逆矩阵,当从点恢复成系数时也需要求逆,矩阵求逆的时间复杂度为$O(n^2)$,因直接使用一般的点将没有优化提升。

采用原根$a$是因为它有很多特殊的性质,此时将一般的采样点变成:
$$(a^0,a^1,\cdots,a^{n-1}) $$
它有这里用到的几个性质:
 - 消去引理:
  由:
  $$a^{N} = 1$$
  可以得到:
  $$a^{N+1} = a\\
  a^{N+2} = a^2 \\
  $$
因此所有指数都可以模$N$,所有的运算都不会无限增长.
 - 折半引理:
一定有
$$ a^{\frac{N}{2}} = -1  $$
因此此时$\texttt{Forward}$公式
$$  A(a^k) = \sum a_i(a^k)^i $$
可以拆分成奇偶项:
$$  
\begin{aligned}
A(a^k) &= \sum a_i(a^k)^i\\
       &= \sum a_{2i}(a^{2k})i + a^k \sum a_{2i+1}(a^{2k})^i
\end{aligned}
$$
这里$a^{2k}$是一个$\frac{n}{2}$点的$\texttt{NTT}$,因此一个$n$点的$\texttt{NTT}$变成了两个$\frac{n}{2}$点的$\texttt{NTT}$.

- 正交性:

$$  
\sum_{k=0}^{n-1}a^{km} = 
\begin{cases}
n,m=0\\
0,m\neq 0
\end{cases}
$$
这里稍微说明一下:
- 当$m=0$时,$\sum_{k=0}^{n-1}a^{km} = \sum_{k=0}^{n-1} 1 = n$.
- 当$m \neq 0$时,$\sum_{k=0}^{n-1}a^{km} = (a^m)^0 + (a^m)^1 + \cdots + (a^m)^{n-1}=\frac{(a^m)^n - 1}{a^m - 1} = 0$.

结合$\texttt{Kyber}$方案中的系数编写演示版本的代码:

```python
def ntt(coeffs):
    N = len(coeffs)
    omega = 4
    q = 17

    result = []
    # m：计算第几个采样点
    for m in range(N):
        value = 0
        # n：遍历每一个系数
        for n in range(N):
            value += coeffs[n] * pow(omega, m*n, q)
        result.append(value % q)
    return result
```
$\texttt{Kyber}$中的模数$q = 17$,长度$N = 4$,原根$\omega = 4(4^4 \equiv 1 \mod {17})$
- 假设上述参数$\texttt{coeff = [1,2,3,0]}$,表示:
$$  A(x) = 1 + 2x + 3x^2 $$
- 第一层循环
```python
for m in range(N):
```
是计算采样点,即遍历计算$A(1),A(\omega),A(\omega ^2),\cdots$,代码中先初始化value.
- 第二层循环

```python\
for n in range(N):
```
开始遍历所有系数,$n=0$时加入$a_0$;$n=1$时加入$a_1 \omega ^m$;$n=2$时加$a_2 \omega^{2m}$...
因此
```python
value += coeffs[n] * pow(omega,m*n,q)
```
就对应公式:
$$ X(m) = \sum a_n \omega^{mn} $$
但是这里两层循环的时间复杂度依然为$O(n^2)$,因此实际使用时会利用可拆分性不断二分,将时间复杂度将为$O(n \log n)$。

注意当原来的公式可以变为:
$$
\begin{aligned}
X(m) &= \sum_{k} x_{2k}\omega^{m(2k)} + \sum_k x_{2k+1}\omega ^{m(2k+1)}\\
&= \sum_k x_{2k}(\omega^2)^{mk}+\omega^m \sum_k x_{2k+1}(\omega ^2)^{mk}
\end{aligned}
$$
拆分后其中一半(偶数项和)是:
$$  E(x) = a_0 + a_2 x + \cdots  $$
另一半(奇数项和)是:
$$  O(x) = a_1 + a_3 x + \cdots  $$
因此:
$$ A(x) = E(x^2) + xO(x^2)  $$
带入$x = \omega^k$得到:
$$
\begin{cases}
A(\omega ^k) = E(\omega^{2k}) + \omega^k O(\omega ^{2k})\\
A(\omega ^{k+N/2}) = E(\omega^{2k} )- \omega^k O(\omega ^{2k})
\end{cases}
$$
注意到式子
$$  E + \omega^kO,E- \omega^kO $$
就是两个蝶形公式。

来看一下官方[$\texttt{kyber}$实现](https://github.com/pq-crystals/kyber/blob/main/ref/ntt.c)里面的ntt:
```C
void ntt(int16_t r[256]) {
  unsigned int len, start, j, k;
  int16_t t, zeta;

  k = 1;
  for(len = 128; len >= 2; len >>= 1) {
    for(start = 0; start < 256; start = j + len) {
      zeta = zetas[k++];
      for(j = start; j < start + len; j++) {
        t = fqmul(zeta, r[j + len]);
        r[j + len] = r[j] - t;
        r[j] = r[j] + t;
      }
    }
  }
}
```
- 第一层循环
```c
for(len = 128; len >= 2; len >>= 1)
```
就是在不断拆分,$128 \to 64 \to 32 \cdots$
- 第二层循环
```c
for(start = 0; start < 256; start = j + len)
```
就是在分别处理拆分后的部分,比如第一次$0 \sim 127$和$128 \sim 255$两个128;下一次$0 \sim 63$和$64 \sim 127$以及$128 \sim 191$和$192 \sim 255$四个64...

- 第三层
```c
for(j = start; j < start + len; j++)
```
就是在真正做蝶形变换,其中$\texttt{even} = r[j],\texttt{odd} = r[j + len]$,$\texttt{t = zeta * odd}$就是
$$
\omega^k O
$$
然后
```c
r[j] = even + t
```
就是
$$
E + \omega^kO
$$

```c
r[j+len] = even - t
```
就是
$$
E - \omega^k O
$$
在上述的代码中$r$是当前正在计算的数据,在一开始的时候是系数$(a_0,a_1,\cdots,a_{255})$,在运算中会不断变化,第一层蝶形结束后,原来的系数变成了两个128点$\texttt{NTT}$的结果,第二层后变成4个$\texttt{NTT}$的结果...最后才变成256点$\texttt{NTT}$,也就是说$r$是一路更新的;$len$就表示公式中的$\frac{k}{2}$,即当前两个蝶形输入之间的举例;$j$表示当前蝶形左边那个元素的位置。

注意到上述
```C
r[j + len] = r[j] - t;
r[j] = r[j] + t;
```
原地计算时要先更新r[j+len],是因为此时r[j]还是$E$,可以直接计算$E - \omega^kO$,然后再更新r[j]为$E + \omega^k O$,如果交换顺序就会导致更新r[j+len]时用的$E$不正确。


## 逆向NTT
逆向NTT(Inverse NTT):
$$ x(n) = \frac{1}{n} \sum_{m=0}^{N}X(m)a^{-mn} \mod M  $$
这里$x(n)$是$A(x)$的系数.