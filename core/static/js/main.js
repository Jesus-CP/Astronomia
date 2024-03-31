document.addEventListener('DOMContentLoaded', function() {
    // Código que se ejecutará después de que el DOM se haya cargado por completo.

    // modal para telefono barra de navegacion
    const menuBtn = document.querySelector('.menu-btn');
    const navMenuMid = document.querySelector('.nav-menu-mid');

    if (menuBtn && navMenuMid) {
        menuBtn.addEventListener('click', () => {
            navMenuMid.classList.toggle('show');

            if (navMenuMid.classList.contains('show')) {
                document.body.style.overflow = 'hidden';
                document.body.style.position = 'relative';
            } else {
                document.body.style.overflow = 'auto';
                document.body.style.position = 'static';
            }
        });
    }

    document.body.addEventListener('click', (event) => {
        if (
            !event.target.closest('.menu-btn') &&
            !event.target.closest('.nav-menu-mid')
        ) {
            if (navMenuMid.classList.contains('show')) {
                navMenuMid.classList.remove('show');
                document.body.style.overflow = 'auto';
                document.body.style.position = 'static';
            }
        }
    });

    // Modal para los comentarios
    var modal = document.getElementById("comentarioModal");
    var btnCrearComentario = document.getElementById("btnCrearComentario");
    var comentarioForm = document.querySelector('.comentario-form');

    if (btnCrearComentario) {
        btnCrearComentario.addEventListener("click", function() {
            modal.style.display = "block";
        });
    }

    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
            
            // Habilita el botón después de cerrar la modal
            btnCrearComentario.disabled = false;
        }
    });

    if (comentarioForm) {
        comentarioForm.addEventListener('submit', function() {
            // Deshabilita el botón al enviar el formulario para evitar clics múltiples
            btnCrearComentario.disabled = true;
            modal.style.display = "none";
        });
    }

    //Codigo Para la funcion del zoom Imagen
    const imageContainer = document.getElementById("imageContainer");
    const fullscreenImage = document.getElementById("fullscreenImage");
    const fullscreenButton = document.getElementById("fullscreenButton");
    const closeButton = document.getElementById("closeButton");
    const resetZoomButton = document.getElementById("resetButton");

    const imageContainerMarcador = document.getElementById("imageContainerMarcador");
    const fullscreenImageMarcador = document.getElementById("fullscreenImageMarcador");
    const fullscreenMarcadorButton = document.getElementById("fullscreenMarcadorButton");
    const closeButtonMarcador = document.getElementById("closeButtonMarcador");
    const resetZoomButtonMarcador = document.getElementById("resetButtonMarcador");

    let panZoomInstance;
    let isFullscreen = false;

    let panZoomInstanceMarcador;
    let isFullscreenMarcador = false;

    function openFullscreen() {
        if (isFullscreen) {
            return;
        }

        imageContainer.style.display = "flex";
        document.documentElement.style.overflow = 'hidden';

        closeButton.style.display = "block";
        resetZoomButton.style.display = "block";

        panZoomInstance = panzoom(fullscreenImage, {
            zoomDoubleClickSpeed: 2,
            minZoom: 1,
            maxZoom: 3,
        });

        // Centrar la imagen horizontal y verticalmente
        centerImage(fullscreenImage);

        isFullscreen = true;
    }


    function closeFullscreen() {
        if (!isFullscreen) {
            return;
        }

        imageContainer.style.display = "none";
        document.documentElement.style.overflow = 'auto';

        if (panZoomInstance) {
            panZoomInstance.dispose();
        }

        closeButton.style.display = "none";
        resetZoomButton.style.display = "none";

        isFullscreen = false;
    }

    function resetImage() {
        if (panZoomInstance) {
            panZoomInstance.moveTo(0, 0);
            panZoomInstance.zoomAbs(0, 0, 1);
            
            centerImage(fullscreenImage);
        }
    }

    function centerImage(imageElement) {
        // Obtener el tamaño del contenedor
        const containerWidth = imageContainer.offsetWidth;
        const containerHeight = imageContainer.offsetHeight;

        // Obtener el tamaño de la imagen
        const imageWidth = imageElement.width;
        const imageHeight = imageElement.height;

        // Calcular las nuevas coordenadas para centrar la imagen
        const newX = (containerWidth - imageWidth) / 2;
        const newY = (containerHeight - imageHeight) / 2;

        // Mover y hacer zoom a las nuevas coordenadas
        panZoomInstance.moveTo(newX, newY);
        panZoomInstance.zoomAbs(newX, newY, 1);
    }

    function openFullscreenMarcador() {
        if (isFullscreenMarcador) {
            return;
        }

        imageContainerMarcador.style.display = "flex";
        document.documentElement.style.overflow = 'hidden';

        closeButtonMarcador.style.display = "block";
        resetZoomButtonMarcador.style.display = "block";

        panZoomInstanceMarcador = panzoom(fullscreenImageMarcador, {
            zoomDoubleClickSpeed: 2,
            minZoom: 1,
            maxZoom: 3,
        });

        centerImageMarcador(fullscreenImageMarcador);

        isFullscreenMarcador = true;
    }

    function centerImageMarcador(imageElement) {
        // Obtener el tamaño del contenedor marcador
        const containerWidth = imageContainerMarcador.offsetWidth;
        const containerHeight = imageContainerMarcador.offsetHeight;
    
        // Obtener el tamaño de la imagen del marcador
        const imageWidth = imageElement.width;
        const imageHeight = imageElement.height;
    
        // Calcular las nuevas coordenadas para centrar la imagen del marcador
        const newX = (containerWidth - imageWidth) / 2;
        const newY = (containerHeight - imageHeight) / 2;
    
        // Mover y hacer zoom a las nuevas coordenadas del marcador
        panZoomInstanceMarcador.moveTo(newX, newY);
        panZoomInstanceMarcador.zoomAbs(newX, newY, 1);
    }
    

    function closeFullscreenMarcador() {
        if (!isFullscreenMarcador) {
            return;
        }

        imageContainerMarcador.style.display = "none";
        document.documentElement.style.overflow = 'auto';

        if (panZoomInstanceMarcador) {
            panZoomInstanceMarcador.dispose();
        }

        closeButtonMarcador.style.display = "none";
        resetZoomButtonMarcador.style.display = "none";

        isFullscreenMarcador = false;
    }

    function resetImageMarcador() {
        if (panZoomInstanceMarcador) {
            panZoomInstanceMarcador.moveTo(0, 0);
            panZoomInstanceMarcador.zoomAbs(0, 0, 1);

            centerImageMarcador(fullscreenImageMarcador);
        }
    }

    if (fullscreenButton) {
        fullscreenButton.addEventListener("click", openFullscreen);
        fullscreenButton.addEventListener("touchstart", openFullscreen);
    }
    
    if (closeButton) {
        closeButton.addEventListener("click", closeFullscreen);
        closeButton.addEventListener("touchstart", closeFullscreen);
    }
    
    if (resetZoomButton) {
        resetZoomButton.addEventListener("click", resetImage);
        resetZoomButton.addEventListener("touchstart", resetImage);
    }
    
    if (fullscreenMarcadorButton) {
        fullscreenMarcadorButton.addEventListener("click", openFullscreenMarcador);
        fullscreenMarcadorButton.addEventListener("touchstart", openFullscreenMarcador);
    }
    
    if (closeButtonMarcador) {
        closeButtonMarcador.addEventListener("click", closeFullscreenMarcador);
        closeButtonMarcador.addEventListener("touchstart", closeFullscreenMarcador);
    }
    
    if (resetZoomButtonMarcador) {
        resetZoomButtonMarcador.addEventListener("click", resetImageMarcador);
        resetZoomButtonMarcador.addEventListener("touchstart", resetImageMarcador);
    }

    document.addEventListener("keyup", function (e) {
        if (e.key === "Escape") {
            closeFullscreen();
            closeFullscreenMarcador();
        }
    });
});

//Modal de eliminar en el listado
document.addEventListener('DOMContentLoaded', () => {
    // Tu código JavaScript aquí
    const eliminarEnlaces = document.querySelectorAll('.eliminar-enlace');
    const modal2 = document.getElementById('confirmarBorradoModal2');
    const siBorrarBoton = document.getElementById('siBorrar');
    const noBorrarBoton = document.getElementById('noBorrar');
    let urlEliminar = '';

    eliminarEnlaces.forEach((enlace) => {
        enlace.addEventListener('click', (event) => {
            event.preventDefault();
            urlEliminar = event.currentTarget.getAttribute('data-url');
            modal2.style.display = 'block';
        });
    });

    if (siBorrarBoton) {
        siBorrarBoton.addEventListener('click', () => {
            if (urlEliminar !== '') {
                window.location.href = urlEliminar; // Redirigir para eliminar la publicación
            }
        });
    }

    if (noBorrarBoton) {
        noBorrarBoton.addEventListener('click', () => {
            modal2.style.display = 'none'; // Cerrar la modal
        });
    }
});