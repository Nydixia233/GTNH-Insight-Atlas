# _local/ — 本地参考区（不入库）

> ⚠️ 本目录除了这个 `README.md`，**所有内容都被 git 忽略**（见根 [.gitignore](../.gitignore)）。
> 放你本地分析时要参考、但**不应上传**的大体积或受版权约束的文件。

---

## 放什么

| 内容 | 例子 |
|------|------|
| mod 源码本体 | GT5-Unofficial 源码树、StructureLib 源码 |
| 反编译 / 映射产物 | MCP 反混淆输出、字节码 dump |
| 离线资料副本 | GTNH Wiki 页面、Dev-Doc 的本地快照 |
| 本地实验 jar / 配置 | 从 `.minecraft/mods/` 拷来的 `gregtech-*.jar` |

实际已放入的内容（2026-06-10 从 `2.9.0-beta-1` Java 17-25 实例提取 + 上游源码）：

```
_local/
├── README.md                ← 唯一入库文件
├── gt5u-src/                ← GT5-Unofficial 源码 @ tag 5.09.52.594（主力参考，含注释）
│                              ※ 单体大仓库,已合并 bartworks/gtPlusPlus/tectech/goodgenerator/
│                                kekztech/gtnhintergalactic/gtnhlanth/kubatech 等 15 个子 mod 源码
│                                终局多方块(Eye of Harmony / Forge of Gods)也在此(tectech 包)
├── nhcoremod-src/           ← GTNewHorizonsCoreMod 源码 @ tag 2.8.279(GTNH 魔改/自定义配方层)
├── structurelib-src/        ← StructureLib 源码 @ tag 1.4.38
├── gtnhlib-src/             ← gtnhlib 源码 @ tag 0.11.9
├── gtnh-dev-doc/            ← 官方 GTNH-Dev-Doc(进程 16 阶段权威源,master)
├── jars/                    ← 三个核心 jar(字节码,IDE 反编译/挂源码用)
│   ├── gregtech-5.09.52.594.jar
│   ├── structurelib-1.4.38.jar
│   └── gtnhlib-0.11.9.jar
├── questbook/               ← BetterQuesting 任务书(JSON,进程金矿,可对照 16 阶段)
│   └── DefaultQuests/{Quests,QuestLines,...}
├── config-gregtech/         ← GregTech config(电压/矿脉/污染等数值实测基准)
│   └── {MachineStats,WorldGeneration,Pollution,...}.cfg
├── config-gtnh/             ← GTNH 自定义数据(CustomToolTips/Fuels/Drops)
├── lang/                    ← GregTech.lang(英) + GregTech_zh_CN.lang(中,内部名↔显示名)
├── changelog-2.8.4-to-2.9.0-beta-1.md   ← 版本差异
└── mods-manifest.txt        ← 241 个 mod 的文件名清单(不拷本体)
```

> ⚠️ jar 内仅 `.class`（无 `.java`）。读源码请用 `gt5u-src/` 等克隆的源码树，或在 IDE 里给 jar 挂上对应 tag 的源码。

---

## 为什么不入库

1. **版权**：GT5U 等 mod 各有 license，不镜像整份源码。本仓库只保留**带出处的短片段**，放在各主题的 `topics/*/snippets/`。
2. **体积**：源码树、jar、反编译产物体积大，不该进文档仓库。
3. **可重建**：这些都能从上游按 [VERSION.md](../VERSION.md) 锁定的版本重新获取，无需版本控制。

---

## 怎么用

1. 源码已克隆到位(`gt5u-src/` 等),版本已锁进 [VERSION.md](../VERSION.md)。
2. 在 IDE(IntelliJ)里打开 `_local/gt5u-src/` 做跳转、查调用、断点。
3. 分析得到的**短片段**,连同 `文件:行号` 出处,誊抄到对应主题的 `snippets/` —— 那才是入库的部分。
4. 整合包更新后:重新提取 jar/config,按新版本号重新拉源码,更新 [VERSION.md](../VERSION.md)。

> 一句话:`_local/` 是你的工作台,`topics/*/snippets/` 是带出处的成品摘录。
