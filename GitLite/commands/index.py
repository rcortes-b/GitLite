import os, hashlib, struct

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

def write_index(paths, index_path, mode):
    entries = [create_index_entry(p) for p in sorted(paths)]

    header = struct.pack("!4sLL", b"DIRC", 2, len(entries))
    body = b"".join(entries)
    data = header + body

    checksum = hashlib.sha1(data).digest()
    with open(index_path, mode) as f:
        f.write(data + checksum)

def read_index(index_path):
    entries = []

    with open(index_path, "rb") as f:
        data = f.read()

    # 1. Header
    header = data[:12]
    signature, version, num_entries = struct.unpack("!4sLL", header)
    assert signature == b"DIRC", "Invalid index file"
    assert version == 2, f"Unsupported index version: {version}"

    offset = 12
    for _ in range(num_entries):
        # 2. Read fixed-size entry header (62 bytes)
        entry_head = data[offset:offset+62]
        fields = struct.unpack("!LLLLLLLLLL20sH", entry_head)
        (
            ctime_s, ctime_n,
            mtime_s, mtime_n,
            dev, ino,
            mode, uid, gid, size,
            sha1, flags
        ) = fields

        offset += 62

        # 3. Read path (null-terminated), then align to 8-byte boundary
        path_end = data.index(b'\x00', offset)
        path_bytes = data[offset:path_end]
        path = path_bytes.decode()

        entry_length = (62 + len(path_bytes) + 1)
        padding = (8 - (entry_length % 8)) % 8
        offset = path_end + 1 + padding

        entries.append({
            "path": path,
            "sha1": sha1.hex(),
            "mode": mode,
            "size": size,
        })

    return entries