---
title: EBF Analysis
slug: electric-blast-furnace-analysis
axis: topic
status: source-only
version_anchor: GTNH 2.9.0-beta-1
source_version: GT5-Unofficial 5.09.52.594
sources:
  - gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:61
  - gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:214
  - gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:237
---

# EBF Analysis

`MTEElectricBlastFurnace` is the controller class for the EBF vertical slice. The class identity is anchored at `gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:61`.

The recipe heat gate compares the recipe special value to the cached heating capacity: `gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:214`.

The capacity formula adds coil heat to the voltage-tier bonus at `gregtech/common/tileentities/machines/multi/MTEElectricBlastFurnace.java:237`.

<div class="atlas-two">
  <FactCard id="ebf.class-definition" />
  <FactCard id="ebf.heat-gate" />
  <FactCard id="ebf.heat-capacity-formula" />
  <FactCard id="ebf.coil-base-heat" />
</div>

Overclock constants used by the EBF path are shared with the global calculator. The normal duration divisor is not repeated here; it is referenced from the data layer.

<FactCard id="oc.duration-divisor-normal" />

<KnowledgeGraph />
