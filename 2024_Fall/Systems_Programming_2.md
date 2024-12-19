---
title: Systems Programming 筆記 part 2
tags: [2024_Fall]
---
<!-- HackMD ID:JiYqw_SGQCaxR3kma8BlmQ -->  

Systems Programming 筆記 part 2  
===  
2024 Fall 台大資工系必修 老師：鄭卜壬  

1. OS Concept & Intro. to UNIX  
2. UNIX History, Standardization & Implementation  
3. File I/O  
4. Standard I/O Library  
5. Files and Directories  
6. System Data Files and Information  
7. Environment of a Unix Process  
8. Process Control  
9. Signals  
10. Inter-process Communication  
11. Thread Programming  
12. Networking  

# ch8 Process Control part 2  

## 權限溢出問題  

Least-privilege model: 一個 process 只能用最少的 privilege，不要多給。  
例子: 期中考 Alice 有個 set-uid 的程式，讓 Bob 執行後，open 一個 Alice 的檔案，再 exec Bob 的程式去做後續操作。因為 Bob 的程式可能沒有 set-uid，那此時就會有問題，Bob 取得多餘的權限。  

### Saved set-UID  

執行 exec 時，會把 euid 複製到 saved set-uid(saved-suid)，這樣在改 euid 後還可以 `setuid(...)` 把 euid 改回 exec 時借到的 euid。  
同時也確保 set-uid program 用 exec 執行 non-set uid program 後，不能夠把 euid 換回 saved set-uid。  
因為不能 get saved-suid，所以要在 exec 後趕快把 saved-suid 存起來。(其實 GNU 有 `getresuid`)  

`setuid(uid)`:  
* superuser 會把 ruid, euid, saved-suid 都設為 uid。如果只要設 euid 則用 `seteuid(uid)`，但不常用。  
* 其他人會把 euid 設為 uid，但 uid 需要是 ruid、saved-suid 之一。因此對 unprivileged user 來說，`setuid` 和 `seteuid` 是一樣的。  

### example tip(BSD), cu(SV)  

> open source 常用 file lock 來限制一個檔案只能有一個 process 執行，可以在檔案寫 pid。  

用同一個數據機 (modem)，因此需要限制一次只能有一個 process 用，所以就用一個 file lock，而只有 `uucp` 可以改 lock，所以會有一個 uucp 的 set-uid 的 program `tip`。  
而在用 uucp 的 euid 取得 lock 後，還是要 `setuid(ruid)` 後來存取其他資料 $(\Delta)$，因此要先在 exec 後馬上把 euid(=saved-suid) 存起來，在做完事之後設 euid 為 saved-suid，然後 release lock。  
**討論**:  
* $\Delta$ 處如果用 exec 執行程式，其實不會有問題，因為 saved set-uid 會被 euid 蓋掉。  
* `tip` 的 owner 不能是 root，否則 `setuid(ruid)` 就會把所有值都清掉改不回來 root。  

### 改掉 ruid  

在有 saved set-uid 之前，BSD 有 `setreuid(ruid, euid)`，可以改 ruid 和 euid。  
unprivileged user 只能把  
* euid 設為 ruid, euid, saved-suid 之一  
* ruid 設為 ruid, euid 之一  

基本上是希望透過 swap ruid 和 euid 來達到類似 saved set-uid 的目的。  
Linux 其實也有實作。  
這是學界跑在業界前面的例子，總是會有許多很創新的想法。  

### seteuid  

`seteuid(euid)`: 一般 user 一樣只能改成 ruid, saved set-uid，跟 `setuid` 一模一樣。但 root 可以只改 euid，改成任何值。  

### summary  

以上都只會牽扯到 main group，supplementary group 不會被改變。  
要記得 set-uid 程式別亂 exec 把權限亂借出去，建議是把 euid 改掉後自己做事。  

## Interpreter files  

Interpreter: 直譯器，像是 shell、perl、python 等。  
Interpreter files: 開頭 `#!`，後面接直譯器的絕對路徑，這樣文字檔案就相當於一個執行檔，exec 會看得懂。  

### 參數  

若 interpreter file `file` 裡面寫 `#!/bin/some arg1`，然後執行 `./file arg2` 則相當於執行 `/bin/some arg1 <pwd>/file arg2`  

### 例子  

如果有個 interpreter file `file.awk` 用 `awk` 寫(`#!/bin/awk -f`)，把 argv 全部印出來，則執行 `./file.awk xxx` 相當於 `/bin/awk -f ./file.awk xxx`，在執行時就會只印出 `awk xxx`。  

### 好處  

如果是寫 `awk 'xxx' $*` 在檔案裡，並用 `execlp` 執行，review: p 會去 PATH 找執行檔的位置，**允許 filename 是 shell script**，所以會把檔案當成 shell script，`/bin/sh` 再 fork, exec `awk`, wait。  
用 interpreter file，執行時就會直接執行 `awk`，不會多一個 shell。  

# ch15 IPC(part 1)  

* pipe  
* FIFO  
* stream pipe  
* named stream pipe  
* message queues  
* **semaphores**:研究所愛考，OS會教  
* **shared memory**:最快，system call`shm_xxx`  
* socket  
* stream  

## pipe  

buffered I/O。如果兩個人寫，寫超過buffer size可能會interleave: "abcd", "1234", result "a1b2c3d4"  

### 限制  

* half-duplex: 只能單向傳輸  
    * Stream pipes are duplex  
* 只能在有共同祖先的process用  
    * Named pipes/FIFOs可以在隨便的process裡用  

## FIFO  

像是開個檔案  
```c  
int mkfifo(const char *pathname, mode_t mode);  
```  
回傳是成功/失敗，  
不能lseek、讀完不能再讀，跟pipe差不多  
Ex  
```shell  
mkfifo fifo1  
prog3 < fifo1 &  
prog1 < infile | tee fifo1 | prog2  
```  

## 很重要  

* **Deadlock**  
* **race condition**  

# Ch10 Signals  

File 在不同系統差異不大， Process 就開始有些差別(ex: wait)，而 Signal 差別更大(有些 system call 不reliable)，有些實際運行會有 race condition 等。  
Ctrl-C 就是一個 signal，系統送給process。  

> 比較：與 Interrupt 的差異  
> Interrupt 的對象是 CPU，而 signal 是 process  
> Interrupt 可能是 CPU 的一個接腳或內部產生，讓 CPU 暫停現在的 process 去某個 subroutine(ISR，interrupt subroutine，通常非常短)。  
> Interrupt先記下發生什麼事，而signal是系統用來通知process。  
> IRQ：Interrupt quest  

Signal 是 kernel 用來通知 process 重要事件的，由 kernel 定義。AKA software interrupt。編號通常是正整數，0 是特別意思（認ID）。  
分成同步、非同步，像是 SIGCHILD 你也不知道小孩什麼時候會死，會是非同步。  

## 產生 Signal 的狀況  

* Terminal-generated: Ctrl-C -> `SIGINT`  
* Exceptions: div by 0 -> `SIGFPE`, illegal memory access -> `SIGSEGV`  
* Function `kill`  
* Shell command kill: `SIGKILL`  
* Software condition: reader of pipe terminated -> `SIGPIPE`, alarm clock expires -> `SIGALRM`  

## process 的反應  

三擇一，沒寫就是 default  
* Ignore(`SIGKILL`, `SIGSTOP` cannot be ignored)  
對 undefined behavior 後果自負(ex: `SIGFPE`)  
* Catch(`SIGKILL`, `SIGSTOP` cannot be caught)  
ex: 收到 `SIGCHILD` 再 `waitpid`  
* Default: Terminate, ignore, stop.  

Default 通常是 Terminate、Ignore、Stop  

## List  

> signal: default action  
> w/core = with core dump  

### 常見/重要  

| Signal    | Default Action   | Description                                                                                                                                    |  
| --------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |  
| `SIGABRT` | Terminate w/core | By calling `abort()`                                                                                                                           |  
| `SIGALRM` | Terminate        | By calling `setitimer()`, `alarm()`                                                                                                            |  
| `SIGCHLD` | Ignore           | Child process state change (e.g., execution, stopping)                                                                                         |  
| `SIGFPE`  | Terminate w/core | Division by zero, floating point overflow, etc.                                                                                                |  
| `SIGHUP`  | Terminate        | Originally used for terminal disconnection; now used to signal background processes (e.g., servers) for rereading config files(avoid stopping) |  
| `SIGINT`  | Terminate        | DELETE/Ctrl-C                                                                                                                                  |  
| `SIGIO`   | Terminate/Ignore | 最厲害非同步，叫系統讀到某個buffer，搞定後傳這個signal。=`SIGPOLL`                                                                             |  
| `SIGKILL` | Terminate        | Cannot be ignored or caught                                                                                                                    |  
| `SIGPIPE` | Terminate        | reader of pipe/socket terminated                                                                                                               |  
| `SIGQUIT` | Terminate w/core | Ctrl-\，terminate foreground process                                                                                                           |  
| `SIGSEGV` | Terminate w/core | Segmentation fault                                                                                                                             |  
| `SIGSTOP` | Stop process     | Cannot be ignored or caught                                                                                                                    |  
| `SIGTSTP` | Stop process     | Ctrl-Z，可以catch                                                                                                                              |  
| `SIGTERM` | Terminate        | `kill` command                                                                                                                                 |  
| `SIGURG`  | ignore           | 網路課，out-of-band data: 傳資料網路塞車，要維持品質                                                                                           |  
| `SIGUSR1` | Terminate        | user defined                                                                                                                                   |  
| `SIGUSR2` | Terminate        | user defined                                                                                                                                   |  

> Note: 鬧鐘、handler 都只有一次有效  

### 不常見/不重要  


| Signal      | Default Action   | Description                                                                        |  
| ----------- | ---------------- | ---------------------------------------------------------------------------------- |  
| `SIGBUS`    | Terminate w/core | Implementation-defined HW fault (e.g., memory alignment error, undefined behavior) |  
| `SIGCONT`   | Continue/Ignore  | Continue a stopped process                                                         |  
| `SIGILL`    | Terminate w/core | illegal hardware instruction, rarely seen                                          |  
| `SIGPROF`   | terminate        | 鬧鐘響                                                                             |  
| `SIGPWR`    | ignore           | ~~電池沒電~~，UPS沒電，init shutdowns the system                                   |  
| `SIGSYS`    | Terminate w/core | Invalid sys call                                                                   |  
| `SIGVTALRM` | Terminate        | 只看user CPU time的alarm                                                           |  
| `SIGWINCH`  | ignore           | terminal size changed                                                              |  
| `SIGXCPU`   | Terminate w/core | 超過soft CPU time limit                                                            |  
| `SIGXFSZ`   | Terminate w/core | 超過soft soft file limit                                                           |  

### w/core but no core dump  

* non-owner setuid process  
* non-grp-owner setgid process  
* no access rights at the working dir  
* file is too big (`RLIMIT_CORE`)  

## Set Disposition of Signal to Handler  

```c  
typedef void (*sighandler_t)(int);  
sighandler_t signal(int signum, sighandler_t handler);  
```  
設`sighandler_t`為指向(輸入 int，無輸出的函數)的指標。  
`signal`會回傳之前的 handler。  
```c  
#define SIG_ERR (void (*)())-1  
#define SIG_DFL (void (*)())0  
#define SIG_IGN (void (*)())1  
```  
都是無輸入、輸出 `void*` 的函數指標，但數值亂設，讓 `signal` 去判斷，可當作 handler 使用。出問題時則回傳 SIG_ERR。  

### Check current disposition  

想達成：若現在是 Ignore，則設為我的 handler。  
由於沒有設計這樣的功能，可以這樣做：  
```c  
int sig_int(); // 某 handler  
if(signal(SIGINT, SIG_IGN)!=SIG_IGN){  
  signal(SIGINT, sig_int);  
}  
```  

### start-up  

* fork：根據原則，沒有必要改的東西就會直接繼承，所以全部繼承。又因為 Memory 裡會有 handler，不會出問題。  
* exec：default 和 ignore 會繼承，但 catch 的 signal 由於新的程式無法 access handler，不會繼承。  

shell 會把 background process 的 interrupt、quit 設為 ignore，反正不會發生(?)  

## Interrupted System Calls  

Interrupt 是很重要的機制，因為可以避免 busy waiting(?)  
可以這樣寫：  
```c  
again:  
if((n=read(fd,buf,buf_size))<0){  
    if(errno==EINTR) // interrupted  
        goto again;  
}  
```  

### Auto-restarting  

為了簡化，4.2BSD 的 read 如果被中斷會自動 restart，方便但也有很多問題。  

## Reentrant Functions  

因為在 handler 裡可能會再收到一次 signal，動作被中斷，所以 handler 裡要是能確保不會有問題的功能：  
Reentrant Functions：可以被 safely recursively called  

與 functional programming 的原則很像，但沒那麼極端。原則是不能用：  
* 外部或共享的狀態、資源  
* 其他Non-reentrant function  

比如  
* global variable(standard I/O: printf, scanf)  
* pointer to a **fixed** address(POSIX.1 system database: getpwnam()等)  
* static(可視為只有該 func 可見的 global variable)  
* access file  
* 操作 heap 的東西(malloc、free)  

Reentrant 少到可以正面表列。  

Ex: 如果需要回傳一個 array，local variable會消失、static 和 malloc 也不行，解決辦法是一律叫參數直接傳 alloc 好的指標。（有點像 funcional programming 的精神）  

> printf 雖然不是 reentrant，但為了 debug 還是會用。  

**Note**: 因為原本的程式不知道自己被 signal 中斷，而 errno 在 handler 可能被改，所以 handler 通常在一開始存起來、最後設回去。(但還是有可能其他 signal 在存好前來，導致無法還原，這在 unreliable signal 無解，得要把 signal block 掉)  

## Unreliable signals  

**Signals could get lost!**  
Ex 1: 註冊完只會有效一次，所以通常會在 handler 再 `signal` 註冊一次，但如果要處理的 signal 剛好在這之前來就會照 default。  

Ex 2: 不想馬上處理 Ctrl-C，且 Ctrl-C 一定會來，來了之後才要繼續做事。  
具體故事：  
教授上課時知道當天有重要電話，但不能馬上接，可以  
1. 先接聽一秒問是誰打來的，用筆記寫下來，上課完再回電。  
對應到在 handler 設一個 flag，做完要做的事若 flag 沒被設(上完課電話都還沒來)，就 `pause` 直到 flag 被設(待在教室等電話來)。  
2. 開飛航模式，上課完才接電話(但是這裡比較特別，對方打電話不通會一直嘟嘟嘟不會 timeout)。  
對應到把 signal block 掉，做完事再 `sigsuspend`(上完課再解除飛航模式)。  

下面是第一種作法：  
```c=  
int flag=0;  
main(){  
  signal(SIGINT, handler);  
  ...  
  while(flag == 0)  
    pause(); // 等到flag=1(收到 signal)  
  // 做 Ctrl-C 時真的要做的事  
}  
handler(){  
  signal(SIGINT, handler);  
  flag=1;  
}  
```  
看起來沒問題，但如果 signal 在5、6行間來就會等到死，所以不能這樣寫。  

## Reliable signals  

* **signal generated**:  
事件發生(在 PCB on 某個 bit)  
* **signal delivered**:  
process take action for the signal(deliver 可以被 block)  

中間時間為 **pending**  

### Block a signal  

只能阻止 deliver，不能阻止 generate  
A signal is blocked until: 1.) Being unblocked. 2.) Action becomes ignore.  
* `sigpending(*set)`: 檢查 pending 的 signal，**blocked signal 也算 pending！**  
* `sigprocmask(how, *set, *old_set)`: 設定 **signal mask** (要擋哪些 signal)，與 cwd、umask 都是 independently inherited。  

#### block 時來 signal，再 unblock 會怎樣？  

都是 depend on implementation  
* 同 signal 來很多次：POSIX 沒有定義。像感覺遮斷一樣，有可能會 deliver 很多次，但也可能只是 on PCB 的 bit，所以只有一次。  
* 不同 signal 的順序：POSIX 沒有定義。但有可能是最嚴重的優先(會 terminate 的)  

## kill & raise  

* `int kill(pid, signum)`: send `signum` to `pid`  
    * `pid>0`: to process  
    * `pid==0`: all processes with the same gid  
    * `pid<0`: to all processes with gid==-pid  
* `int raise(signum)`: send `signum` to myself.(=`getpid`+`kill`)  

### 可以 kill 的對象  

Real or effective UID of the sender == that of the receiver (both are processes)  

### signum 0  

Don't send signal, but still check if a process is alive and we can send signal to it.  
success: 0, fail: -1  
> 如果做的事是：如果某 process 是活的，則XXX，這會有TOC-TOU問題（這種問題都是不常發生，但還是要避免）  

### behavior on signal to itself  

At least one (pending, unblocked) signal is **delivered** before `kill` or `raise` returns(不只這兩個).  
**應用**: `abort`，關掉(block)其他 signal，保證結束前會收到自殺 signal。  

## alarm & pause  

* `unsigned int alarm(unsigned int secs)`: set alarm clock, return remaining time. Since default is termination, you have to catch it.  
* `int pause(void)`: suspend until signal comes. Return if a signal handler is executed and returns.  

### sleep1:  
```c  
sighandler_t sig_alrm(int signum){  
  // do nothing, just to wake up pause  
}  
int sleep1(int nsecs){  
  if((old_handler=signal(SIGALRM, sig_alrm))==SIG_ERR)  
    return nsecs;  
  alarm(nsecs);  
  // If the alarm somehow arrives here, the pause will never return (race condition).  
  pause();  
  return alarm(0); // turn off alarm  
}  
```  

## Nonlocal Jumps  

Powerful but dangerous user-level mechanism for transferring control to an arbitrary location.  

### Stack Frame  

When a function is called, a stack frame is created. It contains:  
* return address  
* passed parameters  
* saved registers  
* local variables  

Put in the stack of the virtual memory.  
Problems:  
* Review: `setvbuf` 不能用 local variable 作為 buffer。  
* `f1()` call vfork and return, child exits after calling f2(that may clean `pid` in stack). **Parent cannot access `pid` in the stack.**  

### Longjmp & setjmp  

* `int setjmp(jmp_buf env)`: save the current context in `env`, return 0 if directly called, or `val` from `longjmp()`.  
* `void longjmp(jmp_buf env, int val)`: restore the context in `env`, return `val`.  

`jmp_buf` 可能記了不同東西， machine-dependent. 但通常會記:  
* CPU registers  
* stack pointers  
* return address  

理論上要用在很深的 stack: A call B, B call C,... When an error occurs in C, then we can directly longjmp to A.  
但其實 jmp 其實更 powerful，實際上可以亂跳。  

#### Type qualifiers in C  

* `const`: read-only  
* `volatile`: may be changed by other means, must stored in memory instead of register  
* `restrict`: no other pointer can access the object (so no overlap)  
Ex: `void *memcpy(void *restrict dest, const void *restrict src, size_t n)` and `void *memmove(void *dest, const void *src, size_t n)`  

雖然 compile 時不一定能檢查會不會重複，但可能會檢查。  

#### (still imperfect) sleep2  

```c  
static jmp_buf env_alrm;  
static void sig_alrm(int signum){  
  longjmp(env_alrm, 1);  
}  
unsigned int sleep2(unsigned int nsecs){  
  if(signal(SIGALRM, sig_alrm)==SIG_ERR)  
    return nsecs;  
  if(setjmp(env_alrm)==0){  
    alarm(nsecs);  
    // alarm arrives here, handler jump to setjmp and return  
    pause(); // alarm arrives after calling pause, pause will  
    // not return and still jump to setjmp and return.  
  }  
  return alarm(0); // remaining time(maybe waken up by other signal)  
}  
```  

Problem: If another signal comes(say `SIG_INT`), the `SIG_INT` handler saves and tries to restore the `errno`. But before the saving is done, the alarm may come and change the unsaved `errno`.  
雖然不完美但還是有可能這樣寫。  

## alarm + pause  

* Can act as a timeout  
(for slow system call like `read`). But need to worry about  
  * race condition  
  * autorestart of `read`(Linux does)  
* timeout & restart by longjmp  

## Signal Sets  

> 要養成用預設型別的好習慣，像是 `sigset_t`, `pid_t`, `uid_t` 等。  

* `int sigemptyset(sigset_t *set)`  
* `int sigfillset(sigset_t *set)`  
* `int sigaddset(sigset_t *set, int sig_no)`  
* `int sigdelset(sigset_t *set, int sig_no)`  
* `int sigismember(const sigset_t *set, int sig_no)`  

### sigprocmask  
`sigprocmask(how, *set, *old_set)`  
* `old_set`: return the old signal mask.  
* `how` can be `SIG_BLOCK`, `SIG_UNBLOCK`, `SIG_SETMASK`  
* If any unblocked signals are pending, at least one  
of unblocking signals will be delivered before the  
sigprocmask() returns.(as `kill` and `raise`)  

### sigpending  
`int sigpending(sigset_t *set)`  
return the set of signals that are blocked and pending.  

### example  

```c  
static void sig_quit(int signum) {  
  printf("caught SIGQUIT\n");  
  signal(SIGQUIT, SIG_DFL);  
  // restored to default  
}  

int main(void) {  
  sigset_t newmask, oldmask, pendmask;  

  signal(SIGQUIT, sig_quit);  

  sigemptyset(&newmask);  
  sigaddset(&newmask, SIGQUIT);  
  sigprocmask(SIG_BLOCK, &newmask, &oldmask);  
  // save original to oldmask so that we can restore it later  

  sleep(5);  

  sigpending(&pendmask);  
  if (sigismember(&pendmask, SIGQUIT))  
    printf("\nSIGQUIT pending\n");  
    // 在等五秒期間希望 SIGQUIT 被 triggered  

  sigprocmask(SIG_SETMASK, &oldmask, NULL); // 在這個瞬間去處理 sig_quit  
  // 大多的系統只處理一次，所以如果在上面 sleep 按了很多次 ^\ ，還是會當作只有一次，先印出下面這行然後才結束。  
  printf("SIGQUIT unblocked\n");  

  sleep(5);  
  exit(0);  
}  
```  
## Reliable signal  

### sigaction  

特色  
* **一次註冊終身有效**  
* 才是 **reliable** 版本  
* `signal` 可能是 call `sigaction`  
* Signal mask  
  * Additional signals can be masked before the handler function is called.  
  * The caught signal is **blocked** in the handler function to avoid signal lost.(不會 race condition)，handler 裡會發現 signal 被 blocked。  

`int sigaction(int signum, const struct sigaction *act,  
struct sigaction *oldact)`  
* `act`: new action  
* `oldact`: set to old action  

```c  
struct sigaction{  
  void (*sa_handler)(int);  
  sigset_t sa_mask;  
  int sa_flags;  
  void (*sa_sigaction)(int,siginfo_t*, void*); // input: (int signum, siginfo_t *info, void *ucontext)  
}  
```  
* `sa_flags`，只寫重要的，並且有些不重要的細節沒寫:  
  * `SA_INTERRUPT`: 會中斷 system call，不會自動 restart  
  * `SA_NODEFER`: 在 call handler 時不會 block signal，**注意這是 unreliable**。  
  * `SA_RESETHAND`: 在 call handler 之前把 disposition 設回 default，跟 **unreliable** 的行為一樣。  
  * `SA_RESTART`: 會自動 restart system call，但不是所有 system call 都會被 restart。  
  * `SA_SIGINFO`: 用 `sa_sigaction` 而不是 `sa_handler`，可以得到 `siginfo` 和 context。  
* `sa_mask`: **additional** signals to be blocked during the handler.  

`siginfo` 大致上就是各種錯誤處理會想用的資訊。  
`ucontext` 其實是 `ucontext_t` struct，存了更多系統狀態，register、stack pointer 等等，一般不會用到。  

### sigsetjmp and siglongjmp  

`int sigsetjmp(sigjmp_buf env, int savemask)`  
`void siglongjmp(sigjmp_buf env, int val)`  
Saves and restores the current signal mask in env if `savemask!=0`. For `setjmp` and `longjmp` some OS may not do this.  
As usual, you should assume local variables are not restored. Again, variables in the register will be restored, but you cannot control what is in the register.  

### sigsuspend  

`int sigsuspend(const sigset_t *mask)` = `sigprocmask` + `pause`  
* Atomically block the signals in mask and suspend the process until a signal is caught or ternimates the process.  
* Return when a signal is caught and the signal handler returns.  
* The **signal mask is restored** before the handler is called.  

相當於若被 on 起來(block)的那些 signal 發生，不會因此結束，會繼續等。  

### Ex: Avoid race condition (Ch8)  

child 和 parent 一起用 unbuffered I/O 每次寫一個字，導致混在一起。  
在 Ch15 用 pipe 解決，child 或 parent 要等對方時，用 read 把自己 suspend，等到對方在 pipe 寫東西時才繼續。這也可以用 signal 來做：  
* 初始化 `TELL_WAIT`: 註冊 signal handler，並用 mask 避免在 `sigsuspend` 前就收到。  
* `TELL` 對方: parent 傳 `SIGUSR1`，child 傳 `SIGUSR2`  
* `WAIT` 對方: `sigsuspend`，並改回原本的 signal mask(假設等對方只有一次)  

**大重點**: `TELL_WAIT` 要在 `fork` 前執行，不然 fork 完，parent 可能在 child 還沒 `TELL_WAIT` 時就傳 signal(發生 race condition)，導致 `sigsuspend` 等不到。  
一樣是 critical region 的觀念，若是包含 fork 前一小段才能避免剛 fork 完的問題。  

### Reliable real sleep  

Suspend until time expires or signal caught and the handler returns.  
Problems: `alarm(10)`, 3 secs passed, `sleep(5)`  
Answer: If user set an alarm before, the alarm will be ignored.(Don't wait the remaining 2 secs, replace the SIGALRM) But the sleep may return early if the alarm rings.  

Implementation: We can block alarm and use atomic `sigsuspend` to avoid `SIGALRM` comes between `alarm` and `pause` in `sleep1`.  

### abort  

如同之前寫的  
1. 如果 `SIGABRT` 的 handler 是 `SIG_IGN`，設為 `SIG_DFL`(讀取、修改都用 `sigaction` 達成)  
2. 如果是 `SIG_DFL`(不是 catch)，就先 `fflush`  
3. 把目前的 signal mask 設為只有 `SIGABRT` 不 block，然後再 `kill` 自己(=`raise`)，利用 side effect(有一個不是 ignore 的 signal 才回傳，而只會是 `SIGABRT`)。  
4. 如果 `SIGABRT` 被 caught，則 `fflush`(剛才 catch 的話不會 fflush)、設為 `SIG_DFL` 並再 `kill` 一次。  

要 fflush 因為 `abort` 不像 `exit` 會 flush、atexit、釋放記憶體、關閉文件等，而 fflush 算是比較重要的(不然使用者不知道為什麼印不出來)。  

## Critical region(session)  

避免在這個區塊，一些共享資源被修改造成 race condition(對資源)；或是 multi-thread 時，這個區塊被多個 thread 同時執行(對程式)。  
這裡就是用 `sigprocmask` 來避免某些 signal 的 handler 會把某些資源修改，並且 critical region 在 `sigsuspend` 結束。  
要嘛就避免同時 access 資源，要嘛就對資源上鎖(但同時還要避免 deadlock、race condition)。  

# Ch11 Threads  

## The process model  

<!-- explain process concept -->  
* Resource grouping  
  * Includes address space, open files, child processes, pending alarms, signal handlers, accounting information(CPU time, etc), etc.  
* Single thread of execution  
  * The entity scheduled for execution by the operating systemduled for execution on CPU  

### Memory arrangement(Virtual memory)  

* kernel space  
  * open file descriptor table, etc  
  * command line arguments, environment variables  
* stack  
  * local variables, stackframe(function parameters)  
* heap  
  * dynamic memory allocation  
* global variables(uninitialized/initialized)  
* text/instructions  
  * function  

如果是 32-bit 的架構，那指標就允許 4GB 的 virtual memory，但一般不會用到這麼多，且也會有一些給 kernel space 用。  
system call 也許也會 call 其他 function，這不會放在 stack，而是放在 kernel space 裡面的 kernel stack。  

## The thread model  

a lightweght process, share some resources with other threads in the same process.  
A thread has it's own  
* program counter  
* registers  
* stack  
* scheduling policy  
* errno variable  
* signal mask  

## process vs thread  

Process 就像陌生人，thread 就像兄弟姊妹。  
* process  
  * 可能是不同 user 的  
  * 資源不易共享(為了安全)  
  * cost 高  
* thread(lightweight process)  
  * 同個使用者的  
  * share 大部分資源  
  * threads 通常都平等，沒有 parent-child 關係(除了 pthread 的 main thread)  
  * cost 低  

Virtual memory  
* process  
  * 一個 stack、一個 heap，兩者碰到的話會出錯，有的系統會提醒。  
* thread  
  * 每個 thread 有自己的 stack 的預留空間，使用者可以自己設大小，其他東西是共用的。  

Thread benefits  

* asyncronous events(把其他 threads 的某 signal 擋掉，只有一個 thread 接收)  
* share memory and file descriptors  
* 一起做，提升 throughput  
* response time(等 I/O 時，其他 thread 可以繼續做事)  

Thread drawbacks  

* be careful  
* hard to debug  
* 單核 CPU 不一定 threads 有用(但 I/O 有用)  

> shared memory 是 IPC 最快的方法，因此 thread 很好用  

## Implement threads  

### User-level threads  

Kernel 完全不知道有 threads  
process 自己模擬 threads，自己做 thread table(tcb)，儲存 thread 狀態、switching、scheduling。  
好處: system call 比較慢，自己 switch 比較快。  

> setjmp, longjmp:  
> * signal handling  
> * thread switching  
> * error handling  

ex: Old Linux, pthreads(POSIX standard)  

#### Problem  

* 要自己用 non-blocking 或 I/O multiplexing 處理 blocking system call  

> preemptive/non-preemptive OS  
> * preemptive: OS 可以隨時把 CPU 拿走。現在的 OS 大多是 preemptive  
> * non-preemptive: 只有 thread 自己可以放棄 CPU  

* 因此在 non-preemptive OS，一個 thread 可能會 block 其他 thread。可以用 alarm signal 解決，一直讓 thread timeout  

### Kernel-level threads  

Kernel 知道 thread，所以可以用 kernel 的 thread scheduling。  
system call 可以 block，比較簡單。  
可以在同個 process 或不同 process 跑。  
ex: windows 2000/XP  

#### Problem  

* system call 的 cost 變高  
* destroy, create thread 的 cost 變高  
  * 可以 recycle  

### Hybrid threads  

想辦法結合兩者的好處，ex: Solaris  

## Thread support  

傳統 UNIX 只支援一個 process，所以會用各種 thread library，ex: POSIX pthreads, Win32 threads, SProc on SGI。  
這邊只介紹 pthreads。  
跟 fork 的概念類似，沒有必要不能 share 那就 share。  

## pthreads  

### create a thread  

`int pthread_create(pthread_t *thread, pthread_attr_t *attr, void *(*start_routine)(void *), void *arg)`  

- `thread`: New thread's ID  
- `attr`: Assign attributes for the new thread. NULL for default.  
- `start_routine`: The function that the new thread will run. void* 代表任何型態的 pointer。  
- `arg`: A pointer to the argument that will be passed to the start routine.  

跟 fork 一樣，不一定自己或新 thread 哪個先跑。沒有 parent-child 關係，return code 也不一定是 create 的 thread 接收。  

### thread ID  

* `pthread_t pthread_self()`: 得到自己的 thread ID  
* `int pthread_equal(pthread_t t1, pthread_t t2)`: 比較兩個 thread ID 是否相同，非零代表相同。  

### thread attributes  

`pthread_attr_t` 是一個 struct，可以設定 thread 的 attributes。  
pthreads 中各種東西通常都是 struct，因此需要用 init、destroy 來初始化、銷毀，包含 thread/mutex attributes、mutex 等。  
* `int pthread_attr_init(pthread_attr_t *attr)`: 得到 attributes 的初始值  
* `int pthread_attr_destroy(pthread_attr_t *attr)`: 銷毀 attributes，因為 attr 裡面可能還有其他 allocate 的東西，這個會幫忙 free，並把值都設為 invalid 避免誤用。  

屬性有哪些？  
* `detachstate`: terminate 後是否要讓其他人看 return state 及是否要回收，類似要不要有 zombie process  
* `guardsize`: 每個 thread 的 stack 後多一點緩衝，比如 1M 接著 4K  
* `stackaddr`: stack 的起始位置  
* `stacksize`: stack 的大小  

後面三個與 stack 有關，比較不常用。  

#### detachstate  

類似 double fork，讓 thread 死後馬上把資源清乾淨。  
* `pthread_attr_getdetachstate` 可以得到目前的 detach state。  
* `pthread_attr_setdetachstate` 可以設定 detach state。  
  * `PTHREAD_CREATE_JOINABLE`: 預設，可以被其他 thread join  
  * `PTHREAD_CREATE_DETACHED`: 不能被 join，結束後會自動回收資源  

正常是要先做好 `attr` 再 create。但如果已經 create 完也是可以再設為 detach，就像 file 開完後還能用萬能的 `fcntl` 設定是否 blocking，用到 `pthread_detach`，可以 detach 任何一個 thread，注意只是 set attribute，不會真的 detach。  

### 傳參數  

`pthread_create` 最後一個參數可以是任意型態的 pointer，而不同 threads 間理論上會 share heap，所以可以直接傳 pointer，要確保 routine 能讀到 pointer 內容。傳 array `char*`、`int*` 很正常，不過記得傳 int 要用 `&` 取址。  
因此 `start_routine` 要 take 一個 pointer 參數。  

注意  
* 因為不同 threads 都會取同一個 address，要確保 thread 讀完後才改數值或是 free。  
* 因為只能傳 address 有點討厭，open source 可能會直接把要傳的 `int` 直接轉換成 `void*`，但要注意這要求 `sizeof(int)<=sizeof(void*)`。  

### Thread Termination  

* 所有 threads 一起死掉: thread 是 process 的一部分，因此在 process 死掉後，所有 thread 都會死掉，因此 main thread 不能隨便 return，要確保其他都做完事。  
* thread 自己死掉:  
  * return from routine: 正常死亡，預期你把資源清乾淨，所以**不會**執行 cleanup handler。  
  * call `pthread_exit`: 比較不正常的正常死亡，**會**執行 cleanup handler。  
  * cancelled by another thread: 異常死亡，**會**執行 cleanup handler。  

#### pthread_exit  

`void pthread_exit(void *retval)`: 結束自己的 thread，並回傳 retval。這邊的「回傳」與 `return` 的作用是一樣的，都是在 `pthread_join` 讀取。因此與 `return` 的差別基本上只有：  
如果在 `main` 裡，`return` 會結束整個 process，`pthread_exit` 會先等其他 thread 做完事再結束。  

#### pthread_join  

`int pthread_join(pthread_t thread, void **retval)`: 等待 undetached thread 結束，回傳值會放在 `retval。`  

* 只有 `cancel` 代表**異常死亡**，所以 `retval` 會是 `PTHREAD_CANCELED`。  
* system call 出錯通常都是回傳**負值**，具體出什麼錯再用 `errno` 讀；但 pthread 一律是用 **return value** 判斷。  
* 如果 undetached thread 沒有被 join，會變成 zombie thread。  
* 如果兩個 thread **同時** join 一個 thread，會是 undefined。但如果一前一後，後面那個就會出錯  
* 如果 join: detached、已經被 join 的 thread、或不存在的 thread，`join` 的回傳值會得到 `EINVAL`、`ESRCH` 等錯誤。  
* `join` **時**被 cancel，則其他 thread 還是可以 `join` 本來要 join 的 thread。  
* 沒有像 `wait` 或 `waitpid(-1)` 這樣等任一個 thread 的方法，man page 甚至說如果你覺得需要這樣的功能，你的設計可能有問題。  

#### pthread_cancel  

分成 `cancelstate`(是否接受別人 cancel) 和 `canceltype`(收到 cancel 的話什麼時候要結束)。  
判斷流程  
* `cancelstate` 是 `PTHREAD_CANCEL_DISABLE`  
  * 不理，但是 cancel 會類似 flag 繼續保留，等到變成 ENABLE 時再嘗試 cancel。  
* `cancelstate` 是 `PTHREAD_CANCEL_ENABLE`(default)  
  * `canceltype` 是 `PTHREAD_CANCEL_ASYNCHRONOUS`  
    * 立刻結束  
  * `canceltype` 是 `PTHREAD_CANCEL_DEFERRED`(default)  
    * 等到下一個 cancellation point 結束，cancellation point 是指在呼叫一堆正面表列的 system call 之前，其中一些跟等待有關或甚至可能 forever suspend，比如 `wait`、`sigsuspend`，確保不會因為休息而導致資源永遠不釋放，有人真的很需要就可以把人 cancel。  
    * 或呼叫了 `pthread_testcancel`，也會結束  

**注意**: cancel 完還是得要 join，或是設為 detached，否則還會是 zombie thread。  
預設值是 undetached、`CANCEL_ENABLE`、`CANCEL_DEFERRED`，不像用 signal kill process 會直接死。因為 thread 不像 process 是各自獨立，有許多共用資源，比如 lock 或 heap 內的記憶體，因此要確保 cancel 對象把資源清乾淨才能結束。  

### Thread Cleanup Handlers  

cleanup handler: 類似 exit 的 atexit，是 LIFO，應該是用來處理後事(清鎖、刪記憶體之類的)。  
`void pthread_cleanup_push(void (*routine)(void *), void *arg)`: push 一個 cleanup handler 到 stack。  
`void pthread_cleanup_pop(int execute)`: pop 一個 cleanup handler，如果 execute 是非零，就執行這個 handler。  

clearnup handler 會在 `pthread_exit`、`pthread_cancel`、`pthread_cleanup_pop` 時執行。return 因為死亡方式太正常了，所以不會執行。  
如果這兩個函數是用 macro 寫的，必須成對出現，不然括號可能出錯。就算沒有也可以寫成對，確保若 return 的話會執行所有 handler。  

### 與 Process 的比較  

| Process   | Thread                 |  
| :-------- | :--------------------- |  
| `fork`    | `pthread_create`       |  
| `exit`    | `pthread_exit`         |  
| `waitpid` | `pthread_join`         |  
| `atexit`  | `pthread_cleanup_push` |  
| `getpid`  | `pthread_self`         |  
| `abort`   | `pthread_cancel`       |  

## Thread Synchronization  

就算只是 `i++`，也有可能因為具體實作不是 atomic 導致兩個 threads race condition，導致只加到 1。因此需要  
* mutex(mutual-exclusion interfaces)  
* rwlock  
* condition variable(最厲害)  
* mmap  

### Mutex  

相當於 (advisory) lock，希望 lock 住才能讀寫。多個 thread 一起 lock 會是第一個執行的 thread 得到，而通常會是優先度最高的 thread，但也沒有保證。  
> fork 時會繼承 mutex，所以要小心。review: 不繼承 file lock(因為是在 i-node 裡面存哪個 process 有 lock)。  

mutex、mutex_attr 都是 struct，所以要用 `init`、`destroy` 來初始化、銷毀。`pthread_mutex_init`、`pthread_mutex_destroy`、`pthread_mutexattr_init`、`pthread_mutexattr_destroy`。  

`PTHREAD_MUTEX_INITIALIZER` 可以靜態初始化 mutex。  

#### attribute  

##### process-shared  

sync 三者的 attribute 都有 `process-shared`，代表要不要跨 process，除了 mmap 是 Advanced I/O 搬來的，其他 pthreads 系列(mutex, rwlock, condition variable)會是 `PTHREAD_PROCESS_SHARED` 或 `PTHREAD_PROCESS_PRIVATE`，**預設是 private**。  


##### type  

mutex 獨有，用來處理  
* **deadlock**: 如果同一個 thread lock 兩次或兩個 thread 互相 lock 對方持有的 lock 後才要 unlock 自己的，會造成 deadlock。  
* **error checking**，其中 error 的可能性有: unlock 但沒有 own lock、或是 unlocked 之後又 unlock。  
`PTHREAD_MUTEX_<type>`  

* NORMAL: **沒有** error checking、deadlock detection，若發生就放給它爛。  
* ERRORCHECK: 有 error checking、deadlock detection。若產生會回傳錯誤碼。  
* RECURSIVE: 有 error checking，lock 會有 counter，變成 0 才相當於 unlock。  
* DEFAULT: depends on 系統。Linux 是 NORMAL  

functions: `pthread_mutexattr_gettype`、`pthread_mutexattr_settype`  

#### lock, unlock, trylock  

`int pthread_mutex_[lock|unlock|trylock](*mutex)`  
* lock: block 直到得到 lock  
* trylock: non-blocking，得到就得到，沒得到就 return 錯誤碼 EBUSY(注意不像 system call 是用 errno，pthread 是直接 return)。這某種程度上也可以算是避免 deadlock。  
* unlock  

因為是 advisory，所以確保正確性仍是 programmer 的責任。在使用資源前都要取得 lock。  

### Memory-mapped I/O  

不太正統的 shared memory。  
把 file map 到 virtual memory，這樣就可以直接讀寫 memory 來達到 File I/O，不用 read/write。  
Virtual memory 中 stack 到 heap 中間有很大的空白，所以就是把 file map 到這裡。  
copy-on-write 前面寫過，但還是再提一些。好處是 read-only 的部分就不用複製。像是現在大部分電腦都是馮諾伊曼架構，不允許在運行時改程式碼，所以 text 部分就不會更改。  

`void *mmap(void *addr, size_t len, int prot, int flags, int fd, off_t offset)`  
* `addr`: 要 map 到哪裡，通常是 NULL，讓 OS 選擇，就算指定也只是建議。  
* `len`: map 多大，可以設為非 page 大小的倍數。  
* `prot`: protection，控制rwx，當然不能超過對檔案的權限 `PROT_READ`、`PROT_WRITE`、`PROT_EXEC`、`PROT_NONE`  
* `flags`:  
  * `MAP_FIXED` 讓 `addr` 不是建議而是強制，不常用。  
  * **process-shared**: `MAP_SHARED`、`MAP_PRIVATE`，前者是各 process 共享，後者是各 process 獨立 (copy-on-write)。  
  * `MAP_ANONYMOUS` 不是 map file，而是 map anonymous memory，通常用來做 shared memory。fd 會被忽略，所以可以亂寫 -1，要注意有的系統要求寫 -1。  

回傳的指標就代表 map 到的 vitual memory 的開頭。  

之所以說這不太正統，是因為畢竟原本單純是用來 map file to memory，正統的 shared memory 會是 shm 開頭的 system call。  
shared memory 是 IPC 最快的方法，比如很多個 ptt server process 因為要可以共用一個 shared memory 來確認密碼。  

#### page-align 問題  

addr, len, offset 理想上都要是 page size 的倍數才方便，確實系統也會要求 addr len 是倍數。像是這種 system call 確實都比較麻煩，SBRK(malloc 時會呼叫的 system call) 也會要求是 page size 的倍數。  
解決辦法: addr 就 NULL，自動選。offset 設 0 讓它從頭開始。系統通常不會要求 len 是倍數，會自動補 0 變成倍數。  

#### Example: cp  

開啟兩個檔案 source 和 dest。  
把 dest 清空後，`lseek` 到 source 的大小並寫一個 byte 以確保大小相同。  
把兩者都 map 到各自的 memory。  
用 `memcpy` 把 source 的內容複製到 dest。  

(理論上要有 unmapping，但跟 close 一樣系統會幫你做)  

#### Example: shared memory  

就像 unbuffered I/O 會有 buffer cache，之後才真正寫到 disk，mmap 後也一樣會先寫到 memory，因此就可以用來做 shared memory。  

有一段記憶體 `char buf[BUFSIZE]`，要讓兩個 process 共享。  
同時舉例 mutex，因為 mutex 也要讓兩個 process 共享，所以就乾脆定義一個 struct 包在一起，但**注意**還是得要用 attr 把它設為 `PTHREAD_PROCESS_SHARED`(雖然我沒實驗過但應該是要這樣寫才對)。  

這有兩種實作方法，一個是 fd 用開 `/dev/zero` 來 map，另一個是用 `MAP_ANONYMOUS`。  

不過 exec 就沒辦法用了，user space 會被清空。  

### Deadlock  

上面 mutex 有寫到各種 deadlock 的情況，也寫到 trylock 可以避免。這邊再補充一個方法，控制 **locking granularity**，把多個 lock 整合。  
優點:  
* ABC 資源的 lock 如果分開就比較容易 deadlock，如果整合成一個就沒有這個問題  
* 若太多 lock 雖然很平行化，但會一直 lock、unlock 浪費時間  

缺點  
* 平行度、效率變差。  

### RW Lock  

概念和 file lock 一樣。  
實作上與 mutex 一樣，是一個 `pthread_rwlock_t` struct，也有 `init`、`destroy`、`rdlock`、`wrlock`、`unlock`、`tryrdlock`、`trywrlock`(自己加 `pthread_rwlock_` 在前面)，以及靜態初始化 `PTHREAD_RWLOCK_INITIALIZER`。  
(實作上可能會限制一個 rwlock 最多能被 lock 幾次)  

> mutex 也不是一無是處，因為實作簡單。比如說如果全部都是要 write，那不如直接用 mutex。  

### Thread Pool  

有一個 master thread 負責分配工作，另外有一些 worker threads 負責做事，把 jobs 放在 queue 裡。每個 job 可能會指定要用哪個 thread 做，因此可以用 rwlock 實作，append 前取 wrlock，find 前取 rdlock。  
這衍生出一個問題，如果 queue 裡沒有工作，那就會造成 busy waiting，因此可以用 condition variable 來解決。  

### Condition Variable  

適用於需要等到某個條件成立才繼續的情況，這個條件的檢查、改變是由一個 mutex 保護。  
主要操作：`wait`、`signal`、`broadcast`。  
`pthread_cond_t` 一樣要 `init`、`destroy`，或是靜態初始化 `PTHREAD_COND_INITIALIZER`。  
`signal` 會叫醒**某個**等待該 condition 的 thread，但不知道會是哪個，`broadcast` 會叫醒**所有**等待的 thread。  
**注意**: 可以想成 wait 時才會接收 signal。  

#### 用法  

1. acquire mutex  
2. check condition(通常要用 **while**)  
3. call `pthread_cond_wait(cond_t *c, mutex_t *m)`:  
   * suspend 前 release mutex(讓別的 thread 有機會改變 condition，必須是 atomic，否則 suspend 前就 signal 的話就睡不醒了)  
   * suspend until `signal` or `broadcast`  
   * wake up and reacquire mutex  
4. release mutex  

在 condition 的觀點，在 lock 到 unlock 間是 critical region，因為 lock 住，其他 thread 無法改變條件，在這裡不會使得條件滿足。  
**注意**: wait return 前必須取得 mutex，所以如果暫時還拿不到的話就會 suspend。  

#### Example: wait for x==y  

```c  
pthread_mutex_lock(&m);  
while(x != y)  
  pthread_cond_wait(&c, &m);  
// do something when we know x==y  
pthread_mutex_unlock(&m);  

// 另一個 thread  
pthread_mutex_lock(&m);  
x++;  
pthread_mutex_unlock(&m);  
// A  
pthread_cond_signal(&c);  
```  

如果在 A 的地方別的 thread 改 x 怎麼辦？反正多通知不虧，沒差。  

#### Example: Avoid race condition (Ch8)  

前面那個 fork 完兩個 process 一起用 unbuffered I/O 一次寫一個字元的例子。之前用過:  
* pipe，等待方用 read suspend，通知方用 write  
* signal，等待方用 sigsuspend，通知方用 signal  

這邊用 condition variable 來實作，概念上也很像 signal。想要 spawn 出來的 thread 先跑，則:  

```c  
int done = 0;  
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;  
pthread_cond_t c = PTHREAD_COND_INITIALIZER;  
void *spawned(void *arg) {  
  pthread_mutex_lock(&m);  
  // print something  
  done = 1;  
  pthread_cond_signal(&c);  
  pthread_mutex_unlock(&m);  
  return NULL;  
}  
int main(int argc, char *argv[]) {  
  pthread_t p;  
  pthread_create(&p, NULL, spawned, NULL);  
  pthread_mutex_lock(&m);  
  while (done == 0)  
    pthread_cond_wait(&c, &m);  
  pthread_mutex_unlock(&m);  
  // print something  
}  
```  
其實 `unlock` `signal` 交換也行，都會正常運作，但在 real-time 的應用(比如直播)，就很需要讓優先的 thread 先執行，所以先 `signal` 比較好，因為可以讓先 `wait` 的人醒來，比較不會等太久。  

**一行都不能少**，否則會有 race condition:  
* 如果把 `done=1`、`while(done==0)` 拿掉，可能先 signal 再 wait，就會等到死。  
* 如果把 mutex 刪掉(假設 wait 不需要)，那會有 TOCTOU 問題，檢查 `done==0` 後 修改並 signal，但還沒 wait，一樣會等到死。  

## Threads vs fork  

問題: 如果 fork 一個有很多 thread 的 process，新的 process 會複製所有 threads 嗎？  
答案: 不會，只會複製 call fork 的 thread。  
因此很有可能其他 thread 的 lock 沒有釋放，那 child 裡那些 lock 就永遠不會釋放。  
解決辦法: 最簡單的是用 `exec`，直接重跑一個程式。  

另外一個方法是 `int pthread_atfork(void (*prepare)(void), void (*parent)(void), void (*child)(void))`，在 fork 前執行 `prepare`、return 到 parent 前執行 `parent`、return 到 child 前執行 `child`，可以用來清理 lock。  
通常會把 `prepare` 設為 lock 所有 lock，`parent` 設為 unlock 所有 lock，`child` 也設為 unlock 所有 lock。相當於 prepare 會使得所有其他取得 lock 的 thread 都告一段落並 unlock 後再繼續，很合理。  
註冊多次的話，都會被執行，但 prepare 是 FIFO，parent、child 是 LIFO。  

## Thread signals  

* 每個 thread 都有自己的 signal mask  
* handler(disposition) 是共享的  
* signal 會給其中一個 thread，exception 這種有特定對象的話就給引發的 thread，否則會給**隨便一個**  

引發方式-什麼事情引發  
* Synchronously  
  * exception 等，會給引發的 thread  
  * 同 process 的 thread 用 `pthread_kill`，給指定的 thread  
* Asynchronously  
  * 外在的 process 用 `kill`，會給隨便一個沒有 block 這個 signal 的 thread，全 block 就 pending  

### Signal Mask  

* fork、create thread 時會繼承 signal mask  
* `pthread_sigmask` 類似 `sigprocmask`，參數一樣  
* `int sigwait(sigset_t *set, int *signop)`: 等待 `set` 裡的 signal，也就是 unblock 它們，與 `sigsuspend` 相反。`signop` 會儲存收到的 signal。  
多個 threads 在等同個 signal，則系統決定其中一個收到。  

### Synchronous Signal Handling  

Process 的 signal 是 asynchronous，因為不知道什麼時候會來。  

#### Dedicated Signal Handling Threads  

非常直觀，就對 signal 用專門的 thread 處理(多對一、一對一、多對多都有可能)，裡面就是無窮迴圈一直 `sigwait` 它要等的 signal，其他 threads 把 signal block。  
如果還設了 `sigaction`，系統決定其中一個，但不會這樣找麻煩。  

## Thread Safety  

如果兩個 threads 同時 `lseek` 並 `write`，因為共用 file desc. table，也共用 offset，會導致 race condition。因此需要 atomic operation `pread` `pwrite`，不會改掉 offset。  

### Thread-Safe Functions  

可以被多個 threads 同時呼叫的 function，不會用到 global, static variable，或是有好好上 lock。  
負面表列某些不 safe 的 functions。像是 `rand` 有 hidden state，但你可以把它當作參數傳入 `rand_r`，這樣就是 thread-safe 了。  

#### Thread-Safe Functions v.s. Async-Signal Safe  

Async-Signal Safe 指 signal handler 中可用的 reentrant function。  
$\Leftarrow$(絕大多情況) 但 $\not\Rightarrow$，因為如果函數有 lock，再 call 一次的話會 deadlock(等上層 unlock)。  

#### FILE is Thread-Safe  

因為有 `f[lock|unlock|trylock]file(FILE *fp)`，所有 I/O 都會上 recursive lock。  
但是因為 lock unlock 會導致變慢，若每次只讀寫一個字元就會超慢(granularity 太細)，因此提供後綴 `_unlocked` 的版本。  

# Ch7 Environment of a Unix Process  

每個 process 都以為自己有專用的  
* CPU，但實際上是系統會幫忙排程。  
* memory，但實際上是一個 virtual memory。  

把一個 executable(elf) 拆開，會發現剛開始執行不是直接進到 main 而是 `_start`。可以用 `nm -g`(list symbols of object file) `readelf -a`(read elf file) `objdump -d` 等指令看。  
> `objdump` 時會發現有些位置是用相對位置，好處是如果內容不變但相對的點(如 `_start`)改變，就不用修改。  

## ELF(Executable and Linkable Format)  

One unified format for  
* Relocatable object files (.o)  
* Executable object files  
* Shared object files (.so)  

Better than `a.out` format  

### 編譯程式的流程  

source code .c .cpp  
C Preprocessor `gcc -E`: 把 header 檔、macro 展開  
preprocessed code .i  
C Compiler `gcc -S`: 把 C code 編譯成 assembly code  
assembly code .s  
Assembler `gcc -C`: 把 assembly code 編譯成 object code  
object code .o  
Linker `gcc -o`: 把 object code 和 library link 起來  
executable file  

### ELF Object file format  

* ELF header: magic number, type, machine, byte ordering, entry point, size etc.  
* Program header table: segment information  
* `.text` section: code  
* `.data` section: initialized data  
* `.bss` section:  
  * uninitialized data  
  * block started by symbol(習慣已久的稱呼，不太重要)  
  * 不佔空間  
* `.symtab` section: symbol table，寫 compiler 時很重要，會包含 procedure, static variable 在哪的資訊。  
* `.rel.text` section: relocation information for `.text` section  
* `.rel.data` section: relocation information for `.data` section  
* `.debug` section: debugging information  

`.rel`: 需要在 link 時填入  

### Relocating object files  

如果在 a 檔案裡要用 b 檔案的 function 或 variable，在生成 a 的 `.o` 檔時就會把 `rel.text` 或 `rel.data` 的位置設為 0。並在 relocate 時把 b 的位置填進去。  
Relocate 時，就是把多個 relocatable object files link 起來，也就是把各自的各 section 合併。  
> 合併時就會發現相對位置真的很重要。  

### Memory layout of a process  

* Text segment: code, read-only, sharable(when fork)  
* Initialized data segment: global, static, initialized data(與 text 都是 exec 會 load from program)  
* Uninitialized data segment: global, static, uninitialized data, zeroed by exec  
* Stack: automatic(理解為 local) variables, return address, saved registers  
* Heap: malloc, free, brk, sbrk  

## Virtual Memory  

講 ELF 的原因就是因為 text data bss 會對應到 process 的 text data bss segement。  
OS 會建一個 page table，把 virtual address 對應到 physical address。但因為 physical memory 有限，所以會有些資料被放在 disk 上(swap)。  

### Page Table  

VPN: Virtual Page Number，在 virtual memory 中的 page number  
PPN: Physical Page Number，在 physical memory 中的 page number  
Page table 就是 VPN 到 PPN 的 mapping。而每個 address 會包含 page number(VPN 或 PPN) 和 offset，virtual 轉換成 physical 時 offset 不變。  
每個 process 有自己的 page table。page table 會需要是非常高效的，所以會有硬體優化，Memory Management Unit(MMU)。  

> 去年期末考題：setjmp longjmp 時，canjmp 變數要是 `static volatile sig_atomic_t`，其實就是不能跨 page，否則很可能需要多個 instruction。(canjump 是確保有 setjmp 過)  

### stack (frame)  

stack frame 會有 return address、saved registers、local variables。  

#### longjmp and setjmp's Effects on Variables  

* auto: default when no modifier, may be optimized in register, **can be recovered**  
* register: recommend to put in register, **can be recovered**  
* volatile: may be changed, so read from memory each time when access, **not recovered**  
* static: global, **not recovered**  

> 可以有 `const volatile`，雖然自己改不了，但 somehow 硬體可能可以直接改。  

### allocate memory  

老朋友: `malloc` `calloc`(nobj, size) `realloc`(reuse existing memory or copy to new memory)  
`sbrk`: system call，很麻煩  
`alloca`: allocate from stack frame, no need to free! But unsafe(too big=>issue), not standard(so not portable)  

系統會 track 哪些地方用多少、沒用過，可能是 Linked list。  

### environment variables  

Use `extern char **environ` instead of `char **envp` in arguments! Becuase external variable will change if env is changed.  

### Library  

* Static Library，靜態連結的函式庫，link 時直接把 binary 搬進去 text。好處是不用管環境問題，但很浪費空間。`.a` 檔。  
* Shared Library，動態連結的函式庫(dynamic link library, DLL)。好處是常常更新的話不用一直編譯用到的程式。也許剛開始就 load 或是要用的時候才 load。`.so` 檔。  

shard library 就是用 `mmap` 來做，所以也在stack、heap 之間，也解釋了 `mmap` 裡 permission 用 x 的用處。  