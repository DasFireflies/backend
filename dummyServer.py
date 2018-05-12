import socket

def Main():
    host = "172.31.27.46"
    port = 5000

    #create socket
    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print("executing line after mySocket.accept()")
    print ("Connection from: " + str(addr))

    while True  :
        #receiving data
        data = conn.recv(1024).decode()
        print ("from connected  user: " + str(data))

        #sending data
        print("Sending string...")
        data = "Server says hi!\r\n"
        conn.send(data.encode())

    conn.close()

if __name__ == '__main__':
    Main()
