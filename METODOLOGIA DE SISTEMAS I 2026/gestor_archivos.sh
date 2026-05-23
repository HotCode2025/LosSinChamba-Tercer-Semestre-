
while true; do
    echo "Seleccione una opción:"
    echo "1) Crear un nuevo archivo"
    echo "2) Eliminar un archivo"
    echo "3) Listar archivos en el directorio actual"
    echo "4) Mostrar información de un archivo"
    echo "5) Salir" 
    read opcion

    case $opcion in 
        1) 
            echo "Ingrese el nombre del archivo a crear:"
            read filename
            touch "$filename"
            echo "Archivo '$filename' creado."
            ;;
        2) 
            echo "Ingrese el nombre del archivo a eliminar:"
            read filename
            if [ -f "$filename" ]; then
                rm "$filename"
                echo "Archivo '$filename' eliminado."
            else
                echo "Archivo '$filename' no encontrado."
            fi
            ;;
        3) 
            echo "Mostrando archivos en el directorio actual:"
            ls -l
            ;;
        4) 
            echo "Ingrese el nombre del archivo a mostrar:"
            read filename
            if [ -f "$filename" ]; then
                ls -lh "$filename"
                else
                echo "Archivo '$filename' no encontrado."
            fi
            ;;  
        5) 
            echo "Saliendo..."
            exit 0
            ;;
        *) 
            echo "Opción no válida. Por favor, seleccione una opción del 1 al 5."
            ;;      
    esac
done