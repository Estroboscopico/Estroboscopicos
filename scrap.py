import yt_dlp
import json

def extraer_todo_robusto(url_base, archivo_salida):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True
    }
    
    # Preparamos la estructura de nuestro JSON
    datos_completos = {
        'canal': 'ESTROBOSCOPICOS',
        'url_canal': url_base,
        'suscriptores': 0,
        'videos_largos': [],
        'shorts': [],
        'listas': []
    }
    
    # Definimos las URLs exactas de cada pestaña
    rutas = {
        'videos_largos': f"{url_base}/videos",
        'shorts': f"{url_base}/shorts",
        'listas': f"{url_base}/playlists"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for categoria, url in rutas.items():
            print(f"Consultando la pestaña: {url}...")
            
            try:
                info = ydl.extract_info(url, download=False)
                
                # Aprovechamos para capturar los suscriptores si la API nos los devuelve
                if datos_completos['suscriptores'] == 0 and info.get('channel_follower_count'):
                    datos_completos['suscriptores'] = info.get('channel_follower_count')
                    
                if 'entries' in info:
                    for item in info['entries']:
                        if not item: continue
                        
                        # Extraer la mejor miniatura
                        miniatura = None
                        if item.get('thumbnails'):
                            miniatura = item['thumbnails'][-1].get('url')
                            
                        # Clasificamos según la pestaña que estamos procesando
                        if categoria == 'listas':
                            datos_completos['listas'].append({
                                'id_lista': item.get('id'),
                                'titulo': item.get('title'),
                                'url': item.get('url'),
                                'cantidad_videos': item.get('playlist_count', 0)
                            })
                        else:
                            datos_completos[categoria].append({
                                'id': item.get('id'),
                                'titulo': item.get('title'),
                                'url': item.get('url'),
                                'vistas': item.get('view_count'),
                                'duracion': item.get('duration'),
                                'fecha_publicacion': item.get('upload_date'),
                                'miniatura': miniatura
                            })
            except Exception as e:
                print(f"Aviso: Hubo un problema extrayendo la pestaña {categoria}. Error: {e}")
                
    # Guardar en archivo
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(datos_completos, f, ensure_ascii=False, indent=4)
        
    print("\n✅ Extracción completa. Resumen de ESTROBOSCOPICOS:")
    print(f" - Suscriptores: {datos_completos['suscriptores']}")
    print(f" - Vídeos normales: {len(datos_completos['videos_largos'])}")
    print(f" - Shorts: {len(datos_completos['shorts'])}")
    print(f" - Listas de reproducción: {len(datos_completos['listas'])}")

if __name__ == "__main__":
    canal = 'https://www.youtube.com/@ESTROBOSCOPICOS'
    salida = 'datos_totales_canal.json'
    
    extraer_todo_robusto(canal, salida)