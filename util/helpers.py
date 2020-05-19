from socket import socket
from hashlib import sha256

SIZE_NUM_BYTES = 4


def send_bytes(sock: socket, payload: bytes):
    size_bytes = len(payload).to_bytes(SIZE_NUM_BYTES, byteorder='big')
    # print("send size bytes", len(payload))
    payload = size_bytes + payload
    sock.sendall(payload)


def recv_bytes(sock: socket):
    size_bytes = recvall(sock, SIZE_NUM_BYTES)
    size = int.from_bytes(size_bytes, 'big')
    # print("received size bytes", size)
    return recvall(sock, size)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        buf_size = min(n - len(data), 4096)
        packet = sock.recv(buf_size)
        if not packet:
            return None
        data.extend(packet)
    return data


def hash_transaction(tx):
    return sha256(str(tx.to_dict()).encode('utf-8')).hexdigest()
