import socket
import time
import os

def connect_to_iqfeed(host="127.0.0.1", port=9100):
    """Establishes a connection to IQFeed."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Connected to IQFeed")
        return sock
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def send_request(sock, request):
    """Sends a request to IQFeed."""
    try:
        print(f"Sending request: {request}")
        sock.sendall(request.encode("utf-8") + b"\r\n")
    except Exception as e:
        print(f"Error sending request: {e}")

def receive_data(sock, buffer_size=4096):
    """Receives data from IQFeed."""
    data = b""
    while True:
        try:
            chunk = sock.recv(buffer_size)
            if not chunk:
                break
            data += chunk
            if b"!ENDMSG!" in chunk:
                break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break
    print(f"Raw data: {data.decode('utf-8')}")
    return data.decode("utf-8")

def clean_data(raw_data):
    """Cleans system messages from the raw data, removes trailing commas, and reverses the order of lines."""
    lines = raw_data.splitlines()
    cleaned_lines = [
        line.rstrip(',') for line in lines if not line.startswith("!")  # Убираем системные сообщения и запятые
    ]
    cleaned_lines.reverse()  # Реверсируем строки, чтобы порядок был "старый к новому"
    return "\n".join(cleaned_lines)



def download_historical_data(symbols, interval, start_date, end_date, save_path):
    """Downloads historical data from IQFeed for a list of symbols.

    Args:
        symbols (list): List of symbols to download data for.
        interval (str): Time interval in seconds.
        start_date (str): Start date and time in 'YYYYMMDD HHMMSS' format.
        end_date (str): End date and time in 'YYYYMMDD HHMMSS' format.
        save_path (str): Directory to save the downloaded files.
    """
    for symbol in symbols:
        sock = connect_to_iqfeed()
        if not sock:
            continue

        # Construct the HIT request to fetch all data between the dates
        request = f"HIT,{symbol},{interval},{start_date},{end_date},0,,,,,,"
        print(f"Constructed request for {symbol}: {request}")

        send_request(sock, request)
        time.sleep(1)  # Wait for the response to be received

        data = receive_data(sock)
        print(f"Received data for {symbol}: {data}")

        sock.close()

        # Check for errors in the response
        if "E,!NO_DATA!," in data:
            print(f"Error: No data available for {symbol}.")
            continue

        # Clean the data to remove system messages
        cleaned_data = clean_data(data)

        # Ensure the save directory exists
        os.makedirs(save_path, exist_ok=True)

        # Save the cleaned data to a file named after the symbol
        file_path = os.path.join(save_path, f"{symbol}.txt")
        with open(file_path, "w") as f:
            f.write(cleaned_data)
        print(f"Data for {symbol} saved to {file_path}")

if __name__ == "__main__":
    # Example usage
    symbols = ["IVV", "VOO", "QQQ", "VTI", "IWM", "EEM", "VEA", "EFA", "VWO", "GLD", "LQD", "TLT", "VNQ", "XLF",
               "XLV", "EWJ", "MCHI", "IYR", "DIA", "XLE", "XLY", "XLP", "XLI", "XLB", "XLRE", "XLK", "XLU", "XLC", "SOXL"
]  # List of symbols
    interval = "60"  # Interval in seconds
    start_date = "20200101 000000"  # Start date/time
    end_date = "20250102 000000"  # End date/time

    # Specify the directory to save files
    save_path = os.path.expanduser("~/Desktop/history/etf")

    download_historical_data(symbols, interval, start_date, end_date, save_path)
