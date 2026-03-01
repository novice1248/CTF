// gcc -o challenge challenge.c
#include <stdio.h>
#include <string.h>

int main(void) {
    //　32文字まで受け取るinput
    char input[32];
    // REDACTEDで初期化されたxor_flag
    const char xor_flag[] = "REDACTED";
    // xor_flagの長さを取得
    size_t flag_len = strlen(xor_flag);

    // フラグの入力
    printf("Enter flag: ");
    fflush(stdout);
    scanf("%31s", input);

    // 入力の長さがxor_flagの長さと異なる場合はエラー
    if(strlen(input) != flag_len) {
        printf("Wrong length\n");
        return 1;
    }
    // 各文字を7でXORした結果がxor_flagと一致するか確認
    for(size_t i = 0; i < flag_len; i++) {
        if((input[i] ^ 7) != xor_flag[i]) {
            printf("Wrong at index %zu\n", i);
            return 1;
        }
    }
    printf("Correct\n");
    return 0;
}
