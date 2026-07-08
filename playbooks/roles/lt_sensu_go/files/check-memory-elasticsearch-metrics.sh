#!/bin/bash
timestamp=$(date +"%s")
hostname=$(hostname)
es_memory_usage=$(jstat -gc $(ps -u elasticsearch -o pid | sed -n '2p') | sed -n '2p' | awk '{row_sum=$3+$4+$6+$8} END {printf "%.0f", row_sum*1024}')

echo "$hostname.memory.elasticsearchv2 $es_memory_usage $timestamp"