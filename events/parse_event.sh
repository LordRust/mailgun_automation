#!/bin/bash

jq -r '.[] | [.recipient, ."delivery-status"."description", ."delivery-status"."message", .event, .timestamp, .severity] | @tsv' "$1"
