# KiCad Basics

KiCad 是一个开源 EDA 软件，可以完成从原理图到 PCB 制造文件的完整流程。

KiCad 常见文件包括：

- `.kicad_sch`：原理图文件。
- `.kicad_pcb`：PCB 布局文件。
- Gerber 文件：用于 PCB 制造。
- Drill 文件：用于描述钻孔信息。

KiCad 典型操作流程：

1. 新建工程。
2. 绘制原理图。
3. 为元器件分配封装。
4. 更新 PCB。
5. 放置元器件。
6. 布线。
7. 运行 DRC。
8. 导出制造文件。

对于 AI 工程实践，KiCad 文件可以作为结构化数据来源。后续可以用 Python 解析原理图、网表和 PCB 文件，提取元器件、引脚、网络和坐标信息。

