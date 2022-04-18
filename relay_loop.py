#################################################################################
from subprocess import call

relay_start = 'python3 -m ch340_relay_sw'
file_refresh = 'seed_refresh.cmd'

i = 0
while i < 1:
    print(i)
    call(relay_start)
    call(file_refresh)