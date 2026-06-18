<script setup lang="ts">
const props = defineProps<{
  status: string
}>()

const labels: Record<string, string> = {
  verified: 'verified',
  'source-only': 'source only',
  pending: 'pending',
  contradicted: 'contradicted'
}

const marks: Record<string, string> = {
  verified: 'OK',
  'source-only': 'SRC',
  pending: 'TODO',
  contradicted: 'ERR'
}
</script>

<template>
  <span class="verification-badge" :data-status="props.status">
    <span>{{ marks[props.status] ?? props.status }}</span>
    <span>{{ labels[props.status] ?? props.status }}</span>
  </span>
</template>
