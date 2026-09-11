import { run, claudeCode } from "@ai-hero/sandcastle";
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";

// Blank template: customize this to build your own orchestration.
// Run this with: npx tsx .sandcastle/main.mts
// Or add to package.json scripts: "sandcastle": "npx tsx .sandcastle/main.mts"

await run({
  agent: claudeCode("claude-opus-4-8"),
  sandbox: docker(),
  promptFile: "./.sandcastle/prompt.md",
  logging: {
    type: "file",
    path: "/Users/brianlane/Development/python/sandcastle-test/.sandcastle/logs/main.log",
  },
  hooks: {
    host: {
      onSandboxReady: [
        {
          command: "echo Setup complete!",
        },
      ],
    },
    sandbox: {
      // onSandboxReady: [{ command: "  tail -f .sandcastle/logs/main.log" }],
    },
  },
});
