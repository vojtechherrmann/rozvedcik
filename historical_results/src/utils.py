import re
from typing import Union, List

import pandas as pd
from pandas import Series as PDS, DataFrame as PDF


def convert_series_to_int(s: PDS) -> PDS:
    new_s = PDS([None]*len(s), index=s.index).astype(object)
    new_s[~pd.isnull(s)] = s[~pd.isnull(s)].astype("Int64")
    return new_s


def convert_pdf_to_int(pdf: PDF, cols_rgx: Union[str, List[str]]) -> PDF:
    if isinstance(cols_rgx, str):
        cols_rgx = [cols_rgx]
    pdf_out = pdf.copy()
    for c in pdf_out.columns:
        if any([re.match(pattern=one_cols_rgx, string=c) for one_cols_rgx in cols_rgx]):
            pdf_out[c] = convert_series_to_int(pdf_out[c])
    return pdf_out
