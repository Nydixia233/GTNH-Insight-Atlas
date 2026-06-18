<script setup lang="ts">
import { data as atlas } from '../theme/data.data'
</script>

<template>
  <section class="atlas-grid">
    <div class="atlas-two">
      <article class="atlas-card">
        <h1>GTNH Insight Atlas</h1>
        <p>
          A data-backed, source-traceable vertical slice for Electric Blast Furnace,
          overclocking, and voltage tiers.
        </p>
      </article>
      <article class="atlas-card">
        <h2>Audit Summary</h2>
        <table class="atlas-table">
          <tbody>
            <tr><th>Pages</th><td>{{ atlas.stats.page_count }}</td></tr>
            <tr><th>Facts</th><td>{{ atlas.stats.fact_count }}</td></tr>
            <tr><th>Verified</th><td>{{ atlas.stats.statuses.verified }}</td></tr>
            <tr><th>Source only</th><td>{{ atlas.stats.statuses['source-only'] }}</td></tr>
          </tbody>
        </table>
      </article>
    </div>
    <div class="atlas-two">
      <a class="atlas-card" href="/topics/electric-blast-furnace/">Electric Blast Furnace</a>
      <a class="atlas-card" href="/foundations/overclock">Overclocking</a>
      <a class="atlas-card" href="/reference/voltage-tiers">Voltage tiers</a>
      <a class="atlas-card" href="/pages/data-browser">Data browser</a>
    </div>
  </section>
</template>
