#define _CRT_SECURE_NO_WARNINGS
#include <openssl/evp.h>
#include <openssl/err.h>
#include <stdio.h>
#include <windows.h>
#include <stdlib.h>

uint8_t key[16] = {
	0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10
};
uint8_t input[16] = {
	0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10
};

//
static int32_t show_hex(int8_t* title, uint8_t* buf, uint32_t total)
{
	uint32_t idx;
	uint8_t* data = buf;

	printf("%s(%d):\n\t", title, total);
	for (idx = 0; idx < total; idx++) {
		printf("%02hhx", data[idx]);
		printf("%s", 15 == (idx & 15) ? "\n\t" : ", ");
	}
	printf("\n");

	return 0;
}

void SM4_encrypt()
{
	uint8_t out[16];
	uint32_t total_len = 0, out_len = 0;
	EVP_CIPHER* cipher = NULL;
	
	//���ü���ģʽΪSM4_ECB
	cipher = EVP_sm4_ecb();

	//����������
	EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
	
	//��ʼ�������ģ���5������ȷ���Ǽ��ܻ��ǽ��ܣ�1Ϊ���ܣ�0Ϊ����
	EVP_CipherInit(ctx, cipher, key, 0, 1);
	//�޸����ģʽ��Ĭ�����ΪPKCS
	//EVP_CIPHER_CTX_set_padding(ctx);

	EVP_CipherUpdate(ctx, out, &out_len, input, 16);
	total_len += out_len;

	//EVP_CipherFinal(ctx, out + total_len, &out_len);
	//total_len += out_len;

	//show_hex("plaintxt:", input, 16);
	//show_hex("key:", key, 16);
	//����������������
	//show_hex("cipher:", out, 16);
}

int main()
{
	//����ʱ�䣬���ȵ�΢��
	double time = 0;
	double counts = 0;
	LARGE_INTEGER nFreq;
	LARGE_INTEGER nBeginTime;
	LARGE_INTEGER nEndTime;
	QueryPerformanceFrequency(&nFreq);
	QueryPerformanceCounter(&nBeginTime);//��ʼ��ʱ
	
	//��2000�Σ���SM4_encrypt������ע�͵����
	for (int i = 0; i < 2000; i++)
		SM4_encrypt();

	QueryPerformanceCounter(&nEndTime);//ֹͣ��ʱ
	time = (double)(nEndTime.QuadPart - nBeginTime.QuadPart) / (double)nFreq.QuadPart;//�������ִ��ʱ�䵥λΪs
	//cout<<"����ʱ�䣺"<<time*1000<<"ms"<<endl;
	printf("����2000��ƽ��ÿ�λ���ʱ�� %f ms\n", (time * 1000 /2000));

    return 0;
}