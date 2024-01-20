from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
from openai import OpenAI
import json

# Flaskの起動
app = Flask(__name__)
CORS(app)

# ルーティングの設定
@app.route('/',methods=['GET','POST'])

def home():
    return generate()

def generate():
    data = request.get_json()
    # デバッグ用
    print(data)
    print(data.get('key'))
    
    # APIクライアントの初期化
    client = OpenAI(
        # This is the default and can be omitted
        organization=os.environ.get('OpenAI_organization'),
        api_key=os.environ.get('API_KEY_openai')
    )

    #messages = data.get('messages', [])

    # メッセージの設定
    messages = [
        {"role": "assistant", "content": "前回のシナリオは「" + data.get('key') + "」でした。この続きのシナリオを書いてください。形式としてシナリオ名及びシナリオ内容と、それに対応する2つの行動の選択肢を出力してください。jsonフォーマット { シナリオ名:文章, シナリオ内容:文章, 選択肢1:文章, 選択肢2:文章 } の形で返してください。"},
    ]

    # APIリクエストの設定
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # GPTのエンジン名を指定します
        messages=messages,
        max_tokens=300,  # 生成するトークンの最大数
        n=1,  # 生成するレスポンスの数
        stop=None,  # 停止トークンの設定
        temperature=0.7,  # 生成時のランダム性の制御
        top_p=1,  # トークン選択時の確率閾値
    )

    # 生成されたテキストの取得
    print(response)
    for i, choice in enumerate(response.choices):
        print(f"\nresult {i}:")
        print(choice.message.content.strip())
    #修正前
    #return jsonify([choice['message']['content'] for choice in response['choices']])
    #修正後(rawjson)
    return jsonify([choice.message.content for choice in response.choices])
        
    # 日本語出力
    # 生成されたテキストの取得
    # result = [choice.message.content for choice in response.choices]
    # 結果をJSONファイルとして出力
    # with open('output.json', 'w', encoding='utf-8') as f:
    #    json.dump(result, f, ensure_ascii=False, indent=4)
    # JSON形式での返却（日本語をそのまま出力）
    # return make_response(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    app.run(debug=True)
