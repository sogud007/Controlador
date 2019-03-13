import requests

def getCuentasCobro(unidad_privada_id):
    url = "http://127.0.0.1:8000/CuentaCobro/api/"
    response = requests.get(url)
    cuentas = response.json()
    cuentas_usuario = []    
    for cuenta in cuentas:
        id_unidad = extractId(cuenta['UNIDAD_PRIVADA']['UNIDAD_PRIVADA_ID'])
        if(id_unidad == unidad_privada_id):
            cuenta['PERIODO_COBRO']['FECHA_INICIAL'] = cambioFecha(cuenta['PERIODO_COBRO']['FECHA_INICIAL'])
            cuenta['PERIODO_COBRO']['FECHA_FINAL'] = cambioFecha(cuenta['PERIODO_COBRO']['FECHA_FINAL'])
            cuentas_usuario.append(cuenta)
    return cuentas_usuario

def cambioFecha(valor):
    start = 0
    end = valor.find('T', start)
    return valor[start:end]

def getNoticias(propiedad_id):
    url = "http://127.0.0.1:8000/Noticia/api/"
    response = requests.get(url)
    noticias = response.json()
    noticias_usuario = []
    for noti in noticias:
        id_prop = extractId(noti['PROPIEDAD_ID'])
        if(id_prop == propiedad_id):
            noticias_usuario.append(noti)
    return noticias_usuario

def getPropiedadHorizontal(propiedad_id):
    url = "http://127.0.0.1:8000/PropiedadHorizontal/api/"
    response = requests.get(url)
    propiedades = response.json()
    propiedad = {}
    for p in propiedades:
        if (p['id'] == propiedad_id):
            propiedad = p
    return propiedad

def extractId(elemento):
    start = elemento.find('ObjectId(') + 10
    end = elemento.find('))>', start) - 1
    return elemento[start:end]     