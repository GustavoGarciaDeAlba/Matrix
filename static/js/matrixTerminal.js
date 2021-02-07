//Creación de objeto terminal
let matrixTerminal = new Terminal()


function terminalMatrix() {

    //Inicializacion de terminal
    defineTerminal(matrixTerminal)

    //Implementacion de terminal en html
    $(".terminalMain").append(matrixTerminal.html)

    //Función recursiva que evaluar y opera comandos ingresados
    inputCommandTerminal()
}

/*
    Se evaluan los comandos ingresados en la terminal
    llamando a funciones de la terminal y haciendo
    consultas/operaciones a los archivos txt (memoria?)
    de cadausuario.
*/
function inputCommandTerminal() {
    matrixTerminal.input(usr + "@" + usr + ":~$", function (comando) {
        //Se extrae el valor pasado por Flask para llamar a una funcion py que abra el archivo del usr
        //LOGRE PASAR INFORMACION DE FLASK A JS
        // let usr = '{{usr}}' Esta parte requiere investigacion

        //partir el comando en seccion
        //cada seccion estara dividida por un espacio 
        let comandoSeccionado = comando.split(" ");
        switch (comandoSeccionado[0]) {
            case "clr":
                clearTerminal()
                break;
            case "read":
                readFile(comandoSeccionado[1])
                break
            case "edit":
                let i, texto_a_agregar = ""
                for (i = 3; i < comandoSeccionado.length; i++) {
                    texto_a_agregar += comandoSeccionado[i] + " "
                }
                edit(comandoSeccionado[1], texto_a_agregar)
                break
            case "list":
                list(inodo_del_directorio_actual)
                break
            case "createf":
                createf(comandoSeccionado[1])
                break
            case "createdir":
                crearDirectorio(comandoSeccionado[1])
                break
            case "renamedir":
                renameDir(comandoSeccionado[1], comandoSeccionado[2])
                break
            case "delete":
                deleteFile(comandoSeccionado[1])
                break
            case "deletedir":
                deleteDir(comandoSeccionado[1])
                break
            case "rename":
                renameFile(comandoSeccionado[1], comandoSeccionado[2])
                break
            case "copy":
                copyFile(comandoSeccionado[1])
                break
            case "ls":
                listFiles()
                break
            case "cd":
                moverse(comandoSeccionado[1])
                break
            default:
                matrixTerminal.print('"' + comando + '" no es un comando reconocido...')
                break;
        }
        inputCommandTerminal()

        //Proceso de recibir comandos
        //Comunicar con Python para abrir archivos y operarlos
        //Interpretar y operar en base a comandos, OWR archivos del usuario
    })
}

function moverse(nombre_del_archivo) {
    //parametros_a_enviar = "comando=createf&nombreArchivo=" + nombre_del_archivo;
    parametros_a_enviar = "comando_a_enviar=cd-" + nombre_del_archivo;
    send_request_to_python(parametros_a_enviar);
}

//Creara un archivo
function createf(nombre_del_archivo) {
    matrixTerminal.print("creating " + nombre_del_archivo + "...")
    //parametros_a_enviar = "comando=createf&nombreArchivo=" + nombre_del_archivo;
    parametros_a_enviar = "comando_a_enviar=createf-" + nombre_del_archivo;
    send_request_to_python(parametros_a_enviar);
}
//Creara un directorio
function crearDirectorio(nombre_del_archivo) {
    matrixTerminal.print("creating " + nombre_del_archivo + "...")
    //parametros_a_enviar = "comando=createf&nombreArchivo=" + nombre_del_archivo;
    parametros_a_enviar = "comando_a_enviar=createdir-" + nombre_del_archivo;
    send_request_to_python(parametros_a_enviar);
}
//Copiara un archivo
function copyFile(nombre_del_archivo) {
    matrixTerminal.print("copying " + nombre_del_archivo + "...")
    //parametros_a_enviar = "comando=createf&nombreArchivo=" + nombre_del_archivo;
    parametros_a_enviar = "comando_a_enviar=copy-" + nombre_del_archivo;
    send_request_to_python(parametros_a_enviar);
}

//Renombrara un archivo
function renameFile(nombre_del_archivo_viejo, nombre_del_archivo_nuevo) {
    matrixTerminal.print("renaming file " + nombre_del_archivo_viejo + " to " + nombre_del_archivo_nuevo)
    //parametros_a_enviar = "comando=createf&nombreArchivo=" + nombre_del_archivo;
    parametros_a_enviar = "comando_a_enviar=rename-" + nombre_del_archivo_viejo + "-" + nombre_del_archivo_nuevo;
    send_request_to_python(parametros_a_enviar);
}

//Renombrara un directorio
function renameDir(nombre_del_archivo_viejo, nombre_del_archivo_nuevo) {
    matrixTerminal.print("renaming directory " + nombre_del_archivo_viejo + " to " + nombre_del_archivo_nuevo)
    //parametros_a_enviar = "comando=createf&nombreArchivo=" + nombre_del_archivo;
    parametros_a_enviar = "comando_a_enviar=renamedir-" + nombre_del_archivo_viejo + "-" + nombre_del_archivo_nuevo;
    send_request_to_python(parametros_a_enviar);
}

//Abrira y escribira el contenido de un archivo
function edit(nombre_del_archivo, texto_a_agregar) {
    matrixTerminal.print("openning " + nombre_del_archivo + " for edition...")
    //matrixTerminal.input("Input the new text: ", function (texto_a_agregar) {
    parametros_a_enviar = "comando_a_enviar=edit-" + nombre_del_archivo + "-" + texto_a_agregar;
    send_request_to_python(parametros_a_enviar);
}

//Eliminara un archivo
function deleteFile(nombre_del_archivo) {
    matrixTerminal.print("deleting file:" + nombre_del_archivo)
    parametros_a_enviar = "comando_a_enviar=delete-" + nombre_del_archivo;
    send_request_to_python(parametros_a_enviar);
}
//Eliminara un directorio
function deleteDir(nombre_del_archivo) {
    matrixTerminal.print("deleting directory " + nombre_del_archivo)
    parametros_a_enviar = "comando_a_enviar=deletedir-" + nombre_del_archivo;
    send_request_to_python(parametros_a_enviar);
}

function readFile(nombre_del_archivo) {
    matrixTerminal.print("openning " + nombre_del_archivo + " for reading...")

    let info_to_send = {
        "comando": "read",
        "nombre": nombre_del_archivo
    }

    $.ajax({
        type: "POST",
        url: "/dataManager",
        contentType: "application/json;charser=utf-8",
        data: JSON.stringify(info_to_send),
        dataType: "JSON",
        success: function (contenido_archivo) {
            console.log(contenido_archivo)

            let countKey = Object.keys(contenido_archivo).length, i;
            for (i = 0; i < countKey; i++) {
                matrixTerminal.print(contenido_archivo[i])
            }
        }
    })
}


//Imprimir todos los nombre y pesos de los archivos que tenemos en el directorio en el que nos encotramos
function listFiles() {
    matrixTerminal.print("searching for files ...")

    let info_to_send = {
        "comando": "list"
    }

    $.ajax({
        type: "POST",
        url: "/dataManager",
        contentType: "application/json;charser=utf-8",
        data: JSON.stringify(info_to_send),
        dataType: "JSON",
        success: function (contenido_archivo) {
            console.log(contenido_archivo)
            matrixTerminal.print("Files found: ")

            let inodo_del_archivo = Object.keys(contenido_archivo)
            let nombre_del_archivo = Object.values(contenido_archivo)

            for (i = 0; i < nombre_del_archivo.length; i++) {
                matrixTerminal.print(">> " + inodo_del_archivo[i] + "\t" + nombre_del_archivo[i])
            }
        }
    })
}

//Envia solicitudes http a la terminal
function send_request_to_python(parametros_a_enviar) {
    let url = "/terminal";
    let params = parametros_a_enviar;
    let http = new XMLHttpRequest();
    http.open("GET", url + "?" + params, true);
    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
            //alert(http.responseText);
        }
    }
    http.send();
}

//Limpieza de terminal
function clearTerminal() {
    matrixTerminal.clear()
}

//Inicializacion de terminal
function defineTerminal() {
    matrixTerminal.setHeight("200px")
    matrixTerminal.setWidth('1200px')
    matrixTerminal.setTextColor("#00FF41")
}
