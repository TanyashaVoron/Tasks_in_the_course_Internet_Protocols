import json
import re
import subprocess
import sys
from urllib import request
from prettytable import PrettyTable

ip_regex = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
not_resolve_node = 'traceroute: unknown host'
tracing_route = 'traceroute to'
time_limit = '* * *'


def get_console_tracer(hostname):
    return subprocess.Popen(['traceroute', hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readline


def get_ip_info(ip):
    return json.loads(request.urlopen(f'http://ipinfo.io/{ip}/json').read())


def get_list_ip(address):
    list_ip = []
    ip = ""
    count_time_out = 0

    for line in iter(get_console_tracer(address), ""):

        line = line.decode(encoding='cp866')[4:]

        if not_resolve_node in line:
            print(not_resolve_node)
            return

        elif tracing_route in line:
            print(line)
            ip = ip_regex.findall(line)[0]

        elif time_limit in line:
            if count_time_out == 2:
                break
            count_time_out += 1
            continue

        list_ips = ip_regex.findall(line)

        if not list_ips:
            return list_ip

        ip_ = list_ips[0]

        if ip_ == ip:
            break

        list_ip.append(ip_)
        print(line, 'ip = [', ip_, ']')
        count_time_out = 0

    return list_ip


def get_table(list_ip):
    table = PrettyTable(['№', 'ip', 'as', 'country', 'provider'])

    for ip_num in range(len(list_ip)):
        info_ip = get_ip_info(list_ip[ip_num])
        print(info_ip)

        org = info_ip.get('org') or '*'

        table.add_row([
            ip_num + 1,
            info_ip.get('ip') or '*',
            org.split()[0] or '*',
            ' '.join(org.split()[1:]) or '*',
            info_ip.get('country') or '*'
        ])

    return table


def main():
    #print(get_table(get_list_ip(input(sys.argv[1]))))
    print(get_table(get_list_ip(input('вводите доменное имя или IP адрес: '))))


if __name__ == '__main__':
    main()
