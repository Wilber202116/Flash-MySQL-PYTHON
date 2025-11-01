// Trabajando el frontend
const API_URL = "https://flash-mysql-python.onrender.com/movies/"

// UTILIDADES
    // Uso del res con fetch
async function fetchJson(url, options = {}) {
    try{
        const res = await fetch(url, options)
        if (!res.ok) throw new Error ("Error en la peticion" + res.status)

        return await res.json() // develve la peticion con codigo
    }catch (error)
    {
        console.log(error)
        alert("Ocurrio un error")
        return null
    }
}

    // Convertir archivo de imagen a BASE64
function toBase64(file){
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        // Obtenemos el archivo
        reader.onload = () => resolve(reader.result.split(",")[1])
        reader.onerror = reject
    })
}

// Listar peliculas
async function loadMovies(params = {}) {
    const query = new URLSearchParams(params).toString()

    const movies = await fetchJson(`${API_URL}/list` + `?${query}`)
    if(!movies) return
    // console.log(movies)
    
    const tBody =  document.querySelector("#movies-table tbody")
    tBody.innerHTML = ""

    movies.forEach(i => {tBody.appendChild(createMovieRow(i))})
}

// Eliminar peliculas

async function deleteMovie(id){
    console.log(id)
    if(!confirm("¿Seguro que quiere eliminar esta pelicula para siempre?")) return
    const data = await fetchJson(API_URL + id, {method: "DELETE"})

    // Evitar errores inesperados
    if(data){
        alert(data.message)
        loadMovies()
    }
    
}

function editMovie(id){
    //console.log(id)
    window.location.href = "form.html?id=" + id

}

function createMovieRow(i){
    const row = document.createElement("tr")
    row.innerHTML = ` 
    <td>${i.id}</td> 
    <td>${i.titulo}</td>
    <td>${i.director}</td>
    <td>${i.anio}</td>
    <td>${i.genero}</td>
    <td>${i.calificacion}</td>
    <td>
        <img width=100 src="data:image/png;base64,${i.imagen} ">
    </td>
    <td>
        <button onClick='editMovie(${i.id})'
        class="button is-warning mt-3">Editar</button>
        <button OnClick='deleteMovie(${i.id})' class="button is-danger mt-3">Eliminar</button>
    </td>
    `
    return row
}

// document.addEventListener("click", e => {
//     console.log("SI ENTRE POR ACA")
//     const btn = e.target.closest("button[data-action]")
//     console.log(btn)
//     if(!btn) return;

//     const id = btn.dataset.id
//     const action = btn.dataset.action

//     if (action == "edit") return editMovie(id)
//     if (action == "delete") return deleteMovie(id)
// });

// Listar peliculas



// Editar peliculas

async function loadMoviesData( id,form, filenameSpan, image_preview, preview_field, currentPictureInput) {
    document.getElementById("form_title").textContent ="Editar pelicula"
    document.getElementById("movie_id").value = id
       
    const editMovie = await fetchJson(API_URL + "list/" + id)

    console.log(editMovie)

    if(!editMovie) return;

    const fields = ["titulo", "director", "anio", "genero", "calificacion"]

    fields.forEach(f => form[f].value = editMovie[f])

    if (editMovie.imagen){
        currentPictureInput.value = editMovie.imagen
        image_preview.src = "data:image/png;base64,"+editMovie.imagen
        preview_field.style.display = ""
        filenameSpan.textContent = "Imagen actual cargada"
    }
}

async function initForm(){

    const form = document.getElementById("movie_form")
    const params = new URLSearchParams(window.location.search)
    
    const movieId = params.get("id")
    
    const currentPictureInput = document.getElementById("current_image")
    const image_preview = document.getElementById("imagen_preview")
    const preview_field = document.getElementById("preview_field")
    const file_name = document.getElementById("file_name")

    const fileInput = document.getElementById("imagen")

    setupFileInput(fileInput, file_name, image_preview, preview_field)

    if(movieId){
        
        await loadMoviesData(movieId,form, file_name, image_preview,preview_field, currentPictureInput)
    }
    
    form.addEventListener("submit", async (e) => {
        handleFormSumit(e, form, fileInput, currentPictureInput, movieId)
    })
}

async function handleFormSumit(e, form, fileInput, currentPictureInput, movieId) {

    e.preventDefault()

    const formData = new FormData(form)
    const movie = Object.fromEntries(formData)

    if(fileInput.files.length > 0){
        movie.imagen = await toBase64(fileInput.files[0])
    }else{
        movie.imagen = currentPictureInput.value || ""
    }

    let url = API_URL
    let method = "POST"

    if(movieId){
        method ="PUT"
        url = API_URL + movieId
    }

    const data = await fetchJson(url, {
        method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(movie)
    })

    if(data){
        alert(data.message)
        window.location.href = "index.html"
    }
}



function setupFileInput(fileInput, filenameSpan,imagenPreview, preview_field){
    if(!fileInput) return

    fileInput.addEventListener("change", () => {
        if(fileInput.files.length > 0){
           const file = fileInput.files[0]
           filenameSpan.textContent = file.name
           imagenPreview.src = URL.createObjectURL(file)
           preview_field.style.display = ""
        }else{
            filenameSpan.textContent = "Ningun archivo seleccionado"
            preview_field.style.display = "none"
        }
    })
    
}

function getfilters(){
    return{
        genero: document.querySelector("#filter_genero").value.trim(),
        calificacion: document.querySelector("#filter_calificacion").value.trim()
    }
}

// Inicializa todas las funciones

document.addEventListener("DOMContentLoaded", () => {
    loadMovies()
    const filterBtn = document.querySelector("#filter_btn")
    filterBtn.addEventListener("click", () => {
        const filters = getfilters()
        loadMovies(filters)
    })
})

// Crear peliculas




// Filtrar peliculas
