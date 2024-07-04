import cv2
import socket
import struct
import pickle

# Cấu hình địa chỉ và port
server_ip = '10.68.169.113'  # Địa chỉ IP của laptop
port = 9999

# Khởi tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, port))
connection = client_socket.makefile('wb')

# Mở camera
camera = cv2.VideoCapture(0)

try:
    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break
        
        # Mã hóa frame thành dạng chuỗi byte
        data = pickle.dumps(frame)
        # Đóng gói kích thước frame trước khi gửi
        message_size = struct.pack("L", len(data))
        # Gửi kích thước frame trước
        client_socket.sendall(message_size + data)

finally:
    camera.release()
    connection.close()
    client_socket.close()
