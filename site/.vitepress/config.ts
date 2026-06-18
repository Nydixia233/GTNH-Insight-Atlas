import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import yaml from '@rollup/plugin-yaml'
import { defineConfig } from 'vitepress'

const here = path.dirname(fileURLToPath(import.meta.url))
const root = path.resolve(here, '../..')
const generated = path.resolve(root, 'generated')
const markdownIndexPath = path.join(generated, 'markdown-index.json')
const markdownIndex = fs.existsSync(markdownIndexPath)
  ? JSON.parse(fs.readFileSync(markdownIndexPath, 'utf-8'))
  : { sidebar: [] }

export default defineConfig({
  title: 'GTNH Insight Atlas',
  description: 'Data-backed, source-traceable GTNH knowledge atlas.',
  srcDir: '../content',
  outDir: '.vitepress/dist',
  cleanUrls: true,
  themeConfig: {
    nav: [
      { text: 'GTNH 2.9.0-beta-1 · GT5U 5.09.52.594', link: '/' },
      { text: 'Data Browser', link: '/pages/data-browser' },
      { text: 'Graph', link: '/topics/electric-blast-furnace/analysis' }
    ],
    sidebar: markdownIndex.sidebar,
    search: {
      provider: 'local'
    }
  },
  vite: {
    plugins: [yaml()],
    resolve: {
      alias: {
        '@data': path.resolve(root, 'data'),
        '@generated': generated
      }
    }
  }
})
