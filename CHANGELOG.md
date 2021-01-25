# Changelog

## 0.0.12
 - added CHANGELOG.md
 - added `hellolan me` which returns the current local IP address (matches closest to `192.168.1.`)
 - will return all or a subset of ips if positional arguments or an `--all` flag is passed
 - `hellolan hostname` will now return the current machine's hostname in the absence of a specified IP address
 - added `ifcfg` as a dependency (for determining my lan IP)
 - make assumption that time between scan results is instantaneous compared to rendering (fixes render glitch)

## 0.0.11
 - add natural sorting to cli table
 - removed `force` flag (`nmap -R`) because I saw no improvement over hostname resolution

## 0.0.10
 - added mac and vendor to the table if they are available (if it was run with sudo)

## 0.0.9
 - fixed decorator bug in cli (don't use 0.0.8 directly)

## 0.0.8
 - refactor CLI so that any of the data views are "watch"-able (`--watch`)

## 0.0.7
 - add `--watch` flag to cli table. will perform multiple back to back scans and update the table
 - added `reprint` as a dependency for stdout refreshes
 - moved ssh code into separate file
 - added `hellolan hostname <ip>` command

## 0.0.6
 - add `hellossh` command (shortcut for `hellolan ssh- ...`)

## 0.0.5
 - update dependencies
