import os
import pandas as pd
from pdfquery import PDFQuery
from tqdm.auto import tqdm

caminho_pdf = './pdfs'
caminho_xml = './xml'

names_files = {
    'Nome': {
        'precisa_extrair_codigo': True,
        'xml_codigo': [
            '204.777, 410.127, 391.228, 422.127',
            '204.777, 410.127, 423.719, 422.127',
            '204.777, 410.127, 373.258, 422.127',
            '204.777, 410.127, 423.719, 422.127',
            '204.777, 410.127, 390.607, 422.127',
            '204.777, 410.127, 447.244, 422.127',
            '204.777, 410.127, 445.955, 422.127',
            '204.777, 410.127, 445.275, 422.127',
            '204.777, 410.127, 440.594, 422.127',
            '204.777, 410.127, 439.932, 422.127',
            '204.777, 410.127, 439.932, 422.127',
            '204.777, 410.127, 431.318, 422.127',
            '204.777, 410.127, 429.027, 422.127',
            '204.777, 410.127, 423.924, 422.127',
            '204.777, 410.127, 413.904, 422.127',
            '204.777, 410.127, 412.352, 422.127',
            '204.777, 410.127, 409.686, 422.127',
            '204.777, 410.127, 348.59, 422.127',
            '204.777, 410.127, 384.578, 422.127',
            '239.875, 395.127, 437.26, 422.127',
        ],
        'xml_index': 8, # índice do LTTextBoxHorizontal
    },
}


def extrair_pdf_conteudo(pdf, nome_do_arquivo):
    dados = {}
    for chave, valor in names_files.items():
        texto = ''
        for codigo in valor.get('xml_codigo', []):
            texto = pdf.pq(f'LTTextBoxHorizontal[index="{valor["xml_index"]}"]:in_bbox("{codigo}")').text().strip()
            if texto:
                break
        
            if not texto:
                print(
                    f'Não achou valor para o campo `{chave}`, '
                    'provavelmente precisa de novo código, '
                    f'olhar o código em {caminho_xml}/{nome_do_arquivo}.xml')
            else:
                print(f'Texto extraído para o campo `{chave}`: {texto}')
                
        dados[chave] = texto
    
    return dados



# Lista para armazenar os nomes dos arquivos antigos e novos
nomes_arquivos = []

# Percorrer os arquivos PDF no diretório
for pdf_nome in tqdm(os.listdir(caminho_pdf)):
    if pdf_nome.endswith('.pdf'):
        caminho_do_pdf = os.path.join(caminho_pdf, pdf_nome)
        nome_do_arquivo, _ = os.path.splitext(pdf_nome)

        # Extrair informações do PDF usando o pdfquery
        pdf = PDFQuery(caminho_do_pdf)
        pdf.load()

        # Transformar o PDF em XML para obter os códigos das colunas
        pdf.tree.write(f'{caminho_xml}/{nome_do_arquivo}.xml', pretty_print=True)

        # Extraindo informações do PDF
        dados = extrair_pdf_conteudo(pdf=pdf, nome_do_arquivo=nome_do_arquivo)

        # Fechar o arquivo PDF
        pdf.file.close()

        # Obter o novo nome do arquivo
        if 'Nome' in dados and dados['Nome'] and dados['Nome'] != ' ':
            novo_nome_pdf = f"{dados['Nome']}.pdf"  # Usando o campo 'Nome' para renomear
            
            # Verificar se o arquivo PDF existe antes de tentar renomeá-lo
            if os.path.exists(os.path.join(caminho_pdf, pdf_nome)):
                nomes_arquivos.append({'antigo': pdf_nome, 'novo': novo_nome_pdf})
            else:
                print(f"O arquivo {pdf_nome} não foi encontrado.")

# Renomear os arquivos
for arquivo in nomes_arquivos:
    caminho_antigo = os.path.join(caminho_pdf, arquivo['antigo'])
    caminho_novo = os.path.join(caminho_pdf, arquivo['novo'])
    
    # Verificar se o arquivo antigo existe antes de tentar renomeá-lo
    if os.path.exists(caminho_antigo):
        os.rename(caminho_antigo, caminho_novo)
        print(f"Arquivo renomeado para {arquivo['novo']}")
    else:
        print(f"O arquivo {arquivo['antigo']} não foi encontrado.")
