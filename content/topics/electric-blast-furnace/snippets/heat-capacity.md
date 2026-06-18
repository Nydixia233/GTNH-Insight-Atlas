---
title: EBF Heat Capacity Snippet
slug: ebf-heat-capacity-snippet
axis: topic
status: source-only
version_anchor: GTNH 2.9.0-beta-1
source_version: GT5-Unofficial 5.09.52.594
sources:
  - gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:237
---

# EBF Heat Capacity Snippet

Source anchor: `gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:237`.

```java
this.mHeatingCapacity = (int) getCoilLevel().getHeat() + 100 * (GTUtility.getTier(getMaxInputVoltage()) - 2);
```
