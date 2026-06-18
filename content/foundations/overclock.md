---
title: Overclocking
slug: overclock
axis: foundation
status: source-only
version_anchor: GTNH 2.9.0-beta-1
source_version: GT5-Unofficial 5.09.52.594
sources:
  - gregtech/api/util/OverclockCalculator.java:33
  - gregtech/api/util/OverclockCalculator.java:35
  - gregtech/api/util/OverclockCalculator.java:57
  - gregtech/api/util/OverclockCalculator.java:63
  - gregtech/api/util/OverclockCalculator.java:125
---

# Overclocking

The Atlas stores overclock constants as facts and lets components consume those facts. The power multiplier is anchored at `gregtech/api/util/OverclockCalculator.java:33`; normal duration division at `gregtech/api/util/OverclockCalculator.java:35`; heat overclock division at `gregtech/api/util/OverclockCalculator.java:57`; heat discount exponent at `gregtech/api/util/OverclockCalculator.java:63`; and perfect overclock duration division at `gregtech/api/util/OverclockCalculator.java:125`.

<div class="atlas-two">
  <FactCard id="oc.eut-increase-per-oc" />
  <FactCard id="oc.duration-divisor-normal" />
  <FactCard id="oc.duration-divisor-perfect" />
  <FactCard id="oc.heat-oc-divisor" />
  <FactCard id="oc.heat-discount-exponent" />
  <FactCard id="oc.duration-divide-loop" />
</div>
