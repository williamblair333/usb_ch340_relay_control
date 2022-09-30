<<<<<<< HEAD
#################################################################################
from subprocess import call

relay_start = 'python3 -m ch340_relay_sw'
file_refresh = 'seed_refresh.cmd'

i = 0
while i < 1:
    print(i)
    call(relay_start)
=======
#################################################################################
from subprocess import call

relay_start = 'python3 -m ch340_relay_sw'
file_refresh = 'seed_refresh.cmd'

i = 0
while i < 1:
    print(i)
    call(relay_start)
>>>>>>> 3f7e0f571f7fc6a16ba04f6fc0c85bce74bec9e0
    call(file_refresh)