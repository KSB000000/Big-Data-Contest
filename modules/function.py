import pandas as pd


def MONTH_SORT(MONTH, data):
    data["YM"] = data["YM"].astype(str)
    MONTH = f"2023{int(MONTH):02}"
    data = data[data["YM"] == MONTH]
    return data


def TYPE_SORT(TYPE, data):
    data = data[data["MCT_TYPE"] == TYPE]
    return data


def ADDR_SORT(ADDR, data):
    data = data[data["ADDR"].str.contains(ADDR)]
    return data


def CNT_SORT(grade, data):
    data["UE_CNT_GRP"] = data["UE_CNT_GRP"].str.extract(r'(\d+)').astype(int)
    data = data[data["UE_CNT_GRP"] <= grade]
    return data


def AMT_SORT(grade, data):
    data["UE_AMT_GRP"] = data["UE_AMT_GRP"].str.extract(r'(\d+)').astype(int)
    data = data[data["UE_AMT_GRP"] <= grade]
    return data


def AMT_PER_SORT(grade, data):
    data["UE_AMT_PER_TRSN_GRP"] = data["UE_AMT_PER_TRSN_GRP"].str.extract(r'(\d+)').astype(int)
    data = data[data["UE_AMT_PER_TRSN_GRP"] <= grade]
    return data


def DOE_SORT(DOE, data):
    data = data.sort_values(by=f"{DOE}_UE_CNT_RAT", ascending=False)
    return data


def FIND_MAX_DOE(NM, data):
    if data.empty:  # 데이터가 비어있는지 확인
        return "NA"

    data = data[
        [
            "MON_UE_CNT_RAT",
            "TUE_UE_CNT_RAT",
            "WED_UE_CNT_RAT",
            "THU_UE_CNT_RAT",
            "FRI_UE_CNT_RAT",
            "SAT_UE_CNT_RAT",
            "SUN_UE_CNT_RAT",
        ]
    ]

    max_value = data.max(axis=1).values[0]

    max_days = data.columns[data.isin([max_value]).any()].tolist()

    return max_days


def FIND_REST_DOE(NM, data):
    data = data[data["MCT_NM"] == NM]
    data = data[
        [
            "MON_UE_CNT_RAT",
            "TUE_UE_CNT_RAT",
            "WED_UE_CNT_RAT",
            "THU_UE_CNT_RAT",
            "FRI_UE_CNT_RAT",
            "SAT_UE_CNT_RAT",
            "SUN_UE_CNT_RAT",
        ]
    ]

    rest_DOE = []

    for DOE in [
        "MON_UE_CNT_RAT",
        "TUE_UE_CNT_RAT",
        "WED_UE_CNT_RAT",
        "THU_UE_CNT_RAT",
        "FRI_UE_CNT_RAT",
        "SAT_UE_CNT_RAT",
        "SUN_UE_CNT_RAT",
    ]:
        if data[DOE].values[0] == 0:
            rest_DOE.append(DOE)

    if not rest_DOE:
        rest_DOE.append("NA")
    return rest_DOE


def FIND_MAX_TIME(NM, data):
    data = data[data["MCT_NM"] == NM]
    data = data[
        [
            "HR_5_11_UE_CNT_RAT",
            "HR_12_13_UE_CNT_RAT",
            "HR_14_17_UE_CNT_RAT",
            "HR_18_22_UE_CNT_RAT",
            "HR_23_4_UE_CNT_RAT",
        ]
    ]
    max_value = data.max(axis=1).values[0]

    max_time = data.columns[data.isin([max_value]).any()].tolist()

    return max_time


def TIME_SORT(TIME, data):
    data = data.sort_values(by=f"HR_{TIME}_UE_CNT_RAT", ascending=False)
    return data


def LOCAL_SORT(LOCAL, data):
    if LOCAL == "LOCAL":
        data = data.sort_values(by="LOCAL_UE_CNT_RAT", ascending=False)

    return data


def FIND_LOCAL_BOOL(NM, data, mean):
    data = data[data["MCT_NM"] == NM]
    data = data[["LOCAL_UE_CNT_RAT"]]
    if data.values[0] >= mean:
        return "LOCAL"
    else:
        return "TOURIST"


def SEX_SORT(SEX, data):
    if SEX == "MAL":
        data = data.sort_values(by="RC_M12_MAL_CUS_CNT_RAT", ascending=False)
    if SEX == "FEM":
        data = data.sort_values(by="RC_M12_FME_CUS_CNT_RAT", ascending=False)
    return data


def FIND_MAX_SEX(NM, data):
    data = data[data["MCT_NM"] == NM]
    data = data[["RC_M12_MAL_CUS_CNT_RAT", "RC_M12_FME_CUS_CNT_RAT"]]
    max_value = data.max(axis=1).values[0]
    max_sex = data.columns[data.isin([max_value]).any()].tolist()

    return max_sex


def OLD_SORT(OLD, data):
    if OLD == "60":
        data = data.sort_values(by=f"RC_M12_AGE_OVR_60_CUS_CNT_RAT", ascending=False)
    elif OLD == "20":
        data = data.sort_values(by=f"RC_M12_AGE_UND_20_CUS_CNT_RAT", ascending=False)
    else:
        data = data.sort_values(by=f"RC_M12_AGE_{OLD}_CUS_CNT_RAT", ascending=False)
    return data


def FIND_MAX_OLD(NM, data):
    data = data[data["MCT_NM"] == NM]
    data = data[
        [
            "RC_M12_AGE_UND_20_CUS_CNT_RAT",
            "RC_M12_AGE_30_CUS_CNT_RAT",
            "RC_M12_AGE_40_CUS_CNT_RAT",
            "RC_M12_AGE_50_CUS_CNT_RAT",
            "RC_M12_AGE_OVR_60_CUS_CNT_RAT",
        ]
    ]
    max_value = data.max(axis=1).values[0]

    max_old = data.columns[data.isin([max_value]).any()].tolist()

    return max_old


def RECOMMEND(MONTH, TYPE, ADDR, CNT, AMT, AMT_PER, DOE, TIME, LOCAL, SEX, OLD, data):
    try:

        data["LOCAL_UE_CNT_RAT"] = pd.to_numeric(
            data["LOCAL_UE_CNT_RAT"], errors="coerce"
        )
        LOCAL_mean = data["LOCAL_UE_CNT_RAT"].mean()
        if MONTH != "NA":
            data = MONTH_SORT(MONTH, data)

        if TYPE != "NA":
            data = TYPE_SORT(TYPE, data)

        if ADDR != "NA":
            data = ADDR_SORT(ADDR, data)

        if CNT != "NA":
            data = CNT_SORT(CNT, data)

        if AMT != "NA":
            data = AMT_SORT(AMT, data)

        if AMT_PER != "NA":
            data = AMT_PER_SORT(AMT_PER, data)

        if DOE != "NA":
            data = DOE_SORT(DOE, data)

        if TIME != "NA":
            data = TIME_SORT(TIME, data)

        if LOCAL != "NA":
            data = LOCAL_SORT(LOCAL, data)

        if SEX != "NA":
            data = SEX_SORT(SEX, data)

        if OLD != "NA":
            data = OLD_SORT(OLD, data)

        result = data.head(1)
        result_name = result["MCT_NM"]
        recom_DOE = FIND_MAX_DOE(result_name, result)
        rest_DOE = FIND_REST_DOE(result_name, result)
        recom_TIME = FIND_MAX_TIME(result_name, result)
        recom_OLD = FIND_MAX_OLD(result_name, result)
        recom_SEX = FIND_MAX_SEX(result_name, result)
        recom_LOCAL = FIND_LOCAL_BOOL(result_name, result, LOCAL_mean)
        output = []
        output = [
            f"기준 월: ['{MONTH}월']",
            f"업종: ['{TYPE}']",
            f"가게이름: ['{result_name.values[0]}']",
            f"가장 혼잡한 요일: {recom_DOE}",
            f"쉬는 요일: {rest_DOE}",
            f"가장 바쁜 시간대: {recom_TIME}",
            f"가장 많이 찾는 나이대: {recom_OLD}",
            f"남녀 성비: {recom_SEX}",
            f"현지인/관광객 맛집: ['{recom_LOCAL}']",
        ]
    except IndexError:
        return "-1"
    
    return output


def Move_Recommend(Input_Index, Move_List, Month, DOE, Time, data):
    try:
        result = {}
        original_data = data
        Range = 100
        if Input_Index < Range:
            L_Range = Input_Index
            Left_Idx = Input_Index - (Range - L_Range)
            Right_Idx = Input_Index + (Range - L_Range)
        elif Input_Index + Range > 9658:
            Right_Idx = 9658
            Left_Idx = Input_Index - Range
        else:
            Left_Idx = Input_Index - Range
            Right_Idx = Input_Index + Range
        data["Distance_Index"] = pd.to_numeric(data["Distance_Index"], errors='coerce')
        for TYPE in Move_List:
            data = original_data.copy()
            if TYPE in ["관광지", "쇼핑", "숙박"]:
                data = data[data["MCT_TYPE"] == TYPE]
                data = data.sort_values(by="ALL_RECOMMEND", ascending=False)
                data["Distance_index"] = data["Distance_index"].astype(float)
                differences = abs(data["Distance_index"].values - Input_Index)
                # 가장 차이가 적은 인덱스 찾기
                closest_index = differences.argmin()
                # 가장 차이가 적은 데이터의 MCT_NM 가져오기
                closest_mct_nm = data["MCT_NM"].values[closest_index]
                result[TYPE] = closest_mct_nm
            else:
                data = data[
                    (data["Distance_Index"] >= Left_Idx)
                    & (data["Distance_Index"] <= Right_Idx)
                ]
                data = data[
                    (data["Distance_Index"] >= Left_Idx)
                    & (data["Distance_Index"] <= Right_Idx)
                ]
                if Month != "NA":
                    data = MONTH_SORT(Month, data)
                if DOE != "NA":
                    data = data[~data["Zero_Days"].apply(lambda x: DOE in x)]
                if Time != "NA":
                    data = data[~data["Zero_Hours"].apply(lambda x: Time in x)]
            
                data["Sum"] = data["UE_CNT_GRP"] + data["UE_AMT_GRP"]
                data = data.sort_values(by="Sum", ascending=True)

                Count = data.shape[0]

                for i in range(Count):
                    if data["MCT_TYPE"].values[i] == TYPE:
                        result[TYPE] = data["MCT_NM"].values[i]
                        break
        # print(result)
    except IndexError:
        return "-1"
    
    return result
