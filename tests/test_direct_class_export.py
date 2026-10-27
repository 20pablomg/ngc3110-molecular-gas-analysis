from pathlib import Path
from src.convert_to_jy import convert_pair


def test_export_without_independent_moment(tmp_path):
    fit = tmp_path / 'fit.dat'
    moment = tmp_path / 'moment.dat'
    out = tmp_path / 'out.dat'
    fit.write_text('fuente linea I_fit err_I\nNGC3110_SOU HNC 1.2 0.1\n')
    moment.write_text('fuente linea I_manual SigmaI\nNGC3110_SOU HNC 1.1 0.2\n')
    table = convert_pair(fit, moment, out)
    assert 'I_moment_Jy' not in table.columns
    assert out.exists()
