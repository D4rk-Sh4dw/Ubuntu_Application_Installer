#!/bin/bash
echo "=== Interactive Alias Generator ==="
read -p "Enter the alias name (e.g., 'update'): " alias_name
read -p "Enter the command to execute (e.g., 'sudo apt update'): " alias_command

if [ -z "$alias_name" ] || [ -z "$alias_command" ]; then
    echo "Error: Alias name or command cannot be empty."
    exit 1
fi

ALIAS_STRING="alias ${alias_name}='${alias_command}'"

# Append to bashrc
echo "$ALIAS_STRING" >> ~/.bashrc
echo "Success! The alias has been added to your ~/.bashrc file."
echo "Note: You might need to restart your terminal or run 'source ~/.bashrc' to use it."
