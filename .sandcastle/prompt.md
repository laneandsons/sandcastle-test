# Context

<!-- Use !`command` to pull in dynamic context. Commands run inside the sandbox. -->
<!-- Example: !`git log --oneline -10` or !`gh issue list --state open --label Sandcastle --limit 100 --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` -->

# Task

<!-- Describe what the agent should do. -->

Read the Sandcastle issues available for this repo.

If it is empty, Close the issue and proceed to the next one.

If there is work to do, please perform the work and create a PR, then go to the next issue and repeat.

# Done

When the task is complete, output <promise>COMPLETE</promise> to signal early termination.
