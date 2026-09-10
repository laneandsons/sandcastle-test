# Context

<!-- Use !`command` to pull in dynamic context. Commands run inside the sandbox. -->
<!-- Example: !`git log --oneline -10` or !`gh issue list --state open --label Sandcastle --limit 100 --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` -->

# Task

<!-- Describe what the agent should do. -->

Build a small CLI tool that accepts one argument, a language name, and outputs a "Hello World" example in that language. Make sure to include the languages Gleam and Haskell, and half a dozen other highly used languages.

Please build this in Python using uv. 

# Done
When the task is complete, output <promise>COMPLETE</promise> to signal early termination.
