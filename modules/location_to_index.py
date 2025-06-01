from scipy.spatial import distance

from modules.llm.search_address_llm import search_address_llm
from modules.util.geocode_address import geocode_address


def location_to_index(location: str, df, model):
    """
    Args:
        location (str): 장소이름

    Returns:
        bool : 장소 인덱스 반환 여부
        str : 위도
        str : 경도
        int : 해당 장소의 인덱스(장소가 없다면 가장 가까운 점의 인덱스)
    """

    df.columns = df.columns.str.strip()

    # 1.파일에서 찾기
    result = df[df["MCT_NM"] == location]

    if not result.empty:
        return (
            True,
            result.iloc[0]["Latitude"],
            result.iloc[0]["Longitude"],
            result.iloc[0]["Distance_index"],
        )

    answer, address = search_address_llm(location, model)
    if address == None:
        return (False, 0, 0, 0)

    y, x = geocode_address(address)
    target = [float(y), float(x)]
    coordinates = df[["Latitude", "Longitude"]].astype(float).values

    distances = [distance.euclidean(target, point) for point in coordinates]
    return (True, y, x, distances.index(min(distances)))
