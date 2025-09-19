from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import json
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 設定請求超時
            url = "https://kite.kagi.com/tech_zh-Hant.xml"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; RSS Reader)')
            
            # 使用較短的超時時間
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_content = response.read().decode('utf-8')
            
            # 提取文章資訊
            articles = []
            items = re.findall(r'<item>(.*?)</item>', xml_content, re.DOTALL)
            
            for item in items[:3]:  # 只取前3個
                title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
                link = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
                
                if title and link:
                    articles.append({
                        "title": title.group(1).strip(),
                        "link": link.group(1).strip()
                    })
            
            # 回傳 JSON 響應
            json_str = json.dumps({
                "status": "success",
                "articles": articles,
                "count": len(articles)
            }, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json_str.encode('utf-8'))
            
        except urllib.error.URLError as e:
            self._send_error_response(f"網路請求錯誤: {str(e)}")
        except Exception as e:
            self._send_error_response(f"處理錯誤: {str(e)}")
    
    def _send_error_response(self, error_msg):
        json_str = json.dumps({
            "status": "error",
            "message": error_msg
        }, ensure_ascii=False)
        
        self.send_response(500)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json_str.encode('utf-8')) 

'''
# 新增測試功能
if __name__ == "__main__":
    print("啟動本地測試伺服器...")
    server = HTTPServer(("localhost", 8000), handler)
    print("伺服器啟動在 http://localhost:8000")
    print("按 Ctrl+C 停止伺服器")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止")
        server.server_close()
        '''