<script setup lang="ts">
import { computed } from 'vue'
import { data as atlas } from '../theme/data.data'
import SourceTrace from './SourceTrace.vue'
import VerificationBadge from './VerificationBadge.vue'

const props = defineProps<{
  id: string
}>()

const fact = computed(() => atlas.factsById[props.id])

function displayValue(value: unknown): string {
  if (Array.isArray(value)) return value.join(', ')
  if (typeof value === 'boolean') return value ? 'true' : 'false'
  return String(value)
}
</script>

<template>
  <section v-if="fact" class="atlas-card fact-card">
    <h3>{{ fact.label }}</h3>
    <VerificationBadge :status="fact.verification.status" />
    <p class="fact-value">{{ displayValue(fact.value) }} <small>{{ fact.unit }}</small></p>
    <p v-if="fact.notes">{{ fact.notes }}</p>
    <div class="atlas-grid">
      <SourceTrace v-for="source in fact.source" :key="`${source.file}:${source.line}`" :source="source" />
    </div>
  </section>
  <section v-else class="atlas-card fact-card">
    <h3>Missing fact</h3>
    <p class="fact-value">{{ props.id }}</p>
  </section>
</template>
