import pandas as pd

import numpy as np

from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests


def ttest_all_rows(df1, df2):
    """
    Perform a t-test across every row of the dataframes of two independent
    samples.
    :param df1: Dataframe 1, with the same rows as dataframe 2
    :param df2: Dataframe 2, with the same rows as dataframe 1
    :return: Dataframe of p values for each row
    """

    df_pval = pd.DataFrame(index=df1.index)
    pvals = np.array([])
    for row in df1.iterrows():
        name = row[0]
        try:
            ttest_res = ttest_ind(df1.loc[name], df2.loc[name])
            pvals = np.append(pvals, ttest_res.pvalue)
        except:
            pvals = np.append(pvals, np.nan)

    df_pval["p_value"] = pvals
    return df_pval


def corrected_t_test(
    group1, group2, alpha=0.5, multiple_comparisons_correction_method="fdr_bh"
):
    """
    Perform a t-test (corrected for multiple comparisons) across every row of
    the dataframes of two independent samples.
    :param group1: Dataframe of group 1, with the same rows as group2
    :param group2: Dataframe of group 2, with the same rows as group1
    :param alpha: FWER, family-wise error rate. Default 0.5
    :param multiple_comparisons_correction_method:
            Method used for testing and adjustment of pvalues. Can be either
            the full name or initial letters. Available methods are:

        - `bonferroni` : one-step correction
        - `sidak` : one-step correction
        - `holm-sidak` : step down method using Sidak adjustments
        - `holm` : step-down method using Bonferroni adjustments
        - `simes-hochberg` : step-up method  (independent)
        - `hommel` : closed method based on Simes tests (non-negative)
        - `fdr_bh` : Benjamini/Hochberg  (non-negative)
        - `fdr_by` : Benjamini/Yekutieli (negative)
        - `fdr_tsbh` : two stage fdr correction (non-negative)
        - `fdr_tsbky` : two stage fdr correction (non-negative)
    :return: Dataframe of pvalues (raw and corrected) and whether the
    hypothesis that can be rejected for given alpha
    """

    results = ttest_all_rows(group1, group2)
    pval_array = np.squeeze(np.array(results))

    results["reject"], results["p_value_corrected"], _, _ = multipletests(
        pval_array, alpha=alpha, method=multiple_comparisons_correction_method
    )
    return results
