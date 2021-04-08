# 문자열 입력
input_str = "aabbccc"

# 문자열 Comptression 함수
def str_compression(input_str):

    # 결과 값 저장 변수 선언
    comp_str = ""

    # 문자열 개수를 세기 위한 변수 선언
    count = 1

    # 문자열 전체 배열 - 1 만큼 배열 진행 (ex. len(str) = 7일 경우 0, 5 까지 진행)
    for i in range(len(input_str) - 1):
        #print("i: {}, input_str[{}]: {}, count: {}, comp: {}".format(i, i, input_str[i], count, comp_str))
        # 현재 문자열과 다음 문자열 비교
        if input_str[i] == input_str[i+1]:

            # 같을 경우 count 증가
            count += 1

        # 현재 문자열과 다음 문자열 비교
        else:

            # 다를 경우 결과 값에 데이터 추가
            comp_str += input_str[i] + str(count)

            # 데이터를 추가하였으므로 count 변 수 초기화
            count = 1

        #print("i: {}, input_str[{}]: {}, count: {}, comp: {}\n".format(i, i, input_str[i], count, comp_str))

    # 마지막 데이터 입력
    comp_str += input_str[i+1] + str(count)

    return comp_str

print(str_compression(input_str))
