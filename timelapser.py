import subprocess

output = subprocess.check_output(["ls"],universal_newlines=True)

print(output)