###########################################
# main.py
#   script principal del curso BigData 
###########################################

import numpy as np
import pandas as pd
import os
import logging

from pathlib import Path
from tqdm import tqdm

#========================================================================
# Main
#========================================================================
def main():
    """Main function for ETL
    """
    logger = logging.getLogger('main')
    logger.info("Iniciando ETL para llamadas 123!!!")

    try:
        generate_unique_values_report(filename="llamadas123_julio_2022.csv")
    except Exception as e:
        logger.info("Error generando el reporte")
        logger.info(e)

    logger.info("DONE!!!")

#========================================================================
# generate_unique_values_report
#========================================================================
def generate_unique_values_report(filename):
    """Genera una tabla con el resumen de los valores unicos por cada columna
    en el archivo dado (filename)

    Args:
        filename (str): nombre del archivo para generar el reporte
    """
    logger = logging.getLogger('generate_unique_values_report')

    # Read data
    data = get_data(file=filename, dir="raw")
    lista_columnas = list(data.columns)

    # loop para llenar el dictionario con los valores unicos
    dict_valores = dict()
    logger.info("Creating report")
    for elem in tqdm(lista_columnas):
        dict_valores[elem] = len(data[elem].unique())
    
    # Crea una tabla (pandas.dataframe) desde un dictionario
    df_sum = pd.DataFrame.from_dict(dict_valores, orient="index")
    df_sum = df_sum.rename({0:"Count"}, axis=1)                    # renombra la columna 0 con Count

    # Guardar la tabla en el directorio output
    outname = "report_unique_values_" + filename 
    save_data(data=data, dir='processed', out_name=outname)

#========================================================================
# save_data
#========================================================================
def save_data(data, dir, out_name):
    """Guarda un archivo csv, de la tabla data en el diretorio y nombre 
    indicado

    Args:
        data (pandas.dataframe): Datos a guardar
        dir (str): nombre del directorio donde almacenar los datos
        out_name (str): nombre del archivo a guardar
    """
    logger = logging.getLogger('save_data')

    # obtener la ruta para guardar el archivo
    filepath = os.path.join(project_dir, "data", dir, out_name)

    logger.info("Saving {}".format(filepath))

    # grabar el archivo CSV
    data.to_csv(filepath, index=False)


#========================================================================
# get_data
#========================================================================
def get_data(file, dir):
    """Lee el archivo indicado, retorna un dataframe de pandas con los datos

    Args:
        file (str): nombre del archivo de entrada
        dir (str): nombre del directorio donde se encuentran los datos

    Returns:
        pandas.dataframe: dataframe con los datos
    """
    logger = logging.getLogger('get_data')

    # get full path where file is located
    filepath = os.path.join(project_dir, "data", dir, file)
    
    # read data
    data = pd.read_csv(filepath, sep=";", encoding="latin-1")

    logger.info("File: {} table shape:{}".format(file, data.shape) )
    return data





if __name__ == '__main__':
    # Basic configuration for logging (time - function name - level logs - message)
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.captureWarnings(True)
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    project_dir = Path(".").resolve()

    main()