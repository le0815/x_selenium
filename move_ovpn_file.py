import subprocess
import os
import shutil

path = "vpn_acc/"
path_vpn_old = "serverListTCP/"


def MoveFile():
    # get emails
    with open("mailTemp.txt", "r") as file:
        emails = file.readlines()

    list_vpn = os.listdir(path_vpn_old)
    for vpn in list_vpn:
        # create directory
        folder_name = vpn[0:len(vpn) - 5]
        temp_path = os.path.join(path, folder_name)
        os.makedirs(temp_path)

        # move .ovpn file to new folder
        old_ovpn_path = f"{path_vpn_old}/{vpn}"
        new_ovpn_path = f"{temp_path}/{vpn}"
        shutil.move(old_ovpn_path, new_ovpn_path)

        # move email addr to new folder
        with open(f"{temp_path}/email.txt", 'a') as file:
            for _ in range(len(emails)):
                if _ == 4:
                    break
                file.write(emails.pop())

    # rewrite mailTemp.txt
    with open("mailTemp.txt", "w") as file:
        for email in emails:
            file.write(email)


def EditovpnFile():
    ovpn_path = 'serverListTCP/'
    # load all vpn folder
    list_ovpn_files = os.listdir(ovpn_path)

    for ovpn_file in list_ovpn_files:

        vpn_path = f"{ovpn_path}{ovpn_file}"

        # read all data from old ovpn file
        with open(vpn_path, "r") as file:
            old_data_vpn = file.readlines()

        # get ip addr from data
        ip_addr = []
        idx = 4
        while idx < old_data_vpn.index("remote-random\n"):
            ip_addr.append(old_data_vpn[idx])
            old_data_vpn.remove(old_data_vpn[idx])

        # rewrite data in ovpn file:
        with open(vpn_path, 'w') as file:
            file.writelines(old_data_vpn)

        # create new ovpn file from ip_addr
        idx = 1
        for ip in ip_addr:
            # replace old ip_addr in old data
            old_data_vpn[3] = ip

            # create new ovpn file
            ovpn_file_name = f"{idx}_{ovpn_file}"
            with open(f"{ovpn_path}{ovpn_file_name}", "w") as file:
                file.writelines(old_data_vpn)

            idx += 1


def Temp():
    # load all vpn folder
    path = 'serverListTCP/'
    list_vpn_folder = os.listdir(path)
    for vpn_folder in list_vpn_folder:

        if '_' in vpn_folder:
            continue

        vpn_path = f"{path}{vpn_folder}/.ovpn"

        # read all data from old ovpn file
        with open(vpn_path, "r") as file:
            old_data_vpn = file.readlines()
        # get ip addr from data
        ip_addr = []
        idx = 4
        while idx < old_data_vpn.index("remote-random\n"):
            ip_addr.append(old_data_vpn[idx])
            old_data_vpn.remove(old_data_vpn[idx])
        # rewrite data in ovpn file:
        with open(vpn_path, 'w') as file:
            file.writelines(old_data_vpn)


if __name__ == "__main__":
    MoveFile()