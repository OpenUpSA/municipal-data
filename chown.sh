#!/bin/bash
shopt -s extglob
chown -R django:django /app/!(.git)
shopt -u extglob
