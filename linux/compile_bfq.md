## Compile the BFQ IO scheduler for Linux as an out-of-tree module

See http://algo.ing.unimo.it/people/paolo/disk_sched/ for
background. Unfortunately BFQ has not yet accepted in mainline kernel,
so you need to compile it by yourself. All instructions around require
you to rebuild the whole kernel.

However BFQ also supports being compiled as an out-of-tree module. The
following instructions are obtained by sligthly adapting to my need
[this Facebook
post](https://www.facebook.com/groups/ubuntugr/permalink/1160635153984315/?comment_id=1162158627165301&comment_tracking=%7B%22tn%22%3A%22R%22%7D),
kindly [translated from Greek by "Nik Th" on the BFQ mailing
list](https://groups.google.com/d/msg/bfq-iosched/YEmSV5xeCew/fJdI2UHcBwAJ).

I work on an up-to-date Debian unstable system.

### Install the kernel headers

Install the packages `build-essential` and `linux-header-*-*`,
according to your kernel version and architecture.

### Get the patched Linux sources

You can use either install the package `linux-source-*.*` or download
a vanilla kernel (be sure its version matches the one running on your
computer). Then apply the patches distributed at
http://algo.ing.unimo.it/people/paolo/disk_sched/sources.php (again,
take the correct version).

Alternatively, you can directly clone the development GIT repository
at https://github.com/linusw/linux-bfq and checkout the tag
corresponding to the correct kernel and BFQ version (I used this last
method).

### Copy the relevant files in an out-of-tree directory

Create a directory outside the Linux kernel and copy the following
files from the subdirectory `block` in it:

* `bfq*.*`
* `blk.h`
* `blk-mq.h`
* `blk-stat.h`

### Create a `Makefile`

Create a `Makefile` in the same directory with the following content:

    ifneq ($(KERNELRELEASE),)
    # kbuild part of makefile
    obj-m := bfq-iosched.o
    bfq-iosched-y: bfq-cgroup.o bfq-ioc.o bfq-iosched.o bfq-sched.o

    else
    # normal makefile
    KDIR ?= /lib/modules/`uname -r`/build

    default: $(MAKE) -C $(KDIR) M=$$PWD

    endif

### Build BFQ

Simple!

    $ make -C /lib/modules/`uname -r`/build M=$(pwd) modules

The modules is in the file `bfq-iosched.ko`.

### Install BFQ

Copy the modules in the modules tree:

    # cp bfq-iosched.ko /lib/modules/`uname -r`/updates/
    # depmod -a
    # modinfo bfq-iosched
    # modprobe bfq-iosched

### Use BFQ for your devices

If you want to enable BFQ on device `sda` use:

    # echo bfq > /sys/block/sda/queue/scheduler
    # cat /sys/block/sda/queue/scheduler
    noop deadline cfq [bfq]

### Use BFQ as the default IO scheduler at boot

Arrange so that `bfq-iosched` is included in the initrd and pass the
argument `elevator=bfq` to the Linux kernel at boot. No further
instructions on this because I am not using it for the moment (see the
original document).
