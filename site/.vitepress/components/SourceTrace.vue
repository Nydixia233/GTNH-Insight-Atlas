<script setup lang="ts">
import type { SourceEntry } from '../theme/data.data'

const props = defineProps<{
  source: SourceEntry
}>()

const lockedVersion = '5.09.52.594'
const href = `https://github.com/GTNewHorizons/GT5-Unofficial/blob/${props.source.version}/src/main/java/${props.source.file}#L${props.source.line}`
</script>

<template>
  <span>
    <a class="source-trace" :href="href" target="_blank" rel="noreferrer">
      <span class="source-trace-text">{{ props.source.file }}:{{ props.source.line }}</span>
    </a>
    <span v-if="props.source.version !== lockedVersion" class="verification-badge" data-status="contradicted">
      version mismatch
    </span>
  </span>
</template>
