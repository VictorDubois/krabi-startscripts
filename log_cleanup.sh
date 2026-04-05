#!/bin/bash

# Set your folder path
LOG_DIR="/var/log/krabi"

# Max allowed size in kilobytes (10 GB = 10 * 1024 * 1024 = 10971520 KB)
MAX_SIZE=10971520

# Get folder size in KB
DIR_SIZE=$(du -sk "$LOG_DIR" | cut -f1)

echo "Check log folder size"
# Check if size exceeds limit
if [ "$DIR_SIZE" -gt "$MAX_SIZE" ]; then
    echo "Cleaning logs: current size = $DIR_SIZE KB"

    # Find and sort files by modification time (oldest first), then delete until size is OK
    find "$LOG_DIR" -type f -printf '%T@ %p\n' | sort -n | while read -r line; do
        FILE=$(echo "$line" | cut -d' ' -f2-)
        FILE_SIZE=$(du -k "$FILE" | cut -f1)

        echo "deleting $FILE"
        rm -r "$FILE"
        DIR_SIZE=$((DIR_SIZE - FILE_SIZE))

        # Stop deleting if under the limit
        if [ "$DIR_SIZE" -le "$MAX_SIZE" ]; then
            break
        fi
    done
fi
