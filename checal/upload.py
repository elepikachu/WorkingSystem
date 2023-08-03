import pandas as pd
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from io import BytesIO

def read_excel_M(io):
    df_original = pd.read_excel(io=io, sheet_name=0)

    # remove the 0 label
    df_data = df_original.drop(df_original.columns[0], axis=1)

    for col in df_data.select_dtypes(include=['int', 'float']).columns:
        second_last = df_data[col].iloc[-2]
        df_data[col] = df_data[col] * second_last * 0.01

    if df_data.shape[0] > 2:
        df_data = df_data.iloc[:-2, :]
    else:
        print('输入数组行数不足两行')

    sums = df_data.sum()
    df_data = df_data.append(sums, ignore_index=True)
    print(df_data)

    #              CH4    C2H6   C2H4    C2H2   C3H8   C3H6   C4H10  C4H10  C4H8   C5H12
    multipliers = [44 / 16, 44 / 30, 44 / 28, 44 / 26, 44 / 44, 44 / 42, 44 / 58, 44 / 58, 44 / 56, 44 / 72, 44 / 70,
                   44 / 86, 44 / 84, 0, 0, 0, 1, 44 / 28, 0, 0]
    df_data_CO2_original = df_data[:-1]
    df_data_CO2 = df_data_CO2_original.multiply(multipliers, axis=0)

    sums2 = df_data_CO2.sum()
    df_data_CO2 = df_data_CO2.append(sums2, ignore_index=True)

    multipliers2 = [50.01, 47.26, 48.72, 49.37, 46.68, 45.87, 46.04, 45.94, 45.47, 45.13, \
                   44.76, 44.04, 43.72, 141.8, 42.12, 0, 0, 10.11, 9.39, 0]
    #               C5H10  C6H14  C6J12  H2    H2O    N2 CO2  CO   H2S  else
    df_data_heat_original = df_data[:-1]
    df_data_heat = df_data_heat_original.multiply(multipliers2, axis=0) * 10000  # Gj

    sums3 = df_data_heat.sum()
    df_data_heat = df_data_heat.append(sums3, ignore_index=True)

    return df_data, df_data_CO2, df_data_heat


def read_excel_V(io):
    df_original_V = pd.read_excel(io=io, sheet_name=1)
    df_data = df_original_V.drop(df_original_V.columns[0], axis=1)
    df_original_V
    tran = 22.4 / 8.4
    #              CH4       C2H6      C2H4      C2H2     C3H8     C3H6     C4H10   C4H10     C4H8     C5H12
    multipliers3 = [tran / 16, tran / 30, tran / 28, tran / 26, tran / 44, tran / 42, tran / 58, tran / 58, tran / 56,
                    tran / 72, \
                    tran / 70, tran / 86, tran / 84, tran / 2, tran / 18, tran / 28, tran / 44, tran / 28, tran / 34, 0]
    #               C5H10    C6H14    C6J12    H2      H2O         N2        CO2    CO       H2S     else

    # remove the 0 label
    df_original_V = df_original_V.drop(df_original_V.columns[0], axis=1)[:-2]
    df_data_V = df_original_V.multiply(multipliers3, axis=0)

    sums4 = df_data_V.sum()
    df_data_V = df_data_V.append(sums4, ignore_index=True)


    #              CH4    C2H6   C2H4    C2H2   C3H8   C3H6   C4H10  C4H10  C4H8   C5H12
    multipliers = [44 / 16, 44 / 30, 44 / 28, 44 / 26, 44 / 44, 44 / 42, 44 / 58, 44 / 58, 44 / 56, 44 / 72, 44 / 70,
                   44 / 86, 44 / 84, 0, 0, 0, 1, 44 / 28, 0, 0]
    df_data_CO2_original = df_data_V[:-1]
    df_data_CO2 = df_data_CO2_original.multiply(multipliers, axis=0)

    sums2 = df_data_CO2.sum()
    df_data_CO2 = df_data_CO2.append(sums2, ignore_index=True)

    multipliers2 = [50.01, 47.26, 48.72, 49.37, 46.68, 45.87, 46.04, 45.94, 45.47, 45.13, \
                   44.76, 44.04, 43.72, 141.8, 42.12, 0, 0, 10.11, 9.39, 0]
    #               C5H10  C6H14  C6J12  H2    H2O    N2 CO2  CO   H2S  else
    df_data_heat_original = df_data_V[:-1]
    df_data_heat = df_data_heat_original.multiply(multipliers2, axis=0) * 10000  # Gj

    sums3 = df_data_heat.sum()
    df_data_heat = df_data_heat.append(sums3, ignore_index=True)

    return df_data_V, df_data_CO2, df_data_heat


def excel_generate(io, met):
    output = BytesIO()  # 转二进制流
    writer = pd.ExcelWriter(output, engine='openpyxl')

    if met == 'V':
        data_df, data_df2, data_df3 = read_excel_V(io)
    elif met == 'M':
        data_df, data_df2, data_df3 = read_excel_M(io)
    else:
        return HttpResponse('method error')

    data_df2.to_excel(writer, "碳排放", float_format='%.2f')
    data_df3.to_excel(writer, "热值", float_format='%.2f')

    writer.save()
    output.seek(0)  # 重新定位到开始
    response = HttpResponse(content_type='application/vnd.ms-excel')
    if met == 'M':
        response['Content-Disposition'] = "attachment;filename=%s" % escape_uri_path('1-MassFraction.xlsx')
    else:
        response['Content-Disposition'] = "attachment;filename=%s" % escape_uri_path('2-VolumeFraction.xlsx')
    response.write(output.getvalue())
    output.close()

    return response