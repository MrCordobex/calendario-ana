import os
import random
import uuid

def renombrar_fotos_aleatorio():
    # 1. Pedimos la carpeta al usuario
    ruta = input("Introduce la ruta de la carpeta donde están las fotos (ej: Fotos/01_Enero): ")
    
    # Limpiamos comillas por si has copiado la ruta como "ruta"
    ruta = ruta.strip('"').strip("'")

    if not os.path.exists(ruta):
        print("❌ Error: Esa carpeta no existe.")
        return

    # Extensiones permitidas (incluimos HEIC por si acaso)
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.heic', '.webp')
    
    # Obtenemos todos los archivos que sean imágenes
    archivos = [f for f in os.listdir(ruta) if f.lower().endswith(extensiones_validas)]
    
    if not archivos:
        print("⚠️ No he encontrado imágenes en esa carpeta.")
        return

    print(f"📸 Encontradas {len(archivos)} fotos. Procesando...")

    # 2. Barajamos la lista aleatoriamente
    random.shuffle(archivos)

    # 3. PASO DE SEGURIDAD: Renombramos todo a nombres temporales únicos
    # Esto evita conflictos si ya existen archivos llamados "1.jpg"
    temp_map = []
    for archivo in archivos:
        extension = os.path.splitext(archivo)[1] # Sacamos la extensión (.jpg)
        nombre_temp = f"temp_{uuid.uuid4()}{extension}"
        
        ruta_vieja = os.path.join(ruta, archivo)
        ruta_temp = os.path.join(ruta, nombre_temp)
        
        os.rename(ruta_vieja, ruta_temp)
        temp_map.append(ruta_temp)

    # 4. Renombramos los temporales a números (1, 2, 3...)
    contador = 1
    for ruta_temp in temp_map:
        # Recuperamos la extensión del archivo temporal
        extension = os.path.splitext(ruta_temp)[1]
        
        # Nuevo nombre: 1.jpg, 2.jpg...
        nuevo_nombre = f"{contador}{extension}"
        ruta_final = os.path.join(ruta, nuevo_nombre)
        
        os.rename(ruta_temp, ruta_final)
        print(f"✅ Foto asignada al día {contador}: {nuevo_nombre}")
        
        contador += 1

    print("\n🎉 ¡Listo! Todas las fotos han sido aleatorizadas y numeradas.")

if __name__ == "__main__":
    renombrar_fotos_aleatorio()