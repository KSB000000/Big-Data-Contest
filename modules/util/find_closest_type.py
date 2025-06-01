from modules.util.cosine_similarity import cosine_similarity
from modules.util.get_embedding import get_embedding


def find_closest_type(input_list):
    closest_types = []
    # Type_List 정의
    Type_List = [
        "숙박",
        "꼬치구이",
        "아이스크림/빙수",
        "분식",
        "포장마차",
        "중식",
        "쇼핑",
        "가정식",
        "샌드위치/토스트",
        "기타세계요리",
        "맥주/요리주점",
        "동남아/인도음식",
        "햄버거",
        "스테이크",
        "치킨",
        "피자",
        "부페",
        "도시락",
        "야식",
        "커피",
        "패밀리 레스토랑",
        "떡/한과",
        "민속주점",
        "차",
        "구내식당/푸드코트",
        "일식",
        "베이커리",
        "단품요리 전문",
        "도너츠",
        "양식",
        "기사식당",
        "주스",
        "관광지",
    ]
    # Type_List의 각 단어에 대해 미리 임베딩을 계산해둠
    type_embeddings = {type_item: get_embedding(type_item) for type_item in Type_List}

    for input_word in input_list:
        input_embedding = get_embedding(input_word)

        # 각 Type_List 항목과의 유사도를 계산하여 가장 유사한 항목을 찾음
        highest_similarity = -1
        most_similar_type = None

        for type_item, type_embedding in type_embeddings.items():
            similarity = cosine_similarity(input_embedding, type_embedding)
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_type = type_item

        closest_types.append(most_similar_type)

    return closest_types
