#!/usr/bin/env bash
set -euo pipefail

: "${DEPLOY_HOST:?Set DEPLOY_HOST}"
: "${DEPLOY_USER:?Set DEPLOY_USER}"
: "${DEPLOY_PATH:?Set DEPLOY_PATH}"
: "${PUBLIC_URL:?Set PUBLIC_URL}"

branch="${CI_COMMIT_REF_NAME:-main}"
target="$DEPLOY_PATH"
if [[ "$branch" != "main" ]]; then
  safe_branch="${branch//[^a-zA-Z0-9._-]/-}"
  target="$DEPLOY_PATH/previews/$safe_branch"
fi

ssh "$DEPLOY_USER@$DEPLOY_HOST" "mkdir -p '$target' '${target}.previous' && rsync -a --delete '$target/' '${target}.previous/'"
rsync -az --delete site/ "$DEPLOY_USER@$DEPLOY_HOST:$target/"
curl --fail --silent --show-error "$PUBLIC_URL" | grep -q 'PYWEB-SSG-OK'

