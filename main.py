import sys
from datetime import date
from socket import socket, AF_INET, SOCK_STREAM

from network.GameRoom import GameRoom
from network.create_game_room import create_game_room

if __name__ == '__main__':

    date_1 = date(day=12, month=9, year=2002)
    date_2 = date(day=29, month=8, year=2004)
    march_10_2025 = date(day=10, month=3, year=2025)
    lived_days_1 = (march_10_2025 - date_1).days
    lived_days_2 = (march_10_2025 - date_2).days
    print(lived_days_1 % 3, lived_days_2 % 3)
    """
    Misma comfiguración del cliente hasta el momento
    """
    ip: str
    port: int
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    else:
        exit('Usage: python main.py <ip> <port>')
    with socket(AF_INET, SOCK_STREAM) as s:
        s.setblocking(True)
        s.bind((ip, port))
        s.listen()
        print('Waiting for connection...')
        conn, addr = s.accept()
        """
        Una vez aceptada la conexión, creamos una "sala de juego"'
        """
        with conn:
            print('Connected by', addr)
            command = conn.recv(8).decode() #Mensajes de control limitados a 8 bytes
            msg, difficulty, square = command.split(',') #Esto se modificara cuando halla más mensajes de control
            room: GameRoom
            match msg:
                case 'GAME':
                    """
                    Recivimos la instrucción del cliente de jugar contra la máquina con la dificultad
                    y casilla 'X' o 'O' escojidas
                    """
                    room = create_game_room(difficulty=difficulty, square=square, user_socket=conn)
                    room.run()  #Este metodo debe de ser ejecutado en un hilo para permitir multiconexión
                case 'JOIN': #Mensaje reservado para que otro jugador humano entre a una partida con otro jugador humano
                    """
                    Aún no implementado
                    """
                    raise NotImplementedError
