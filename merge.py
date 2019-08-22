from scapy.utils import PcapReader, PcapWriter, PcapNgReader


def mergecap(onlyfiles, merge_file_out):
    writer = BufferedPcapWriter(merge_file_out)
    readers = {}
    reader_id = 0
    onlynames = []
    for file in onlyfiles:
        readers[reader_id] = CustomReader(file, reader_id)
        reader_id = reader_id + 1
        onlynames.append(file.split("/")[-1])

    has_data = True
    current_packets = []

    while has_data:
        has_data = False
        for r_id, reader in readers.items():
            pkt = reader.current()
            if pkt is None:
                continue
            has_data = True
            current_packets.append(pkt)
        if len(current_packets) > 0:
            min_pkt = min(current_packets, key=lambda x: x[1].time)
            writer.write(min_pkt[1])
            readers[min_pkt[0]].read_next()
            del current_packets[:]

    writer.flush()
    print('{} merged into {}'.format(onlynames, merge_file_out))


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


class CustomReader:
    def __init__(self, filename, reader_id):
        if filename.endswith(".pcap"):
            self.reader = PcapReader(filename)
        if filename.endswith(".pcapng"):
            self.reader = PcapNgReader(filename)
        self.reader_id = reader_id
        self.current_packet = self.reader.read_packet()

    def current(self):
        if self.current_packet is None:
            return None
        return self.reader_id, self.current_packet

    def read_next(self):
        self.current_packet = self.reader.read_packet()