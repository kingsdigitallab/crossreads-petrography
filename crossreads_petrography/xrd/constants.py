from ..constants import *

PATH_XRD_INPUT_DATA = PATH_INPUT_DATA / 'XRD'
PATH_XRD_INPUT_COLAB = '/content/drive/MyDrive/Crossreads B D1/XRD input data'
COLS_TO_IGNORE = {'Rwp', 'Rexp', 'Chi2', 'GOF'}

XRD_PARAM_MAPPING = {
    'Qcalcite': 'XRD calcite content (%)',
    'QMgCalcite': 'XRD magnesian calcite content (%)',
    'Qdolomite': 'XRD dolomite content (%)',
    # ... (include all mappings from the original code)
    '*': 'XRD other minerals'
}

CLAY_MINERALS = ['XRD kaolinite content (%)', 'XRD smectite content (%)', 'XRD chlorite content (%)', 'XRD glauconite content (%)']
K_FELDSPAR = ['XRD orthoclase content (%)', 'XRD microcline content (%)', 'XRD K-sanidine content (%)', 'XRD anorthoclase content (%)']
PLAGIOCLASE = ['XRD albite content (%)', 'XRD oligoclase content (%)', 'XRD andesine content (%)', 'XRD labradorite content (%)', 'XRD bytownite content (%)', 'XRD anorthite content (%)']