from nxt.locator import find
from nxt.brick import Brick
from constants import MAILBOX1, MAILBOX3, MAILBOX7, MAILBOX10, NXT_BLUETOOTH_MAC_ADDRESS
import RPP
from threading import Thread, Lock
from nxt.locator import BrickNotFoundError
from nxt.error import DirectProtocolError
from time import sleep
from os import name, system
from Assets import datetime_formated

# By default use MAILBOX1 to send messages
# and MAILBOX10 to receive reponse messages
#     MAILBOX3  to receive data messages

'''
Manage the communication between the supervisor and the robot over Bluetooth
'''
class SupervisorClient:
    def __init__(self, nxt_bluetooth_mac):
        self._is_nxt_connected: bool = False
        self._nxt_brick: Brick = self.establish_nxt_connection(nxt_bluetooth_mac)
        # As soon as messages are read they're stored here
        self._recv_data_msg: list[tuple[int]] = []
        self._recv_response_msg: list[int] = []
        # mutexes
        self._msg_data_lock: Lock = Lock()
        self._there_is_running_program_on_nxt: bool = False
    
    # --- Connection Management ---
    
    def connect_to_nxt(self, nxt_bluetooth_mac: str) -> Brick|bool:
        try:
            nxt_brick = find(host=nxt_bluetooth_mac)
            self._is_nxt_connected = True
            self.show_success_message('Connected on NXT :]')
            return nxt_brick
        except BrickNotFoundError:
            self.clear_console()
            self.show_warning_message("NXT is unreachable")
            self.show_warning_message("Trying to connect agin...")
            self._is_nxt_connected = False
            return False
    
    """force the connection with the NXT, ad infinitum every 500ms
    
    :param str nxt_bluetooth_mac: NXT MAC address
    
    :return: The nxt Brick object
    :rtype: nxt.Brick.Brick
    """
    def force_nxt_connection(self, nxt_bluetooth_mac: str) -> Brick:
        attemps = 0
        while not self._is_nxt_connected and attemps < 5:
            nxt_brick = self.connect_to_nxt(nxt_bluetooth_mac)
            sleep(0.3)
            attemps += 1
        if not self._is_nxt_connected:
            raise BrickNotFoundError
        return nxt_brick

    def establish_nxt_connection(self, host: str) -> Brick:
        nxt_brick = self.connect_to_nxt(host)
        if not nxt_brick:
            nxt_brick = self.force_nxt_connection(host)
        return nxt_brick

    def close_nxt_connection(self) -> None:
        return self._nxt_brick.close()
    
    # --- Message Handling ---
    
    def send_message(self, request_code) -> None:
        try:
            formatted_msg = RPP.format_message(request_code=request_code)
            self._nxt_brick.message_write(MAILBOX1, formatted_msg)
        except DirectProtocolError:
            self.show_warning_message("It's impossible to send messages\
                                    - there's nothing running on NXT")
    
    def _send_data_message(self, data: list[bytes]) -> None:
        try:
            for chunk in data:
                self._nxt_brick.message_write(MAILBOX1, chunk)
                print(f'ENVIANDO -> {chunk}')
        except DirectProtocolError:
            self.show_warning_message("It's impossible to send messages\
                                    - there's nothing running on NXT")

    def send_coordinates(self, data: list[bytes]) -> None:
        try:
            #packed_coordinates = RPP.pack_coordinates(data, 8)
            # self.send_message(RPP.START_SENDING_COORDS)
            # sleep(0.4)
            self._send_data_message(data)
            # sleep(0.4)
            # self.send_message(RPP.STOP_SENDING_COORDS)
        except DirectProtocolError:
            self.show_warning_message("It's impossible to send messages\
                                    - there's nothing running on NXT")

    def _read_message(self, mailbox: int) -> str:
        try:
            (inbox, received_message) = self._nxt_brick.message_read(mailbox, 0, True)
            return received_message.decode().replace('\x00', '')
        except DirectProtocolError:
            return ''
    
    def _read_all_messages(self, mailbox: int, is_data_msg: bool) -> None:
        has_active_program = self._is_running_program_on_nxt()
        while has_active_program:
            received_message = self._read_message(mailbox)
            #print(f'MENSAGEM RECEBIDA -> {received_message}')
            if received_message:
                data = RPP.parse_message(received_message)
                if is_data_msg:
                    with self._msg_data_lock:
                        self._recv_data_msg.append(data)
                else:
                    with self._msg_data_lock:
                        self._recv_response_msg.append(data)
                print(f'[RECEIVED] -> {datetime_formated()} - {data}')
            has_active_program = self._is_running_program_on_nxt()
        self.show_warning_message("It's impossible to read new messages - \
                                there's nothing running on NXT")
        self.show_warning_message('Ending NXT connection')
        self.close_nxt_connection()
    
    def get_data_msgs(self) -> list[tuple[int]]:
        with self._msg_data_lock:
            temp = self._recv_data_msg.copy()
            self._recv_data_msg.clear()
        return temp
    
    def get_response_msgs(self) -> list[int]:
        with self._msg_data_lock:
            temp = self._recv_response_msg.copy()
            self._recv_response_msg.clear()
        return temp
    
    # --- Utilities ---
    
    """Start two threads that catch all the messages from the NXT Brick
        from two differents mailboxes, using self._read_all_messages
    """
    def catch_all_messages(self) -> None:
        Thread(target=self._read_all_messages, kwargs={'mailbox': MAILBOX3, 'is_data_msg': True}).start()
        Thread(target=self._read_all_messages, kwargs={'mailbox': MAILBOX10, 'is_data_msg': False}).start()
    
    def _is_running_program_on_nxt(self) -> bool:
        try:
            current_program_name = self._nxt_brick.get_current_program_name()
            if current_program_name:
                self._current_program_name = current_program_name
                return True
        except DirectProtocolError:
            self._current_program_name = None
            return False
    
    def get_nxt_brick(self) -> Brick|None:
        return self._nxt_brick

    def clear_console(self) -> None:
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def show_warning_message(self, message) -> None:
        print(f'[WARNING] - {message}')
    
    def show_success_message(self, message) -> None:
        print(f'[SUCCESS] - {message}')
    
if __name__ == '__main__':
    supervisor_client = SupervisorClient(NXT_BLUETOOTH_MAC_ADDRESS)
    data = [ (120, 220), (320, 420) ]
    data1 = [ (510, 610), (710, 810), (910, 1010) ]
    packets = RPP.pack_coordinates(data1, 8)
    supervisor_client.send_message(request_code=RPP.START_SENDING_COORDS)
    sleep(0.8)
    #sleep(2)
    supervisor_client.send_coordinates(packets)
    #sleep(0.2)
    #supervisor_client.send_coordinates(data1)
    #sleep(0.2)
    #supervisor_client.send_coordinates(data1)
    # supervisor_client.catch_all_messages()
    # supervisor_client.close_nxt_connection()
