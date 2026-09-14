#!/usr/bin/env bash
# Auto-commit and push the repo. Run by the forgeai-autosync systemd user timer.
# Never force-pushes. Aborts (without committing) on likely secrets or files over 50 MB.
set -uo pipefail

REPO="/home/aliz/Documents/Codes/forgeAI-hackathon"
cd "$REPO" || exit 1
exec >>"$REPO/.autosync.log" 2>&1
ts="$(date '+%F %T')"

if [ -f "$REPO/.conflict_handover.txt" ]; then
  echo "$ts skip: active conflict handover pending (.conflict_handover.txt exists). Please resolve and remove the file."; exit 1
fi

if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || [ -f .git/MERGE_HEAD ]; then
  echo "$ts skip: rebase/merge already in progress"; exit 0
fi

branch="$(git branch --show-current)"
[ -n "$branch" ] || { echo "$ts skip: detached HEAD"; exit 0; }

# 1. Check for uncommitted changes and commit safely
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

# 2. Fetch remote branch
if ! git fetch -q origin "$branch"; then
  echo "$ts ABORT: git fetch failed (network or remote issue), nothing changed"; exit 1
fi

# 3. Check for divergence and conflict detection
if git rev-parse --verify -q "origin/$branch" >/dev/null; then
  local_head="$(git rev-parse HEAD)"
  remote_head="$(git rev-parse "origin/$branch")"
  merge_base="$(git merge-base HEAD "origin/$branch" || true)"

  if [ "$local_head" != "$remote_head" ] && [ "$merge_base" != "$remote_head" ]; then
    # Remote has commits we do not have. Test merge in-memory before touching working tree.
    merge_tree_output="$(git merge-tree --write-tree HEAD "origin/$branch" 2>&1 || true)"
    if echo "$merge_tree_output" | grep -qi "conflict"; then
      # CONFLICT DETECTED! Working tree is completely untouched.
      cat <<EOF > "$REPO/.conflict_handover.txt"
================================================================================
                    MERGE CONFLICT ALERT — HANDOVER REQUIRED
================================================================================
Timestamp: $ts
Branch: $branch
Local HEAD:  $local_head ($(git log -1 --oneline HEAD))
Remote HEAD: $remote_head ($(git log -1 --oneline "origin/$branch"))

In-memory merge-tree detected merge conflicts with origin/$branch.
THE WORKING DIRECTORY HAS NOT BEEN TOUCHED. NO FILES WERE CORRUPTED.
Auto-sync has been safely suspended until this is resolved.

Conflict details:
$merge_tree_output

Resolution instructions:
1. Review the conflicting files listed above.
2. Run in terminal:
     git pull --rebase origin $branch
   OR
     git merge origin/$branch
3. Open conflicting files, resolve the conflict markers, and save.
4. Stage and commit:
     git add <resolved-files>
     git commit -m "fix(sync): resolve merge conflicts with origin/$branch"
5. Push to remote:
     git push origin $branch
6. Remove this handover file to resume autosync:
     rm "$REPO/.conflict_handover.txt"
================================================================================
EOF
      echo "$ts ABORT: merge conflict detected with origin/$branch. Script interrupted. Handover written to .conflict_handover.txt"
      exit 1
    fi

    # Clean merge is verified in advance; now perform rebase
    if ! git rebase -q "origin/$branch"; then
      git rebase --abort
      echo "$ts ABORT: rebase failed unexpectedly, cleanly aborted"; exit 1
    fi
  fi
fi

# 4. Push cleanly if ahead
if [ -n "$(git log --oneline "origin/$branch..HEAD" 2>/dev/null)" ] || ! git rev-parse --verify -q "origin/$branch" >/dev/null; then
  if git push -q -u origin "$branch"; then
    echo "$ts pushed $branch"
  else
    echo "$ts push failed"
    exit 1
  fi
fi

