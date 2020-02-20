import subprocess

output = subprocess.check_output(["ls","-lha"],universal_newlines=True)

print(output)