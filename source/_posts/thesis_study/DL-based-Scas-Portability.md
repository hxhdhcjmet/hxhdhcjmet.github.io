---
title: DL_based_Scas_Portability
date: 2026-07-29 19:45:00
tags:
    - kyber
    - 侧信道攻击
    - 深度学习
    - 可移植性
categories:
    - 论文学习
---
# Enhancing Portability in Deep Learning-Based Side-Channel Attacks Against Kyber

> 此篇按论文阅读顺序记录学习内容,而非按一般论文结构

NICV:

- 定位泄漏点:采集并计算得到不同时间点的NICV,峰值代表此处泄露,攻击重点也就在这里。
    

分类:

- Intra-board protability:相同设备,不同测量位置
    
- Inter-board protability:不同设备
    

NICV Analysis: B1_MD~B1_MD2 < B1_MD~B2_MD < B1_MD~B1_corner 说明同板子间差异比不同板子间差异更显著

在某些情况下,探针位置带来的NICV差异会掩盖不同板子间的差异

MLPM(Multiple Leakage Point Model):多泄露点联合建模,使用如NICV、SNR等方法检测泄漏点,可以检测出多出泄漏点,综合使用这些点来建模恢复密钥。相较于传统单点模型,能够利用多个弱泄露、提升攻击成功率、更符合真实硬件泄露。

Ablated-MLPM:通过删除部分泄漏点,检查此时的恢复密钥的成功率来判断评价每个点的贡献。可以用于找关键泄漏点、验证模型的有效性、指导侧信道防护设计。

Sensitivity:用于评估去掉部分点后模型预测变化,Sens大说明这些点重要,Sens小说明这些点对预测作用不大; Resilience:消融掉部分点后的模型重新训练,计算预测准确率变化。如果是不重要的点,那么去掉后再次训练模型的预测结果与之前的差值绝对值应当不大(可靠),否则如果去掉这些前面的对预测作用不大的点,重新训练后预测能力大大下降(degradation),那依然是Resilience性不好。

CNN:Convolutional Neural Network,专门处理具有局部结构数据的神经网络;Convolution Layer:卷积层,为CNN的核心层。CNN在此处用于自动学习输入数据的局部特征,而不需要人工设计特征。即CNN优势为:不需要精确泄露模型(数据驱动)、自动选择POI、可以利用多个泄漏点。CNN缺点为:需要大量数据(CPA可能几千trace,CNN可能需要几十万trace)、容易过拟合、解释性差(能找出某点重要，但不知到为什么重要)。
