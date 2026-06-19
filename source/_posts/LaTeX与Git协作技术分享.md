---
title: LaTeX与Git协作技术分享
date: 2026-06-19 11:41:44
tags:
    - LaTeX
    - Hexo
    - Git
categories:
    - 技术笔记
---

# 本地配置 LaTeX 环境：高效协作指南

## 1. 引言

LaTeX 很适合用来撰写实验报告、课程设计报告和论文类文档。相比 Word，它在数学公式、交叉引用、目录、图表编号和参考文献管理方面更稳定，也更适合多人维护同一个文档。

Overleaf 这类在线平台确实省去了本地配置的麻烦，但免费版通常会遇到编译时间限制、项目数量限制、协作人数限制等问题。对于需要频繁插图、反复编译、多人成员同时修改的实验报告项目，本地 LaTeX 环境配合 Git 往往更高效、更可控。

本文主要分享一种适合实验报告协作的工作方式：本地使用 VS Code + LaTeX Workshop 写报告，用 Git 管理版本，用 GitHub/Gitee 等平台同步和合并。目标不是把 LaTeX 所有语法讲完，而是给出一套能直接落地的项目结构和协作流程。

一句话总结：**LaTeX 负责排版，Git 负责协作，VS Code 负责把两者连起来。**

## 2. 环境配置

### 2.1 安装 LaTeX 编译环境

LaTeX 需要先安装本地发行版，常见选择如下：

| 系统 | 推荐工具 | 说明 |
| --- | --- | --- |
| Windows | TeX Live 或 MiKTeX | TeX Live 体积较大但完整；MiKTeX 较轻量 |
| macOS | MacTeX | 基于 TeX Live，适合 macOS |
| Linux | TeX Live | 可通过系统包管理器安装 |

中文实验报告建议优先使用 **XeLaTeX** 编译，因为它对中文和系统字体支持更友好。

安装完成后，可以在终端中检查：

```powershell
xelatex --version
latexmk --version
```

如果命令无法识别，通常是环境变量没有配置好，或者安装过程没有完成。

### 2.2 安装 Git

Git 用来管理版本和多人协作。安装完成后，在终端中检查：

```powershell
git --version
```

第一次使用 Git 时，建议配置用户名和邮箱：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

这里的用户名和邮箱会出现在提交记录中，方便团队成员知道每次修改是谁完成的。

### 2.3 安装 VS Code 和插件

推荐使用 VS Code，并安装以下插件：

- **LaTeX Workshop**：提供 LaTeX 编译、预览、错误定位等功能
- **GitLens**：增强 Git 历史记录查看能力，可选
- **Markdown All in One**：方便维护项目说明文档，可选

LaTeX Workshop 安装后，可以在 VS Code 的 `settings.json` 中加入以下配置：

```json
{
  "latex-workshop.latex.autoBuild.run": "never",
  "latex-workshop.latex.outDir": "%DIR%/build",
  "latex-workshop.view.pdf.viewer": "tab",
  "latex-workshop.latex.recipe.default": "lastUsed",
  "latex-workshop.latex.recipes": [
    {
      "name": "latexmk (xelatex)",
      "tools": ["latexmk"]
    },
    {
      "name": "xelatex",
      "tools": ["xelatex"]
    }
  ],
  "latex-workshop.latex.tools": [
    {
      "name": "latexmk",
      "command": "latexmk",
      "args": [
        "-xelatex",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-outdir=%OUTDIR%",
        "%DOC%"
      ]
    },
    {
      "name": "xelatex",
      "command": "xelatex",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-output-directory=%OUTDIR%",
        "%DOC%"
      ]
    }
  ]
}
```

其中最重要的是：

- `autoBuild.run: "never"`：关闭自动编译，避免每次保存都触发编译导致卡顿
- `outDir: "%DIR%/build"`：把编译中间文件统一放到 `build/` 目录
- `latexmk (xelatex)`：适合需要目录、引用、参考文献的文档，能自动多轮编译

手动编译可以使用 LaTeX Workshop 的侧边栏按钮，也可以使用快捷键 `Ctrl+Alt+B`。

## 3. 推荐项目结构

### 3.1 不要把所有内容写进一个文件

实验报告一旦超过几页，就不建议把所有内容塞进一个 `main.tex`。单文件写法前期看起来简单，后期会出现几个问题：

- 文件越来越长，查找和修改困难
- 多人同时编辑同一个文件，Git 冲突会变多
- 图片、代码、参考文献分散，项目难以维护
- 格式定义和正文混在一起，复用性差

更推荐把 LaTeX 项目当成一个小型代码项目来管理：主文件只负责组织结构，正文、图片、格式、参考文献分目录存放。

### 3.2 推荐目录结构

```text
实验报告项目/
├── main.tex                    # 主文件，只负责组织全文结构
├── README.md                   # 项目说明、分工、编译方式
├── .gitignore                  # 忽略编译中间文件
├── format/
│   ├── labreport.cls           # 自定义文档类
│   └── custom.sty              # 自定义命令、环境、样式
├── content/
│   ├── abstract.tex            # 摘要
│   ├── environment.tex         # 实验环境
│   ├── principle.tex           # 实验原理
│   ├── task1.tex               # 任务一主文件
│   ├── task2.tex               # 任务二主文件
│   ├── conclusion.tex          # 总结
│   ├── task1/
│   │   ├── plan.tex            # 任务一方案设计
│   │   ├── process.tex         # 任务一实现过程
│   │   └── result.tex          # 任务一结果分析
│   └── task2/
│       ├── plan.tex
│       ├── process.tex
│       └── result.tex
├── figure/
│   ├── task1/
│   └── task2/
├── code/
│   ├── task1/
│   └── task2/
├── refs/
│   └── references.bib          # BibTeX 参考文献
└── build/                      # 编译输出目录，不提交到 Git
```

说明：

| 目录/文件 | 作用 |
| --- | --- |
| `main.tex` | 全文入口，负责引入各章节 |
| `format/` | 存放模板、格式、自定义命令 |
| `content/` | 存放正文内容 |
| `figure/` | 存放图片，建议按任务分类 |
| `code/` | 存放实验代码或关键代码片段 |
| `refs/` | 存放参考文献数据库 |
| `build/` | 存放编译产物，不建议提交 |

第三方宏包一般不需要复制到项目里，例如 `ctex`、`amsmath`、`graphicx` 等都应该由本地 LaTeX 发行版提供。项目里只放自己写的模板文件和样式文件即可。

## 4. 基础模板示例

### 4.1 `main.tex`

`main.tex` 应该尽量保持简洁，只负责组织文章结构。

```latex
\documentclass{format/labreport}

\title{实验报告标题}
\author{姓名1 \quad 姓名2 \quad 姓名3}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

\input{content/abstract.tex}
\input{content/environment.tex}
\input{content/principle.tex}
\input{content/task1.tex}
\input{content/task2.tex}
\input{content/conclusion.tex}

\bibliographystyle{plain}
\bibliography{refs/references}

\end{document}
```

注意：`\input{}` 的路径是以 `main.tex` 所在目录为基准的，不是以当前被引入文件所在目录为基准。

例如在 `content/task1.tex` 中继续引入 `content/task1/plan.tex`，应该写：

```latex
\input{content/task1/plan.tex}
\input{content/task1/process.tex}
\input{content/task1/result.tex}
```

不要写成：

```latex
\input{task1/plan.tex}
```

因为编译入口仍然是 `main.tex`。

### 4.2 `format/labreport.cls`

建议不要把自定义文档类命名为 `report.cls`，因为 LaTeX 本身就有标准 `report` 文档类，容易混淆。可以使用更明确的名字，例如 `labreport.cls`。

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{labreport}[2026/06/12 Lab report template]

\LoadClass[12pt,a4paper]{article}

\RequirePackage[UTF8]{ctex}
\RequirePackage{geometry}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{float}
\RequirePackage{xcolor}
\RequirePackage{listings}
\RequirePackage{hyperref}

\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}

\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  citecolor=blue,
  urlcolor=blue
}

\newcommand{\experiment}[1]{\section{实验 #1}}
\newcommand{\task}[1]{\subsection{任务 #1}}
```

如果格式要求比较复杂，例如学校有固定封面、页眉页脚、图表标题格式，可以继续在这个文件里扩展。正文文件只写内容，不要到处写格式命令。

### 4.3 插入图片示例

图片路径同样以 `main.tex` 所在目录为基准。

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.75\textwidth]{figure/task1/result.png}
  \caption{任务一实验结果}
  \label{fig:task1-result}
\end{figure}
```

正文中引用图片：

```latex
如图~\ref{fig:task1-result} 所示，实验结果符合预期。
```

图片命名建议使用英文、数字、下划线或短横线，例如 `task1_result.png`。尽量不要使用空格和特殊符号，避免跨平台路径问题。

## 5. Git 协作流程

### 5.1 基本原则

多人协作时，不要把 Git 当成网盘使用。Git 的核心价值是记录每次修改的原因和内容，所以提交要小而清晰。

建议遵守以下原则：

- 每个人负责明确的章节或任务文件
- 修改前先拉取最新版本
- 完成一个小功能或一小段内容后就提交
- 不要把 `build/`、临时文件、日志文件提交到仓库
- 尽量不要多人同时大改同一个 `.tex` 文件
- 格式调整集中到模板文件，正文中少写临时格式命令

### 5.2 推荐流程

第一次参与项目：

```powershell
git clone 仓库地址
cd 实验报告项目
```

每次开始写之前：

```powershell
git pull
```

完成一部分内容后：

```powershell
git add content/task1.tex content/task1/result.tex figure/task1/result.png
git commit -m "docs(task1): add result analysis"
git push
```

如果团队使用分支协作，可以按任务创建分支：

```powershell
git checkout -b task1-report
git push -u origin task1-report
```

写完后再通过 Pull Request 或 Merge Request 合并到主分支。

### 5.3 提交信息建议

提交信息不需要很长，但要让别人看得懂你改了什么。

推荐格式：

```text
docs(task1): add experiment principle
docs(task2): update result analysis
fix(format): adjust figure caption style
chore: update gitignore
```

常见前缀：

| 前缀 | 含义 |
| --- | --- |
| `docs` | 修改报告正文、说明文档 |
| `fix` | 修复错误 |
| `format` | 调整排版格式 |
| `chore` | 更新配置、忽略文件等杂项 |

### 5.4 `.gitignore` 示例

LaTeX 编译会产生大量中间文件，这些文件不应该提交到 Git。

```gitignore
# LaTeX build output
build/

# Common LaTeX temporary files
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.run.xml
*.synctex.gz
*.toc

# Editor files
.vscode/*
!.vscode/settings.json
```

是否提交最终 PDF 可以由团队决定。一般建议源码仓库主要保存 `.tex`、图片、代码和参考文献；最终版 PDF 可以放到 `release/` 目录，或者通过平台的 Release 功能发布。

## 6. 协作写作建议

### 6.1 一人负责一块，减少冲突

可以按任务分工：

| 成员 | 负责内容 |
| --- | --- |
| A | 实验环境、实验原理 |
| B | 任务一方案、过程、结果 |
| C | 任务二方案、过程、结果 |
| D | 总结、格式检查、最终编译 |

多人协作最怕所有人都改 `main.tex`。通常只有维护目录结构的人需要修改 `main.tex`，其他人只改自己负责的 `content/` 文件。

### 6.2 正文尽量一行一句

LaTeX 源文件中的换行通常不会直接影响 PDF 排版，因此可以采用“一行一句”的写法。这样 Git diff 更清晰，发生冲突时也更容易处理。

不推荐：

```latex
本实验首先完成环境配置，然后实现核心算法，最后对实验结果进行分析。通过对比不同参数下的输出结果，可以发现模型在特定条件下具有更好的稳定性。
```

推荐：

```latex
本实验首先完成环境配置，然后实现核心算法，最后对实验结果进行分析。
通过对比不同参数下的输出结果，可以发现模型在特定条件下具有更好的稳定性。
```

### 6.3 统一标签命名

交叉引用建议统一命名，避免重复。

```latex
\label{fig:task1-result}
\label{tab:task2-params}
\label{eq:loss-function}
\label{sec:experiment-environment}
```

常用前缀：

| 前缀 | 用途 |
| --- | --- |
| `fig:` | 图片 |
| `tab:` | 表格 |
| `eq:` | 公式 |
| `sec:` | 章节 |
| `lst:` | 代码 |

### 6.4 善用 AI，但不要直接粘贴

AI 可以帮助润色、生成表格、解释编译错误、整理实验步骤，但最终内容仍然需要人工检查。尤其是实验报告中的数据、结论和参考文献，必须以实际实验结果为准。

比较适合让 AI 做的事情：

- 根据实验指导书整理报告结构
- 将口语化描述润色成正式表达
- 把实验数据整理成 LaTeX 表格
- 根据报错日志定位 LaTeX 编译问题
- 检查段落逻辑是否连贯

不建议直接让 AI 生成最终结论后不检查就提交。实验报告最重要的是可复现、可解释、与真实结果一致。

## 7. 常见问题

### 7.1 中文显示乱码

优先检查三件事：

1. `.tex` 文件是否保存为 UTF-8 编码
2. 是否使用 XeLaTeX 编译
3. 是否加载了 `ctex` 或使用了 `ctexart`、`ctexrep` 等中文文档类

### 7.2 引用显示为 `??`

常见原因是编译次数不够。目录、交叉引用和参考文献通常需要多轮编译。

建议使用：

```text
latexmk (xelatex)
```

它会自动判断需要编译几轮。

### 7.3 找不到图片

重点检查图片路径。只要从 `main.tex` 开始编译，图片路径就应该以 `main.tex` 所在目录为基准。

正确示例：

```latex
\includegraphics{figure/task1/result.png}
```

### 7.4 编译突然出错

可以按下面顺序排查：

1. 查看 VS Code 中 LaTeX Workshop 的错误信息
2. 打开 `build/` 目录中的 `.log` 文件
3. 清空 `build/` 后重新编译
4. 检查最近一次修改的 `.tex` 文件
5. 检查括号、环境、公式符号是否成对出现

如果错误信息很长，可以把关键报错和相关 `.tex` 片段发给 AI 辅助分析。

### 7.5 Git 合并冲突怎么办

冲突文件中通常会出现类似内容：

```text
<<<<<<< HEAD
当前分支的内容
=======
别人提交的内容
>>>>>>> branch-name
```

处理方式：

1. 打开冲突文件
2. 判断应该保留哪部分，或手动合并两边内容
3. 删除 `<<<<<<<`、`=======`、`>>>>>>>` 标记
4. 保存文件并重新编译
5. `git add` 后提交

不要在没看懂的情况下直接全部接受一边，否则容易把队友的内容覆盖掉。

## 8. 最终交付前检查清单

提交最终报告前，建议检查：

- [ ] 能从 `main.tex` 成功编译出 PDF
- [ ] 目录、页码、图表编号正常
- [ ] 所有 `\ref{}`、`\cite{}` 都没有显示为 `??`
- [ ] 图片路径正确，图片清晰且编号完整
- [ ] 表格没有超出页面
- [ ] 公式编号和引用一致
- [ ] 参考文献格式符合要求
- [ ] `build/` 和临时文件没有提交到 Git
- [ ] 每位成员负责的内容都已经合并
- [ ] 最终 PDF 已经人工通读一遍

## 9. 参考链接

- [LaTeX 本地环境配置教程](https://blog.csdn.net/m0_59559215/article/details/158886485)
- [Git 安装教程](https://blog.csdn.net/mukes/article/details/115693833)
- [VS Code Git 使用指南](https://zhuanlan.zhihu.com/p/367494699)

## 10. 总结

本地 LaTeX 环境配合 Git 协作，真正解决的是两个问题：报告排版稳定，以及多人修改可追踪。只要项目结构清晰、分工明确、提交规范，实验报告就不会在最后一天变成一堆互相覆盖的文件。

推荐的做法很简单：

1. 用 `main.tex` 组织全文
2. 用 `content/` 拆分正文
3. 用 `figure/` 管理图片
4. 用 `format/` 管理格式
5. 用 Git 管理每一次修改
6. 用 `build/` 收纳编译产物

把这些习惯坚持下来，LaTeX 就不只是一个排版工具，而是一套更可靠的协作写作流程。

