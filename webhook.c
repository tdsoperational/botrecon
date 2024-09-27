#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <wininet.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "wininet.lib")
#define MAX_URL_LENGTH 2048

void printerr() {
    DWORD error = GetLastError();
    char buffer[256];
    FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
                   NULL, error, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
                   buffer, sizeof(buffer), NULL);
    printf("Error: %s\n", buffer);
}

void delwe() {
    char webhook_url[MAX_URL_LENGTH];
    HINTERNET hInternet, hConnect, hRequest;
    URL_COMPONENTS urlComp = { 0 };
    char hostName[256] = { 0 };
    char urlPath[1024] = { 0 };
    DWORD statusCode;
    DWORD statusCodeSize = sizeof(DWORD);

    while (1) {
        printf("webhook URL: ");
        fgets(webhook_url, sizeof(webhook_url), stdin);
        webhook_url[strcspn(webhook_url, "\n")] = 0;

        hInternet = InternetOpen("TLD14Browser/12.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
        if (hInternet == NULL) {
            printf("failed to initialize WinINet.\n");
            printerr();
            continue;
        }

        urlComp.dwStructSize = sizeof(urlComp);
        urlComp.lpszHostName = hostName;
        urlComp.dwHostNameLength = sizeof(hostName);
        urlComp.lpszUrlPath = urlPath;
        urlComp.dwUrlPathLength = sizeof(urlPath);
        InternetCrackUrl(webhook_url, 0, 0, &urlComp);

        hConnect = InternetConnect(hInternet, urlComp.lpszHostName, urlComp.nPort, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);
        if (hConnect == NULL) {
            printf("failed to connect to server.\n");
            printerr();
            InternetCloseHandle(hInternet);
            continue;
        }

        hRequest = HttpOpenRequest(hConnect, "DELETE", urlComp.lpszUrlPath, NULL, NULL, NULL, INTERNET_FLAG_SECURE, 0);
        if (hRequest == NULL) {
            printf("failed to create DELETE request.\n");
            printerr();
            InternetCloseHandle(hConnect);
            InternetCloseHandle(hInternet);
            continue;
        }

        if (!HttpSendRequest(hRequest, NULL, 0, NULL, 0)) {
            printf("failed to send DELETE request.\n");
            printerr();
            InternetCloseHandle(hRequest);
            InternetCloseHandle(hConnect);
            InternetCloseHandle(hInternet);
            continue;
        }

        if (!HttpQueryInfo(hRequest, HTTP_QUERY_STATUS_CODE | HTTP_QUERY_FLAG_NUMBER, &statusCode, &statusCodeSize, NULL)) {
            printf("failed to get status code.\n");
            printerr();
        } else {
            if (statusCode == 204) {
                printf("webhook deleted.\n");
            } else if (statusCode == 429) {
                printf("rate limited.\n");
            } else {
                printf("failed to delete the webhook. Status Code: %lu\n", statusCode);
            }
        }

        InternetCloseHandle(hRequest);
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);

        printf("gimme more\n");
    }
}

int main() {
    delwe();
    return 0;
}
