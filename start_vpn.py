import subprocess

command = "sudo -S /usr/sbin/openvpn --config /home/ha/PycharmProjects/x_selenium/vpn_acc/NCVPN-AE-Dubai-TCP/NCVPN-AE-Dubai-TCP.ovpn --auth-user-pass ~/Desktop/html_example/auth_ovpn.txt"


def vpn(queue):
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print(proc.returncode)

    proc.stdin.write(b"2904\n")
    proc.stdin.close()

    while proc.returncode is None:
        if b'Timers: ping 20, ping-restart 40' in proc.stdout.readline():
            print("connected")
            queue.put("connected")
        else:
            print("connecting to vpn")

        proc.poll()
