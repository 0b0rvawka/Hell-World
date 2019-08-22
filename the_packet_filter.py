# -*- coding: utf-8 -*-

from datetime import datetime
from scapy.utils import PcapReader, PcapWriter
from scapy.layers.l2 import Dot1Q
from scapy.layers.inet import IP, TCP, UDP, IPerror, TCPerror, UDPerror
from scapy.layers.inet6 import IPv6

def pickle_pcap(onlyfiles, pcap_file_out, per_quest, per_beg, per_end, prot_quest, net_prot, netprot_mass, trans_prot,
                transprot_mass, appl_prot, ip_quest, addr_mass, callback=None):

    writer = BufferedPcapWriter(pcap_file_out, buffer_size=1000)

    count = 0  # сколько ваще пакетов во всех файлах
    interesting_packet_count = 0  # сколько из них пакетов, подпадающих под наши фильтры

    for file in onlyfiles:
        count_file = 0  # кол-во пакетов в этом файле
        interesting_packet_count_file = 0  # кол-во из них пакетов, подпадающих под наши фильтры

        for pkt_data in PcapReader(file):  # цикл по пакетам
            count += 1  # общее кол-во пакетов увеличиваем
            count_file += 1  # кол-во пакетов файла увеличиваем
            vlan_indicator = 0
            net_pkt = None
            good_ip = 0

            print(count)

            if count == 46:
                pass


            if per_quest == 1:  # фильтр по Period
                if (datetime.fromtimestamp(pkt_data.time)) < per_beg or (
                datetime.fromtimestamp(pkt_data.time)) >= per_end:
                    continue

            if prot_quest == 1 or ip_quest == 1:
                if 'type' not in pkt_data.fields:  # например, LLC frame имеет не тип, а len - отбрасываем такие
                    continue

                ether_pkt = pkt_data  # переходим на уровень ether
                while ether_pkt.type == 0x8100:  # если есть один VLAN, то + уровень
                    vlan_indicator = 1
                    ether_pkt = ether_pkt.getlayer(Dot1Q)

                if net_prot == 1:
                    if vlan_indicator == 1:
                        if ether_pkt.type not in netprot_mass and 33024 not in netprot_mass:
                            continue
                    else:
                        if ether_pkt.type not in netprot_mass:
                            continue

                if trans_prot == 1 or appl_prot == 1 or ip_quest == 1:
                    if ether_pkt.type == 0x0800:  # для IPv4
                        ip_pkt = ether_pkt.getlayer(IP)  # переходим на уровень IP
                        if trans_prot == 1:
                            if ip_pkt.proto == 1 and ip_pkt.proto not in transprot_mass:
                                icmp_pkt = ip_pkt.getlayer(IPerror)
                                if icmp_pkt is None or icmp_pkt.proto not in transprot_mass:
                                    continue
                            else:
                                if ip_pkt.proto not in transprot_mass:
                                    continue

                        if ip_quest == 1 or appl_prot == 1:  # фильтр по IP
                            if ip_pkt.proto == 17:  # рассматриваем слой UDP
                                net_pkt = ip_pkt.getlayer(UDP)
                                which_prot_is_it = 'udp'
                            elif ip_pkt.proto == 6:  # рассматриваем слой TCP
                                net_pkt = ip_pkt.getlayer(TCP)
                                which_prot_is_it = 'tcp'
                            elif ip_pkt.proto == 1:  # рассматриваем слой ICMP
                                icmp_pkt = ip_pkt.getlayer(IPerror)
                                if icmp_pkt is not None:
                                    if icmp_pkt.proto == 6:
                                        net_pkt = icmp_pkt.getlayer(TCPerror)
                                        which_prot_is_it = 'tcp'
                                    elif icmp_pkt.proto == 17:
                                        net_pkt = icmp_pkt.getlayer(UDPerror)
                                        which_prot_is_it = 'udp'
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                continue

                            #if which_prot_is_it == 'tcp':
                            #    ip_total_len = ip_pkt.len
                            #    ip_header_len = ip_pkt.ihl * 32 / 8
                            #    if net_pkt.dataofs is not None:
                            #        tcp_header_len = net_pkt.dataofs * 32 / 8
                            #    else:
                            #        continue
                            #    seg_len = ip_total_len - ip_header_len - tcp_header_len
                            #else:
                            #    if net_pkt is not None:
                            #        seg_len = net_pkt.len # сюда фрагментированные куски не попадают - надо с этими сучками разобраться
                            #    else:
                            #        continue

                            #if appl_prot == 1:
                            #    if ip_pkt.proto not in (17, 6):
                            #        continue
                            #    if net_pkt is None or seg_len == 0.0 or (
                            #            net_pkt.sport not in listofapplpr and net_pkt.dport not in listofapplpr):
                            #        continue

                    elif ether_pkt.type == 0x86DD:  # для IPv6
                        ip_pkt = ether_pkt.getlayer(IPv6)  # переходим на уровень IP
                        if trans_prot == 1:
                            if ip_pkt.nh == 58 and ip_pkt.nh not in transprot_mass:
                                icmp_pkt = ip_pkt.getlayer(IPerror)
                                if icmp_pkt is None or icmp_pkt.nh not in transprot_mass:
                                    continue
                            else:
                                if ip_pkt.nh not in transprot_mass:
                                    continue

                        if ip_quest == 1 or appl_prot == 1:  # фильтр по IP
                            if ip_pkt.nh == 17:  # рассматриваем слой UDP
                                net_pkt = ip_pkt.getlayer(UDP)
                                which_prot_is_it = 'udp'
                            elif ip_pkt.nh == 6:  # рассматриваем слой TCP
                                net_pkt = ip_pkt.getlayer(TCP)
                                which_prot_is_it = 'tcp'
                            elif ip_pkt.nh == 58:  # рассматриваем слой ICMPv6
                                icmp_pkt = ip_pkt.getlayer(IPerror)
                                if icmp_pkt is not None:
                                    if icmp_pkt.nh == 6:
                                        net_pkt = icmp_pkt.getlayer(TCPerror)
                                        which_prot_is_it = 'tcp'
                                    elif icmp_pkt.nh == 17:
                                        net_pkt = icmp_pkt.getlayer(UDPerror)
                                        which_prot_is_it = 'udp'
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                continue

                            #if which_prot_is_it == 'tcp':
                            #    ip_total_len = ip_pkt.len
                            #    ip_header_len = ip_pkt.ihl * 32 / 8
                            #    tcp_header_len = net_pkt.dataofs * 32 / 8
                            #    seg_len = ip_total_len - ip_header_len - tcp_header_len
                            #else:
                            #    seg_len = net_pkt.len

                            #if appl_prot == 1:
                            #    if ip_pkt.nh not in (17, 6):
                            #        continue
                            #    if net_pkt is None or seg_len == 0 or (
                            #            net_pkt.sport not in listofapplpr and net_pkt.dport not in listofapplpr):
                            #        continue
                    else:
                        continue

                    if ip_quest == 1:  # уточняли принадлежность IP
                        for addr in addr_mass:
                            #if addr.startswith("::"):
                            #    continue # если пустые строки попадаются
                            if addr.endswith("A"):
                                spec_ip = 0
                                any_ip, any_port, info = addr.split(":")
                            elif addr.endswith("S"):
                                spec_ip = 1
                                server_ip = ''
                                server_port = ''
                                client_ip, client_port, info = addr.split(":")
                            elif addr.endswith("D"):
                                spec_ip = 1
                                client_ip = ''
                                client_port = ''
                                server_ip, server_port, info = addr.split(":")

                        # тут обратная логика: если встретился удовлетворяющий адрес, то выход из цикла перебора адресов

                            if spec_ip == 1:  # уточняли принадлежность IP
                                if client_ip != '' and client_port != '':
                                    if net_pkt is None:
                                        continue
                                    if ip_pkt.src + str(net_pkt.sport) == client_ip + client_port:
                                        good_ip = 1
                                        continue
                                if client_ip != '' and client_port == '':
                                    if ip_pkt.src == client_ip:
                                        good_ip = 1
                                        continue
                                if client_ip == '' and client_port != '':
                                    if str(net_pkt.sport) == client_port:
                                        good_ip = 1
                                        continue

                                if server_ip != '' and server_port != '':
                                    if net_pkt is None:
                                        continue
                                    if ip_pkt.dst + str(net_pkt.dport) == server_ip + server_port:
                                        good_ip = 1
                                        continue
                                if server_ip != '' and server_port == '':
                                    if ip_pkt.dst == server_ip:
                                        good_ip = 1
                                        continue
                                if server_ip == '' and server_port != '':
                                    if str(net_pkt.dport) == server_port:
                                        good_ip = 1
                                        continue

                            elif spec_ip == 0:
                                if any_ip != '' and any_port != '':
                                    if (ip_pkt.src+ str(net_pkt.sport) == any_ip + any_port) or \
                                            (ip_pkt.dst + str(net_pkt.dport) == any_ip + any_port):
                                        good_ip = 1
                                        continue
                                if any_ip != '' and any_port == '':
                                    if (ip_pkt.src == any_ip) or (ip_pkt.dst == any_ip):
                                        good_ip = 1
                                        continue
                                if any_ip == '' and any_port != '':
                                    if (str(net_pkt.sport) == any_port) or (str(net_pkt.dport) == any_port):
                                        good_ip = 1
                                        continue

                        if good_ip == 0:
                            continue

            interesting_packet_count += 1  # в случае прохождения до конца увеличиваем счётчик пакетов всех файлов, удовлетворяющих фильтры
            interesting_packet_count_file += 1  # в случае прохождения до конца увеличиваем счётчик пакетов этого файла, удовлетворяющих фильтры
            writer.write(pkt_data)

        bullshit, fname = file.rsplit('/', 1)

        if callback is not None:
            callback('В "{}" {} пакетов с {} релевантными ({}%)'.format(fname, count_file, interesting_packet_count_file,
        round(interesting_packet_count_file / count_file * 100, 2)))# вывод информации по анализу файла

    writer.flush()
    # end = time.time()
    if callback is not None:
        callback('Всего {} пакетов с {} релевантными ({}%) сохранено в {}'.format(count, interesting_packet_count, round(
    interesting_packet_count / count * 100, 2), pcap_file_out))# вывод информации по анализу всех файлов


class BufferedPcapWriter:
    def __init__(self, filename, buffer_size=10000):
        self.buffer = []
        self.writer = PcapWriter(filename)
        self.threshold = buffer_size

    def write(self, pkt):
        self.buffer.append(pkt)
        if len(self.buffer) >= self.threshold:
            self.writer.write(self.buffer)
            del self.buffer[:]

    def flush(self):
        if len(self.buffer) > 0:
            self.writer.write(self.buffer)
            del self.buffer[:]