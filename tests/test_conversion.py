from pathlib import Path
import importlib.util
import pandas as pd
import pytest

SPEC = importlib.util.spec_from_file_location("converter", Path(__file__).parents[1] / "src" / "convert_to_jy.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_matches_rows_by_source_not_position(tmp_path):
    fit = pd.DataFrame({"fuente":["N","S"], "linea":["HCN","HCN"], "I_fit":[1.,2.], "err_I":[.1,.2]})
    mom = pd.DataFrame({"fuente":["S","N"], "linea":["HCN","HCN"], "I_manual":[20.,10.], "SigmaI":[2.,1.], "I_moment":[21.,11.]})
    a,b,out=(tmp_path/x for x in ["fit.dat","mom.dat","out.dat"])
    fit.to_csv(a,sep="\t",index=False);mom.to_csv(b,sep="\t",index=False)
    result=module.convert_pair(a,b,out)
    n=result.set_index("fuente").loc["N"]
    assert n["I_manual_Jy"] == round(10*module.DENSE,4)
    assert out.exists()


def test_rejects_unmatched_rows(tmp_path):
    fit=pd.DataFrame({"fuente":["N"],"linea":["HCN"],"I_fit":[1],"err_I":[.1]})
    mom=pd.DataFrame({"fuente":["S"],"linea":["HCN"],"I_manual":[2],"SigmaI":[.1],"I_moment":[2]})
    a,b,out=(tmp_path/x for x in ["a.dat","b.dat","c.dat"])
    fit.to_csv(a,sep="\t",index=False);mom.to_csv(b,sep="\t",index=False)
    with pytest.raises(ValueError,match="unmatched"):
        module.convert_pair(a,b,out)
