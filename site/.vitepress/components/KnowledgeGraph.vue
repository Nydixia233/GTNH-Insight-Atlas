<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { data as atlas } from '../theme/data.data'

const el = ref<HTMLDivElement | null>(null)

onMounted(() => {
  if (!el.value) return
  const chart = echarts.init(el.value)
  chart.setOption({
    tooltip: {},
    legend: [{ data: ['doc', 'fact', 'source'] }],
    series: [
      {
        type: 'graph',
        layout: 'force',
        roam: true,
        categories: [{ name: 'doc' }, { name: 'fact' }, { name: 'source' }],
        data: atlas.graph.nodes.map((node) => ({
          id: node.id,
          name: node.id,
          category: node.type,
          symbolSize: node.type === 'doc' ? 38 : 24
        })),
        links: atlas.graph.edges.map((edge) => ({
          source: edge.from,
          target: edge.to,
          value: edge.type
        })),
        label: {
          show: true,
          fontSize: 10,
          overflow: 'truncate',
          width: 120
        },
        force: {
          repulsion: 120,
          edgeLength: 80
        }
      }
    ]
  })
  window.addEventListener('resize', () => chart.resize())
})
</script>

<template>
  <div ref="el" class="graph-surface" aria-label="Atlas knowledge graph"></div>
</template>
