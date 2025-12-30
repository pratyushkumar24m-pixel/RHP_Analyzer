import math

def calculate_beneish(dsri, gmi, aqi, sgi, depi, sgai, lvgi, tata):
    return (-4.84 +
            0.920 * dsri +
            0.528 * gmi +
            0.404 * aqi +
            0.892 * sgi +
            0.115 * depi -
            0.172 * sgai +
            4.679 * tata -
            0.327 * lvgi)

def calculate_altman(working_capital, retained_earnings, ebit, mve, liabilities, sales, assets):
    return (
        1.2 * (working_capital / assets) +
        1.4 * (retained_earnings / assets) +
        3.3 * (ebit / assets) +
        0.6 * (mve / liabilities) +
        1.0 * (sales / assets)
    )

def calculate_f_score(net_income, cfo, roa_current, roa_prev,
                      long_debt, long_debt_prev, curr_ratio, curr_ratio_prev,
                      shares, shares_prev):
    score = 0
    score += 1 if net_income > 0 else 0
    score += 1 if cfo > 0 else 0
    score += 1 if roa_current > roa_prev else 0
    score += 1 if long_debt < long_debt_prev else 0
    score += 1 if curr_ratio > curr_ratio_prev else 0
    score += 1 if shares <= shares_prev else 0
    return score

def calculate_c_score(accruals, asset_growth, depreciation, gross_margin, sales_growth):
    score = 0
    score += 1 if accruals > 0 else 0
    score += 1 if asset_growth > 0.25 else 0
    score += 1 if depreciation < 0.15 else 0
    score += 1 if gross_margin < 0 else 0
    score += 1 if sales_growth < 0.1 else 0
    return score
