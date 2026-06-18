---
title: EBF Verification
slug: electric-blast-furnace-verification
axis: topic
status: verified
version_anchor: GTNH 2.9.0-beta-1
source_version: GT5-Unofficial 5.09.52.594
sources:
  - gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:214
---

# EBF Verification

The first verified record for this slice is the heat gate: a recipe is accepted when `recipe.mSpecialValue <= mHeatingCapacity`.

<FactCard id="ebf.heat-gate" />
