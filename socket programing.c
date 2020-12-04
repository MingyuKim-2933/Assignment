#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

#define MAX 256
#define MAX_DATA 200
#define PORT 45000
#define PENDING 10

int DATA_SEND_RECV(int, char*);


int main(int argc, char* argv[])
{
    char user[12];
    strcpy(user, argv[0]);
    int sock_flag, conn_flag;
    struct sockaddr_in server_addr;

    if ((sock_flag = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        printf("Socket 생성 실패...\n");
        exit(0);
    }
    else
        printf("Socket 생성 성공 ...\n");

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_addr.sin_port = htons(PORT);

    if ((connect(sock_flag, (struct sockaddr*) & server_addr, sizeof(server_addr))) < 0) {
        printf("서버-클라이언트 연결 실패 \n");
        exit(0);
    }
    else
        printf("서버-클라이언트 연결 성공 \n");

    DATA_SEND_RECV(sock_flag, user);
    close(sock_flag);
}
int DATA_SEND_RECV(int sock_flag, char user[12])
{
    int idx;
    int fd[MAX];
    int fp[MAX];
    int upload_count = 0;
    int download_count = 0;
    char* msg;
    char client_buf[MAX];
    char server_buf[3000];
    char data[MAX_DATA];
    char temp[MAX];
    char flag[6][20] = { "FLAG_CHAT", "FLAG_UPLOAD", "FLAG_DOWNLOAD", "FLAG_LIST_USER", "FLAG_LIST_FILE", "FLAG_EXIT" };
    for (;;) {
        idx = -1;
        msg = "";
        memset(client_buf, 0x00, MAX);
        memset(server_buf, 0x00, MAX);
        memset(data, 0x00, MAX_DATA);
        memset(temp, 0x00, MAX);
        printf("--Message TYPE--\n");
        printf("0 : chat, 1 : upload, 2 : download, 3 : list_user, 4 : list_file, 5 : exit\n");
        printf("Enter the message type: ");
        scanf("%d", &idx);

        strcpy(client_buf, flag[idx]);
        strcat(client_buf, "|");
        strcat(client_buf, user);
        strcat(client_buf, "|");

        switch (idx) {
        case 0: //CHAT
            strcpy(data, "Hello World\n");
            strcat(client_buf, data);
            write(sock_flag, (char*)client_buf, sizeof(client_buf));
            read(sock_flag, (char*)server_buf, sizeof(server_buf));
            msg = strtok(server_buf, "|");
            msg = strtok(NULL, "|");
            msg = strtok(NULL, "|");
            printf("%s\n", msg);
            break;

        case 1: //UPLOAD
            fd[upload_count] = open("file.pdf", O_RDONLY);
            if ((fd[upload_count] = open("file.pdf", O_RDONLY)) == -1) {
                printf("파일 읽기 실패\n");
                break;
            }
            else {
                while ((read(fd[upload_count], data, 200)) > 0) {
                    strcpy(temp, client_buf);
                    read(fd[upload_count], data, 200);
                    strcat(temp, data);
                    printf("Message : %s\n", temp);
                    write(sock_flag, (char*)temp, sizeof(temp));
                }


                strcat(client_buf, "EOF");
                printf("Message : %s\n", client_buf);
                write(sock_flag, (char*)client_buf, sizeof(client_buf));
                printf("전송완료\n");
                read(sock_flag, (char*)server_buf, sizeof(server_buf));
                printf("%s\n", server_buf);

                close(fd[upload_count]);
                upload_count += 1;
            }
            break;

        case 2: //DOWNLOAD
            printf("File name :");
            scanf("%s", data);
            fp[download_count] = open(data, O_WRONLY | O_CREAT);
            strcat(client_buf, data);
            printf("Message :%s\n", client_buf);
            write(sock_flag, (char*)client_buf, sizeof(client_buf));

            while (strcmp(msg, "Done.") != 0 || strcmp(msg, "file.") != 0) {
                if ((fp[download_count] = open(data, O_RDWR)) == -1) {
                    printf("파일 읽기 실패 \n");
                    break;
                }
                else {
                    read(sock_flag, server_buf, sizeof(server_buf));
                    msg = strtok(server_buf, "|");
                    msg = strtok(NULL, "|");
                    msg = strtok(NULL, "|");
                    write(fp[download_count], msg, strlen(msg));
                    printf("%s\n", server_buf);
                }
            }
            close(fp[download_count]);
            download_count += 1;
            break;

        case 3: //LIST_USER
            strcpy(data, "NULL");
            strcat(client_buf, data);
            write(sock_flag, (char*)client_buf, sizeof(client_buf));
            read(sock_flag, (char*)server_buf, sizeof(server_buf));
            msg = strtok(server_buf, "|");
            msg = strtok(NULL, "|");
            msg = strtok(NULL, "|");
            printf("%s\n", msg);
            break;

        case 4: //LIST_FILE
            strcpy(data, "NULL");
            strcat(client_buf, data);
            write(sock_flag, (char*)client_buf, sizeof(client_buf));
            read(sock_flag, (char*)server_buf, sizeof(server_buf));
            msg = strtok(server_buf, "|");
            msg = strtok(NULL, "|");
            msg = strtok(NULL, "|");
            printf("%s\n", msg);
            break;

        case 5: //EXIT
            strcpy(data, "EXIT");
            strcat(client_buf, data);
            write(sock_flag, (char*)client_buf, sizeof(client_buf));
            read(sock_flag, (char*)server_buf, sizeof(server_buf));
            msg = strtok(server_buf, "|");
            msg = strtok(NULL, "|");
            msg = strtok(NULL, "|");
            if (strcmp("BYE", msg) == 0) {
                printf("서버 종료 ...\n");
                exit(0);
            }
            break;
        }
    }
}
