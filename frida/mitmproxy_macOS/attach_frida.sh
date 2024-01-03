#!/bin/bash
PROCESSES=()

for process_name in "$@"; do
    BATCH=()
    
    # Get all PIDs of a process with the given name.
    while read -r pid; do
        BATCH+=("$pid")
    done < <(pgrep "^${process_name}$")
    
    # If nothing was added to the batch, then a PID was probably passed, so just add it directly.
    if [ ${#BATCH[@]} -eq 0 ]; then
        PROCESSES+=("$process_name")
    else
        PROCESSES=("${PROCESSES[@]}" "${BATCH[@]}")  # Add the current batch to the list of PIDs.
    fi
done

for process in "${PROCESSES[@]}"; do
    # This might not be ideal, since it can flood a given console and hide any errors.
    # Perhaps some piping fanciness could help?
    sudo frida -l disable-ssl-pinning.js $process & disown
done