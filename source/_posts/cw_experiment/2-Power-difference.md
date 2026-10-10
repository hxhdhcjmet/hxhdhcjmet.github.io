---
title: 2-Power_difference
date: 2026-08-09 12:21:13
tags:
  - cw_experiment
  - Power_difference
  - 侧信道攻击
categories:
  - 密码学
---
# Power Difference
## EMpty Trace
- 使用chipwhisperer连接到目标设备后，初始时程序不执行任何实际操作，将程序烧录到目标设别后收集empty trace,绘制成图如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/2_empty_trace.png)
- 添加一些操作：在get_pt()函数中电平拉高和拉低之间(采样区间)添加一些操作后再看看采集到的trace的形状，添加代码后如下图:
```c
uint8_t get_pt(uint8_t* pt, uint8_t len)
{
    trigger_high();
    volatile long int A = 0x2BAA;
    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;
    
    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;

    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;
    
    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;
    A *= 2;

    trigger_low();
    simpleserial_put('r', 16, pt);
    return 0x00;
}
```
此时采集到的trace绘制成图如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/2-function_trace.png)

可以很明显看到两种情况下的trace差异。再将两种图画在一起看看，如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/2_diff_empty_function.png)

可以明显看到差异大致是在200~800之间，而两版代码的唯一差别就是后者加了一个手动循环展开的A的连续乘法，也就是说这部分代码在大约200时开始执行，直到800时结束。其中对变量A用关键字`volatile`标识是为了防止编译器对A进行优化，确保CPU实际操作是按照我们代码写的方式一遍一遍执行。

- 我们再将上面的手动16次循环改成for循环版的，代码修改如下:
```c
uint8_t get_pt(uint8_t* pt, uint8_t len)
{
    trigger_high();
    volatile int i = 0;
    volatile long int A = 0x2BAA;
    for (;i<16;i++){
        A *= 2;
    }
    trigger_low();
    simpleserial_put('r', 16, pt);
    return 0x00;
}
```
此时得到的trace绘制成图如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/2_loop_version.png)
可以看到与手动写16次循环的trace也很不同。尤其这里在功能上完全行同的两种C代码，究其原因可以在汇编代码上看出不同，这也就是说两种情况下CPU执行的指令是很不同的(后者会有很多分支预测、比较、跳转等指令)，trace是硬件指令执行的反应，所执行的指令不同，trace也就会有很大差别。

## Power analysis for Password Bypass

- 利用上述讲到的CPU执行的具体指令不同会导致trace的不同，通过分析trace来反推CPU执行的指令，进而推测出密码(具体数据)。先看一下本实验在板子上运行的程序的原始代码:
```c
#include "hal.h"
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

#define IDLE 0
#define KEY 1
#define PLAIN 2

#define BUFLEN 64

uint8_t memory[BUFLEN];
uint8_t tmp[BUFLEN];
char asciibuf[BUFLEN];
uint8_t pt[16];

static void delay_2_ms(void);
void my_puts(char *c)
{
  do {
    putch(*c);

  } while (*++c);
}
static void delay_2_ms()
{
  for (volatile unsigned int i=0; i < 0xfff; i++ ){
    ;
  }
}
void my_read(char *buf, int len)
{
  for(int i = 0; i < len; i++) {
    while (buf[i] = getch(), buf[i] == '\0');

    if (buf[i] == '\n') {
      buf[i] = '\0';
      return;
    }
  }
  buf[len - 1] = '\0';
}
int main(void)
  {
    platform_init();
  init_uart();
  trigger_setup();

    char passwd[32];
    char correct_passwd[] = "h0px3";
  while(1){

        my_puts("*****Safe-o-matic 3000 Booting...\n");
        //Print some fancy-sounding stuff so that attackers
        //will get scared and leave us alone
        // my_puts("Aligning bits........[DONE]\n");
        // delay_2_ms();
        // my_puts("Checking Cesium RNG..[DONE]\n");
        // delay_2_ms();
        // my_puts("Masquerading flash...[DONE]\n");
        // delay_2_ms();
        my_puts("Decrypting database..[DONE]\n");
        delay_2_ms();
        my_puts("\n\n");
        //Give them one last warning
        my_puts("WARNING: UNAUTHORIZED ACCESS WILL BE PUNISHED\n");
        trigger_low();
        //Get password
        my_puts("Please enter password to continue: ");
        my_read(passwd, 32);
        uint8_t passbad = 0;
        trigger_high();
        for(uint8_t i = 0; i < sizeof(correct_passwd); i++){
            if (correct_passwd[i] != passwd[i]){
                passbad = 1;
                break;
            }
        }
        if (passbad){
            //Stop them fancy timing attacks
             int wait = 1;
            for(volatile int i = 0; i < wait; i++){
                ;
            }
            delay_2_ms();
            delay_2_ms();
            my_puts("PASSWORD FAIL\n");
            led_error(1);
        } else {
            my_puts("Access granted, Welcome!\n");
            led_ok(1);
        }
        //All done;
        while(1);
  }
  return 1;
  }
```
 - 其中的关键比较逻辑为:
```c
for(uint8_t i = 0; i < sizeof(correct_passwd); i++){
    if (correct_passwd[i] != passwd[i]){
        passbad = 1;
        break;
    }
}
```
这里逐位比较串口读入的密码passwd与正确密码correct_passed(一开始定义了是h0px3)，一旦发现某一位错误就立即退出，并执行了一个空循环和两个delay_2_ms()的延迟操作，以防止时间攻击。但是这些是在比较结束后执行的，攻击者可以忽略这部分操作，仅关注比较部分差异(如输入的密码首位是h和a将会造成比较操作的执行差异)

- 实验给我们hint是密码第一位为h且长度为5，其中收集trace的函数是接收我们自己传入的密码password并收集3000条传入该密码的trace。
- 由于密码的每一位都是0-9a-z的字符，且`\x00`属于无效空字符，可以以它为基准，收集其他情况下作为输入的trace与这条invalid trace的差异，绘制成图，代码如下:
```python
%matplotlib inline
import matplotlib.pyplot as plt
from tqdm import tqdm
plt.figure(figsize=(12, 6))
LIST_OF_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"
ref_trace = cap_pass_trace("\x00\n")[:1000]   # 参考波形
for CHARACTER in tqdm(LIST_OF_CHARACTERS,desc = "BP-ing"):
    trace = cap_pass_trace(CHARACTER + "\n")[:1000]
    plt.plot(trace - ref_trace, label=CHARACTER) 

plt.xlabel("Sample Index (points)")          # X轴标签
plt.ylabel("Voltage / Digital Value")        # Y轴标签
plt.title("Difference from Reference Trace for Each Character")   # 标题
plt.legend(loc='lower left', ncol=4, fontsize=8)  
plt.savefig("2_trace_comparison.png", dpi=300, bbox_inches='tight')
plt.show()
```
结果如下图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/2_trace_comparison.png)
可以很明显地看到正确密码位'h'相较于其他所有错误位的trace与invalid trace的差异是最大最明显的，即使我们输入的是单独一位作为密码，它们实际都是错的。这给了我们破解完整密码的启示：当前密码位正确时与invalid trace的差异是最明显的！
- 这里的明显若要量化表示的话，就是'h'对应的trace与invalid 对应的trace逐位做差，取绝对值后求和是最大的:
```python
import numpy as np
LIST_OF_VALID_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"
all_diff = {}
ref_trace = cap_pass_trace("\x00\n")
for CHARACTER in LIST_OF_VALID_CHARACTERS:
    trace = cap_pass_trace(CHARACTER + "\n")
    diff = np.sum(np.abs(trace - ref_trace))
    all_diff[CHARACTER] = diff

sorted_diff = sorted(all_diff.items(),key = lambda x : x[1],reverse = True)
for k,v in sorted_diff:
    print(f"{k} diff = {v}")
```
这里的确算得h的absolute difference是最大的为475，相较于其他的为大约30左右，能很明显地区分开来。

- 完整密码破解方法即为一位一位重复上述过程，其中破解第$i$位密码时使用前$i-1$位已经破解出来的作前缀，第$i$位为遍历位，代码如下:
```python
from tqdm.notebook import tqdm
guessed_pw = ""
for i in tqdm(range(5),desc = "ALL BIT BP-ing..."):
    ref_trace = cap_pass_trace(guessed_pw + "\x00\n")
    curr_max_diff = 0
    curr_c = ''
    for c in tqdm(LIST_OF_VALID_CHARACTERS,desc = f"BP number {i+1} bit ing...",leave = False):
        trace = cap_pass_trace(guessed_pw + c + "\n")
        diff = np.sum(np.abs(trace - ref_trace))
        if diff > curr_max_diff:
            curr_max_diff = diff
            curr_c = c
    guessed_pw += curr_c
    print(guessed_pw)
```
这里用的是非原版的absolute difference超过阈值就算正确密码位，而是所有可能都遍历完后取最大值，前者取的阈值依赖经验估计，而后者则不需要。不过后者需要跑完所有可能字符，耗时会久点。最终结果如下截图:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/2-BP_result_success.png)
发现的确为一开始的.C文件中定义的correct password。
- 这里尝试修改一下.C文件中的密码为'And0Sakura',再次破解结果如下:
![](https://cdn.jsdelivr.net/gh/hxhdhcjmet/blogimage@main/2026/08/2-change_passed_still_success.png)
同样解密正确，破解成功！