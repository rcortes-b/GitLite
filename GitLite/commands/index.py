import os, hashlib, struct, sys

def create_index_entry(path):
    stat_result = os.stat(path)

    with open(path, "rb") as f:
        content = f.read()

    sha1 = hashlib.sha1(content).digest()

    ctime_s = int(stat_result.st_ctime)
    ctime_n = int((stat_result.st_ctime - ctime_s) * 1e9)
    mtime_s = int(stat_result.st_mtime)
    mtime_n = int((stat_result.st_mtime - mtime_s) * 1e9)

    dev = stat_result.st_dev
    ino = stat_result.st_ino
    mode = stat_result.st_mode
    uid = stat_result.st_uid
    gid = stat_result.st_gid
    size = stat_result.st_size

    path_bytes = path.encode()
    flags = len(path_bytes) & 0xFFF

    entry_head = struct.pack(
        "!LLLLLLLLLL20sH",
        ctime_s, ctime_n,
        mtime_s, mtime_n,
        dev, ino,
        mode, uid, gid, size,
        sha1, flags
    )

    # Path, null byte, then pad to multiple of 8
    entry_path = path_bytes + b'\x00'
    total_length = len(entry_head) + len(entry_path)
    padding = (8 - (total_length % 8)) % 8
    entry = entry_head + entry_path + (b'\x00' * padding)
    
    return entry

def write_index(paths, index_path, index_entries=None):
    entries = []

    if index_entries is not None:
        for p in sorted(paths):
            found = False
            for entry in index_entries:
                if entry['path'] == p:
                    found = True
                    break
            if found is False:
                entries.append(create_index_entry(p))
            else:
                entries.append(entry['raw'])
        print('index entries', index_entries)
    else:
        entries = [create_index_entry(p) for p in sorted(paths)]

    print('entries', len(entries))
    print('\nend of entries\n')

    header = struct.pack("!4sLL", b"DIRC", 2, len(entries))
    body = b"".join(entries)
    data = header + body


    checksum = hashlib.sha1(data).digest()
    with open(index_path, 'wb') as f:
        f.write(data + checksum)

def read_index(path):
    with open(path, 'rb') as f:
        data = f.read()

    entries = []
    pos = 0

    # Read header
    signature, version, count = struct.unpack('!4sLL', data[:12])
    pos = 12

    if signature != b'DIRC':
        raise Exception("Not a valid index file")

    for _ in range(count):
        entry_start = pos

        # Read fixed-size header (62 bytes)
        fields = struct.unpack("!LLLLLLLLLL20sH", data[pos:pos+62])
        (
            ctime_s, ctime_n,
            mtime_s, mtime_n,
            dev, ino,
            mode, uid, gid, size,
            sha1, flags
        ) = fields
        pos += 62

        # Get filename
        path_end = data.index(b'\x00', pos)
        path = data[pos:path_end].decode()
        pos = path_end + 1

        # Align to 8-byte boundary
        entry_len = pos - entry_start
        padding = (8 - (entry_len % 8)) % 8
        pos += padding

        entries.append({
            'path' : path,
            'raw': data[entry_start:pos],
            'fields':{
                'ctime_s' : ctime_s,
                'ctime_n' : ctime_n,
                'mtime_s' : mtime_s,
                'mtime_n' : mtime_n,
                'dev' : dev,
                'ino' : ino,
                'mode' : mode,
        		'uid' : uid, 
                'gid' : gid,
                'size' : size,
                'sha1' : sha1.hex(),
                'flags' : flags
			}
        })

    return entries
