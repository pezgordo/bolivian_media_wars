import urllib.request
from bs4 import BeautifulSoup
from collections import Counter
import re
import sqlite3
import datetime
from unidecode import unidecode
import requests



# connect to db
conn = sqlite3.connect('bol_wars.db')
cursor = conn.cursor()

todays_date = datetime.date.today()
today_date_str = todays_date.strftime("%Y-%m-%d")

urls = [
    'https://unitel.bo/',
    #'https://monteronoticias.com/',
    #'https://lavozdetarija.com/',
    'https://www.la-razon.com/',
    'https://www.eldia.com.bo/index.php',
    #'https://www.abi.bo/',
    'https://www.redbolivision.tv.bo/',
    'https://www.atb.com.bo/',
    #'https://lapalabradelbeni.com.bo/',
    'https://www.noticiasfides.com/',
    #'https://datos-bo.com/',
    #'https://www.cabildeodigital.com/',
    #'https://www.leo.bo/',
    #'https://www.money.com.bo/',
    'https://elpotosi.net/',
    #'https://lapatria.bo/',
    #'https://elfulgor.com/',
    'https://correodelsur.com/',
    #'https://www.ver.bo/',
    'https://www.eldiario.net/portal/',
    #'https://elandaluz.com.bo/',
    #'https://www.brujuladigital.net/',
    #'https://www.oxigeno.bo/',
    #'https://newstime.bo/',
    #'https://jornada.com.bo/',
    'https://www.opinion.com.bo/',
    'https://www.lostiempos.com/',
    #'https://elpais.bo/',
    'https://www.reduno.com.bo/',
    'https://eldeber.com.bo/',
    'https://erbol.com.bo/'
]

#url = 'https://unitel.bo/'
#url = 'https://monteronoticias.com/'
#url = 'https://lavozdetarija.com/'
#url = 'https://www.la-razon.com/'
#url = 'https://www.eldia.com.bo/'
#url = 'https://www.abi.bo/'
#url = 'https://www.redbolivision.tv.bo/'
#url = 'https://www.atb.com.bo/'
#url = 'https://lapalabradelbeni.com.bo/'
#url = 'https://www.noticiasfides.com/'
#url = 'https://datos-bo.com/'
#url = 'https://www.cabildeodigital.com/'
#url = 'https://www.leo.bo/'
#url = 'https://www.money.com.bo/'
#url = 'https://elpotosi.net/'
#url = 'https://lapatria.bo/'
#url = 'https://elfulgor.com/'
#url = 'https://correodelsur.com/'
#url = 'https://www.ver.bo/'
#url = 'https://www.eldiario.net/portal/'
#url = 'https://elandaluz.com.bo/'
#url = 'https://www.brujuladigital.net/'
#url = 'https://www.oxigeno.bo/'
#url = 'https://newstime.bo/'
#url = 'https://jornada.com.bo/'
#url = 'https://www.opinion.com.bo/'
#url = 'https://www.lostiempos.com/'
#url = 'https://elpais.bo/'
#url = 'https://www.reduno.com.bo/'
#url = 'https://eldeber.com.bo/'
#url = 'https://erbol.com.bo/'



# Keyword categories
categories = {
    'opositores': {'oposicion', 'adrian oliva', 'anez', 'carolina ribera', 'carlos mesa', 'cesar apaza', 'comcipo',
                'fernando camacho', 'jeanine anez', 'jorge quiroga', 'juan carlos medrano',
                'luisa nayar', 'oscar ortiz', 'pumari', 'rafael quispe', 'rek', 'roman loayza',
                'ruben costas', 'samuel doria medina', 'shirley franco', 'tata quispe',
                'tuto quiroga', 'victor hugo cardenas', 'wilson santamaria', 'ortiz'},
    
    'masistas': {'adriana salvatierra', 'andronico', 'choquehuanca', 'cuellar', 'del castillo',
                'diego pary', 'eva', 'eva copa', 'evo', 'evo morales', 'evista', 'evistas', 'arcista', 'arcistas', 'felix patzi', 'gabriela zapata',
                'garcia linera', 'jhonny fernandez', 'luis arce', 'arce', 'marcelo montenegro',
                'nelida sifuentes', 'romero', 'torrico', 'edmundo novillo', 'wilfredo chavez', 'csutcb'},
    
    'economia': {'aduana', 'abastecimiento', 'aguinaldo', 'anh', 'bono', 'balance', 'cañeros', 'carbonato', 'capitalizacion', 'creditos',
                'combustible', 'combustibles', 'comercio exterior', 'comerciante', 'comerciantes', 'contrabando', 'crisis', 'deficit', 'desembolso', 
                'deuda externa', 'diesel', 'dolar', 'dolares', 'economia', 'economica', 'empleo', 'etanol', 'exportacion', 'exportaciones', 'gasolina',
                'industrializacion', 'informalidad', 'litio', 'jubilacion', 'mineria', 'pge',
                'presupuesto', 'recursos', 'subsidio', 'subvencion', 'ypfb'},
    
    'narcotrafico': {'antidroga', 'antidrogas', 'coca', 'cocaina', 'chapare', 'droga', 'drogas', 'fabrica de droga',
                'felcn', 'marihuana', 'narco', 'narcotraficante', 'narcotrafico', 'pcc', 'sello rojo',
                'sebastian marset', 'tropico de cochabamba', 'marset', 'heroina', 'fentanilo'},
    
    'politica': {'alcalde', 'alcaldes', 'cadena perpetua', 'consejales', 'congreso', 'constitucion', 'corrupto', 'corrupcion', 'csutcb', 'democracia', 
                 'diputado', 'diputados', 'elecciones', 'electoral', 'estabilidad', 'exministros', 'gobierno', 'golpe',
                'golpe de estado', 'MAS', 'masistas', 'ministro', 'milei', 'opositores', 'parlamento',
                'procuradoria', 'politica', 'politicas', 'referendum', 'reeleccion', 'revocatorio', 'revocatoria', 'senado', 'senadores',
                'tse', 'viceministro', 'viceministros', 'voto'},
    
    'seguridad': {'abuso sexual', 'accidente', 'armas', 'apunalada', 'apunalado', 'aprehendido', 'aprehendida', 'aprehendidos', 'aprehenden', 'asesinato', 'atropellar', 'ataque', 'ataco', 'blindado', 'bloqueo', 'carcel', 'capturado', 
                  'capturaron', 'cadaver', 'chonchocoro', 'coronel', 'condena', 'conflicto', 'desaparecida', 'derrame', 'derechos', 'ebrio', 'ebria', 'explosivo', 'golpear',
                  'feminicidio', 'feminicida', 'feminicidas', 'fuego', 'fusiles', 'incendios', 'interpol', 'intoxicacion', 'ilegal', 'ladron', 'ladrones', 
                  'muerte', 'muere', 'organizacion criminal', 'organizaciones criminales', 'palmasola', 'pelea', 'policia', 
                  'prision', 'protesta', 'robar', 'robo', 'sangre', 'secuestro', 'seguridad', 'sequias', 'sufrio', 'victima', 'vigilancia', 'violenta', 'violento'}
}

    # Scrap

for url in urls:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        html_data = response.read().decode('utf-8')
        
        # Use BeautifulSoup to clean up the HTML and extract text
        soup = BeautifulSoup(html_data, 'html.parser')
        text = soup.get_text()
        
        if "captcha" in text.lower():
            print(f"{url} may be asking for a CAPTCHA.")
        else:
            print(f"{url} is accessible without a CAPTCHA.")
    except Exception as e:
        print(f"Error accessing {url}: {e}")


        # ignore this words
        ignore_words = {'que', 'con', 'por', 'los', 'del', 'una', 'para', 'las', 'pero', 'como', 'the',
                        'más', 'leer', 'erbol', 'medio', 'tambien', 'este', 'fuente', 'todavía', 'porque',
                        'qué', 'tras', 'puede', 'noticias', 'salud', 'opinión', 'deportes', 'virales', 'policial',
                        'tecnología', 'ciencia', 'según', 'ante', 'entre', 'campeón', 'llegar', 'sobre', 
                        'conozca', 'fueron', 'tabla', 'ver', 'esta', 'multimedia', 'multideportivo', 'puntos',
                        'mostrador', 'actualidad', 'int', 'click', 'recibe', 'todo', 'hasta', 'redacción',
                        'hoy', 'infobae', 'revista', 'vez', 'contra', 'clave', 'pide', 'fue', 'haciendo', 
                        'hace', 'mundo', 'todos', 'cualquier', 'afirmó', 'sea', 'brujula', 'acerca', 'belleza',
                        'hay', 'han', 'edición', 'haber', 'está', 'impresa', 'finanzas', 'suscripción',
                        'hide', 'author', 'comment', 'count', 'type', 'express', 'suscríbete', 'cuaritediciembre',
                        'usuariodiciembre', 'usuarionoviembre', 'ticonadiciembre', 'cuaritenoviembre', 'ticonanoviembre',
                        'noticiero', 'portada', 'señal', 'bolivision', 'abi', '000', 'telf', 'eldia', 'sociedad', 'negocios', 
                        'diciembre', 'noviembre', 'octubre', 'marcas', 'unitel', 'tendencias', 'telepais', 'batidora', 'estan',
                        'era', 'san', 'paz', 'fin', 'ano', 'anos', 'despues', 'otro', 'afirma', 'reves', 'presenta', 'dire', 'vamos',
                        'facebook', 'tik', 'tok', 'twitter', 'instagram', 'youtube', 'threads', 'inicio', 'bad', 'bunny', 'kendall', 
                        'jenner', 'asi', 'editorial', 'hemeroteca', 'ediciones', 'diario', 'sociales', 'como', 'estara', 'estan',
                        'email', 'protected', 'dic', 'asi', 'actualmente', 'ahora', 'aun', 'varios', 'and', 'cuentan', 'dice',
                        'tinta', 'deja', 'com', 'cargar', '591', 'atb', 'novelas', 'programacion', 'contactenos', 'close',
                        'anteriores', 'desde'




                        }

        # Remove any non-word characters and convert all words to lowercase
        #words = [unidecode(word) for word in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)\w{3,}\b', text.lower()) if unidecode(word) != 'mas' and word not in ignore_words]
        #words = [unidecode(" ".join(match)) for match in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)(\w{3,}(\s+\w{3,})?)\b', text.lower()) if unidecode(" ".join(match)) != 'mas' and " ".join(match) not in ignore_words]
        #words = [unidecode(match[0]) for match in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)(\w{3,}(\s\w{3,})?)\b', text.lower()) if unidecode(match[0]) != 'mas' and match[0] not in ignore_words]
        single_words = [unidecode(word) for word in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)\w{3,}\b', text.lower()) if unidecode(word) != 'mas' and word not in ignore_words]
        phrase_matches = [unidecode(match[0]) for match in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)(\w{3,}(\s\w{3,})?)\b', text.lower()) if unidecode(match[0]) != 'mas' and match[0] not in ignore_words]
        #phrase_matches = [unidecode(match[0].replace('\n', ' ')) for match in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)([\w\s]{3,})\b', text.lower()) if unidecode(match[0]) != 'mas' and match[0] not in ignore_words]
        #phrase_matches = [unidecode(match[0].replace('\n', ' ')) for match in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)([\w\s]{3,})\b', text.lower()) if unidecode(match[0].replace('\n', ' ')) != 'mas' and match[0].replace('\n', ' ') not in ignore_words]
        #phrase_matches = [unidecode(match[0]) for match in re.findall(r'\b(?!00z)(?!\d{2}t\d{2}\b)(\w{3,}(?:\s\w{3,})?)\b', text.lower()) if unidecode(match[0]) != 'mas' and match[0] not in ignore_words]



        # Build a regex pattern based on categories and keywords
        pattern_parts = []
        for category, keywords in categories.items():
            category_pattern = fr'\b(?:{"|".join(map(re.escape, keywords))})\b'
            pattern_parts.append(f'({category_pattern})')

        full_pattern = '|'.join(pattern_parts)

        # Extract matches using regex
        matches = re.findall(full_pattern, unidecode(text.lower()))

        # Flatten the list of tuples produced by re.findall
        matches = [match for tup in matches for match in tup]

        # Filter out ignored words
        filtered_matches = [unidecode(match) for match in matches if unidecode(match) != 'mas' and match not in ignore_words]

        # Count the words using Counter for each category
        category_counts = {}
        for category, keywords in categories.items():
            category_matches = [item for item in filtered_matches if any(keyword in item for keyword in keywords)]
            category_counts[category] = Counter(category_matches)

        # Print the counts for each category
        for category, counts in category_counts.items():
            total_count = sum(counts.values())
            #print(f"{category.capitalize()} counts:", counts)
            #print(f"Total {category.capitalize()} count:", total_count)

        for category, counts in category_counts.items():
            for word, count in counts.items():
                add_to_word_categories = (category, word, count, url, today_date_str)
                #print(add_to_word_categories)

                cursor.execute('''
                                INSERT INTO word_categories (category, word, count, site, date)
                                VALUES (?, ?, ?, ?, ?)
                                ''', add_to_word_categories)
            

        #print(pattern_parts)
        #print(category_counts)


        # Count the words using Counter
        word_counts = Counter(single_words)

    

        # Print the 10 most common words
        #print(word_counts.most_common(100))


        

        most_common = (word_counts.most_common(100))

        data_to_add = [(item[0], item[1], url, todays_date) for item in most_common]

        cursor.executemany('''
                        INSERT INTO word_count (word, count, site, date)
                        VALUES (?, ?, ?, ?)
                        ''', data_to_add)
        
        conn.commit()
        

        #print(data_to_add)



    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")



# Close the database connection

conn.close()