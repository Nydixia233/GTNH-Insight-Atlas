# Version Anchor

This file is the single source of truth for the Atlas version model.

## Site Anchor

| Item | Value |
| --- | --- |
| Modpack | GregTech: New Horizons |
| Release | `2.9.0-beta-1` |
| Package line | Java 17-25 |
| Pack name | `GT_New_Horizons_2.9.0-beta-1_Java_17-25` |

The site navigation displays this pack-level anchor for human orientation.

## Source Anchors

Mechanic facts are anchored to the exact mod versions present in the running pack jars.

| Mod | Locked version | Local reference |
| --- | --- | --- |
| GT5-Unofficial | `5.09.52.594` | `_local/gt5u-src/` |
| StructureLib | `1.4.38` | `_local/structurelib-src/` |
| NewHorizonsCoreMod | `2.8.279` | `_local/nhcoremod-src/` |
| GTNHLib | `0.11.9` | `_local/gtnhlib-src/` |

`data/**/*.yml` source entries must use `source.version: 5.09.52.594` for GT5U facts. `source_refs.py` verifies the referenced file, line, and optional `expect` snippet against `_local/gt5u-src/src/main/java` unless `GT5U_SRC` overrides that path.

## Why Two Anchors

GTNH is a modpack, not one source repository. A pack release name is useful for players, but source-level claims need the exact mod jar version. Beta pack names can also move while individual mod versions change. This project therefore records both:

- pack release for site context
- exact mod version for source validation
