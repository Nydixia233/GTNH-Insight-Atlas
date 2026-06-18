<script setup lang="ts">
import { computed, ref } from 'vue'
import overclockFacts from '@data/mechanics/overclock.yml'
import { data as atlas } from '../theme/data.data'
import FactCard from './FactCard.vue'

const recipeEUt = ref(30)
const duration = ref(200)
const machineVoltage = ref(512)
const machineHeat = ref(3600)
const recipeHeat = ref(1800)
const perfect = ref(true)

function factValue(id: string): number {
  const found = atlas.factsById[id]
  return Number(found?.value ?? overclockFacts.find((fact: { id: string }) => fact.id === id)?.value)
}

function log4ceil(value: number): number {
  let tier = 0
  let threshold = 8
  while (threshold < value) {
    threshold *= 4
    tier += 1
  }
  return tier
}

const result = computed(() => {
  const eutIncrease = factValue('oc.eut-increase-per-oc')
  const normalDivisor = perfect.value
    ? factValue('oc.duration-divisor-perfect')
    : factValue('oc.duration-divisor-normal')
  const heatDivisor = factValue('oc.heat-oc-divisor')
  const machineTier = Math.max(log4ceil(machineVoltage.value / 8), 1)
  const recipeTier = Math.max(log4ceil(recipeEUt.value / 8), 1)
  const overclocks = Math.max(machineTier - recipeTier, 0)
  const heatOverclocks = Math.min(Math.floor((machineHeat.value - recipeHeat.value) / 1800), overclocks)
  const regularOverclocks = overclocks - heatOverclocks
  const outputEUt = Math.ceil(recipeEUt.value * Math.pow(eutIncrease, overclocks))
  const outputDuration = Math.max(
    Math.floor(duration.value / Math.pow(heatDivisor, heatOverclocks) / Math.pow(normalDivisor, regularOverclocks)),
    1
  )
  return { overclocks, heatOverclocks, regularOverclocks, outputEUt, outputDuration }
})
</script>

<template>
  <section class="atlas-card">
    <div class="atlas-two">
      <div>
        <label class="control-row">
          <span>Recipe EUt</span>
          <input v-model.number="recipeEUt" class="atlas-input" type="number" min="1" />
        </label>
        <label class="control-row">
          <span>Duration</span>
          <input v-model.number="duration" class="atlas-input" type="number" min="1" />
        </label>
        <label class="control-row">
          <span>Machine voltage</span>
          <input v-model.number="machineVoltage" class="atlas-input" type="number" min="8" />
        </label>
        <label class="control-row">
          <span>Machine heat</span>
          <input v-model.number="machineHeat" class="atlas-input" type="number" />
        </label>
        <label class="control-row">
          <span>Recipe heat</span>
          <input v-model.number="recipeHeat" class="atlas-input" type="number" />
        </label>
        <label class="control-row">
          <span>Perfect overclock</span>
          <input v-model="perfect" type="checkbox" />
        </label>
      </div>
      <div class="atlas-card">
        <h3>Result</h3>
        <table class="atlas-table">
          <tbody>
            <tr><th>Total overclocks</th><td>{{ result.overclocks }}</td></tr>
            <tr><th>Heat overclocks</th><td>{{ result.heatOverclocks }}</td></tr>
            <tr><th>Regular overclocks</th><td>{{ result.regularOverclocks }}</td></tr>
            <tr><th>Output EUt</th><td>{{ result.outputEUt }}</td></tr>
            <tr><th>Output duration</th><td>{{ result.outputDuration }}</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
  <div class="atlas-two">
    <FactCard id="oc.eut-increase-per-oc" />
    <FactCard id="oc.heat-oc-divisor" />
  </div>
</template>
