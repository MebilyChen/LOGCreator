【网络问题，仓库暂时停更，如果有人知道怎么解决可以issue】  
![image](https://github.com/MebilyChen/LOGCreator/assets/71856534/373e0b58-4a65-4362-ac31-ff6be9f38d54)
![image](https://github.com/MebilyChen/LOGCreator/assets/71856534/f6067047-767d-4676-ab55-54029117bdd1)
```
18:06:34.969: [LOGCreator] git -c credential.helper= -c core.quotepath=false -c log.showSignature=false push --progress --porcelain origin refs/heads/master:master
Enumerating objects: 30, done.
Counting objects:   3% (1/28)
Counting objects:   7% (2/28)
Counting objects:  10% (3/28)
Counting objects:  14% (4/28)
Counting objects:  17% (5/28)
Counting objects:  21% (6/28)
Counting objects:  25% (7/28)
Counting objects:  28% (8/28)
Counting objects:  32% (9/28)
Counting objects:  35% (10/28)
Counting objects:  39% (11/28)
Counting objects:  42% (12/28)
Counting objects:  46% (13/28)
Counting objects:  50% (14/28)
Counting objects:  53% (15/28)
Counting objects:  57% (16/28)
Counting objects:  60% (17/28)
Counting objects:  64% (18/28)
Counting objects:  67% (19/28)
Counting objects:  71% (20/28)
Counting objects:  75% (21/28)
Counting objects:  78% (22/28)
Counting objects:  82% (23/28)
Counting objects:  85% (24/28)
Counting objects:  89% (25/28)
Counting objects:  92% (26/28)
Counting objects:  96% (27/28)
Counting objects: 100% (28/28)
Counting objects: 100% (28/28), done.
Delta compression using up to 12 threads
Compressing objects:   4% (1/23)
Compressing objects:   8% (2/23)
Compressing objects:  13% (3/23)
Compressing objects:  17% (4/23)
Compressing objects:  21% (5/23)
Compressing objects:  26% (6/23)
Compressing objects:  30% (7/23)
Compressing objects:  34% (8/23)
Compressing objects:  39% (9/23)
Compressing objects:  43% (10/23)
Compressing objects:  47% (11/23)
Compressing objects:  52% (12/23)
Compressing objects:  56% (13/23)
Compressing objects:  60% (14/23)
Compressing objects:  65% (15/23)
Compressing objects:  69% (16/23)
Compressing objects:  73% (17/23)
Compressing objects:  78% (18/23)
Compressing objects:  82% (19/23)
Compressing objects:  86% (20/23)
Compressing objects:  91% (21/23)
Compressing objects:  95% (22/23)
Compressing objects: 100% (23/23)
Compressing objects: 100% (23/23), done.
Writing objects:   4% (1/24)
Writing objects:   8% (2/24)
Writing objects:  12% (3/24)
Writing objects:  16% (4/24)
Writing objects:  20% (5/24)
Writing objects:  25% (6/24)
Writing objects:  29% (7/24)
Writing objects:  33% (8/24)
Writing objects:  37% (9/24)
Writing objects:  41% (10/24)
Writing objects:  45% (11/24)
Writing objects:  50% (12/24)
Writing objects:  54% (13/24)
error: RPC failed; HTTP 400 curl 92 HTTP/2 stream 0 was not closed cleanly: CANCEL (err 8)
send-pack: unexpected disconnect while reading sideband packet
Writing objects:  54% (13/24), 984.00 KiB | 32.00 KiB/s
Writing objects:  66% (16/24), 984.00 KiB | 32.00 KiB/s
Writing objects:  70% (17/24), 984.00 KiB | 32.00 KiB/s
Writing objects:  75% (18/24), 984.00 KiB | 32.00 KiB/s
Writing objects:  79% (19/24), 11.47 MiB | 384.00 KiB/s
Writing objects:  79% (19/24), 11.51 MiB | 375.00 KiB/s
Writing objects:  83% (20/24), 11.51 MiB | 375.00 KiB/s
Writing objects:  87% (21/24), 11.51 MiB | 375.00 KiB/s
Writing objects:  91% (22/24), 11.51 MiB | 375.00 KiB/s
Writing objects:  95% (23/24), 11.51 MiB | 375.00 KiB/s
Writing objects: 100% (24/24), 11.51 MiB | 375.00 KiB/s
Writing objects: 100% (24/24), 45.18 MiB | 1.42 MiB/s, done.
Total 24 (delta 12), reused 0 (delta 0), pack-reused 0
fatal: the remote end hung up unexpectedly
Done
```

# Usage
生成的exe程序在dist文件夹里，自己生成也行，这样能保证是最新版（因为每次都忘了上传exe）  
`pyinstaller --onefile --icon=AppSettings/icon.ico main_savev0.11_trpg.py`  
初次启动因为缺文件而有BUG，如果真有人想用，来问我要初始化启动文件  
![目录](https://github.com/MebilyChen/LOGCreator/assets/71856534/308267dd-8902-4ee7-aacc-e59ed9b66be5)
配合活字3使用更佳  
更新：基本适配了回声

# Updates
优化：多轮掷骰，尤其是全体掷骰的多轮掷骰表现，多轮掷骰和全体掷骰适配活字剧本格式（;分隔）  
修改了名牌里如果有【】活字输出会乱码的bug  
伤害掷骰格式由[技能名]伤害改成了[技能名伤害]  
修改了小地图修改角色标签的行为（修改标签不记录，因此生成新标签时使用的是旧数据，用于参考 → 修改标签后会记录，因此生成新标签时使用的是新数据，无法参考但能保证更新）  
更新了文字效果，需要导出活字格式使用，不导就是原样显示：`【高亮】`，`【【惊吓】】`，`（淡化）`，`[小高亮]`，代码里查询 `# 部分活字文字特效编辑` 跳转到编辑项（部分）  
把SAN值显示改成了SAN_/SAN（之前是SAN_/POW/SAN）   
图片支持gif啦(〃'▽'〃)    
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
输出活字Log格式时自动折叠多个连续【骰子】（不会按相同理由归纳，需要时尽量RP手动打断）
多轮掷骰优化
解决了无法增加角色栏的BUG
output log可自定义命名
回车环境状态栏可发送至log
优化了小地图导入图片
小地图隐藏文字标签
一些小修补
增加了自动保存（10分钟间隔）
多项修补+功能添加
优化了巴别塔bug
双击条目可查看全部信息
优化适配回声
保存output log时文件名会显示上一个起的名字（同次软件开启下）

.draw牌堆(draw_表示暗抽，?表示不放回)，格式json，详情可见程序或参考   
.draw高级命令：`.drawself` 用在角色栏，会生成独立牌组,`.alldraw`用在骰子栏，全员draw。  
两种牌堆格式：  
列表 `name.json` `["A"，"B"，"C"]` 可以直接抽，文件名name即为draw名。  
字典 `name.json` `{"AA":["A"，"B"，"C"],
"BB":["A"，"B"，"C"],
"CC":["A"，"B"，"C"],
"name":["A"，"B"，"C"，"{%BB%}"，"{%AA%}和{%BB%}"，"{%CC%}与{%AA%}"]
}` 需要具备一个与文件名相同的列表键，引用同文件下其他列表的格式为`{%xxx%}`   

.who [+理由] 随取幸运儿  
.whoabcd [+理由] 随取幸运顺序  
.yesno [+理由] 是否  

# Todo
## --计算
暂无
## --features 
优化：自动加减基础数值（MP、HP）（不这么做是因为要有理由Focus再UnFocus笔记栏来保存..设置了health_data但没有投入使用，就看怎么用方便）   
优化：NPC列表  
优化：推理信息库-计算器直接显示在共用库栏位（新建一个Frame，避免无法发布到另一个窗口），精简框架，不要占满屏  
优化：牌堆；实用命令，比如抽人 .who ABCD等  
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
【多轮掷骰】命令头部的`*`表示轮数（3`*`意志）  
【暗骰】保持焦点在暗骰角色的消息框，点击Bot的掷骰按钮（公式取自暗骰角色，是否显示技能名取决于Bot公式栏）"  
【.st draw who[+理由] whoabcd[+理由] yesno[+理由]】输入后点击发送按钮或回车（而不是掷骰按钮）    
【掷骰原因】消息栏填写掷骰原因，可以包括技能文字点掷骰按钮来触发检定（例如“我使用r斗殴击晕敌人”）"   
【HP/MP+-】在公式栏填写（例如“HP+1d3”  

## 如何创建NPC模板
0. 如果巴别塔报错，先关闭巴别塔（把文件名改一下就行）  
1. 创建新角色，更名为模板名（比如“基本怪物”、“基本人类”、“基本邪教徒”、“Muffin Stinger”（姓名也可以在创建 / 导入模板后再改））  
2. 。st录入数值  
3. 重启程序（关闭程序时会自动保存）  
4. 在KP栏把自己的名字改成模板名，会自动录入数值(即时数值例如HP、MP变化不会录入)。如果不想更改KP，新建一个NPC栏来用也行，最好不用骰子栏，会出奇怪BUG" 。或者多开程序也行，但注意一定要分开保存程序数据文件，被覆盖就会哭哭。  
5. 如果要重新启用巴别塔，删除新创建的角色，改回第0步的文件名（除非把新添加的角色也加入巴别塔）  
