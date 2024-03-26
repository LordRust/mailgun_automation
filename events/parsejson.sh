#!/bin/bash

jq -r '.items[] | [.address, .code, .error, .created_at, .MessageHash] | @tsv' "$1"
