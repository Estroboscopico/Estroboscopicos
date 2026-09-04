document.addEventListener("DOMContentLoaded", () => {
    // 1. Hacemos la petición (fetch) para leer el archivo JSON
    fetch('datos_totales_canal.json')
        .then(response => response.json())
        .then(datos => {
            
            // 2. Actualizar los suscriptores
            document.getElementById('contador-subs').textContent = 
                `${datos.suscriptores} Suscriptores`;

            // 3. Función auxiliar para renderizar vídeos o shorts
            const renderizarVideos = (arrayVideos, contenedorId) => {
                const contenedor = document.getElementById(contenedorId);
                
                // Mostrar solo los 6 más recientes para no saturar la página (opcional)
                const videosMostrar = arrayVideos.slice(0, 6);

                videosMostrar.forEach(video => {
                    const tarjeta = document.createElement('article');
                    tarjeta.className = 'tarjeta-video';
                    
                    tarjeta.innerHTML = `
                        <a href="${video.url}" target="_blank">
                            <img src="${video.miniatura}" alt="Miniatura de ${video.titulo}">
                            <div class="info-tarjeta">
                                <h3>${video.titulo}</h3>
                                <p class="vistas">${video.vistas ? video.vistas + ' vistas' : ''}</p>
                            </div>
                        </a>
                    `;
                    contenedor.appendChild(tarjeta);
                });
            };

            // 4. Función auxiliar para renderizar listas de reproducción
            const renderizarListas = (arrayListas, contenedorId) => {
                const contenedor = document.getElementById(contenedorId);

                arrayListas.forEach(lista => {
                    const tarjeta = document.createElement('article');
                    tarjeta.className = 'tarjeta-lista';
                    
                    tarjeta.innerHTML = `
                        <a href="${lista.url}" target="_blank">
                            <div class="info-tarjeta">
                                <h3>📂 ${lista.titulo}</h3>
                                <p>${lista.cantidad_videos} vídeos</p>
                            </div>
                        </a>
                    `;
                    contenedor.appendChild(tarjeta);
                });
            };

            // 5. Llamamos a las funciones para llenar la web
            renderizarVideos(datos.videos_largos, 'contenedor-videos');
            renderizarVideos(datos.shorts, 'contenedor-shorts');
            renderizarListas(datos.listas, 'contenedor-listas');

        })
        .catch(error => {
            console.error("Error al cargar el JSON:", error);
            document.getElementById('contenedor-videos').innerHTML = "<p>Error al cargar los vídeos.</p>";
        });
});