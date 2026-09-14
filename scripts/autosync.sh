#!/usr/bin/env bash
# Auto-commit and push the repo. Run by the forgeai-autosync systemd user timer.
# Never force-pushes. Aborts (without committing) on likely secrets or files over 50 MB.
set -uo pipefail

REPO="/home/aliz/Documents/Codes/forgeAI-hackathon"
cd "$REPO" || exit 1
exec >>"$REPO/.autosync.log" 2>&1
ts="$(date '+%F %T')"

if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || [ -f .git/MERGE_HEAD ]; then
  echo "$ts skip: rebase/merge in progress"; exit 0
fi

branch="$(git branch --show-current)"
[ -n "$branch" ] || { echo "$ts skip: detached HEAD"; exit 0; }

git add -A
if ! git diff --cached --quiet; then
  if git diff --cached -U0 | grep -qE 'pt-sk-[A-Za-z0-9]{8,}|AIza[0-9A-Za-z_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY'; then
    git reset -q; echo "$ts ABORT: possible secret in changes, nothing committed"; exit 1
  fi
  big="$(git diff --cached --name-only --diff-filter=AM -z | xargs -0 -r find 2>/dev/null -maxdepth 0 -type f -size +50M)"
  if [ -n "$big" ]; then
    git reset -q; echo "$ts ABORT: files over 50 MB: $big"; exit 1
  fi
  git commit -q -m "auto-sync: $ts"
fi

git fetch -q origin
if git rev-parse --verify -q "origin/$branch" >/dev/null; then
  if ! git rebase -q "origin/$branch"; then
    git rebase --abort; echo "$ts ABORT: conflict with origin/$branch, resolve manually"; exit 1
  fi
fi

if [ -n "$(git log --oneline "origin/$branch..HEAD" 2>/dev/null)" ] || ! git rev-parse --verify -q "origin/$branch" >/dev/null; then
  git push -q -u origin "$branch" && echo "$ts pushed $branch" || echo "$ts push failed"
fi
