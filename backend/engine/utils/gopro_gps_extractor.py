# coding=utf-8

"""Lê e exporta para CVS os dados de GoPro contidos no stream GPMF de um container MP4.

Como instalar requisitos de pacotes Python
-------------------------------------------

É necessário instalar os requisitos com ``--no-deps`` devido a que o requisito ``rambo/python-gpmf`` faz uso de uma
versão muito antiga de harchoir com o nome "harchoir3" que não existe mais no repositório pip.

::
    pip install --no-deps -r requirements.txt


Como usar
---------

::
    python3 gopro-gps-extractor samples/hero6.mp4


Referências
-----------

* https://gopro.github.io/gpmf-parser/
* https://github.com/gopro/gpmf-parser
* https://sno.phy.queensu.ca/~phil/exiftool/TagNames/GoPro.html
* https://github.com/juanmcasillas/gopro2gpx
"""
# - *- coding: utf- 8 - *
import sys
import os
import csv
import numpy as np
from datetime import datetime
from utils.gpmf import extract, parse
from construct import GreedyRange

def gpmfDataAsKeyValueList(data):
    """Converte os dados GPMF crus em uma lista de tuplas (chave, valor), onde o valor pode ser ou um literal de tipo
    básico ou uma outra lista de tuplas chave-valor recursivamente.

    São usadas listas de tuplas com chave-valor em lugar de um dicionario, devido a que é comum existirem mais de um
    valor com a mesma chave, como é o caso dos sub-streams de dados de sensores, todos com dados diferente mas usando
    a mesma chave ``STRM``.
    """
    result = []
    elements = GreedyRange(parse.FOURCC).parse(data)
    for element in elements:
        if element.type == 0:  # elemento do tipo zero indica uma sub-lista
            elementValue = gpmfDataAsKeyValueList(element.data)
        else:
            try:
                elementValue = parse.parse_value(element)
            except ValueError:
                elementValue = element.data
        result.append((element.key, elementValue))
    return result


def getFirstOrDefault(collection, default=None):
    """Função auxiliar que retona o primeiro elemento de uma coleção ou, caso a coleção esteja vazia, um valor
    default será retornado"""
    return next(iter(collection), default)


def getValues(keyValuePairs, key):
    """Retorna todos os valores das tuplas com chave ``key``."""
    for (k, v) in keyValuePairs:
        if key == k:
            yield v


def getValue(keyValuePairs, key):
    """Retorna o primeiro valor da tupla com chave ``key``."""
    return next(iter(getValues(keyValuePairs, key)), None)


def list_devices(gpmfData):
    """Enumera as tuplas (id, nome) dos dispositivos presentes nos dados GPMF."""
    for (k, v) in gpmfData:
        if k == b'DEVC':
            yield (getValue(v, b'DVID'), getValue(v, b'DVNM'))


def getDeviceStreams(gpmfData, deviceId):
    """Enumera os sub-streams de dados de sensores contidos nos dados GPMF para o dispositivo ``deviceId``, retornando
    os dados do sensor como um dicionário."""
    for device_data in getValues(gpmfData, b'DEVC'):
        if getValue(device_data, b'DVID') == deviceId:
            for stream in getValues(device_data, b'STRM'):
                yield {i: j for i, j in stream}  # converte os dados do sub-stream de lista de tuplas para um dicionário


def getStreamData(stream, scaling):
    """Obtem os valores de um sub-stream de dados de sensor, aplicando scaling e fazendo a média dos mesmos, se for
    necessário."""
    data = np.array(stream)
    return data * scaling


def formatDateTime(timestamp):
    timestamp = timestamp.split("T")
    return "{0} {1}".format(timestamp[0], timestamp[1][:8])


def extractGpsData(filename):
    """Extrai os dados de GPS contidos no stream GPMF de um arquivo MP4."""

    try:
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")

        resultContent = []

        gpmfGpsDataKey = b'GPS5'
        payloads, _ = extract.get_gpmf_payloads_from_file(filename)
        for payload, timestamps in payloads:
            gpmfData = gpmfDataAsKeyValueList(payload)
            firstDevice = getFirstOrDefault(list_devices(gpmfData))
            streams = list(getDeviceStreams(gpmfData, firstDevice[0]))
            for gpsStream in streams:
                if not gpsStream:
                    continue
                if gpmfGpsDataKey in gpsStream.keys():
                    scaling = 1.0 / np.array(gpsStream.get(b'SCAL', 1.0))
                    for gps in gpsStream[gpmfGpsDataKey]:
                        gpsData = getStreamData(gps, scaling)
                        data = {
                            "datetime": formatDateTime(gpsStream.get(b'GPSU', -1).isoformat()),
                            "latitude": gpsData[0],
                            "longitude": gpsData[1],
                            "speed": gpsData[3],
                        }
                        resultContent.append(data)
        return resultContent
    except Exception as ex:
        raise ex
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def exportGpsData(filename):
    """Exporta no formato CSV os dados de GPS contidos no stream GPMF de um arquivo MP4."""
    dataContent = extractGpsData(filename)
    dataHeader = ["datetime", "latitude", "longitude", "speed"]
    with open(filename.replace(".MP4", ".csv"), 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=dataHeader)

        writer.writeheader()
        writer.writerows(dataContent)
    csvFile.close()

if __name__ == '__main__':
    exportGpsData(sys.argv[1])
