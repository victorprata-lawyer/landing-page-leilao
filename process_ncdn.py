import os
import re
import sqlite3
from pdfminer.high_level import extract_text

DB_PATH = 'assets.db'

def normalizar_texto(texto):
    if not texto: return ""
    # Remove quebras de linha e transforma múltiplos espaços em um só
    return re.sub(r'\s+', ' ', texto.replace('\n', ' ').replace('\r', ' ')).strip()

def buscar_codigo_oportunidade(texto):
    """
    Busca o padrão exato da imagem: OP-SP-ZS-20260331 - 17
    Também aceita variações como OPSP-ZS ou espaços diferentes.
    """
    # Regex flexível para: (OP-)? SP-ZS- (DATA) - (ID)
    padrao = r"(?:OP\s*-\s*)?SP\s*-\s*ZS\s*-\s*\d{8}\s*-\s*\d+"
    match = re.search(padrao, texto, re.IGNORECASE)
    
    if match:
        codigo_bruto = match.group(0).strip()
        # Padronização: remove espaços extras para bater com o banco
        # "OP-SP-ZS-20260331 - 17" vira "OP-SP-ZS-20260331-17"
        return re.sub(r'\s*-\s*', '-', codigo_bruto)
    return None

def processar_pdf(caminho_pdf, conn):
    try:
        print(f"📄 Extraindo texto de: {caminho_pdf}...")
        texto_bruto = extract_text(caminho_pdf)
        texto_limpo = normalizar_texto(texto_bruto)
        
        codigo = buscar_codigo_oportunidade(texto_limpo)
        
        if codigo:
            print(f"✅ Código identificado: {codigo}")
            cursor = conn.cursor()
            
            # Tenta atualizar o status no banco
            cursor.execute(
                "UPDATE assets SET status = 'formalizado' WHERE codigo_oportunidade = ?", 
                (codigo,)
            )
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"⭐ SUCESSO: Ativo vinculado ao código {codigo} foi FORMALIZADO.")
            else:
                print(f"❓ Código '{codigo}' extraído, mas não encontrado no assets.db.")
                print("DICA: Verifique se na sua planilha a coluna 'codigo_oportunidade' está com esse formato exato.")
        else:
            print(f"❌ Padrão de código não encontrado no texto de: {caminho_pdf}")
            # Mostra um pedaço do texto para conferência se falhar
            print(f"DEBUG: {texto_limpo[:200]}...")

    except Exception as e:
        print(f"⚠️ Erro técnico: {e}")

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        conexao = sqlite3.connect(DB_PATH)
        pdfs = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
        
        if not pdfs:
            print("Nenhum PDF encontrado na pasta.")
        else:
            for arq in pdfs:
                processar_pdf(arq, conexao)
        
        conexao.close()
    else:
        print("❌ Banco assets.db não encontrado na raiz.")