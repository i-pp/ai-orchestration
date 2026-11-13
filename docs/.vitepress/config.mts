import { defineConfig } from "vitepress";

export default defineConfig({
  lang: "en-US",
  title: "AI Orchestration",
  description: "Canonical AI development orchestration policies and documentation.",
  // Keep historical source examples out of the generated site until publication review.
  srcExclude: ["ai/example/**"],
  markdown: {
    config(md) {
      md.core.ruler.after("inline", "repository-root-links", (state) => {
        for (const block of state.tokens) {
          if (block.type !== "inline" || !block.children) continue;
          for (const token of block.children) {
            if (token.type !== "link_open") continue;
            const href = token.attrGet("href");
            if (href === "../../.codex/agents/technical-documentation.toml") {
              token.attrSet("href", "https://github.com/i-pp/ai-orchestration/blob/main/.codex/agents/technical-documentation.toml");
            } else if (href === "../../.agents/skills/") {
              token.attrSet("href", "https://github.com/i-pp/ai-orchestration/tree/main/.agents/skills/");
            }
          }
        }
      });
    },
  },
  themeConfig: {
    nav: [
      { text: "Repository", link: "https://github.com/i-pp/ai-orchestration" },
      { text: "\u65e5\u672c\u8a9e", link: "/ai/documentation-policy_jp" },
    ],
    sidebar: [
      { text: "Overview", link: "/" },
      {
        text: "Governance",
        items: [
          { text: "Orchestration architecture", link: "/ai/orchestration" },
          { text: "Execution policies", link: "/ai/policies" },
          { text: "Engineering editorial policy", link: "/ai/editorial-policy" },
        ],
      },
      {
        text: "Technical documentation",
        items: [
          { text: "Documentation policy", link: "/ai/documentation-policy" },
          { text: "Japanese translation", link: "/ai/documentation-policy_jp" },
          { text: "Inventory and migration", link: "/ai/documentation-inventory" },
        ],
      },
    ],
  },
});
