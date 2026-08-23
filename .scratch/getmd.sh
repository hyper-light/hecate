#!/bin/zsh
# usage: getmd.sh <outdir> <slug1> <slug2> ...
OUT="$1"; shift
mkdir -p "$OUT"
for s in "$@"; do
  fn=$(echo "$s" | tr '/' '_')
  curl -sL --max-time 60 -A "Mozilla/5.0" "https://docs.temporal.io/${s}.md" -o "${OUT}/${fn}.md"
  echo "== ${s} -> ${OUT}/${fn}.md ($(wc -c < ${OUT}/${fn}.md) bytes)"
done
