import os
import requests
import time
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

# Configurações
TOKEN = os.getenv('TELEGRAM_TOKEN', '8040156850:AAEzyPxxlMTT7YD390EBejnf3U87V9iWgXA')

def processar_mensagem(chat_id, texto, usuario):
    print(f"📩 {usuario}: {texto}")
    
    # Respostas inteligentes
    if any(palavra in texto for palavra in ['oi', 'olá', 'ola', 'start', 'hey']):
        resposta = f"""🤖 <b>LOVE AGENTE IA - SISTEMA AUTÔNOMO</b>

Olá <b>{usuario}</b>! 👋 

🎯 <b>Estou online 24/7 pronto para análises!</b>

💫 <b>Comandos disponíveis:</b>
• analise - Análise completa do mercado
• pool - Análise detalhada de pools  
• ajuda - Ver todos os comandos

<code>🔧 Hospedado no Render - {datetime.now().strftime('%H:%M')}</code>"""
    
    elif 'analise' in texto or 'análise' in texto or 'mercado' in texto:
        resposta = f"""📊 <b>LOVE AGENTE IA - ANÁLISE DE MERCADO</b>
⏰ {datetime.now().strftime('%d/%m %H:%M')}
────────────────────

<b>🎯 OPORTUNIDADES IDENTIFICADAS:</b>

🚀 <b>PING/WETH Pool</b>
├ APR: <b>214.18%</b>
├ ROI: <b>4.39%</b> 
├ Fees: <b>$130.58</b>
└ Status: <b>🟡 OTIMIZÁVEL</b>

<code>🤖 Análise automática - Love Agent IA</code>"""
    
    elif 'pool' in texto or 'liquidez' in texto:
        resposta = f"""🏊 <b>ANÁLISE DETALHADA - POOL PING/WETH</b>
⏰ {datetime.now().strftime('%d/%m %H:%M')}
────────────────────

<b>📈 PERFORMANCE:</b>
├ ROI: <b>4.39%</b>
├ APR: <b>214.18%</b>
├ Fees Acumulados: <b>$130.58</b>
└ Idade: <b>7.5 dias</b>

<code>💡 Dica: Configure alertas automáticos</code>"""
    
    elif any(palavra in texto for palavra in ['ajuda', 'help', 'comandos']):
        resposta = """🆘 <b>LOVE AGENTE IA - AJUDA</b>

💫 <b>COMANDOS DISPONÍVEIS:</b>
• analise - Análise completa do mercado
• pool - Análise detalhada de pools
• ajuda - Esta mensagem de ajuda

<code>🔧 Hospedado no Render - Sempre online!</code>"""
    
    else:
        resposta = f"""🤖 <b>LOVE AGENTE IA</b>

Não entendi completamente, <b>{usuario}</b>!

💡 <b>Experimente:</b>
• "analise" - Para análise de mercado
• "pool" - Para análise de pools

<code>🎯 Estou aqui para ajudar!</code>"""
    
    # Enviar resposta
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            'chat_id': chat_id, 
            'text': resposta,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }, timeout=10)
        print(f"✅ Respondi para {usuario}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if 'message' in data:
            mensagem = data['message']
            chat_id = mensagem['chat']['id']
            texto = mensagem.get('text', '').lower()
            usuario = mensagem['chat'].get('first_name', 'Usuário')
            
            processar_mensagem(chat_id, texto, usuario)
        
        return 'OK', 200
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return 'ERROR', 500

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return '🤖 LOVE AGENTE IA - ONLINE', 200

@app.route('/')
def home():
    return '🤖 LOVE AGENTE IA - BOT TELEGRAM', 200

def configurar_webhook():
    """Configura o webhook no Telegram"""
    webhook_url = f"https://{request.host}/webhook"
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    
    try:
        response = requests.post(url, json={'url': webhook_url})
        if response.status_code == 200:
            print(f"✅ Webhook configurado: {webhook_url}")
        else:
            print(f"❌ Erro ao configurar webhook: {response.text}")
    except Exception as e:
        print(f"❌ Erro na configuração do webhook: {e}")

if __name__ == '__main__':
    print("🚀 LOVE AGENTE IA INICIANDO NO RENDER...")
    print("📍 Sistema webhook ativado!")
    print("=" * 50)
    
    # Configurar webhook ao iniciar
    with app.app_context():
        configurar_webhook()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)