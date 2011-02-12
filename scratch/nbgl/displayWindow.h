#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define FALSE 0
#define TRUE 1

#define REQUEST_NOTHING 0
#define REQUEST_CREATE 1
#define REQUEST_DESTROY 2
#define REQUEST_RESIZE 3

/* Display Window */
typedef struct {
    int id;
    char title[128];
    int x;
    int y;
    int w;
    int h;    
    void (*initRendering)();
    void (*handleResize)(int w, int h);
    void (*handleKeypress)(unsigned char key, int x, int y);
    void (*drawScene)();
    void (*update)(int arg);
} Window;

typedef struct Window *WindowP;

/*typedef struct WindowID; */
typedef struct WindowID *WindowIDP;

struct WindowID {
    int id;
    WindowIDP next;
};



int continueRunning;

int changeRequest;

int _request;

int numOpenWindows;
    
void setWindowParameters(int id, char* title, int x, int y, int w, int h, int scn);
void _createWindow();
void _destroyWindow();
void _destroyWindow2(int id);
void _close();
int getNumOpenWindows();
void incNumOpenWindows(); 
void decNumOpenWindows();
int getChangeRequest();
void setRequest(int value);
void _changeWindowSize(int id, int w, int h);
void setChangeRequest(int value);
void *TaskCode(void *argument);
void createEventLoopThread();

void insertIntoWindowIDsList(WindowIDP);
int deleteFromWindowIDsList(int id);
int existsInWindowIDsList(int id);


