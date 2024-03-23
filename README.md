# Usage
生成的exe程序在dist文件夹里，自己生成也行，这样能保证是最新版（因为每次都忘了上传exe）  
`pyinstaller --onefile --icon=AppSettings/icon.ico main_savev0.11_trpg.py`  
初次启动因为缺文件而有BUG，如果真有人想用，来问我要初始化启动文件  
![目录](https://github.com/MebilyChen/LOGCreator/assets/71856534/308267dd-8902-4ee7-aacc-e59ed9b66be5)
配合活字3使用更佳  

# Updates
图片支持gif啦  
更新了TRPG掷骰模块:联合骰、SC、优劣势、补正骰、对抗骰、武器伤害Built-in  
更新了自定义数值/笔记栏  
.st存入Json数据库  
技能成长自动判定  
导出技能st  
骰子性格（结果播报语句。但因为不会出现在log里，所以基本也没啥影响...）  
时间模块  
#Armor  
推理信息库  
载入新立绘时自动插入活字命令  
巴别塔（看控制台）  
装载NPC模板，保留栏位名称并读取某一模板    

# Todo
## --计算
自动加减基础数值（MP、HP）（不这么做是因为要有理由Focus再UnFocus笔记栏来保存..但已经设置了health_data了，就看怎么用方便）  
## --features
优化：NPC列表  
优化推理信息库-计算器直接显示在共用库栏位（新建一个Frame，避免无法发布到另一个窗口），精简框架，不要占满屏  
牌堆；实用命令，比如抽人 .who ABCD等 (基本坑，暂时先去用正经骰娘Bot吧)  
输出染色HTML，骰子性格：针对每个技能单独comment(坑)  
优化地图，实现实时同步数值和时间，Canvas保存  
## --bugs
复杂掷骰算式（多个不同面骰子+常数）优化  
补正骰优化  
对抗骰优化  
武器伤害Built-in优化 
自动加减基础数值（SAN）优化  
巴别塔新增角色BUG  
Armor显示优化  
小地图图形缩放BUG  

# Tips
## 界面
### 主界面  
最多支持到7个PL+1Bot+1KP一共9个栏位，可以继续加，但界面会崩  
![主界面](https://github.com/MebilyChen/LOGCreator/assets/71856534/be388bcb-a07f-449e-a38a-869d2d95a281)
状态Icon演示：  
![状态Icon演示](https://github.com/MebilyChen/LOGCreator/assets/71856534/beb13955-67b5-4c89-acdb-6d0cc25ea645)
掷骰演示：  
![掷骰演示](https://github.com/MebilyChen/LOGCreator/assets/71856534/f5a6f1d3-136c-4a5e-ad9a-132a171ec8d3)
![掷骰演示2](https://github.com/MebilyChen/LOGCreator/assets/71856534/0b3235a3-5aa0-4c07-98ca-4b75be60bb9b)
### 调查信息库界面
![调查信息库界面](https://github.com/MebilyChen/LOGCreator/assets/71856534/6d996d5c-9c7a-46c8-a124-97baaede4953)
### 小地图
![简易地图](https://github.com/MebilyChen/LOGCreator/assets/71856534/6bfc25c0-0a20-40e8-a761-978970636e57)
![地图使用](https://github.com/MebilyChen/LOGCreator/assets/71856534/0e79fff3-cfa9-4b84-a182-48a8a7e36d0f)
### 巴别塔模块 
![巴别塔](https://github.com/MebilyChen/LOGCreator/assets/71856534/7034db10-ceef-4347-9e6d-1d0fef8273c2)
### 活字3支持
![活字3命令支持](https://github.com/MebilyChen/LOGCreator/assets/71856534/1f984fb9-6282-4942-8623-2129143d2db6)

## 交互
.st HP、MP时均修改的是上限，修改实时hp/mp需使用掷骰栏掷骰，或者直接修改。在角色笔记栏中修改不会实时影响到角色卡数值，退出时才会保存到角色卡
使用 .st#斗殴@1D3+5来载入武器伤害公式  
小地图可用于追逐、探索和战斗，更好的战斗体验可以结合CCF。小地图中的M是MOV，不是MP  
NPC活动也可以用程序多开+复制粘贴，但如此就无法无缝RP"（而且战斗时无法触发PC的Armor显示、无法同步计算时间等），建议KP栏装载至少一个常用NPC，或者保证留有NPC栏位。  
一些复杂操作：  
[右键姓名牌] 选择简卡图片  
[左键头像栏] 选择头像  
[左键Icon栏] 选择状态Icon  
[右键头像栏/Icon栏] 状态Icon叠加/撤销  
[左键@] 在Focus文本框插入@角色名  
[右键@] 插入活字命令  
如果没有头像图和状态Icon，就会缩进到Frame内的左侧，左上是状态，左中是头像  

## 掷骰
复制Bot消息至此并发送，或：  
【掷骰】点击每个角色的掷骰按钮进行掷骰，公式栏填写公式或技能，留空默认1d100"  
【优劣势】命令头部的+/-表示优劣势（++意志30）"  
【补正骰】命令后部的+/-表示补正（意志+30）"  
【联合骰】技能1+技能2+技能3..."  
【对抗骰】在角色消息栏@其他对抗人 并点击掷骰"  
【全体掷骰】保持焦点在Bot消息框，点击Bot的掷骰按钮"  
【暗骰】保持焦点在暗骰角色的消息框，点击Bot的掷骰按钮（公式取自暗骰角色）"  
【.st】输入后点击发送按钮或回车（而不是掷骰按钮）"  
【掷骰原因】消息栏填写掷骰原因，可以包括技能文字点掷骰按钮来触发检定（例如“我使用r斗殴击晕敌人”）"   

## 如何创建NPC模板
0. 如果巴别塔报错，先关闭巴别塔（把文件名改一下就行）  
1. 创建新角色，更名为模板名（比如“基本怪物”、“基本人类”、“基本邪教徒”、“Muffin Stinger”（姓名也可以在创建 / 导入模板后再改））  
2. 。st录入数值  
3. 重启程序（关闭程序时会自动保存）  
4. 在KP栏把自己的名字改成模板名，会自动录入数值(即时数值例如HP、MP变化不会录入)。如果不想更改KP，新建一个NPC栏来用也行，最好不用骰子栏，会出奇怪BUG" 。或者多开程序也行，但注意一定要分开保存程序数据文件，被覆盖就会哭哭。  
5. 如果要重新启用巴别塔，删除新创建的角色，改回第0步的文件名（除非把新添加的角色也加入巴别塔）  
