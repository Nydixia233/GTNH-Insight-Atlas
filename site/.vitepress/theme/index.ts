import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import DataBrowser from '../components/DataBrowser.vue'
import DataDashboard from '../components/DataDashboard.vue'
import FactCard from '../components/FactCard.vue'
import KnowledgeGraph from '../components/KnowledgeGraph.vue'
import OverclockSandbox from '../components/OverclockSandbox.vue'
import SourceTrace from '../components/SourceTrace.vue'
import VerificationBadge from '../components/VerificationBadge.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('DataBrowser', DataBrowser)
    app.component('DataDashboard', DataDashboard)
    app.component('FactCard', FactCard)
    app.component('KnowledgeGraph', KnowledgeGraph)
    app.component('OverclockSandbox', OverclockSandbox)
    app.component('SourceTrace', SourceTrace)
    app.component('VerificationBadge', VerificationBadge)
  }
} satisfies Theme
