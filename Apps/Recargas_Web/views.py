from django.shortcuts import render
import pandas as pd
from .models import Calimaco, GestionRW, Skype, TicketsPagadosDeTienda
from django.http import JsonResponse

def index(request):
    return render(request, "index.html")

def menu(request):
    return render(request, "menu.html")

def cargar_calimaco(request):
    return render(request, "cargar_calimaco.html")

def cargar_skype(request):
    return render(request, "cargar_skype.html")

def cargar_tickets(request):
    return render(request, "cargar_tickets.html")

def handle_uploaded_file(file, file_type):
    if file_type == 'csv':
        df = pd.read_csv(file)
    elif file_type == 'xlsx' or file_type == 'xls':
        df = pd.read_excel(file)
    else:
        raise ValueError("Tipo de archivo no soportado")

    df.columns = df.columns.str.strip().str.lower()

    return df

def cargar_archivo(request):
    try:
        if request.method == "POST":
            archivo_csv = request.FILES.get("archivo_csv")
            if not archivo_csv:
                return JsonResponse({
                    "status_server": "error",
                    "message": "No se ha subido ningún archivo.",
                })

            try:
                file_type = archivo_csv.name.split('.')[-1]
                df = handle_uploaded_file(archivo_csv, file_type)

                print(f"Archivo cargado correctamente: {archivo_csv.name}")

                # Normalizar los nombres de las columnas (eliminar espacios, convertir a minúsculas)
                df.columns = df.columns.str.strip().str.lower()

                # Diccionario para mapear nombres esperados a sus equivalentes normalizados
                column_mapping = {
                    "identifer_cal": "identifer_cal",
                    "fecha": "fecha",
                    "estado": "estado",
                    "fecha_de_modificacion": "fecha_de_modificacion",
                    "usuario": "usuario",
                    "email": "email",
                    "cantidad": "cantidad",
                    "id_externo": "id_externo",
                    "metodo": "metodo",
                    "respuesta": "respuesta",
                    "agente": "agente",
                    "fecha_de_registro_del_jugador": "fecha_de_registro_del_jugador",
                }

                # Verifica que las columnas requeridas existen en el archivo
                for key, normalized_name in column_mapping.items():
                    if normalized_name not in df.columns:
                        print(f"Falta la columna: {key}")
                        return JsonResponse({
                            "status_server": "error",
                            "message": f"El archivo no tiene la columna {key}.",
                        })

                for _, row in df.iterrows():
                    try:
                        Calimaco.objects.update_or_create(
                            identifer_cal=row[column_mapping["identifer_cal"]],
                            fecha=row[column_mapping["fecha"]],
                            estado=row[column_mapping["estado"]],
                            fecha_de_modificacion=row[column_mapping["fecha_de_modificacion"]],
                            usuario=row[column_mapping["usuario"]],
                            email=row[column_mapping["email"]],
                            cantidad=row[column_mapping["cantidad"]],
                            id_externo=row[column_mapping["id_externo"]],
                            metodo=row[column_mapping["metodo"]],
                            respuesta=row[column_mapping["respuesta"]],
                            agente=row[column_mapping["agente"]],
                            fecha_de_registro_del_jugador=row[column_mapping["fecha_de_registro_del_jugador"]],
                        )
                    except Exception as e:
                        print(f"Error procesando la fila: {row} - {str(e)}")
                        return JsonResponse({
                            "status_server": "error",
                            "message": f"Error procesando los datos del archivo: {str(e)}",
                        })

                return JsonResponse({
                    "status_server": "success",
                    "message": "Felicitaciones, la data fue importada correctamente 😉",
                })

            except Exception as e:
                print(f"Error al leer el archivo: {str(e)}")
                return JsonResponse({
                    "status_server": "error",
                    "message": f"Error al leer el archivo: {str(e)}",
                })

        else:
            return render(request, "cargar_calimaco.html")

    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        return JsonResponse({
            "status_server": "error",
            "message": f"Error interno del servidor: {str(e)}",
        })

def cargar_archivo_gestionrw(request):
    try:
        if request.method == "POST":
            archivo = request.FILES.get("archivo")
            if not archivo:
                return JsonResponse({
                    "status_server": "error",
                    "message": "No se ha subido ningún archivo.",
                })

            try:
                file_type = archivo.name.split('.')[-1]
                df = handle_uploaded_file(archivo, file_type)

                print(f"Archivo cargado correctamente: {archivo.name}")

                # Imprimir los nombres de las columnas antes de normalizarlas
                print(f"Columnas del archivo antes de normalizar: {list(df.columns)}")

                # Normalizar los nombres de las columnas (eliminar espacios, convertir a minúsculas)
                df.columns = df.columns.str.strip().str.lower()

                # Imprimir los nombres de las columnas después de normalizarlas
                print(f"Columnas del archivo después de normalizar: {list(df.columns)}")

            except Exception as e:
                print(f"Error al leer el archivo: {str(e)}")
                return JsonResponse({
                    "status_server": "error",
                    "message": f"Error al leer el archivo: {str(e)}",
                })

            # Diccionario para mapear nombres esperados a sus equivalentes normalizados
            column_mapping = {
                "identifier": "identifier",
                "local": "local",
                "registro": "registro",
                "tipo": "tipo",
                "proveedor": "proveedor",
                "bono": "bono",
                "telefono": "telefono",
                "tipo_documento": "tipo_documento",
                "numero_documento": "numero_documento",
                "web_id": "web_id",
                "cliente": "cliente",
                "recarga": "recarga",
                "bono_5_por_ciento": "bono_5_por_ciento",
                "promotor": "promotor",
            }

            # Verifica que las columnas requeridas existen en el archivo
            for key, normalized_name in column_mapping.items():
                if normalized_name not in df.columns:
                    print(f"Falta la columna: {key}")
                    return JsonResponse({
                        "status_server": "error",
                        "message": f"El archivo no tiene la columna {key}.",
                    })

            for _, row in df.iterrows():
                try:
                    GestionRW.objects.update_or_create(
                        identifier=row[column_mapping["identifier"]],
                        local=row[column_mapping["local"]],
                        registro=row[column_mapping["registro"]],
                        tipo=row[column_mapping["tipo"]],
                        proveedor=row[column_mapping["proveedor"]],
                        bono=row[column_mapping["bono"]],
                        telefono=row[column_mapping["telefono"]],
                        tipo_documento=row[column_mapping["tipo_documento"]],
                        numero_documento=row[column_mapping["numero_documento"]],
                        web_id=row[column_mapping["web_id"]],
                        cliente=row[column_mapping["cliente"]],
                        recarga=row[column_mapping["recarga"]],
                        bono_5_por_ciento=row[column_mapping["bono_5_por_ciento"]],
                        promotor=row[column_mapping["promotor"]],
                    )
                except Exception as e:
                    print(f"Error procesando la fila: {row} - {str(e)}")
                    return JsonResponse({
                        "status_server": "error",
                        "message": f"Error procesando los datos del archivo: {str(e)}",
                    })

            return JsonResponse({
                "status_server": "success",
                "message": "Felicitaciones, la data fue importada correctamente.",
            })

        else:
            return render(request, "cargar_gestionrw.html")

    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        return JsonResponse({
            "status_server": "error",
            "message": f"Error interno del servidor: {str(e)}",
        })

def cargar_db_skype(request):
    try:
        if request.method == 'POST':
            archivo = request.FILES.get('file_skype')
            if not archivo:
                return JsonResponse({
                    "status_server": "error",
                    "message": "No se ha subido ningún archivo.",
                })

            try:
                file_type = archivo.name.split('.')[-1]
                df = handle_uploaded_file(archivo, file_type)

                print(f"Archivo cargado correctamente: {archivo.name}")

                # Imprimir los nombres de las columnas antes de normalizarlas
                print(f"Columnas del archivo antes de normalizar: {list(df.columns)}")

                # Normalizar los nombres de las columnas (eliminar espacios, convertir a minúsculas)
                df.columns = df.columns.str.strip().str.lower()

                # Imprimir los nombres de las columnas después de normalizarlas
                print(f"Columnas del archivo después de normalizar: {list(df.columns)}")

            except Exception as e:
                print(f"Error al leer el archivo: {str(e)}")
                return JsonResponse({
                    "status_server": "error",
                    "message": f"Error al leer el archivo: {str(e)}",
                })

            # Diccionario para mapear nombres esperados a sus equivalentes normalizados
            column_mapping = {
                "conversationid": "conversationid",
                "from": "from",
                "to": "to",
                "startdate": "startdate",
                "duration": "duration",
                "starttime": "starttime",
                "endtime": "endtime",
                "type": "type",
                "result": "result",
                "failure_reason": "failure_reason",
                "resolution": "resolution",
            }

            # Verifica que las columnas requeridas existen en el archivo
            for key, normalized_name in column_mapping.items():
                if normalized_name not in df.columns:
                    print(f"Falta la columna: {key}")
                    return JsonResponse({
                        "status_server": "error",
                        "message": f"El archivo no tiene la columna {key}.",
                    })

            for _, row in df.iterrows():
                try:
                    Skype.objects.update_or_create(
                        conversationid=row[column_mapping["conversationid"]],
                        from_person=row[column_mapping["from"]],
                        to_person=row[column_mapping["to"]],
                        startdate=row[column_mapping["startdate"]],
                        duration=row[column_mapping["duration"]],
                        starttime=row[column_mapping["starttime"]],
                        endtime=row[column_mapping["endtime"]],
                        type=row[column_mapping["type"]],
                        result=row[column_mapping["result"]],
                        failure_reason=row[column_mapping["failure_reason"]],
                        resolution=row[column_mapping["resolution"]],
                    )
                except Exception as e:
                    print(f"Error procesando la fila: {row} - {str(e)}")
                    return JsonResponse({
                        "status_server": "error",
                        "message": f"Error procesando los datos del archivo: {str(e)}",
                    })

            return JsonResponse({
                "status_server": "success",
                "message": "Los datos han sido cargados exitosamente.",
            })

        else:
            return render(request, 'cargar_skype.html')

    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        return JsonResponse({
            "status_server": "error",
            "message": f"Error interno del servidor: {str(e)}",
        })

def cargar_tickets_pagados_de_tienda(request):
    try:
        if request.method == "POST":
            archivo = request.FILES.get("archivo")
            if not archivo:
                return JsonResponse({
                    "status_server": "error",
                    "message": "No se ha subido ningún archivo.",
                })

            try:
                file_type = archivo.name.split('.')[-1]
                df = handle_uploaded_file(archivo, file_type)

                print(f"Archivo cargado correctamente: {archivo.name}")

                # Imprimir los nombres de las columnas antes de normalizarlas
                print(f"Columnas del archivo antes de normalizar: {list(df.columns)}")

                # Normalizar los nombres de las columnas (eliminar espacios, convertir a minúsculas)
                df.columns = df.columns.str.strip().str.lower()

                # Imprimir los nombres de las columnas después de normalizarlas
                print(f"Columnas del archivo después de normalizar: {list(df.columns)}")

            except Exception as e:
                print(f"Error al leer el archivo: {str(e)}")
                return JsonResponse({
                    "status_server": "error",
                    "message": f"Error al leer el archivo: {str(e)}",
                })

            # Diccionario para mapear nombres esperados a sus equivalentes normalizados
            column_mapping = {
                "order_id": "order_id",
                "product_id": "product_id",
                "customer_email": "customer_email",
                "customer_id": "customer_id",
                "product_name": "product_name",
                "total": "total",
                "currency": "currency",
                "order_date": "order_date",
                "payment_method": "payment_method",
                "status": "status",
            }

            # Verifica que las columnas requeridas existen en el archivo
            for key, normalized_name in column_mapping.items():
                if normalized_name not in df.columns:
                    print(f"Falta la columna: {key}")
                    return JsonResponse({
                        "status_server": "error",
                        "message": f"El archivo no tiene la columna {key}.",
                    })

            for _, row in df.iterrows():
                try:
                    TicketsPagadosDeTienda.objects.update_or_create(
                        order_id=row[column_mapping["order_id"]],
                        product_id=row[column_mapping["product_id"]],
                        customer_email=row[column_mapping["customer_email"]],
                        customer_id=row[column_mapping["customer_id"]],
                        product_name=row[column_mapping["product_name"]],
                        total=row[column_mapping["total"]],
                        currency=row[column_mapping["currency"]],
                        order_date=row[column_mapping["order_date"]],
                        payment_method=row[column_mapping["payment_method"]],
                        status=row[column_mapping["status"]],
                    )
                except Exception as e:
                    print(f"Error procesando la fila: {row} - {str(e)}")
                    return JsonResponse({
                        "status_server": "error",
                        "message": f"Error procesando los datos del archivo: {str(e)}",
                    })

            return JsonResponse({
                "status_server": "success",
                "message": "Los datos han sido cargados exitosamente.",
            })

        else:
            return render(request, "cargar_tickets.html")

    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        return JsonResponse({
            "status_server": "error",
            "message": f"Error interno del servidor: {str(e)}",
        })
