import { defineConfig } from "vitepress";

export default defineConfig({
  lang: "en-US",
  title: "AI Orchestration",
  description: "Canonical AI development orchestration policies and documentation.",
  // Keep historical source examples out of the generated site until publication review.
  srcExclude: ["ai/example/**"],
  themeConfig: {
    nav: [
      { text: "Repository", link: "https://github.com/i-pp/ai-orchestration" },
      { text: "日本語", link: "/ai/documentation-policy_jp" },
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
