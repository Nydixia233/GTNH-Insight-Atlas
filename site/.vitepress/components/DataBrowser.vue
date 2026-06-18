<script setup lang="ts">
import { computed, ref } from 'vue'
import { data as atlas } from '../theme/data.data'
import SourceTrace from './SourceTrace.vue'
import VerificationBadge from './VerificationBadge.vue'

const query = ref('')

const filteredFacts = computed(() => {
  const needle = query.value.trim().toLowerCase()
  if (!needle) return atlas.facts
  return atlas.facts.filter((fact) => {
    return [fact.id, fact.label, fact.unit, fact.document].some((value) =>
      String(value).toLowerCase().includes(needle)
    )
  })
})
</script>

<template>
  <section class="atlas-card">
    <label class="control-row">
      <span>Filter facts</span>
      <input v-model="query" class="atlas-input" type="search" placeholder="oc., ebf., voltage" />
    </label>
  </section>

  <section class="atlas-card">
    <table class="atlas-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Value</th>
          <th>Status</th>
          <th>Source</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="fact in filteredFacts" :key="fact.id">
          <td><code>{{ fact.id }}</code><br />{{ fact.label }}</td>
          <td><code>{{ Array.isArray(fact.value) ? fact.value.join(', ') : fact.value }}</code> {{ fact.unit }}</td>
          <td><VerificationBadge :status="fact.verification.status" /></td>
          <td>
            <SourceTrace v-for="source in fact.source" :key="`${source.file}:${source.line}`" :source="source" />
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
