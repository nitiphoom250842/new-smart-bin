#!/usr/bin/env bash

set -e
TASK=$1
ARGS=${@:2}

help__fixLint="fix lint dart format"
task_fixLint() {
  black . -v
}

help__push="git add . & git commit & git push"
task_push(){
  git add .
  git commit -m $1
  git push
}

help__pull="reset & pull"
task_pull(){
  git reset --hard
  git pull
}

help__run="run for test prod"
task_run(){
  uvicorn main:app --host 0.0.0.0 --port 8080 --env-file .env.prod --reload
}


## main
list_all_helps() {
  compgen -v | egrep "^help__.*"
}

NEW_LINE=$'\n'
if type -t "task_$TASK" &>/dev/null; then
  task_${TASK} ${ARGS}
else
  echo "usage: $0 <task> [<..args>]"
  echo "task:"

  HELPS=""
  for help in $(list_all_helps)
  do

    HELPS="$HELPS    ${help/help__/} |-- ${!help}$NEW_LINE"
  done

  echo "$HELPS" | column -t -s "|"
  exit 1
fi