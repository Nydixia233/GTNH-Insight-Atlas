import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineLoader } from 'vitepress'

const here = path.dirname(fileURLToPath(import.meta.url))
const root = path.resolve(here, '../../..')
const siteDataPath = path.resolve(root, 'generated/site-data.json')
const graphPath = path.resolve(root, 'generated/link-graph.json')

export interface SourceEntry {
  file: string
  line: number
  end_line?: number
  version: string
  expect?: string
}

export interface AtlasFact {
  id: string
  label: string
  value: string | number | boolean | unknown[]
  unit: string
  source: SourceEntry[]
  verification: {
    status: string
    method: string
    record?: string
  }
  notes?: string
  document: string
}

export default defineLoader({
  watch: [siteDataPath, graphPath],
  load() {
    const siteData = JSON.parse(fs.readFileSync(siteDataPath, 'utf-8'))
    const graph = JSON.parse(fs.readFileSync(graphPath, 'utf-8'))
    return {
      ...siteData,
      graph,
      factsById: Object.fromEntries(siteData.facts.map((fact: AtlasFact) => [fact.id, fact]))
    }
  }
})
