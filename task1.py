import dateparser
import spur


shell = spur.SshShell(hostname=REMOTE_HOST,
                      username="<server_ip>",
                      password="<server_password>")

log1 = shell.run(["cat", "log_files/log1"])
log1_data = log1.output.decode("utf-8")
log1_records = log1_data.split("\n")
timings = []
connection_list = []
disconnection_list = []
spurious_list = []


def get_disconnection_record(host_name):
    """
    Get first disconnection record of host_name
    Extract Date and Time of disconnection
    """
    for disconnection in disconnection_list:
        disconnection_data = disconnection.values()
        if host_name in list(disconnection_data)[0]:
            # This is the disconnection for the respective host
            disconnection_timing = disconnection.keys()
            disconnection_timing = dateparser.parse(
                list(disconnection_timing)[0])
            disconnection_time = str(disconnection_timing).split(" ")[1]
            disconnection_date = \
                str(disconnection_timing).split(" ")[0].split("-")
            disconnection_date = \
                f'{disconnection_date[2]}/{disconnection_date[1]}/{disconnection_date[0]}'

            # Now remove this host entry from disconnection list
            disconnection_list.remove(disconnection)
            return disconnection_date, disconnection_time


for record in log1_records:
    timing = record.split(" - ")[0]
    word_tokens = record.split(" - ")[1].split(" ")

    if 'connected' in word_tokens:
        connection_list.append({
            timing: record.split(" - ")[1]
        })
        continue

    if 'disconnected' in word_tokens:
        disconnection_list.append({
            timing: record.split(" - ")[1]
        })
        continue

    spurious_list.append({
        timing: record.split(" - ")[1]
    })


for connection in connection_list:
    connection_timing = connection.keys()
    connection_timing = dateparser.parse(list(connection_timing)[0])
    connection_time = str(connection_timing).split(" ")[1]
    connection_date = \
        str(connection_timing).split(" ")[0].split("-")
    connection_date = \
        f'{connection_date[2]}/{connection_date[1]}/{connection_date[0]}'

    connection_data = connection.values()
    host_name = list(connection_data)[0].split(" ")[-2]
    # Now look for disconnection of this server
    disconnection_date, disconnection_time = \
        get_disconnection_record(host_name)

    print(f'{host_name} - connected at {connection_date} '\
         f'{connection_time} and disconnected at {disconnection_date} '\
         f'{disconnection_time}\n')

spurious_host_list = []

for spurious in spurious_list:
    spurious_data = list(spurious.values())[0]
    spurious_host = spurious_data.split(" ")[-1]
    spurious_host_list.append(spurious_host)

spurious_hosts = ', '.join(spurious_host_list)
print(f'Spurious activities from: {spurious_hosts}\n')