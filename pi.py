import cv2
import socket
import pickle
import threading

def send_video():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)
    
    # Địa chỉ và cổng của máy chủ
    server_ip = "127.0.0.1"
    server_port = 6666
    
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        
        ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        x_as_bytes = pickle.dumps(buffer)
        s.sendto(x_as_bytes, (server_ip, server_port))
        
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
    cap.release()
    s.close()

def receive_commands():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 6667))  # Cổng nhận lệnh
    
    print("Listening for commands...")
    
    while True:
        data, addr = s.recvfrom(1024)
        command = data.decode('utf-8')
        print(f"Received command: {command}")

if __name__ == "__main__":
    # Tạo và khởi chạy luồng gửi video
    video_thread = threading.Thread(target=send_video)
    video_thread.start()
    
    # Tạo và khởi chạy luồng nhận lệnh
    command_thread = threading.Thread(target=receive_commands)
    command_thread.start()

    video_thread.join()
    command_thread.join()
