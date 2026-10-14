"""Valida outputs reais; não importa SciPy e não gera métricas substitutas."""
from pathlib import Path
import json
import math
import csv
import hashlib
import xml.etree.ElementTree as ET
import nbformat

ROOT=Path(__file__).resolve().parents[1]

def verify(root=ROOT):
    nb=nbformat.read(root/'notebooks/TP3/security/01_regressao_e_transicao.ipynb',as_version=4)
    nbformat.validate(nb)
    code=[c for c in nb.cells if c.cell_type=='code']
    assert code and [c.execution_count for c in code]==list(range(1,len(code)+1)), 'Notebook incompleto'
    assert not any(o.output_type=='error' for c in code for o in c.outputs), 'Notebook com erro'
    images=sum('image/png' in o.get('data',{}) for c in code for o in c.outputs)
    assert images>=3, 'Faltam gráficos incorporados'
    out=root/'reports/TP3/regression'
    protocol=json.loads((out/'protocol.json').read_text(encoding='utf-8'))
    digest=hashlib.sha256((root/'data/processed/security/phishing_nlp_dataset.csv').read_bytes()).hexdigest()
    assert protocol['dataset_sha256']==digest
    assert protocol['train_n']+protocol['evaluation_n']==603
    with (out/'metrics.csv').open(encoding='utf-8',newline='') as f:metrics=list(csv.DictReader(f))
    expected={(model,part) for model in ['media_treino','linear_simples','linear_multipla'] for part in ['treino','avaliacao']}
    assert len(metrics)==6 and {(r['modelo'],r['particao']) for r in metrics}==expected
    for row in metrics:
        assert math.isfinite(float(row['r2']))
        assert math.isfinite(float(row['rmse_caracteres'])) and float(row['rmse_caracteres'])>=0
    with (out/'split_manifest.csv').open(encoding='utf-8',newline='') as f:split=list(csv.DictReader(f))
    assert len(split)==603 and len({r['text_sha256'] for r in split})==603
    assert sum(r['particao']=='treino' for r in split)==protocol['train_n']
    for name in ['observado_previsto','residuos','qq']:
        assert (root/f'reports/TP3/figures/{name}.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    suites=ET.parse(root/'reports/TP3/ci/pytest.xml').getroot()
    cases=suites.findall('.//testcase')
    assert cases and not suites.findall('.//failure') and not suites.findall('.//error')
    own=[c for c in cases if 'test_tp3_regression' in c.attrib.get('classname','')]
    assert len(own)==4 and not any(c.find('skipped') is not None for c in own)
    result={'status':'evidencias_automaticas_validadas_revisao_humana_pendente',
            'code_cells':len(code),'embedded_images':images,'test_cases':len(cases),
            'tp3_test_cases':len(own),'dataset_sha256':digest}
    (root/'reports/TP3/ci/validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':verify()
