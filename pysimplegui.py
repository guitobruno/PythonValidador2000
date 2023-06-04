import PySimpleGUI as sg

def show_welcome_screen():
    layout = [
        [sg.Text("Bem-vindo ao Aplicativo de Manutenção de Links!")],
        [sg.Button("Iniciar", key='start_button')]
    ]

    window = sg.Window("Bem-vindo", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'start_button':
            window.close()
            return True

    window.close()
    return False

def main_program():
    import sqlite3
    from urllib.parse import urlparse
    import urllib.request

    sg.theme('DarkRed')
    conexao = sqlite3.connect('links/links.db')
    cursor = conexao.cursor()

    def validar_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    layout = [
        [sg.Text("Manutenção dos links")],
        [sg.Input(key='url')],
        [sg.Button("Incluir URL"), sg.Button("Excluir URL"), sg.Button("Alterar URL"), sg.Button("Listar URLs")],
    ]

    janela = sg.Window("Manutenção dos links", layout)

    while True:
        evento, valores = janela.read()

        if evento == sg.WINDOW_CLOSED:
            break

        if evento == "Incluir URL":
            url = valores['url']
            cursor.execute('INSERT INTO urls (links) VALUES (?)', (url,))
            conexao.commit()

        if evento == "Excluir URL":
            url = valores['url']
            cursor.execute('DELETE FROM urls WHERE links = ?', (url,))
            conexao.commit()

        if evento == "Alterar URL":
            url_antiga = valores['url']
            url_nova = sg.popup_get_text('Digite a nova URL:', default_text=url_antiga)
            cursor.execute('UPDATE urls SET links = ? WHERE links = ?', (url_nova, url_antiga))
            conexao.commit()

        if evento == "Listar URLs":
            cursor.execute('SELECT links FROM urls')
            resultados = cursor.fetchall()
            lista_urls = [f"{i + 1}. {resultado[0]}" for i, resultado in enumerate(resultados)]

            layout_urls = [[sg.Text("Lista de URLs")]]
            for i, url in enumerate(lista_urls):
                layout_urls.append([sg.Button(f"Validar URL {i+1}"), sg.Text(url)])

            layout_urls.append([sg.Button("Validar Todas URLs")])  # Botão para validar todas as URLs

            janela_urls = sg.Window("Lista de URLs", layout_urls)

            while True:
                evento_urls, valores_urls = janela_urls.read()

                if evento_urls == sg.WINDOW_CLOSED:
                    break

                if evento_urls == "Validar Todas URLs":
                    for i, url in enumerate(lista_urls):
                        url_validacao = url.split(". ", 1)[1]  # Obter a URL para validação
                        if validar_url(url_validacao):
                            resultado_validacao = f"A URL {url_validacao} é válida."
                        else:
                            resultado_validacao = f"A URL {url_validacao} é inválida."
                        sg.popup(f"URL: {url_validacao}\n\nResultado da validação:\n{resultado_validacao}")

                for i in range(len(lista_urls)):
                    if evento_urls == f"Validar URL {i+1}":
                        url_validacao = lista_urls[i].split(". ", 1)[1]  # Obter a URL para validação
                        if validar_url(url_validacao):
                            resultado_validacao = f"A URL {url_validacao} é válida."
                        else:
                            resultado_validacao = f"A URL {url_validacao} é inválida."
                        sg.popup(f"URL: {url_validacao}\n\nResultado da validação:\n{resultado_validacao}")

            janela_urls.close()

    janela.close()
    conexao.close()


if show_welcome_screen():
    main_program()
