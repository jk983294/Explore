#include <stdio.h>
#include <sys/inotify.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <unistd.h>

#define NAME_MAX 16
#define EVENT_SIZE (sizeof(struct inotify_event))
#define BUF_LEN (1024 * (EVENT_SIZE + NAME_MAX))

int main(void) {
    unsigned int queue_len;
    char buf[BUF_LEN];
    ssize_t i = 0;

    int fd = inotify_init();
    int wd = inotify_add_watch(fd, "./", IN_ACCESS | IN_MODIFY | IN_CREATE | IN_DELETE);

    while (1) {
        ssize_t len = read(fd, buf, BUF_LEN);
        while (i < len) {
            struct inotify_event *event = (struct inotify_event *)&buf[i];

            printf("wd=%d mask=%d cookie=%d len=%d dir=%s\n", event->wd, event->mask, event->cookie, event->len,
                   (event->mask & IN_ISDIR) ? "yes" : "no");

            if (event->len) {
                printf("name=%s\n", event->name);
            }

            if (event->mask & IN_ACCESS) printf("read event\n");
            if (event->mask & IN_MODIFY) printf("modify event\n");
            if (event->mask & IN_CREATE) printf("create event\n");
            if (event->mask & IN_DELETE) printf("delete event\n");

            i += sizeof(struct inotify_event) + event->len;
        }
    }

    // un-handled event queue msg bytes
    ioctl(fd, FIONREAD, &queue_len);
    printf("%u bytes pending in queue\n", queue_len);

    inotify_rm_watch(fd, wd);
    close(fd);  // this will remove wd also, so above code is not necessary
    return 0;
}
