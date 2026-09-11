#!/usr/bin/env bash
set -euo pipefail
: "${DEPLOY_HOST:?Set DEPLOY_HOST}"
: "${DEPLOY_USER:?Set DEPLOY_USER}"
: "${DEPLOY_PATH:?Set DEPLOY_PATH}"
ssh "$DEPLOY_USER@$DEPLOY_HOST" "rsync -a --delete '${DEPLOY_PATH}.previous/' '$DEPLOY_PATH/'"

