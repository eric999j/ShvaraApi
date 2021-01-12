from http.server import BaseHTTPRequestHandler
import json
import random
import time

class handler(BaseHTTPRequestHandler):

  words = [
  '新しいものを受け入れる',
  '楽観的な試み',
  '付着する',
  '最初に何かを探し、次に良いものを探す',
  'あなたに合った方法を使用してください',
  '独自の知識システムを構築する',
  '速い学習',
  '大きな目標を決定的に設定し、小さな目標を柔軟に置き換える',
  '最初にあなたがコントロールできるものを把握する',
  '平凡にならないでください',
  '優秀は卓越性の敵です',
  '小さなグレードに満足していない',
  '観察、判断、実行および忍耐',
  '本当の助けは与えることではなく、他の人に選択をさせることです'
  ]

  def do_GET(self):
    json_str=json.dumps({
	"Shvara": random.choice(words),
	"Date": time.strftime("%m/%d/%Y", time.localtime())
	}, ensure_ascii=False)
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json_str.encode(encoding='utf_8'))
    return
